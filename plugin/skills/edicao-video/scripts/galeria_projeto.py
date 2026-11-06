# -*- coding: utf-8 -*-
"""Monta sozinho a página VER_VIDEOS.html da pasta Edicao-Video (padrão do kit).

Uso: python galeria_projeto.py <pasta Edicao-Video>

Varre <Edicao-Video>/<Projeto>/<vídeo>/ e põe na página, por projeto (aba) e vídeo (grupo):
  - final/*.mp4    -> "Prontos" (revisão pendente até o usuário aprovar)
  - brutos/*       -> "Brutos"
  - capas/*.jpg    -> pôster do primeiro vídeo pronto
  - drive.json     -> vídeos que só existem no Google Drive (sem cópia no computador):
                      [{"titulo": "...", "drive_id": "<id do arquivo>"}] -> toca embutido pelo
                      player do Drive (https://drive.google.com/file/d/<id>/preview).
                      Só toca para quem estiver logado numa conta com acesso ao arquivo.
Vídeo que o navegador já toca (H.264, sem HDR) entra direto, sem conversão. Os outros (HEVC,
.mov do iPhone, HDR) ganham uma prévia leve em <Edicao-Video>/_previa (previa_videos.py),
gerada uma vez só. Pastas que começam com "_" são ignoradas.
Abre com duplo clique, sem servidor. Rodar de novo depois de cada etapa: é rápido.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import galeria_videos  # noqa: E402
from previa_videos import gerar  # noqa: E402

EXT = (".mp4", ".mov", ".m4v", ".webm")


def toca_no_navegador(arq):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=codec_name,color_transfer", "-of", "json", arq],
                       capture_output=True, text=True)
    s = (json.loads(r.stdout or "{}").get("streams") or [{}])[0]
    return arq.lower().endswith(".mp4") and s.get("codec_name") == "h264" \
        and s.get("color_transfer") not in ("arib-std-b67", "smpte2084")


def video_para_html(arq, raiz):
    """Caminho relativo ao HTML de um arquivo que o navegador toca (original ou prévia)."""
    if toca_no_navegador(arq):
        return os.path.relpath(arq, raiz).replace("\\", "/")
    dest = os.path.join(raiz, "_previa", os.path.splitext(os.path.relpath(arq, raiz))[0] + ".mp4")
    if not (os.path.exists(dest) and os.path.getmtime(dest) >= os.path.getmtime(arq)):
        print("prévia:", gerar(arq, dest, 640), flush=True)
    return os.path.relpath(dest, raiz).replace("\\", "/")


def itens_de(pasta, raiz, situacao, poster=None):
    out = []
    if not os.path.isdir(pasta):
        return out
    for fn in sorted(os.listdir(pasta)):
        arq = os.path.join(pasta, fn)
        if not fn.lower().endswith(EXT) or not os.path.isfile(arq):
            continue
        it = {"id": os.path.relpath(arq, raiz).replace("\\", "/"), "titulo": os.path.splitext(fn)[0],
              "video": video_para_html(arq, raiz), "original": arq,
              "etiquetas": [f"{os.path.getsize(arq) / 2**20:.0f} MB"]}
        if situacao:
            it["situacao"] = situacao
        if poster and not out:
            it["poster"] = poster
        out.append(it)
    return out


def main(raiz):
    raiz = os.path.abspath(raiz)
    abas = []
    for proj in sorted(os.listdir(raiz)):
        pp = os.path.join(raiz, proj)
        if proj.startswith("_") or not os.path.isdir(pp):
            continue
        grupos = []
        for vid in sorted(os.listdir(pp), reverse=True):        # mais recente primeiro
            vp = os.path.join(pp, vid)
            if vid in ("marca",) or vid.startswith("_") or not os.path.isdir(vp):
                continue
            capa = None
            cp = os.path.join(vp, "capas")
            if os.path.isdir(cp):
                jpgs = sorted(f for f in os.listdir(cp) if f.lower().endswith((".jpg", ".png")))
                if jpgs:
                    capa = os.path.relpath(os.path.join(cp, jpgs[-1]), raiz).replace("\\", "/")
            subs = []
            prontos = itens_de(os.path.join(vp, "final"), raiz, "pendente", capa)
            if prontos:
                subs.append({"nome": "Prontos", "itens": prontos})
            dj = os.path.join(vp, "drive.json")
            if os.path.exists(dj):
                drive = [{"id": f"drive-{d['drive_id']}", "titulo": d.get("titulo", "vídeo no Drive"),
                          "embed": f"https://drive.google.com/file/d/{d['drive_id']}/preview",
                          "link": f"https://drive.google.com/file/d/{d['drive_id']}/view",
                          "link_texto": "Abrir no Drive", "etiquetas": ["no Drive"]}
                         for d in json.load(open(dj, encoding="utf-8"))]
                if drive:
                    subs.append({"nome": "No Google Drive", "itens": drive})
            brutos = itens_de(os.path.join(vp, "brutos"), raiz, None)
            if brutos:
                subs.append({"nome": "Brutos", "itens": brutos})
            if subs:
                leia = os.path.join(vp, "LEIA-ME.md")
                nota = None
                if os.path.exists(leia):
                    linha = open(leia, encoding="utf-8").readline().strip("# \n")
                    nota = linha or None
                grupos.append({"nome": vid, "nota": nota, "subgrupos": subs})
        if grupos:
            abas.append({"nome": proj, "grupos": grupos})
    if not abas:
        abas = [{"nome": "Vídeos", "grupos": [{"nome": "Nenhum vídeo ainda", "subgrupos": [{"nome": "-", "itens": []}]}]}]
    dados = {"titulo": "Vídeos · " + os.path.basename(raiz),
             "nota": "Prontos ficam como revisão pendente até você aprovar.", "abas": abas}
    tmp = os.path.join(raiz, "_galeria.json")
    os.makedirs(raiz, exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    saida = os.path.join(raiz, "VER_VIDEOS.html")
    galeria_videos.main(tmp, saida)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
