# -*- coding: utf-8 -*-
"""Transcreve fala em SRT.

Uso: python whisper.py <entrada> <saida.srt> [ini] [fim] [max_len]
  max_len=1 (padrão) = uma palavra por legenda, com tempo por palavra.
  ini/fim em segundos: retranscrever uma janela isolada para conferir trecho duvidoso
  (os tempos do SRT saem relativos a ini).

Motor (WHISPER_MOTOR = auto | ffmpeg | faster), auto escolhe nesta ordem:
  1. faster-whisper na GPU NVIDIA (Colab): rápido, modelo WHISPER_FASTER_MODELO (padrão medium);
  2. filtro whisper do FFmpeg (8.0+) com o modelo ggml (baixar_modelo.py);
  3. faster-whisper na CPU (modelo small).
Idioma: WHISPER_LANG (padrão pt). Pasta dos modelos: ~/.edicao-video/modelos
(ou WHISPER_MODELOS / config.json). O filtro do FFmpeg não aceita 'C:' no caminho
do modelo: roda com a pasta do modelo como diretório atual.
"""
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ambiente  # noqa: E402

LINGUA = os.environ.get("WHISPER_LANG", "pt")
MODELO_GGML = os.environ.get("WHISPER_MODELO", ambiente.MODELO_GGML)


def _srt_ts(t):
    ms = int(round(max(0.0, t) * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def _cuda():
    return ambiente.faster_whisper()["cuda"]


def _carrega_cuda_pip():
    """Carrega cuBLAS/cuDNN dos pacotes pip nvidia-* (o Colab nem sempre traz as versões que o
    ctranslate2 pede: 'libcublas.so.12 is not found', 03/11/2026). Sem os pacotes, não faz nada."""
    if not sys.platform.startswith("linux"):
        return
    import ctypes
    import glob
    import site
    bases = site.getsitepackages() + [site.getusersitepackages()]
    libs = []
    for b in bases:
        for p in ("nvidia/cublas/lib/libcublasLt.so.*", "nvidia/cublas/lib/libcublas.so.*",
                  "nvidia/cudnn/lib/libcudnn*.so.*"):
            libs += sorted(glob.glob(os.path.join(b, p)))
    for _ in range(2):          # 2ª volta pega as que dependiam de outra ainda não carregada
        for so in libs:
            try:
                ctypes.CDLL(so, mode=ctypes.RTLD_GLOBAL)
            except OSError:
                pass


def escolhe_motor():
    m = os.environ.get("WHISPER_MOTOR", "auto")
    if m != "auto":
        return m
    fw = ambiente.faster_whisper()
    if fw["instalado"] and fw["cuda"]:
        return "faster"
    if os.path.exists(os.path.join(ambiente.pasta_modelos(), MODELO_GGML)) and shutil.which("ffmpeg"):
        return "ffmpeg"
    if fw["instalado"]:
        return "faster"
    sys.exit("sem motor de transcrição: rodar baixar_modelo.py (FFmpeg 8+) ou pip install faster-whisper")


def via_ffmpeg(entrada, saida, ini, fim, max_len):
    dest = saida.replace("\\", "/").replace(":", "\\\\:")
    cmd = ["ffmpeg", "-hide_banner", "-v", "error", "-y"]
    if ini:
        cmd += ["-ss", str(ini)]
    if fim:
        cmd += ["-to", str(fim)]
    cmd += ["-i", entrada, "-af",
            f"whisper=model={MODELO_GGML}:language={LINGUA}:queue=600:max_len={max_len}:"
            f"destination={dest}:format=srt", "-f", "null", "-"]
    r = subprocess.run(cmd, cwd=ambiente.pasta_modelos(), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0 or not os.path.exists(saida):
        sys.exit("whisper (ffmpeg) falhou:\n" + r.stderr[-1500:])


def via_faster(entrada, saida, ini, fim, max_len):
    from faster_whisper import WhisperModel
    gpu = _cuda()
    nome = os.environ.get("WHISPER_FASTER_MODELO", "medium" if gpu else "small")
    import numpy as np
    # áudio decodificado pelo FFmpeg e entregue como array: não depende do PyAV
    # (faster-whisper 1.x + PyAV novo quebra em av.open(metadata_errors=...), Colab 03/11/2026)
    cmd = ["ffmpeg", "-hide_banner", "-v", "error"]
    if ini:
        cmd += ["-ss", str(ini)]
    if fim:
        cmd += ["-to", str(fim)]
    r = subprocess.run(cmd + ["-i", entrada, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                       capture_output=True)
    if r.returncode != 0:
        sys.exit("ffmpeg não leu o áudio:\n" + r.stderr.decode("utf-8", "replace")[-1500:])
    audio = np.frombuffer(r.stdout, dtype=np.float32)
    raiz = os.path.join(ambiente.pasta_modelos(), "faster")

    def roda(gpu, nome):
        modelo = WhisperModel(nome, device="cuda" if gpu else "cpu",
                              compute_type="float16" if gpu else "int8", download_root=raiz)
        segs, _ = modelo.transcribe(audio, language=LINGUA, word_timestamps=True, beam_size=5)
        out = []
        for s in segs:           # a GPU só é usada de fato aqui (gerador)
            if str(max_len) == "1":
                out += [(w.start, w.end, w.word.strip()) for w in (s.words or []) if w.word.strip()]
            else:
                out.append((s.start, s.end, s.text.strip()))
        return out

    if gpu:
        _carrega_cuda_pip()
        try:
            itens = roda(True, nome)
        except RuntimeError as e:
            print(f"AVISO: GPU falhou ({str(e)[:120]}); transcrevendo na CPU (mais lento).", file=sys.stderr)
            itens = roda(False, os.environ.get("WHISPER_FASTER_MODELO", "small"))
    else:
        itens = roda(False, nome)
    with open(saida, "w", encoding="utf-8", newline="\n") as f:
        for i, (a, b, t) in enumerate(itens, 1):
            f.write(f"{i}\n{_srt_ts(a)} --> {_srt_ts(b)}\n{t}\n\n")


def transcreve(entrada, saida, ini=None, fim=None, max_len="1"):
    entrada, saida = os.path.abspath(entrada), os.path.abspath(saida)
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    motor = escolhe_motor()
    (via_faster if motor == "faster" else via_ffmpeg)(entrada, saida, ini, fim, max_len)
    return saida


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    a = sys.argv[1:] + [None] * 3
    out = transcreve(a[0], a[1], a[2], a[3], a[4] or "1")
    print(open(out, encoding="utf-8").read())
