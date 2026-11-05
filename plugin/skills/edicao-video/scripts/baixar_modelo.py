# -*- coding: utf-8 -*-
"""Baixa o modelo de transcrição ggml-small.bin (~466 MB) do repositório oficial do
whisper.cpp no Hugging Face para ~/.edicao-video/modelos. Pede confirmação do usuário
antes (o Claude pergunta no chat). Pula se já existir.

Uso: python baixar_modelo.py [nome=ggml-small.bin]
"""
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ambiente  # noqa: E402

URL = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/{}"


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else ambiente.MODELO_GGML
    pasta = ambiente.pasta_modelos()
    os.makedirs(pasta, exist_ok=True)
    dest = os.path.join(pasta, nome)
    if os.path.exists(dest) and os.path.getsize(dest) > 1e8:
        print(f"já existe: {dest}")
        return
    tmp = dest + ".parcial"

    def prog(n, tam, total):
        if total > 0 and n % 200 == 0:
            print(f"  {min(100, n * tam * 100 // total)}%", flush=True)
    urllib.request.urlretrieve(URL.format(nome), tmp, prog)
    os.replace(tmp, dest)
    ambiente.atualiza_config({"modelos": pasta})
    print(f"ok: {dest}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
