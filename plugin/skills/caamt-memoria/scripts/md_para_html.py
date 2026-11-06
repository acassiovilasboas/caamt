# -*- coding: utf-8 -*-
"""Transforma um .md em página HTML para a pessoa ler (abre com duplo clique, sem internet).

  python md_para_html.py <arquivo.md> [saida.html] [--titulo "Título"]

Sem saída: grava ao lado, com o mesmo nome e .html. Só biblioteca padrão. Entende títulos,
parágrafos, listas, tabelas, citações, código, **negrito**, *itálico*, `código` e [links](url).
O .md continua sendo a fonte: editar o .md e rodar de novo.
"""
import html
import os
import re
import sys

CSS = """
:root{--fundo:#F4F5F1;--papel:#FFFFFF;--texto:#17231E;--suave:#4B5A52;--linha:#D9DED6;
--destaque:#8A5D0F;--faixa:#0F2A23;--zebra:#F7F8F5}
@media (prefers-color-scheme:dark){:root{--fundo:#0E1A16;--papel:#15241F;--texto:#E9ECE6;
--suave:#AFBBB3;--linha:#2A3B35;--destaque:#E2A93B;--faixa:#0A1411;--zebra:#192A24}}
*{box-sizing:border-box}body{margin:0;background:var(--fundo);color:var(--texto);
font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
header{background:var(--faixa);color:#EEF0EA;padding:28px 16px}
header div,main{max-width:980px;margin:0 auto}header h1{margin:0;font-size:26px;font-weight:600}
header p{margin:6px 0 0;color:#B9C4BC;font-size:14px}
main{background:var(--papel);padding:24px 20px 48px;margin-top:-1px;min-height:60vh}
h1,h2,h3{line-height:1.25}h2{margin-top:36px;padding-bottom:6px;border-bottom:2px solid var(--linha)}
h3{margin-top:28px;color:var(--destaque)}a{color:var(--destaque)}
blockquote{margin:16px 0;padding:8px 16px;border-left:4px solid var(--destaque);color:var(--suave)}
code{background:var(--zebra);padding:1px 5px;border-radius:4px;font-size:15px}
pre{background:var(--zebra);padding:12px;border-radius:8px;overflow-x:auto}pre code{padding:0}
.tabela{overflow-x:auto;margin:16px 0}table{border-collapse:collapse;width:100%;font-size:15px}
th,td{border:1px solid var(--linha);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--zebra)}tr:nth-child(even) td{background:var(--zebra)}
input.busca{width:100%;padding:10px 12px;margin:0 0 16px;border:1px solid var(--linha);
border-radius:8px;background:var(--papel);color:var(--texto);font-size:16px}
@media print{header{background:none;color:#000}input.busca{display:none}}
"""

JS = """
const b=document.querySelector('.busca');if(b){b.addEventListener('input',()=>{const t=b.value.toLowerCase();
document.querySelectorAll('tbody tr').forEach(r=>{r.style.display=r.textContent.toLowerCase().includes(t)?'':'none'})})}
"""


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|[^)\s]+\.html?)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"(?<![\"'>=])(https?://[^\s<)]+)", r'<a href="\1">\1</a>', t)
    return t


def celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def converter(md):
    linhas, out, i, tem_tabela = md.splitlines(), [], 0, False
    while i < len(linhas):
        l = linhas[i]
        if not l.strip():
            i += 1
        elif l.startswith("```"):
            i += 1
            bloco = []
            while i < len(linhas) and not linhas[i].startswith("```"):
                bloco.append(html.escape(linhas[i]))
                i += 1
            out.append("<pre><code>%s</code></pre>" % "\n".join(bloco))
            i += 1
        elif re.match(r"#{1,4} ", l):
            n = len(l.split(" ")[0])
            out.append("<h%d>%s</h%d>" % (n, inline(l[n + 1:]), n))
            i += 1
        elif l.lstrip().startswith("|") and i + 1 < len(linhas) and re.match(r"\s*\|?\s*:?-{2,}", linhas[i + 1]):
            tem_tabela = True
            cab = celulas(l)
            i += 2
            corpo = []
            while i < len(linhas) and linhas[i].lstrip().startswith("|"):
                corpo.append("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in celulas(linhas[i])))
                i += 1
            out.append('<div class="tabela"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                       % ("".join("<th>%s</th>" % inline(c) for c in cab), "".join(corpo)))
        elif re.match(r"\s*([-*]|\d+\.) ", l):
            num = re.match(r"\s*(\d+)\.", l)
            tag = "ol" if num else "ul"
            abre = '<ol start="%s">' % num.group(1) if num and num.group(1) != "1" else "<%s>" % tag
            itens = []
            while i < len(linhas) and (re.match(r"\s*([-*]|\d+\.) ", linhas[i]) or
                                       (linhas[i].startswith("  ") and linhas[i].strip() and itens)):
                m = re.match(r"\s*(?:[-*]|\d+\.) (.*)", linhas[i])
                if m:
                    itens.append(m.group(1))
                else:
                    itens[-1] += " " + linhas[i].strip()
                i += 1
            out.append("%s%s</%s>" % (abre, "".join("<li>%s</li>" % inline(x) for x in itens), tag))
        elif l.startswith(">"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(linhas[i].lstrip("> "))
                i += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(bloco)))
        elif re.match(r"-{3,}\s*$", l):
            out.append("<hr>")
            i += 1
        else:
            bloco = []
            while i < len(linhas) and linhas[i].strip() and not re.match(r"(#{1,4} |```|\s*\||\s*([-*]|\d+\.) |>)", linhas[i]):
                bloco.append(linhas[i].strip())
                i += 1
            out.append("<p>%s</p>" % inline(" ".join(bloco)))
    return "\n".join(out), tem_tabela


def main(a):
    if not a:
        sys.exit(__doc__)
    origem = a[0]
    resto, titulo = list(a[1:]), None
    if "--titulo" in resto:
        j = resto.index("--titulo")
        titulo = resto[j + 1] if j + 1 < len(resto) else None
        del resto[j:j + 2]
    saida = resto[0] if resto else os.path.splitext(origem)[0] + ".html"
    md = open(origem, encoding="utf-8").read()
    if not titulo:
        m = re.search(r"^# (.+)$", md, re.M)
        titulo = m.group(1).strip() if m else os.path.splitext(os.path.basename(origem))[0]
        md = re.sub(r"^# .+\n?", "", md, count=1, flags=re.M)
    corpo, tem_tabela = converter(md)
    busca = '<input class="busca" type="search" placeholder="Buscar nas tabelas">' if tem_tabela else ""
    pagina = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width, initial-scale=1">'
              "<title>%s</title><style>%s</style></head><body><header><div><h1>%s</h1>"
              "</div></header><main>%s%s</main><script>%s</script></body></html>"
              % (html.escape(titulo), CSS, html.escape(titulo),
                 busca, corpo, JS if tem_tabela else ""))
    with open(saida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print(os.path.abspath(saida))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
