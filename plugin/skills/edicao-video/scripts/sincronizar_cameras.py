# -*- coding: utf-8 -*-
"""Acha o atraso entre duas câmeras que gravaram a mesma cena, pelo som.

  python sincronizar_cameras.py <camera_base> <outra_camera> [--seg 120]

Imprime: ATRASO_S=<n>. Positivo = a outra câmera começou a gravar depois da base, então o
instante t da base corresponde a t - ATRASO_S na outra. Usar nos PLANOS do montar_video.py
(trecho da outra câmera = trecho da base - ATRASO_S). CONFIANCA baixa (< 8): conferir no ouvido.
"""
import subprocess
import sys

import numpy as np

TAXA = 8000


def audio(arq, seg):
    cmd = ["ffmpeg", "-v", "error", "-i", arq, "-t", str(seg), "-ac", "1", "-ar", str(TAXA),
           "-f", "s16le", "-"]
    bruto = subprocess.run(cmd, capture_output=True, check=True).stdout
    x = np.frombuffer(bruto, dtype=np.int16).astype(np.float32)
    if x.size == 0:
        sys.exit("Sem áudio em " + arq)
    return (x - x.mean()) / (x.std() + 1e-9)


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    seg = float(a[a.index("--seg") + 1]) if "--seg" in a else 120.0
    base, outra = audio(a[0], seg), audio(a[1], seg)
    n = 1
    while n < base.size + outra.size:
        n *= 2
    corr = np.fft.irfft(np.fft.rfft(base, n) * np.conj(np.fft.rfft(outra, n)), n)
    pico = int(np.argmax(corr))
    atraso = pico if pico < n // 2 else pico - n  # amostras: base[t] ~ outra[t - atraso]
    confianca = float((corr[pico] - corr.mean()) / (corr.std() + 1e-9))
    print("ATRASO_S=%.3f" % (atraso / TAXA))
    print("CONFIANCA=%.1f" % confianca)


if __name__ == "__main__":
    main(sys.argv[1:])
