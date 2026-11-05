# -*- coding: utf-8 -*-
"""Roda NO COMPUTADOR do usuário. Manda tarefa pesada para o Colab pela pasta do Google
Drive (Drive para computador sincronizado) e lê o resultado. Ver referencias/colab.md.

Uso:
    python colab_job.py kit                       # copia os scripts da skill para Edicao-Video/_kit/scripts
    python colab_job.py enviar <nome> "<cmd1>" ["<cmd2>" ...] [--cwd <pasta>]
    python colab_job.py status [<id>]             # resumo curto (sem id: tudo da fila e feito)

Exemplo (transcrever no Colab um bruto que já está no Drive):
    python colab_job.py enviar transc_01 "python {scripts}/whisper.py \"G:/Meu Drive/Edicao-Video/X/brutos/a.mp4\" \"G:/Meu Drive/Edicao-Video/X/transcricao/a.srt\""

Caminhos dentro do Drive local viram {drive}/...; scripts da skill viram {scripts}/...
Tudo precisa estar dentro do Drive: o Colab não enxerga o disco do computador.
"""
import glob
import json
import os
import shlex
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ambiente  # noqa: E402

SCRIPTS = os.path.dirname(os.path.abspath(__file__))


def raiz_drive():
    d = ambiente.config().get("drive") or ambiente.acha_drive()
    if not d:
        sys.exit("Google Drive para computador não encontrado. Ver referencias/colab.md (passo 1).")
    return d


def pastas():
    base = os.path.join(raiz_drive(), "Edicao-Video")
    return base, os.path.join(base, "_colab", "fila"), os.path.join(base, "_colab", "feito")


def converte(arg, drive):
    a = arg.replace("\\", "/")
    for raiz, marca in ((SCRIPTS.replace("\\", "/"), "{scripts}"), (drive.replace("\\", "/"), "{drive}")):
        if a.lower().startswith(raiz.lower()):
            return marca + a[len(raiz):]
    if len(a) > 2 and a[1] == ":" and a[2] == "/":
        sys.exit(f"caminho fora do Drive (o Colab não enxerga): {arg}")
    return a


def kit():
    base, _, _ = pastas()
    dest = os.path.join(base, "_kit", "scripts")
    os.makedirs(dest, exist_ok=True)
    n = 0
    for f in glob.glob(os.path.join(SCRIPTS, "*.py")):
        shutil.copy2(f, dest)
        n += 1
    nb = os.path.join(os.path.dirname(SCRIPTS), "colab", "edicao_video_gpu.ipynb")
    if os.path.exists(nb):
        shutil.copy2(nb, os.path.join(base, "_kit"))
    print(f"{n} scripts copiados para {dest}")


def enviar(nome, cmds, cwd):
    drive = raiz_drive()
    _, fila, _ = pastas()
    os.makedirs(fila, exist_ok=True)
    jid = time.strftime("%Y%m%d-%H%M%S") + "_" + "".join(c for c in nome if c.isalnum() or c in "-_")
    passos = []
    for c in cmds:
        partes = shlex.split(c.replace("\\", "/"))
        passos.append({"cmd": [converte(p, drive) for p in partes],
                       "cwd": converte(cwd, drive) if cwd else None})
    with open(os.path.join(fila, jid + ".json"), "w", encoding="utf-8") as f:
        json.dump({"id": jid, "criado_em": time.strftime("%Y-%m-%d %H:%M"), "passos": passos},
                  f, ensure_ascii=False, indent=1)
    print(f"tarefa {jid} na fila. O Drive leva alguns segundos para sincronizar.")


def status(jid=None):
    _, fila, feito = pastas()
    if jid:
        arq = os.path.join(feito, jid + ".json")
        if not os.path.exists(arq):
            print("ainda na fila" if os.path.exists(os.path.join(fila, jid + ".json")) else "não encontrada")
            return
        r = json.load(open(arq, encoding="utf-8"))
        print(f"{jid}: {'OK' if r['ok'] else 'FALHOU'} ({r['inicio']} a {r['fim']})")
        for p in r["passos"]:
            print(f"  código {p['codigo']} em {p.get('segundos', '-')} s")
            if p["codigo"] != 0:
                print("  " + p["saida"][-600:])
        return
    print("na fila:", [os.path.basename(f)[:-5] for f in sorted(glob.glob(os.path.join(fila, "*.json")))])
    print("feitas:", [os.path.basename(f)[:-5] for f in sorted(glob.glob(os.path.join(feito, "*.json")))
                      if not f.endswith(".pedido.json")][-10:])


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cwd = None
    if "--cwd" in a:
        i = a.index("--cwd")
        cwd = a[i + 1]
        del a[i:i + 2]
    if a[0] == "kit":
        kit()
    elif a[0] == "enviar" and len(a) >= 3:
        enviar(a[1], a[2:], cwd)
    elif a[0] == "status":
        status(a[1] if len(a) > 1 else None)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
