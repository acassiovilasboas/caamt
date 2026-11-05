# -*- coding: utf-8 -*-
"""Imagens fixas 1080x1920 com a marca do projeto (marca/marca.json).

- cartao_final: fundo na cor principal, logo, linha do CTA e botão na cor de
  destaque com seta. É o último quadro do vídeo (nunca preto: o Reels dá loop).
- cartela: fundo claro e texto, para cobrir emenda entre takes de fundos diferentes.

Uso: python cartelas.py <pasta_saida> [raiz_do_projeto]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marca import carrega  # noqa: E402

W, H = 1080, 1920


def centraliza(d, y, texto, f, cor):
    x0, y0, x1, y1 = d.textbbox((0, 0), texto, font=f)
    d.text(((W - (x1 - x0)) / 2 - x0, y - y0), texto, font=f, fill=cor)
    return y + (y1 - y0)


def cartao_final(saida, m):
    img = Image.new("RGB", (W, H), m.cor("principal"))
    d = ImageDraw.Draw(img)
    logo_arq = m.arquivo("logo_cartao_final", obrigatorio=False)
    y_texto = 1000
    if logo_arq:
        logo = Image.open(logo_arq).convert("RGBA")
        esc = min(820 / logo.width, 380 / logo.height)
        logo = logo.resize((round(logo.width * esc), round(logo.height * esc)), Image.LANCZOS)
        img.paste(logo, ((W - logo.width) // 2, 940 - logo.height), logo)
    linha1 = m.texto("cta", "cartao_linha1", padrao="CLIQUE EM")
    botao = m.texto("cta", "cartao_botao", padrao="SAIBA MAIS")
    m.confere_texto([linha1, botao])
    centraliza(d, y_texto, linha1, ImageFont.truetype(m.fonte("titulo"), 64), m.cor("fundo"))
    f = ImageFont.truetype(m.fonte("legenda"), 84)
    x0, y0, x1, y1 = d.textbbox((0, 0), botao, font=f)
    tw, th = x1 - x0, y1 - y0
    bx0, by0 = (W - tw) / 2 - 56, y_texto + 98
    d.rounded_rectangle([bx0, by0, bx0 + tw + 112, by0 + th + 64], radius=28, fill=m.cor("destaque"))
    d.text((bx0 + 56 - x0, by0 + 32 - y0), botao, font=f, fill=m.cor("texto_escuro"))
    sy = by0 + th + 100
    d.polygon([(W / 2 - 45, sy), (W / 2 + 45, sy), (W / 2, sy + 56)], fill=m.cor("destaque"))
    img.save(saida)
    return saida


def cartela(saida, m, linhas, fundo_img=None):
    """linhas: [(texto, tamanho, papel_da_cor)]. fundo_img: caminho opcional (padrão da marca)."""
    if fundo_img:
        img = Image.open(fundo_img).convert("RGB").resize((W, H), Image.LANCZOS)
        img = Image.blend(img, Image.new("RGB", (W, H), m.cor("fundo")), 0.5)
    else:
        img = Image.new("RGB", (W, H), m.cor("fundo"))
    d = ImageDraw.Draw(img)
    m.confere_texto([t for t, _, _ in linhas])
    y = 700
    for texto, tam, papel in linhas:
        y = centraliza(d, y, texto, ImageFont.truetype(m.fonte("legenda"), tam), m.cor(papel)) + 40
    img.save(saida)
    return saida


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    marca = carrega(sys.argv[2] if len(sys.argv) > 2 else None)
    print(cartao_final(os.path.join(out, "cartao_final.png"), marca))
