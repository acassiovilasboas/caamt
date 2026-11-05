# -*- coding: utf-8 -*-
"""Roda NO COLAB (GPU grátis). Prepara o ambiente e executa as tarefas que o Claude
deixou na pasta do Google Drive. O usuário só abre o notebook e clica em "Executar tudo".

Uso (célula do notebook, depois de montar o Drive):
    python colab_worker.py [--esperar 20] [--uma-vez] [--teste]
      --esperar N : fica N minutos esperando tarefa nova antes de parar (padrão 20)
      --uma-vez   : executa o que estiver na fila e para
      --teste     : roda teste_velocidade.py e grava o resultado no Drive

Fila no Drive (criada pelo colab_job.py no computador do usuário):
    Edicao-Video/_colab/fila/<id>.json   -> {"id", "passos": [{"cmd": [...], "cwd": "..."}]}
    Edicao-Video/_colab/feito/<id>.json  <- resultado de cada passo (código, tempo, fim da saída)
Marcadores nos comandos: {drive} = raiz do Meu Drive, {scripts} = esta pasta.
Só executa python, ffmpeg e ffprobe; script python tem de estar dentro do Drive.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import time

DRIVE = "/content/drive/MyDrive"
BASE = os.path.join(DRIVE, "Edicao-Video")
FILA = os.path.join(BASE, "_colab", "fila")
FEITO = os.path.join(BASE, "_colab", "feito")
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
FFMPEG_URL = ("https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
              "ffmpeg-master-latest-linux64-gpl.tar.xz")
PERMITIDOS = {"python", "python3", "ffmpeg", "ffprobe"}


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def ffmpeg_ok():
    if not shutil.which("ffmpeg"):
        return False
    fl = sh(["ffmpeg", "-hide_banner", "-filters"]).stdout
    if not all(f" {f} " in fl for f in ("subtitles", "zscale", "ebur128")):
        return False
    r = sh(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=s=1080x1920:d=0.5", "-c:v", "h264_nvenc",
            "-f", "null", "-"])
    return r.returncode == 0


def prepara():
    t0 = time.time()
    if not os.path.isdir(DRIVE):
        sys.exit("Drive não montado. Rode antes a célula: from google.colab import drive; drive.mount('/content/drive')")
    if sh(["nvidia-smi"]).returncode != 0:
        print("AVISO: sem GPU. Menu Ambiente de execução > Alterar o tipo > GPU T4, e rodar de novo.")
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        print("instalando faster-whisper...", flush=True)
        sh([sys.executable, "-m", "pip", "install", "-q", "faster-whisper"])
    # cuBLAS/cuDNN que o ctranslate2 pede (o Colab pode não ter a versão certa)
    sh([sys.executable, "-m", "pip", "install", "-q", "nvidia-cublas-cu12", "nvidia-cudnn-cu12==9.*"])
    if not ffmpeg_ok():
        print("baixando FFmpeg completo (BtbN)...", flush=True)
        os.makedirs("/content/ffmpeg", exist_ok=True)
        sh(["bash", "-c", f"curl -sL {FFMPEG_URL} | tar -xJ -C /content/ffmpeg --strip-components=1"])
        os.environ["PATH"] = "/content/ffmpeg/bin:" + os.environ["PATH"]
    for d in (FILA, FEITO):
        os.makedirs(d, exist_ok=True)
    os.environ["EDICAO_VIDEO_SCRIPTS"] = SCRIPTS
    r = sh([sys.executable, os.path.join(SCRIPTS, "ambiente.py"), "--refazer"])
    print(r.stdout.strip() or r.stderr[-800:])
    print(f"preparado em {time.time() - t0:.0f} s", flush=True)


def troca(v):
    return v.replace("{drive}", DRIVE).replace("{scripts}", SCRIPTS) if isinstance(v, str) else v


def valida(cmd):
    exe = os.path.basename(cmd[0])
    if exe not in PERMITIDOS:
        return f"comando não permitido: {exe}"
    if exe.startswith("python"):
        alvo = os.path.realpath(cmd[1]) if len(cmd) > 1 else ""
        if not (alvo.startswith(os.path.realpath(DRIVE)) or alvo.startswith(os.path.realpath(SCRIPTS))):
            return f"script fora do Drive: {cmd[1] if len(cmd) > 1 else ''}"
    return None


def executa(arq):
    with open(arq, encoding="utf-8") as f:
        job = json.load(f)
    jid = job.get("id") or os.path.splitext(os.path.basename(arq))[0]
    print(f"\n== tarefa {jid}", flush=True)
    res = {"id": jid, "inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "passos": [], "ok": True}
    for p in job.get("passos", []):
        cmd = [troca(c) for c in p["cmd"]]
        erro = valida(cmd)
        if not erro and cmd[0] in ("python", "python3"):
            cmd[0] = sys.executable
        if erro:
            res["passos"].append({"cmd": p["cmd"], "codigo": -1, "saida": erro})
            res["ok"] = False
            break
        t0 = time.time()
        r = sh(cmd, cwd=troca(p.get("cwd")) or None)
        saida = (r.stdout + r.stderr)[-2000:]
        res["passos"].append({"cmd": p["cmd"], "codigo": r.returncode, "segundos": round(time.time() - t0, 1),
                              "saida": saida})
        print(f"  {os.path.basename(cmd[1] if len(cmd) > 1 else cmd[0])}: código {r.returncode}, "
              f"{time.time() - t0:.0f} s", flush=True)
        if r.returncode != 0:
            res["ok"] = False
            break
    res["fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(FEITO, f"{jid}.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    shutil.move(arq, os.path.join(FEITO, f"{jid}.pedido.json"))
    print("  OK" if res["ok"] else "  FALHOU (detalhe em _colab/feito)", flush=True)


def main():
    a = sys.argv[1:]
    esperar = float(a[a.index("--esperar") + 1]) if "--esperar" in a else 20.0
    prepara()
    if "--teste" in a:
        r = sh([sys.executable, os.path.join(SCRIPTS, "teste_velocidade.py"), "8"])
        print(r.stdout.strip() or r.stderr[-800:])
        with open(os.path.join(FEITO, "teste_colab.txt"), "w", encoding="utf-8") as f:
            f.write(r.stdout + r.stderr)
    ultimo = time.time()
    while True:
        jobs = sorted(glob.glob(os.path.join(FILA, "*.json")))
        for j in jobs:
            executa(j)
            ultimo = time.time()
        if "--uma-vez" in a or time.time() - ultimo > esperar * 60:
            print("\nFila vazia. Pode fechar o Colab (ou rodar a célula de novo quando houver tarefa).")
            return
        time.sleep(15)


if __name__ == "__main__":
    main()
