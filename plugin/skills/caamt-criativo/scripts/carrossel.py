# -*- coding: utf-8 -*-
"""Carrossel 1080x1350 (3 a 7 telas): capa, uma ideia por tela e tela final com chamada.

  python carrossel.py telas.json

telas.json (caminhos relativos ao próprio .json):
{
  "saida": "carrossel",                      # pasta das telas (tela-01.png, tela-02.png...)
  "cores": {"fundo": "#0B3D91", "texto": "#FFFFFF", "destaque": "#E8B45A"},   # do MARCA.md
  "fonte_titulo": "Poppins-ExtraBold.ttf", "fonte_texto": "Poppins-Bold.ttf",  # opcional
  "rodape": "rodape_logos_brancos.png",      # opcional, da marca da subseção
  "fundo_capa": "base.png",                  # opcional, saída do fundo.py
  "capa": {"rotulo": "ALERTA", "titulo": "Golpe do falso advogado"},
  "telas": [{"titulo": "Como reconhecer", "texto": "Pedido de pagamento por WhatsApp..."}],
  "final": {"titulo": "Na dúvida, ligue para o seu advogado", "texto": "OAB Subseção de ..."}
}
O texto vem conferido com a pauta (aba Pautas). Nada de texto desenhado por gerador de imagem.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H, M = 1080, 1350, 96
AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = os.path.join(AQUI, "..", "modelos", "barra-do-garcas")


def cor(h):
    h = h.lstrip("#")
    h = "".join(c * 2 for c in h) if len(h) == 3 else h
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def fonte(caminho, base, padrao, t):
    for c in ([os.path.join(base, caminho)] if caminho else []) + [os.path.join(MODELO, padrao),
              r"C:\Windows\Fonts\segoeuib.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]:
        if c and os.path.exists(c):
            return ImageFont.truetype(c, t)
    return ImageFont.load_default()


def quebrar(d, txt, f, larg):
    linhas, atual = [], ""
    for p in (txt or "").split():
        tenta = (atual + " " + p).strip()
        if d.textlength(tenta, font=f) <= larg:
            atual = tenta
        else:
            linhas.append(atual)
            atual = p
    return linhas + ([atual] if atual else [])


def escrever(d, xy, txt, f, c, larg, entre=1.25):
    x, y = xy
    for l in quebrar(d, txt, f, larg):
        d.text((x, y), l, font=f, fill=c)
        y += int(f.size * entre)
    return y


def tela(c, base, n, total, rotulo, titulo, texto, fundo=None, grande=False):
    img = Image.new("RGB", (W, H), cor(c["cores"].get("fundo", "#0B3D91")))
    if fundo:
        img.paste(Image.open(os.path.join(base, fundo)).convert("RGB").resize((W, H)))
    d = ImageDraw.Draw(img)
    tx, dest = cor(c["cores"].get("texto", "#FFFFFF")), cor(c["cores"].get("destaque", "#E8B45A"))
    ft = fonte(c.get("fonte_titulo"), base, "Poppins-ExtraBold.ttf", 88 if grande else 70)
    fx = fonte(c.get("fonte_texto"), base, "Poppins-Bold.ttf", 46)
    alto = (len(quebrar(d, titulo, ft, W - 2 * M)) * int(ft.size * 1.12) + 70
            + len(quebrar(d, texto, fx, W - 2 * M)) * int(fx.size * 1.4))
    y = max(220, (H - 160 - alto) // 2)  # bloco centrado, acima do rodapé
    if rotulo:
        d.text((M, y - 70), rotulo.upper(), font=fonte(c.get("fonte_texto"), base, "Poppins-Bold.ttf", 30), fill=dest)
    y = escrever(d, (M, y), titulo, ft, tx, W - 2 * M, 1.12)
    d.rectangle([M, y + 24, M + 120, y + 32], fill=dest)
    escrever(d, (M, y + 70), texto, fx, tx, W - 2 * M, 1.4)
    d.text((W - M - 80, 120), "%d/%d" % (n, total), font=fonte(c.get("fonte_texto"), base, "Poppins-Bold.ttf", 28), fill=tx)
    if c.get("rodape") and os.path.exists(os.path.join(base, c["rodape"])):
        r = Image.open(os.path.join(base, c["rodape"])).convert("RGBA")
        r = r.resize((round(r.width * 80 / r.height), 80))
        img.paste(r, ((W - r.width) // 2, H - 140), r)
    return img


def main(arq):
    base = os.path.dirname(os.path.abspath(arq))
    c = json.load(open(arq, encoding="utf-8"))
    telas = c.get("telas", [])
    total = len(telas) + 2
    if not 3 <= total <= 7:
        sys.exit("Carrossel tem de ter de 3 a 7 telas (capa + %d + final = %d)." % (len(telas), total))
    saida = os.path.join(base, c.get("saida", "carrossel"))
    os.makedirs(saida, exist_ok=True)
    seq = [(c["capa"].get("rotulo"), c["capa"]["titulo"], c["capa"].get("texto", ""), c.get("fundo_capa"), True)]
    seq += [(None, t["titulo"], t.get("texto", ""), None, False) for t in telas]
    seq += [(None, c["final"]["titulo"], c["final"].get("texto", ""), None, True)]
    for i, (rot, tit, txt, fun, gr) in enumerate(seq, 1):
        p = os.path.join(saida, "tela-%02d.png" % i)
        tela(c, base, i, total, rot, tit, txt, fun, gr).save(p)
        print(p)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
