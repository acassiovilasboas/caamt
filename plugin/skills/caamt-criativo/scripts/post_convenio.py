# -*- coding: utf-8 -*-
"""Post de feed 1080x1350 "Convênio Disponível" (foto com a placa + cartão + faixa com o logo
do parceiro + base com os descontos + rodapé CAAMT | OAB | Subseção).

  python post_convenio.py <config.json>

config.json (caminhos relativos ao próprio .json):
{
  "foto": "foto_placa.jpg",            "foto_recorte": [0, 0, 1080, 575],  "foto_desloca_x": 0,
  "logo_parceiro": "logo_branco.png",  "categoria": "Clínica de Vacinação", "nome": "Saúde Livre",
  "publico": ["Descontos para os", "Advogados(as) e Dependentes"],
  "descontos": [["7% à vista", "PIX ou dinheiro"], ["2%", "no cartão de crédito"]],
  "obs": null,
  "modelo": "<pasta com titulo_convenio_disponivel.png, rodape_logos_brancos.png, Poppins-*.ttf>",
  "cores": {"fundo": [6,87,158], "fundo_escuro": [6,80,148], "faixa": [180,0,7],
            "texto_faixa": [160,20,28], "cartao": [255,252,238], "texto_cartao": [47,91,168]},
  "saida": "post_convenio-disponivel_<parceiro>_v1.jpg"
}
"cores" e "modelo" vêm do MARCA.md da subseção. O padrão de cores e o modelo que vêm no kit
são os do modelo de post da Subseção de Barra do Garças: outra subseção usa os
seus. O logo do parceiro entra como arquivo (versão branca), nunca desenhado.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1350
CARD = (61, 580, 509, 988)
FAIXA = (430, 748, 1019, 988)
CORTE = 748
PADRAO = {"fundo": [6, 87, 158], "fundo_escuro": [6, 80, 148], "faixa": [180, 0, 7],
          "texto_faixa": [160, 20, 28], "cartao": [255, 252, 238], "texto_cartao": [47, 91, 168]}


def fonte_texto():
    for c in (r"C:\Windows\Fonts\segoeui.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(c):
            return c
    return None


def f(arq, t):
    return ImageFont.truetype(arq, t) if arq else ImageFont.load_default()


def centro(d, cx, y, txt, fonte, cor):
    b = d.textbbox((0, 0), txt, font=fonte)
    d.text((cx - (b[2] - b[0]) / 2 - b[0], y - b[1]), txt, font=fonte, fill=cor)
    return y + (b[3] - b[1])


def cabe(d, txt, arq, t, larg):
    while d.textlength(txt, font=f(arq, t)) > larg and t > 12:
        t -= 1
    return f(arq, t)


def main(arq_cfg):
    base = os.path.dirname(os.path.abspath(arq_cfg))
    with open(arq_cfg, encoding="utf-8") as fh:
        c = json.load(fh)
    cam = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    cor = {k: tuple(v) for k, v in {**PADRAO, **c.get("cores", {})}.items()}
    mod = cam(c["modelo"])
    F_XB, F_B, F_R = (os.path.join(mod, "Poppins-ExtraBold.ttf"), os.path.join(mod, "Poppins-Bold.ttf"),
                      fonte_texto())
    branco = (255, 255, 255)

    img = Image.new("RGB", (W, H), cor["fundo"])
    fo = Image.open(cam(c["foto"])).convert("RGB")
    if c.get("foto_recorte"):
        fo = fo.crop(tuple(c["foto_recorte"]))
    esc = max(CORTE / fo.height, W / fo.width)
    fo = fo.resize((round(fo.width * esc), round(fo.height * esc)), Image.LANCZOS)
    x0 = max(0, min((fo.width - W) // 2 - int(c.get("foto_desloca_x", 0)), fo.width - W))
    img.paste(fo.crop((x0, 0, x0 + W, CORTE)), (0, 0))
    g = Image.new("L", (1, CORTE))
    for y in range(CORTE):
        g.putpixel((0, y), int(255 * max(0, (y - 440) / (CORTE - 440))))
    img.paste(Image.new("RGB", (W, CORTE), (0, 0, 0)), (0, 0), g.resize((W, CORTE)))

    faixa_base = Image.new("RGB", (W, H - CORTE))
    d = ImageDraw.Draw(faixa_base)
    for y in range(H - CORTE):
        t = y / (H - CORTE)
        d.line([(0, y), (W, y)], fill=tuple(round(cor["fundo"][i] * (1 - t) + cor["fundo_escuro"][i] * t)
                                           for i in range(3)))
    brilho = Image.new("L", faixa_base.size, 0)
    ImageDraw.Draw(brilho).ellipse([880, 160, 1240, 520], fill=120)
    faixa_base.paste(Image.new("RGB", faixa_base.size, (190, 210, 240)), (0, 0),
                     brilho.filter(ImageFilter.GaussianBlur(90)))
    img.paste(faixa_base, (0, CORTE))
    img = img.convert("RGBA")

    cx0, cy0, cx1, cy1 = CARD
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    d.rounded_rectangle(FAIXA, radius=24, fill=cor["faixa"] + (255,))
    d.rounded_rectangle([cx0, CORTE, cx1, cy1], radius=24, fill=cor["cartao"] + (255,))
    d.rounded_rectangle([cx0, cy0, cx1, CORTE + 30], radius=27, outline=cor["cartao"] + (255,), width=4)
    d.rectangle([cx0 + 2, CORTE, cx1 - 2, CORTE + 32], fill=cor["cartao"] + (255,))
    img.alpha_composite(camada)
    titulo = os.path.join(mod, "titulo_convenio_disponivel.png")
    if os.path.exists(titulo):
        img.alpha_composite(Image.open(titulo).convert("RGBA"), (98, 600))
    d = ImageDraw.Draw(img)
    cx, larg = (cx0 + cx1) / 2, cx1 - cx0 - 50
    centro(d, cx, 772, c["categoria"], cabe(d, c["categoria"], F_B, 30, larg), cor["texto_faixa"])
    centro(d, cx, 822, c["nome"], cabe(d, c["nome"], F_XB, 50, larg), cor["texto_faixa"])
    y = 900
    for linha in c.get("publico", []):
        y = centro(d, cx, y, linha, cabe(d, linha, F_R, 25, larg), cor["texto_cartao"]) + 6

    lg = Image.open(cam(c["logo_parceiro"])).convert("RGBA")
    lg = lg.crop(lg.getbbox())
    fx0, fy0, fx1, fy1 = CARD[2], FAIXA[1], FAIXA[2], FAIXA[3]
    e = min(((fx1 - fx0) - 70) / lg.width, ((fy1 - fy0) - 60) / lg.height)
    lg = lg.resize((round(lg.width * e), round(lg.height * e)), Image.LANCZOS)
    img.alpha_composite(lg, (round(fx0 + (fx1 - fx0 - lg.width) / 2), round(fy0 + (fy1 - fy0 - lg.height) / 2)))

    d = ImageDraw.Draw(img)
    centro(d, W / 2, 1022, c.get("titulo_desconto", "DESCONTO"), f(F_B, 30), branco)
    desc = c.get("descontos", [])
    n = max(len(desc), 1)
    gap, alt, py = 36, 92, 1080
    largp = min(440 if n == 1 else 410, (W - 60 - (n - 1) * gap) / n)
    total = n * largp + (n - 1) * gap
    for k, (grande, peq) in enumerate(desc):
        x = (W - total) / 2 + k * (largp + gap)
        d.rounded_rectangle([x, py, x + largp, py + alt], radius=alt // 2, fill=cor["faixa"])
        yy = centro(d, x + largp / 2, py + 8, grande, cabe(d, grande, F_B, 50, largp - 60), branco)
        centro(d, x + largp / 2, yy + 8, peq, cabe(d, peq, F_B, 21, largp - 60), branco)
    if c.get("obs"):
        centro(d, W / 2, py + alt + 22, c["obs"], f(F_B, 20), branco)

    rod = os.path.join(mod, "rodape_logos_brancos.png")
    if os.path.exists(rod):
        r = Image.open(rod).convert("RGBA")
        r = r.resize((round(r.width * 92 / r.height), 92), Image.LANCZOS)
        img.alpha_composite(r, ((W - r.width) // 2, 1228))
    else:
        print("AVISO: sem rodape_logos_brancos.png no modelo; post saiu sem rodapé.")
    saida = cam(c["saida"])
    raiz, ext = os.path.splitext(saida)
    k = 2
    while os.path.exists(saida):  # nunca sobrescreve uma arte já feita
        saida = "%s_%d%s" % (raiz, k, ext)
        k += 1
    img.convert("RGB").save(saida, quality=93)
    print(saida)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
