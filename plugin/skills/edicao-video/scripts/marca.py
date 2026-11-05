# -*- coding: utf-8 -*-
"""Lê marca/marca.json do projeto (documento vivo de marca, ver
referencias/documento-de-marca.md da skill edicao-video).

Uso nos outros scripts:
    from marca import carrega
    m = carrega(r"C:\\caminho\\do\\projeto")   # ou None = procura subindo do cwd
    m.cor("destaque")          -> (255, 225, 77)
    m.ass("destaque")          -> "&H004DE1FF"
    m.fonte("legenda")         -> caminho absoluto do .ttf
    m.familia("legenda")       -> nome da família (para o ASS)
    m.arquivo("logo_cartao_final")
"""
import json
import os
import sys


class Marca:
    def __init__(self, pasta, dados):
        self.pasta = pasta          # .../marca
        self.d = dados

    def _cor_hex(self, papel):
        v = self.d.get("cores", {}).get(papel)
        if not v:
            sys.exit(f"marca.json: cor '{papel}' sem valor. Preencher no MARCA.md e regerar marca.json.")
        v = v.lstrip("#")
        if len(v) != 6:
            sys.exit(f"marca.json: cor '{papel}' inválida: {v}")
        return v.upper()

    def cor(self, papel):
        v = self._cor_hex(papel)
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))

    def ass(self, papel, alfa="00"):
        v = self._cor_hex(papel)
        return f"&H{alfa}{v[4:6]}{v[2:4]}{v[0:2]}"

    def ass_inline(self, papel):
        v = self._cor_hex(papel)
        return f"&H{v[4:6]}{v[2:4]}{v[0:2]}&"

    def arquivo(self, chave, obrigatorio=True):
        rel = self.d.get(chave)
        if not rel:
            if obrigatorio:
                sys.exit(f"marca.json: '{chave}' sem valor.")
            return None
        p = os.path.join(self.pasta, rel)
        if not os.path.exists(p):
            sys.exit(f"marca.json: '{chave}' aponta para arquivo que não existe: {p}")
        return p

    def fonte(self, uso):
        rel = self.d.get("fontes", {}).get(uso)
        if not rel:
            sys.exit(f"marca.json: fonte '{uso}' sem valor.")
        p = os.path.join(self.pasta, rel)
        if not os.path.exists(p):
            sys.exit(f"marca.json: fonte '{uso}' não encontrada: {p}")
        return p

    def pasta_fontes(self):
        return os.path.dirname(self.fonte("legenda"))

    def familia(self, uso):
        """Nome completo da fonte, como o libass procura (ex.: 'Poppins ExtraBold')."""
        from PIL import ImageFont
        f = ImageFont.truetype(self.fonte(uso), 10)
        fam, estilo = f.getname()
        return fam if estilo in ("Regular", "Normal", "") else f"{fam} {estilo}"

    def texto(self, *chaves, padrao=None):
        v = self.d
        for c in chaves:
            v = v.get(c, {}) if isinstance(v, dict) else {}
        return v if isinstance(v, str) and v else padrao

    def confere_texto(self, textos):
        """Para se algum texto de tela tiver sinal proibido pela marca."""
        for t in textos:
            for p in self.d.get("proibido_no_texto", []):
                if p in t:
                    sys.exit(f"texto com '{p}' (proibido pela marca): {t}")


def carrega(raiz=None):
    if raiz is None:
        raiz = os.getcwd()
        while not os.path.exists(os.path.join(raiz, "marca", "marca.json")):
            cima = os.path.dirname(raiz)
            if cima == raiz:
                sys.exit("marca/marca.json não encontrado. Criar o documento de marca primeiro "
                         "(skill edicao-video, referencias/documento-de-marca.md).")
            raiz = cima
    pasta = os.path.join(raiz, "marca")
    with open(os.path.join(pasta, "marca.json"), encoding="utf-8") as f:
        return Marca(pasta, json.load(f))
