# -*- coding: utf-8 -*-
"""Conhece o computador (ou o Colab) antes de editar. Roda uma vez e guarda em cache.

Uso:
    python ambiente.py            # usa o cache se tiver menos de 30 dias
    python ambiente.py --refazer  # mede de novo (ferramenta instalada, erro estranho, outro PC)

Grava ~/.edicao-video/ambiente.json (completo) e imprime um resumo curto, que é o
que o Claude deve ler (economia de tokens). Também cria/atualiza
~/.edicao-video/config.json SÓ com as chaves que ele conhece (skill, scripts,
modelos, drive); chave que o usuário pôs à mão não é apagada nem trocada.

O codificador de vídeo é testado de verdade (0,5 s de vídeo): placa listada pelo
FFmpeg não quer dizer que funciona (ex.: GeForce MX150 lista NVENC e não tem).
"""
import json
import os
import platform
import shutil
import string
import subprocess
import sys
import time

DADOS = os.path.join(os.path.expanduser("~"), ".edicao-video")
ARQ_AMB = os.path.join(DADOS, "ambiente.json")
ARQ_CFG = os.path.join(DADOS, "config.json")
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(SCRIPTS)
VALIDADE_DIAS = 30
MODELO_GGML = "ggml-small.bin"
# ordem de preferência; libx264 é a garantia
CODIFICADORES = ["h264_nvenc", "h264_videotoolbox", "libx264"]


def _roda(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except (OSError, subprocess.TimeoutExpired) as e:
        return -1, str(e)


def le_json(arq):
    try:
        with open(arq, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def grava_json(arq, dados):
    os.makedirs(os.path.dirname(arq), exist_ok=True)
    tmp = arq + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    os.replace(tmp, arq)


def config():
    return le_json(ARQ_CFG)


def atualiza_config(novos):
    """Merge por chave presente: só escreve o que veio em `novos`."""
    cfg = config()
    cfg.update({k: v for k, v in novos.items() if v is not None})
    grava_json(ARQ_CFG, cfg)
    return cfg


def pasta_modelos():
    return (os.environ.get("WHISPER_MODELOS") or config().get("modelos")
            or os.path.join(DADOS, "modelos"))


def em_colab():
    return "COLAB_RELEASE_TAG" in os.environ or os.path.isdir("/content/sample_data")


def ram_gb():
    try:
        if os.name == "nt":
            import ctypes

            class M(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("c", ctypes.c_ulong), ("t", ctypes.c_ulonglong),
                            ("a", ctypes.c_ulonglong), ("x", ctypes.c_ulonglong * 5)]
            m = M()
            m.l = ctypes.sizeof(M)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return round(m.t / 2 ** 30, 1)
        if sys.platform == "darwin":
            return round(int(_roda(["sysctl", "-n", "hw.memsize"])[1].strip()) / 2 ** 30, 1)
        with open("/proc/meminfo") as f:
            return round(int(f.readline().split()[1]) / 2 ** 20, 1)
    except Exception:
        return None


def acha_drive():
    """Pasta raiz do Google Drive sincronizado (Drive para computador) ou montado no Colab."""
    cands = []
    if os.path.isdir("/content/drive/MyDrive"):
        cands.append("/content/drive/MyDrive")
    if os.name == "nt":
        for L in string.ascii_uppercase[3:]:
            cands += [f"{L}:\\Meu Drive", f"{L}:\\My Drive"]
    home = os.path.expanduser("~")
    cs = os.path.join(home, "Library", "CloudStorage")
    if os.path.isdir(cs):
        for d in os.listdir(cs):
            if d.startswith("GoogleDrive"):
                cands += [os.path.join(cs, d, "Meu Drive"), os.path.join(cs, d, "My Drive")]
    cands += [os.path.join(home, "Google Drive"), os.path.join(home, "Meu Drive")]
    for c in cands:
        if os.path.isdir(c):
            return c
    return None


def gpu_nvidia():
    if not shutil.which("nvidia-smi"):
        return None
    c, s = _roda(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], 20)
    return s.strip().splitlines()[0] if c == 0 and s.strip() else None


def faster_whisper():
    try:
        import importlib.util
        if importlib.util.find_spec("faster_whisper") is None:
            return {"instalado": False, "cuda": False}
        import ctranslate2
        return {"instalado": True, "cuda": ctranslate2.get_cuda_device_count() > 0}
    except Exception:
        return {"instalado": False, "cuda": False}


def ffmpeg_info():
    exe = shutil.which("ffmpeg")
    if not exe:
        return {"caminho": None}
    _, v = _roda(["ffmpeg", "-hide_banner", "-version"])
    _, fl = _roda(["ffmpeg", "-hide_banner", "-filters"])
    nomes = {ln.split()[1] for ln in fl.splitlines() if len(ln.split()) > 2 and ln.startswith(" ")}
    filtros = {f: f in nomes for f in ("whisper", "subtitles", "ass", "zscale", "ebur128", "loudnorm",
                                        "afftdn", "xfade", "vidstabdetect")}
    cods = {}
    for c in CODIFICADORES:
        rc, _ = _roda(["ffmpeg", "-hide_banner", "-v", "error", "-f", "lavfi", "-i",
                       "color=c=gray:s=1080x1920:r=30:d=0.5", "-c:v", c, "-pix_fmt", "yuv420p",
                       "-f", "null", "-"], 60)
        cods[c] = rc == 0
    return {"caminho": exe, "versao": v.splitlines()[0] if v else "", "filtros": filtros,
            "codificadores_ok": cods,
            "codificador": next((c for c in CODIFICADORES if cods.get(c)), None)}


def disco_livre_gb(pasta):
    try:
        return round(shutil.disk_usage(pasta).free / 2 ** 30, 1)
    except OSError:
        return None


def libs_python():
    out = {}
    for m in ("PIL", "numpy"):
        try:
            __import__(m)
            out[m] = True
        except ImportError:
            out[m] = False
    return out


def veredito(a):
    falta = []
    if not all(a["python_libs"].values()):
        falta.append("pip install pillow numpy")
    ff = a["ffmpeg"]
    if not ff.get("caminho"):
        falta.append("FFmpeg")
    else:
        for f in ("subtitles", "zscale", "ebur128"):
            if not ff["filtros"].get(f):
                falta.append(f"FFmpeg sem o filtro {f} (instalar build completo)")
    tr = a["transcricao"]
    if not tr["motor"]:
        falta.append("transcrição: baixar modelo (baixar_modelo.py) ou pip install faster-whisper")
    obs = []
    if a["ram_gb"] and a["ram_gb"] < 8:
        obs.append(f"pouca memória ({a['ram_gb']} GB)")
    if a["disco_livre_gb"] is not None and a["disco_livre_gb"] < 10:
        obs.append(f"pouco disco livre ({a['disco_livre_gb']} GB)")
    t = a.get("teste_velocidade") or {}
    fator = t.get("fator_tempo_real")
    lento = fator is not None and fator < 0.25
    if lento:
        obs.append(f"lento: {fator}x tempo real")
    viavel = not falta and not obs
    if falta:
        rec = "instalar o que falta"
    elif lento or (a["ram_gb"] and a["ram_gb"] < 8):
        rec = "usar o Colab (GPU grátis) para transcrever e gravar o vídeo final"
    elif fator is None:
        rec = "rodar teste_velocidade.py para decidir entre local e Colab"
    else:
        rec = "editar neste computador"
    return {"falta": falta, "observacoes": obs, "local_viavel": viavel, "recomendacao": rec}


def mede():
    fw = faster_whisper()
    modelos = pasta_modelos()
    ff = ffmpeg_info()
    ggml = os.path.join(modelos, MODELO_GGML)
    if fw["instalado"] and fw["cuda"]:
        motor = "faster-whisper (GPU)"
    elif ff.get("filtros", {}).get("whisper") and os.path.exists(ggml):
        motor = "ffmpeg-whisper (CPU)"
    elif fw["instalado"]:
        motor = "faster-whisper (CPU)"
    else:
        motor = None
    drive = acha_drive()
    anterior = le_json(ARQ_AMB)
    a = {
        "medido_em": time.strftime("%Y-%m-%d %H:%M"),
        "sistema": f"{platform.system()} {platform.release()}",
        "colab": em_colab(),
        "cpu_nucleos": os.cpu_count(),
        "ram_gb": ram_gb(),
        "disco_livre_gb": disco_livre_gb(drive or os.path.expanduser("~")),
        "python": platform.python_version(),
        "python_libs": libs_python(),
        "gpu_nvidia": gpu_nvidia(),
        "ffmpeg": ff,
        "transcricao": {"motor": motor, "faster_whisper": fw, "modelo_ggml": ggml if os.path.exists(ggml) else None},
        "drive": drive,
        "teste_velocidade": anterior.get("teste_velocidade") if anterior.get("sistema") == f"{platform.system()} {platform.release()}" else None,
    }
    a["veredito"] = veredito(a)
    grava_json(ARQ_AMB, a)
    atualiza_config({"skill": SKILL, "scripts": SCRIPTS, "modelos": modelos, "drive": drive})
    return a


def carrega(refazer=False):
    a = le_json(ARQ_AMB)
    if refazer or not a or not a.get("medido_em"):
        return mede()
    idade = (time.time() - time.mktime(time.strptime(a["medido_em"], "%Y-%m-%d %H:%M"))) / 86400
    return mede() if idade > VALIDADE_DIAS else a


def codificador_args(qualidade_cpu=("-crf", "17", "-preset", "medium")):
    """Argumentos -c:v para o vídeo final, conforme o que funcionou neste ambiente.
    EDICAO_VIDEO_ENCODER força um (ex.: libx264)."""
    c = os.environ.get("EDICAO_VIDEO_ENCODER") or le_json(ARQ_AMB).get("ffmpeg", {}).get("codificador") or "libx264"
    if c == "h264_nvenc":
        return ["-c:v", "h264_nvenc", "-preset", "p6", "-tune", "hq", "-rc", "vbr", "-cq", "19",
                "-b:v", "0", "-profile:v", "high"]
    if c == "h264_videotoolbox":
        return ["-c:v", "h264_videotoolbox", "-q:v", "70", "-profile:v", "high"]
    return ["-c:v", "libx264", *qualidade_cpu]


def resumo(a):
    ff, tr, v = a["ffmpeg"], a["transcricao"], a["veredito"]
    linhas = [
        f"Ambiente ({a['medido_em']}): {a['sistema']}{' [Colab]' if a['colab'] else ''}, "
        f"{a['cpu_nucleos']} núcleos, {a['ram_gb']} GB RAM, {a['disco_livre_gb']} GB livres",
        f"GPU NVIDIA: {a['gpu_nvidia'] or 'não'} | codificador: {ff.get('codificador') or '-'} | "
        f"transcrição: {tr['motor'] or 'nenhuma'}",
        f"FFmpeg: {ff.get('versao', 'não encontrado')[:60]}",
        f"Google Drive: {a['drive'] or 'não encontrado neste computador'}",
    ]
    t = a.get("teste_velocidade")
    if t:
        linhas.append(f"Velocidade: {t['fator_tempo_real']}x tempo real ({t['codificador']}); "
                      f"Reels de 60 s ~ {t['estimativa_60s_min']} min")
    linhas.append(f"Falta: {'; '.join(v['falta']) or 'nada'} | Obs.: {'; '.join(v['observacoes']) or '-'}")
    linhas.append(f"Recomendação: {v['recomendacao']}")
    return "\n".join(linhas)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(resumo(carrega("--refazer" in sys.argv)))
