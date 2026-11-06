# -*- coding: utf-8 -*-
"""Capa (miniatura) 1080x1920 a partir de um quadro do próprio vídeo.

MODELO: copiar para scripts/ do projeto, preencher a CONFIGURAÇÃO e rodar.
Quadro: sorriso de verdade (antes da primeira palavra ou logo depois da
última), conferido em tamanho grande. Sem sorriso no material: avisar o usuário.
Texto só dentro do recorte 4:5 do feed (y 285 a 1635); o script recusa fora disso.
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

def _acha_scripts():
    """Pasta scripts/ da skill: EDICAO_VIDEO_SCRIPTS > ~/.edicao-video/config.json > pasta deste arquivo."""
    p = os.environ.get("EDICAO_VIDEO_SCRIPTS")
    if not p:
        try:
            with open(os.path.join(os.path.expanduser("~"), ".edicao-video", "config.json"), encoding="utf-8") as f:
                p = json.load(f).get("scripts")
        except (OSError, ValueError):
            p = None
    if not p or not os.path.exists(os.path.join(p, "marca.py")):
        p = os.path.dirname(os.path.abspath(__file__))
    return p


SKILL = _acha_scripts()
sys.path.insert(0, SKILL)
from marca import carrega  # noqa: E402
from montar_video import tonemap_de  # noqa: E402

# ------------------------------------------------------------ CONFIGURAÇÃO
PROJETO = None                     # raiz do projeto (None = procura marca/ subindo do cwd)
VIDEO = r"<pasta-do-video>\brutos\<take>.MOV"
TEMPO = 0.0                        # segundo do quadro escolhido
ZOOM = 1.30                        # aproximação no rosto
ROSTO = (540, 800)                 # centro do rosto no quadro 1080x1920
ROSTO_Y_FINAL = 700                # onde o rosto fica na capa
SAIDA = r"<pasta-do-video>\capas\capa_01_<NOME>_V1.jpg"
# (y do topo, [linhas], [tamanhos], papel da cor do texto, papel da cor da caixa)
CAIXAS = [
    (318, ["GANCHO DA CAPA"], [58], "fundo", "principal"),
    (1300, ["LINHA MENOR", "DESTAQUE"], [50, 150], "texto_escuro", "destaque"),
]
# Arte da marca por cima (PNG transparente 9:16, ex.: rodapé com logos da subseção) ou None.
# Os logos (pixels brancos) são subidos até caberem no recorte 4:5 do feed; o buraco embaixo
# é preenchido com a cor da última linha da arte.
RODAPE = None                      # ex.: r"<projeto>\marca\logos\rodape-....png"
# Capa pronta sugerida pelo usuário (imagem): usa no lugar do quadro do vídeo.
CAPA_DO_USUARIO = None
FEED_4x5 = (285, 1635)
W, H = 1080, 1920


def quadro():
    tmp = os.path.join(os.path.dirname(SAIDA), "_quadro_base.png")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    tm = tonemap_de(VIDEO)
    vf = (tm + "," if tm else "") + "scale=1080:1920:flags=lanczos"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(TEMPO), "-i", VIDEO, "-vf", vf,
                    "-frames:v", "1", tmp], check=True)
    img = Image.open(tmp).convert("RGB")
    os.remove(tmp)
    cw, ch = W / ZOOM, H / ZOOM
    x0 = min(max(ROSTO[0] - cw / 2, 0), W - cw)
    y0 = min(max(ROSTO[1] - ROSTO_Y_FINAL / ZOOM, 0), H - ch)
    return img.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((W, H), Image.LANCZOS)


def caixa(d, cy, linhas, fontes, cor_txt, cor_fundo, pad=(44, 26), gap=14):
    med = [d.textbbox((0, 0), l, font=f) for l, f in zip(linhas, fontes)]
    larg = max(b[2] - b[0] for b in med)
    alts = [b[3] - b[1] for b in med]
    alt = sum(alts) + gap * (len(linhas) - 1)
    x0, y0 = (W - larg) / 2 - pad[0], cy - pad[1]
    y1 = y0 + alt + 2 * pad[1]
    if y0 < FEED_4x5[0] or y1 > FEED_4x5[1] or larg + 2 * pad[0] > W - 40:
        sys.exit(f"caixa {linhas} fora do recorte 4:5 (y {y0:.0f} a {y1:.0f}) ou larga demais")
    d.rounded_rectangle([x0, y0, x0 + larg + 2 * pad[0], y1], radius=26, fill=cor_fundo)
    y = cy
    for l, f, b, a in zip(linhas, fontes, med, alts):
        d.text(((W - (b[2] - b[0])) / 2 - b[0], y - b[1]), l, font=f, fill=cor_txt)
        y += a + gap
    return y1


def aplica_rodape(img, arq):
    """Põe a arte transparente por cima; sobe o que for logo branco até y 1600 (dentro do 4:5)."""
    import numpy as np
    rod = Image.open(arq).convert("RGBA").resize((W, H), Image.LANCZOS)
    a = np.array(rod)
    brancos = np.where(((a[:, :, :3].min(2) > 230) & (a[:, :, 3] > 200)).sum(1) > 20)[0]
    sobe = max(0, int(brancos.max()) - (FEED_4x5[1] - 35)) if len(brancos) else 0
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    camada.paste(rod, (0, -sobe))
    if sobe:
        fundo = tuple(int(x) for x in a[H - 1, W // 2, :3])
        camada.paste(Image.new("RGBA", (W, sobe), fundo + (255,)), (0, H - sobe))
    return Image.alpha_composite(img.convert("RGBA"), camada).convert("RGB")


def main():
    for v in (VIDEO, SAIDA):
        if "<" in v or ">" in v:
            sys.exit(f"trocar o marcador <...> na configuração: {v}")
    m = carrega(PROJETO)
    m.confere_texto([l for c in CAIXAS for l in c[1]])
    if CAPA_DO_USUARIO:
        img = Image.open(CAPA_DO_USUARIO).convert("RGB")
        if img.size != (W, H):        # cobre 9:16 sem distorcer (corta o excesso no centro)
            esc = max(W / img.width, H / img.height)
            img = img.resize((round(img.width * esc), round(img.height * esc)), Image.LANCZOS)
            x0, y0 = (img.width - W) // 2, (img.height - H) // 2
            img = img.crop((x0, y0, x0 + W, y0 + H))
    else:
        img = quadro()
    d = ImageDraw.Draw(img)
    for y, linhas, tams, c_txt, c_fundo in CAIXAS:
        fontes = [ImageFont.truetype(m.fonte("legenda"), t) for t in tams]
        caixa(d, y, linhas, fontes, m.cor(c_txt), m.cor(c_fundo))
    if RODAPE:
        img = aplica_rodape(img, RODAPE)
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    img.save(SAIDA, quality=92)
    print(SAIDA)


if __name__ == "__main__":
    main()
