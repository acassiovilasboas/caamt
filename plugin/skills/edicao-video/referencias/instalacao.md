# Instalação das ferramentas

Instalar só com o "pode" do usuário, um item por vez, e conferir com
`ambiente.py --refazer` no fim. Explicar em uma linha para que serve cada coisa.

## Windows (winget, já vem no Windows 10/11)

| Item | Comando | Para que serve |
|---|---|---|
| Python 3 | `winget install -e --id Python.Python.3.12` | roda os scripts |
| Bibliotecas | `python -m pip install pillow numpy` | imagem e medição de áudio |
| FFmpeg completo | `winget install -e --id Gyan.FFmpeg` | corta, legenda, grava o vídeo |
| Modelo de transcrição | `python <skill>/scripts/baixar_modelo.py` (~466 MB) | entende a fala (FFmpeg 8+) |
| Google Drive para computador | `winget install -e --id Google.GoogleDrive` | vídeos do Drive como pasta; Colab |
| uv (só para o MCP do Colab) | `winget install -e --id astral-sh.uv` | roda o colab-mcp |

Depois de instalar Python ou FFmpeg, **fechar e abrir o Claude** (o PATH só atualiza assim).

## Mac (Homebrew: https://brew.sh)

`brew install python ffmpeg` · `python3 -m pip install pillow numpy` ·
`brew install --cask google-drive` · `brew install uv`.
Se o FFmpeg do brew não tiver o filtro `whisper`: `python3 -m pip install faster-whisper`
(o `whisper.py` usa sozinho).

## Alternativa à transcrição pelo FFmpeg

`python -m pip install faster-whisper`: funciona em qualquer FFmpeg; baixa o modelo
na primeira transcrição. Em GPU NVIDIA com CUDA é bem mais rápido.

## Conferir

`python <skill>/scripts/ambiente.py --refazer` → "Falta: nada".
