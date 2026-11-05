# -*- coding: utf-8 -*-
"""Amostras A/B de cadeias de limpeza de voz, todas igualadas em -14 LUFS
(para o ouvido não ser enganado por volume), com medidas lado a lado.

Uso: python cadeias_audio.py <bruto> <pasta_saida> <ini> <fim>
  Trecho de 8 a 15 s com fala e pausas. Saída: <nome>.wav por cadeia + tabela.
  Editar CADEIAS abaixo para testar outras combinações.

Medidas: I (LUFS), TP (pico real), piso nas pausas (dB), fala-piso (quanto a
fala fica acima do ruído), cauda (queda média 100 ms depois do fim das frases:
quanto mais negativa, menos eco).
"""
import os
import re
import subprocess
import sys

import numpy as np

MONO = "pan=mono|c0=0.5*c0+0.5*c1"
# atrim=start_sample=1200 compensa o atraso de 25 ms do afftdn a 48 kHz
CADEIAS = {
    "0_original": "anull",
    "1_leve": ("highpass=f=80,afftdn=nf=-44:nr=10:nt=w,atrim=start_sample=1200,asetpts=N/SR/TB,"
               "equalizer=f=300:t=q:w=1:g=-3"),
    "2_media": ("highpass=f=90,afftdn=nf=-42:nr=15:nt=w,atrim=start_sample=1200,asetpts=N/SR/TB,"
                "equalizer=f=250:t=q:w=1.2:g=-4,equalizer=f=3000:t=q:w=1:g=2,"
                "agate=threshold=0.02:ratio=2:range=0.25:attack=5:release=120:knee=4,"
                "acompressor=threshold=0.063:ratio=2.5:attack=10:release=150"),
    "3_forte": ("highpass=f=100,afftdn=nf=-40:nr=20:nt=w,atrim=start_sample=1200,asetpts=N/SR/TB,"
                "anlmdn=s=0.0005:p=0.002:r=0.006,equalizer=f=250:t=q:w=1.2:g=-5,"
                "equalizer=f=450:t=q:w=1.5:g=-2,equalizer=f=3000:t=q:w=1:g=3,"
                "agate=threshold=0.025:ratio=3:range=0.1:attack=3:release=80:knee=3,"
                "acompressor=threshold=0.063:ratio=3:attack=8:release=120"),
    "4_eco_sala": ("highpass=f=90,afftdn=nf=-42:nr=15:nt=w,atrim=start_sample=1200,asetpts=N/SR/TB,"
                   "equalizer=f=250:t=q:w=1.2:g=-4,equalizer=f=3000:t=q:w=1:g=2,"
                   "agate=threshold=0.022:ratio=2.5:range=0.18:attack=4:release=90:knee=3,"
                   "deesser=i=0.3,acompressor=threshold=0.063:ratio=2.5:attack=10:release=150"),
}


def roda(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("ffmpeg falhou:\n" + r.stderr[-1500:])
    return r


def ebur(arq):
    s = roda(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    s = s[s.rfind("Summary:"):]
    return (float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)),
            float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1)))


def carrega_bin(arq):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-f", "f32le", "-ac", "1", "-ar", "48000", "-"],
                       capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)


def envelope(x, w=0.01, sr=48000):
    n = int(sr * w)
    m = len(x) // n
    return 20 * np.log10(np.maximum(np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1)), 1e-9))


def pausas(arq):
    s = roda(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "silencedetect=n=-35dB:d=0.18",
              "-f", "null", "-"]).stderr
    ini = [float(v) for v in re.findall(r"silence_start: (-?[\d.]+)", s)]
    fim = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", s)]
    return list(zip(ini, fim))


def mede(arq, pz):
    x = carrega_bin(arq)
    i, tp = ebur(arq)
    e = envelope(x)
    fala = np.percentile(e, 90)
    trechos = [x[int(a * 48000):int(b * 48000)] for a, b in pz if b - a > 0.1]
    piso = 20 * np.log10(np.sqrt(np.mean(np.concatenate(trechos) ** 2)) + 1e-12) if trechos else float("nan")
    caudas = []
    for a, _ in pz:
        k = int(a / 0.01)
        if 5 <= k < len(e) - 10:
            caudas.append(e[k + 10] - e[k - 2])
    return i, tp, piso, fala - piso, float(np.median(caudas)) if caudas else float("nan")


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    bruto, saida, ini, fim = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    os.makedirs(saida, exist_ok=True)
    dur = fim - ini
    # pausas medidas uma vez no trecho original, sem ganho (valem para todas as cadeias)
    cru = os.path.join(saida, "_cru.wav")
    roda(["ffmpeg", "-v", "error", "-y", "-ss", str(ini), "-to", str(fim), "-i", bruto, "-af", MONO,
          "-ar", "48000", "-c:a", "pcm_s24le", cru])
    pz = pausas(cru)
    os.remove(cru)
    linhas = []
    for nome, cadeia in CADEIAS.items():
        pre = os.path.join(saida, f"_pre_{nome}.wav")
        roda(["ffmpeg", "-v", "error", "-y", "-ss", str(ini), "-to", str(fim), "-i", bruto, "-af",
              f"{MONO},apad=pad_dur=1,{cadeia}", "-t", f"{dur:.3f}", "-ar", "48000", "-c:a", "pcm_s24le", pre])
        i0, _ = ebur(pre)
        out = os.path.join(saida, f"{nome}.wav")
        roda(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af",
              f"volume={-14.0 - i0:.2f}dB,alimiter=limit=0.84:attack=5:release=50:level=false,"
              f"afade=t=in:d=0.02,afade=t=out:st={dur - 0.05:.2f}:d=0.05",
              "-ar", "48000", "-c:a", "pcm_s24le", out])
        os.remove(pre)
        linhas.append((nome, -14.0 - i0, *mede(out, pz)))
    print(f"{'amostra':14s} ganho    I     TP   piso  fala-piso  cauda100ms")
    for n, g, i, tp, piso, snr, cauda in linhas:
        print(f"{n:14s} {g:+5.1f} {i:5.1f} {tp:5.1f} {piso:6.1f}   {snr:6.1f}    {cauda:6.1f}")
    print(f"\nAmostras em {saida}. O usuário escolhe no ouvido (fone).")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
