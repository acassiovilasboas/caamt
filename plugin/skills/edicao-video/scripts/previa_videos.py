"""Gera prévias leves (MP4 H.264 SDR + pôster JPG) de brutos .mov/.mp4 para tocar no navegador.

O Chrome não toca .mov HEVC/HDR do iPhone; a galeria (galeria_videos.py) usa estas prévias.
A estrutura de pastas da raiz é espelhada em <saida>. Arquivo já gerado e mais novo que o
original é pulado, então dá para rodar de novo depois de cada lote.

Uso:
    python previa_videos.py "<Edicao-Video>\\<Projeto>" --pastas brutos final
    python previa_videos.py "<pasta>" --saida "<pasta>\\_previa"
"""
import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from montar_video import tonemap_de  # noqa: E402

EXT = (".mov", ".mp4", ".m4v")


def gerar(orig, dest, altura):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tm = tonemap_de(orig)
    vf = (tm + "," if tm else "") + f"scale=-2:{altura},format=yuv420p"
    tmp = dest + ".tmp.mp4"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", orig, "-vf", vf, "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "28", "-c:a", "aac", "-b:a", "96k",
                        "-movflags", "+faststart", tmp], capture_output=True, text=True)
    if r.returncode:
        return f"ERRO {orig}: {r.stderr.strip()[-300:]}"
    os.replace(tmp, dest)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", dest, "-frames:v", "1",
                    "-q:v", "5", dest[:-4] + ".jpg"], capture_output=True)
    return f"ok {dest}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raiz")
    ap.add_argument("--saida")
    ap.add_argument("--pastas", nargs="*", help="subpastas da raiz (padrão: todas)")
    ap.add_argument("--altura", type=int, default=640)
    ap.add_argument("-j", type=int, default=2, help="vídeos em paralelo")
    a = ap.parse_args()
    saida = a.saida or os.path.join(a.raiz, "_previa")
    bases = [os.path.join(a.raiz, p) for p in a.pastas] if a.pastas else [a.raiz]
    tarefas = []
    for base in bases:
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if not d.startswith("_") and os.path.join(dp, d) != saida]
            for fn in fns:
                if not fn.lower().endswith(EXT):
                    continue
                orig = os.path.join(dp, fn)
                dest = os.path.join(saida, os.path.splitext(os.path.relpath(orig, a.raiz))[0] + ".mp4")
                if os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(orig):
                    continue
                tarefas.append((orig, dest))
    print(f"{len(tarefas)} prévias a gerar em {saida}", flush=True)
    with ThreadPoolExecutor(a.j) as ex:
        for i, msg in enumerate(ex.map(lambda t: gerar(*t, a.altura), tarefas), 1):
            print(f"[{i}/{len(tarefas)}] {msg}", flush=True)


if __name__ == "__main__":
    main()
