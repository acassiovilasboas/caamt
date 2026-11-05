# -*- coding: utf-8 -*-
"""Inventário rápido da pasta de trabalho: o que já existe de parceiros, artes e vídeos.

  python varrer_pasta.py <pasta> [--saida memoria/inventario.md]

Não abre o conteúdo dos arquivos: olha nome, tipo e tamanho. Imprime um resumo curto e grava
o detalhe em Markdown. Ignora pastas do próprio kit (memoria/, tmp/, _colab/).
"""
import os
import sys
from collections import Counter, defaultdict

IGNORAR = {"memoria", "tmp", "_colab", "_kit", ".git", "node_modules", "__pycache__"}
VIDEO = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".3gp"}
IMAGEM = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif", ".svg"}
DOC = {".pdf", ".doc", ".docx", ".odt", ".xls", ".xlsx", ".csv", ".txt"}
DOC_PARCEIRO = {"alvara": "alvará", "cnpj": "CNPJ", "proposta": "carta proposta",
                "contrato": "contrato", "rg": "documento com foto", "cnh": "documento com foto",
                "cpf": "documento com foto", "comprovante": "comprovante de endereço",
                "tabela": "tabela de valores", "diploma": "diploma", "conselho": "carta do conselho"}
ARTE = ("logo", "moldura", "rodape", "rodapé", "placa", "vinheta", "capa", "template", "convenio",
        "convênio")


def normal(s):
    trocas = str.maketrans("áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ", "aaaaeeiooouc" + "AAAAEEIOOOUC")
    return s.translate(trocas).lower()


def main(a):
    if not a:
        sys.exit(__doc__)
    raiz = os.path.abspath(a[0])
    saida = a[a.index("--saida") + 1] if "--saida" in a else None
    tipos, docs, artes, videos = Counter(), defaultdict(list), [], []
    for pasta, subs, arqs in os.walk(raiz):
        subs[:] = [s for s in subs if s not in IGNORAR and not s.startswith(".")]
        for n in arqs:
            ext = os.path.splitext(n)[1].lower()
            rel = os.path.relpath(os.path.join(pasta, n), raiz)
            nn = normal(n)
            if ext in VIDEO:
                tipos["vídeo"] += 1
                videos.append(rel)
            elif ext in IMAGEM:
                tipos["imagem"] += 1
                if any(normal(k) in nn for k in ARTE):
                    artes.append(rel)
            elif ext in DOC:
                tipos["documento"] += 1
            else:
                continue
            for chave, nome in DOC_PARCEIRO.items():
                if chave in nn.replace("-", " ").replace("_", " ").split() or (len(chave) > 3 and chave in nn):
                    docs[os.path.dirname(rel) or "."].append("%s (%s)" % (n, nome))
                    break
    resumo = ["Pasta: " + raiz,
              "Arquivos: " + (", ".join("%d %s" % (v, k) for k, v in tipos.items()) or "nenhum"),
              "Pastas com documento de parceiro: %d" % len(docs),
              "Artes (logo, moldura, rodapé, placa...): %d" % len(artes),
              "Vídeos: %d" % len(videos)]
    print("\n".join(resumo))
    if saida:
        os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
        with open(saida, "w", encoding="utf-8") as f:
            f.write("# Inventário da pasta\n\n" + "\n".join("- " + r for r in resumo) + "\n")
            f.write("\n## Documentos de parceiro (pelo nome do arquivo; conferir)\n")
            for p, l in sorted(docs.items()):
                f.write("- %s: %s\n" % (p, "; ".join(l[:10])))
            f.write("\n## Artes\n" + "".join("- %s\n" % x for x in artes[:60]))
            f.write("\n## Vídeos\n" + "".join("- %s\n" % x for x in videos[:60]))
        print("Detalhe: " + saida)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
