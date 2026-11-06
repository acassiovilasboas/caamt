# -*- coding: utf-8 -*-
"""Prepara a imagem de base de um post (1080x1350) a partir de uma foto.

Uso:
  python fundo.py FOTO SAIDA.png --modo fundo --cor "#0B3D91" [--foco 0.5,0.3] [--forca 0.6]

Modos (o agente diretor-de-arte escolhe):
  limpo   foto inteira, sem efeito (texto vai num cartão por cima, pequeno)
  topo    foto nítida em cima, que se dissolve na cor da marca embaixo (texto embaixo)
  lado    foto nítida à direita, dissolvida na cor da marca à esquerda (texto à esquerda)
  fundo   foto desfocada e escurecida, coberta pela cor da marca (texto em qualquer lugar)
  duotone foto em dois tons da cor da marca, discreta (texto em qualquer lugar)

--foco   ponto que não pode sair do corte (x,y de 0 a 1; ver o catálogo da biblioteca)
--forca  quanto a cor da marca cobre a foto (0 a 1; padrão 0.6)
--tam    tamanho final (padrão 1080x1350; Stories: 1080x1920)
"""
import argparse
from PIL import Image, ImageFilter, ImageOps


def cor(h):
    import re
    m = re.search(r"#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})", h or "")
    if not m:
        raise SystemExit("Cor inválida: %r (use #RRGGBB ou #RGB)" % h)
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cortar(im, w, h, fx, fy):
    """Corta a foto na proporção w:h mantendo o ponto de foco dentro do quadro."""
    W, H = im.size
    alvo = w / h
    if W / H > alvo:
        cw, ch = int(H * alvo), H
    else:
        cw, ch = W, int(W / alvo)
    x = min(max(int(fx * W - cw / 2), 0), W - cw)
    y = min(max(int(fy * H - ch / 2), 0), H - ch)
    return im.crop((x, y, x + cw, y + ch)).resize((w, h), Image.LANCZOS)


def degrade(w, h, c, de, ate, vertical=True, inicio=0.45, fim=0.8):
    """Máscara: opacidade 'de' até 'ate' entre 'inicio' e 'fim' do eixo."""
    m = Image.new("L", (w, h))
    n = h if vertical else w
    px = []
    for i in range(n):
        t = min(max((i / n - inicio) / max(fim - inicio, 1e-6), 0), 1)
        px.append(int(255 * (de + (ate - de) * t)))
    linha = Image.new("L", (1, n) if vertical else (n, 1))
    linha.putdata(px)
    return linha.resize((w, h))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("foto"); a.add_argument("saida")
    a.add_argument("--modo", default="fundo", choices=["limpo", "topo", "lado", "fundo", "duotone"])
    a.add_argument("--cor", default="#0B3D91")
    a.add_argument("--foco", default="0.5,0.4")
    a.add_argument("--forca", type=float, default=0.6)
    a.add_argument("--tam", default="1080x1350")
    o = a.parse_args()
    w, h = (int(v) for v in o.tam.split("x"))
    fx, fy = (float(v) for v in o.foco.split(","))
    base = cor(o.cor)
    im = cortar(ImageOps.exif_transpose(Image.open(o.foto)).convert("RGB"), w, h, fx, fy)
    plano = Image.new("RGB", (w, h), base)

    if o.modo == "limpo":
        out = im
    elif o.modo == "topo":
        out = Image.composite(plano, im, degrade(w, h, base, 0, 1, True, 0.36, 0.8))
    elif o.modo == "lado":
        out = Image.composite(plano, im, degrade(w, h, base, 1, 0, False, 0.15, 0.6))
    elif o.modo == "fundo":
        borrada = im.filter(ImageFilter.GaussianBlur(radius=max(w, h) / 90))
        escura = Image.blend(borrada, Image.new("RGB", (w, h), (0, 0, 0)), 0.25)
        out = Image.blend(escura, plano, min(max(o.forca, 0), 1))
    else:  # duotone
        g = ImageOps.grayscale(im)
        escuro = tuple(int(c * 0.35) for c in base)
        claro = tuple(min(255, int(c + (255 - c) * 0.55)) for c in base)
        out = ImageOps.colorize(g, escuro, claro)
        out = Image.blend(out, plano, min(max(o.forca, 0), 1) * 0.5)
    out.save(o.saida)
    print("OK:", o.saida, o.modo, "%dx%d" % (w, h))


if __name__ == "__main__":
    main()
