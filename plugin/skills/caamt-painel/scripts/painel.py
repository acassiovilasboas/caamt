# -*- coding: utf-8 -*-
"""Painel da subseção no navegador, a partir dos CSV da planilha (local ou espelho do Drive).

  python painel.py <pasta com os .csv> [saida.html] [--pasta <pasta de trabalho do Claude>]

--pasta liga os botões "Abrir no Claude" (link claude://code/new, abre a sessão com o pedido
escrito, sem enviar). Mostra só o que existe na planilha.
"""
import csv
import datetime
import html
import os
import re
import sys
import urllib.parse

HOJE = datetime.date.today()
ETAPAS = ["Prospecção", "Contato", "Aguardando documentos", "Documentos completos", "Enviado à CAAMT",
          "Aprovado", "Divulgado"]
DOCS = {"PJ": ["Carta proposta", "Alvará (PJ)", "CNPJ (PJ)", "Documento com foto", "Logo JPG"],
        "PF": ["Carta proposta", "Comprovante de endereço (PF)", "Documento com foto", "Logo JPG"]}
PASTA = ""


def ler(pasta, aba):
    p = os.path.join(pasta, aba + ".csv")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def v(d, k):
    return (d.get(k) or "").strip()


def data(s):
    s = (s or "").strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d/%m/%y"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    m = re.match(r"(\d{1,2})/(\d{1,2})$", s)
    if m:
        try:
            return datetime.date(HOJE.year, int(m.group(2)), int(m.group(1)))
        except ValueError:
            return None
    return None


def e(s):
    return html.escape((s or "").strip())


def at(s):
    return html.escape(s or "", quote=True)


def zap(numero, texto):
    d = re.sub(r"\D", "", numero or "")
    if len(d) in (10, 11):
        d = "55" + d
    return "https://wa.me/%s?text=%s" % (d, urllib.parse.quote(texto or "")) if len(d) >= 12 else ""


def site(url):
    h = urllib.parse.urlparse(url).netloc.replace("www.", "")
    return "Google Drive" if "google." in h else h


def b_link(url, rotulo, cls=""):
    url = (url or "").strip()
    if not url:
        return ""
    if not re.match(r"[a-z]+:", url):
        url = "file:///" + url.replace("\\", "/").lstrip("/")
    return '<a class="b %s" href="%s" target="_blank" rel="noopener">%s</a>' % (cls, at(url), rotulo)


def b_copiar(texto, rotulo):
    return '<button class="b" type="button" data-copiar="%s">%s</button>' % (at(texto.strip()), rotulo) if (texto or "").strip() else ""


def b_zap(numero, texto, rotulo="Enviar no WhatsApp"):
    z = zap(numero, texto) if (texto or "").strip() else ""
    return b_link(z, rotulo, "zap") if z else ""


def b_claude(pedido):
    q = "q=" + urllib.parse.quote(pedido)
    if PASTA:
        q += "&folder=" + urllib.parse.quote(PASTA)
    return (b_link("claude://code/new?" + q, "Abrir no Claude", "claude")
            + b_copiar(pedido, "Copiar pedido para o Claude"))


def chip(texto, cls=""):
    return '<span class="chip %s">%s</span>' % (cls, e(texto)) if (texto or "").strip() else ""


def prazo(d):
    if not d:
        return ""
    n = (d - HOJE).days
    if n < 0:
        return chip("Venceu há %d dia%s" % (-n, "s" if n < -1 else ""), "atraso")
    return chip("Hoje", "hoje") if n == 0 else chip("Amanhã", "logo") if n == 1 else chip(d.strftime("%d/%m"), "logo" if n <= 7 else "")


def doc_estado(valor):
    s = (valor or "").strip()
    n = s.lower()
    if not s:
        return "falta", "Falta"
    if n.startswith("ok") or n.startswith("validado"):
        return "ok", "Validado" + s[2:] if n.startswith("ok") else s
    if n.startswith("problema"):
        return "problema", s[0].upper() + s[1:]
    if n.startswith("não se aplica") or n.startswith("nao se aplica"):
        return "na", "Não se aplica"
    return "recebido", s[0].upper() + s[1:] + " · falta conferir"


ROT = {"parc": "Parceiro", "post": "Postagem", "tema": "Tema", "pauta": "Pauta"}


def item(titulo, resumo, corpo, acoes, cls="", aberto=False, claude=False):
    return ('<details class="item %s"%s><summary><span class="rot">%s</span><span class="tit">%s</span><span class="res">%s%s</span></summary>'
            '<div class="corpo">%s<div class="acoes">%s</div></div></details>'
            % (cls, " open" if aberto else "", ROT.get(cls, ""), titulo, resumo, chip("Com o Claude", "claude") if claude else "", corpo, acoes))


def campo(rotulo, valor):
    return '<div class="campo"><span>%s</span><b>%s</b></div>' % (rotulo, e(valor)) if (valor or "").strip() else ""


def parceiro(p, sub):
    nome, tipo = v(p, "Parceiro"), (v(p, "Tipo (PJ/PF)") or "PJ").upper()[:2]
    docs = [(d, doc_estado(p.get(d))) for d in DOCS.get(tipo, DOCS["PJ"])]
    docs = [(d, s) for d, s in docs if s[0] != "na"]
    ok = sum(1 for _, s in docs if s[0] == "ok")
    etapa = v(p, "Etapa")
    idx = next((i for i, x in enumerate(ETAPAS) if x.lower() == etapa.lower()), -1)
    passos = "".join('<li class="%s">%s</li>' % ("feito" if i < idx else "atual" if i == idx else "", e(x))
                     for i, x in enumerate(ETAPAS))
    lista = "".join('<li class="doc %s"><span class="ic" aria-hidden="true"></span><span>%s</span><b>%s</b></li>'
                    % (s[0], e(d.replace(" (PJ)", "").replace(" (PF)", "")), e(s[1])) for d, s in docs)
    msg = v(p, "Próxima mensagem")
    pend = [d for d, s in docs if s[0] == "recebido"]
    acoes = (b_zap(v(p, "WhatsApp/Telefone"), msg) + b_copiar(msg, "Copiar mensagem")
             + b_link(v(p, "Pasta (link)"), "Abrir pasta no Drive" if "google." in v(p, "Pasta (link)") else "Abrir pasta"))
    claude = ""
    if pend:
        claude = b_claude("Confira os documentos da %s (%s)." % (nome, ", ".join(x.replace(" (PJ)", "").replace(" (PF)", "") for x in pend)))
    elif ok < len(docs) and not msg:
        claude = b_claude("Escreva a mensagem de cobrança para a %s." % nome)
    corpo = ('<ol class="etapas">%s</ol><div class="grade2"><div>%s%s%s%s</div><div><h4>Documentos · %d de %d validados</h4>'
             '<ul class="docs">%s</ul></div></div>%s'
             % (passos, campo("Responsável", v(p, "Responsável")), campo("WhatsApp", v(p, "WhatsApp/Telefone")),
                campo("Benefício", v(p, "Benefício")), campo("Próxima ação", v(p, "Próxima ação")), ok, len(docs), lista,
                '<p class="msg">%s</p>' % e(msg) if msg else ""))
    resumo = chip(etapa, "etapa") + chip("%d de %d documentos" % (ok, len(docs)), "ok" if docs and ok == len(docs) else "") + prazo(data(v(p, "Data da próxima ação")))
    titulo = "%s<small>%s</small>" % (e(nome), e(" · ".join(x for x in (v(p, "Categoria"), v(p, "Cidade")) if x)))
    return item(titulo, resumo, corpo, acoes + claude, "parc", claude=bool(claude))


def post(c, sub=False):
    pauta, st = v(c, "Pauta") or v(c, "Tema"), (v(c, "Status") or "ideia").lower()
    falta = [x for x, k in (("a arte", "Arte (link)"), ("a legenda", "Legenda")) if not v(c, k)]
    corpo = ('<div class="grade2"><div>%s%s</div><div>%s</div></div>%s%s%s'
             % (campo("Tema", v(c, "Tema")), campo("Formato", v(c, "Formato")), campo("Roteiro", v(c, "Roteiro")),
                '<p class="msg">%s</p>' % e(v(c, "Legenda")) if v(c, "Legenda") else "",
                campo("Hashtags", v(c, "Hashtags")), campo("Primeiro comentário", v(c, "Primeiro comentário"))))
    acoes = (b_link(v(c, "Arte (link)"), "Abrir a arte") + b_copiar(v(c, "Legenda"), "Copiar legenda")
             + b_copiar(v(c, "Hashtags"), "Copiar hashtags") + b_copiar(v(c, "Primeiro comentário"), "Copiar 1º comentário")
             + (b_link(v(c, "Fonte"), "Abrir notícia (%s)" % site(v(c, "Fonte"))) if re.match(r"https?://", v(c, "Fonte")) else ""))
    claude = b_claude("Faça %s do post de %s: %s." % (" e ".join(falta), v(c, "Data"), pauta)) if falta and st != "publicado" else ""
    resumo = (prazo(data(v(c, "Data"))) if st != "publicado" else chip(v(c, "Data"))) + chip(v(c, "Formato")) + chip(st.capitalize(), "ok" if st == "publicado" else "pronto" if st == "pronto" else "")
    return item(e(pauta), resumo, corpo, acoes + claude, "post", claude=bool(claude))


def tema(t):
    corpo = campo("Para quê", v(t, "Para quê")) + campo("Formatos", v(t, "Formatos"))
    return item(e(v(t, "Tema")), chip(v(t, "Frequência"), "etapa") + chip(v(t, "Dia sugerido")), corpo,
                b_claude("Monte as próximas postagens do tema %s." % v(t, "Tema")), "tema")


def pauta(p):
    return item(e(v(p, "Título")), chip(v(p, "Tema"), "etapa") + chip(v(p, "Data")),
                '<p class="msg">%s</p>' % e(v(p, "Resumo")) if v(p, "Resumo") else "",
                (b_link(v(p, "Fonte"), "Abrir notícia (%s)" % site(v(p, "Fonte"))) if v(p, "Fonte") else "")
                + b_claude("Crie um post a partir da pauta: %s." % v(p, "Título")), "pauta")


def secao(id_, titulo, itens):
    corpo = "".join(itens) or '<p class="vazio">Nada aqui ainda.</p>'
    return '<section id="%s" class="aba"><h2>%s <small>%d</small></h2>%s</section>' % (id_, titulo, len(itens), corpo)


CSS = """:root{--pg:#0A0B0D;--sl:#0F1114;--cx:#16191E;--t:#F2F3F5;--s:#A4A9B3;--l:#FFFFFF24;--az:#7C9CFF;--li:#B39CFF;--azs:#7C9CFF1F;--lis:#B39CFF24;--am:#E8B45A}
*{box-sizing:border-box}body{margin:0;background:var(--pg);color:var(--t);font:400 19px/1.5 Inter,system-ui,"Segoe UI",Roboto,Arial,sans-serif}
header{background:radial-gradient(circle at 100% 0,#7C9CFF17,transparent 55%),var(--sl);padding:18px 16px 14px;position:sticky;top:0;z-index:3;border-bottom:1px solid var(--l)}
header .rot{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--az);font-weight:600}
header h1{margin:2px 0 12px;font-size:26px;font-weight:800}header h1::after{content:"";display:block;width:64px;height:3px;margin-top:8px;border-radius:2px;background:linear-gradient(90deg,var(--az),var(--li))}
nav{display:flex;gap:8px;overflow-x:auto}nav button{font:inherit;font-size:18px;font-weight:600;padding:10px 18px;border-radius:12px;border:1px solid var(--l);background:transparent;color:var(--s);cursor:pointer;white-space:nowrap}
nav button[aria-selected=true]{background:var(--azs);border-color:var(--az);color:var(--t)}
main{max-width:980px;margin:0 auto;padding:18px 16px}.aba{display:none}.aba.ativa{display:block}
h2{font-size:28px;font-weight:700;margin:6px 0 16px}h2 small{font-size:18px;color:var(--s);font-weight:400}h4{margin:0 0 8px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--az);font-weight:600}
.item{background:var(--cx);border:1px solid var(--l);border-left:4px solid var(--l);border-radius:14px;margin:0 0 12px;overflow:hidden}
.item.claude-item{border-left-color:var(--li)}.item:has(.chip.atraso),.item:has(.chip.hoje){border-left-color:var(--am)}
summary{list-style:none;cursor:pointer;padding:16px 52px 16px 18px;position:relative;display:flex;flex-direction:column;gap:8px}
summary::-webkit-details-marker{display:none}summary::after{content:"";position:absolute;right:20px;top:26px;width:11px;height:11px;border-right:3px solid var(--s);border-bottom:3px solid var(--s);transform:rotate(45deg);transition:.2s}
details[open] summary::after{transform:rotate(225deg);top:32px}summary:active{background:var(--azs)}
.rot{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--az);font-weight:600}
.tit{font-size:22px;font-weight:700;line-height:1.25}.tit small{display:block;font-size:16px;font-weight:400;color:var(--s);margin-top:2px}
.res{display:flex;flex-wrap:wrap;gap:6px}.corpo{padding:4px 18px 18px;border-top:1px solid var(--l)}
.chip{display:inline-block;padding:3px 12px;border-radius:999px;background:transparent;border:1px solid var(--l);font-size:15px;color:var(--s);font-weight:500}
.chip.etapa{border-color:var(--az);color:var(--t);background:var(--azs)}.chip.atraso{background:var(--am);border-color:var(--am);color:#0A0B0D;font-weight:700}
.chip.hoje{border-color:var(--am);color:var(--am);font-weight:700}.chip.logo{border-color:var(--am);color:var(--t)}
.chip.ok{background:var(--az);border-color:var(--az);color:#0A0B0D;font-weight:700}.chip.pronto{border-color:var(--az);color:var(--az)}.chip.claude{background:var(--lis);border-color:var(--li);color:var(--li);font-weight:700}
.etapas{display:flex;flex-wrap:wrap;gap:4px;list-style:none;padding:0;margin:16px 0}.etapas li{flex:1 1 110px;font-size:14px;padding:8px;text-align:center;border-radius:8px;border:1px solid var(--l);color:var(--s)}
.etapas li.feito{background:var(--azs);border-color:var(--az);color:var(--t)}.etapas li.atual{background:var(--az);border-color:var(--az);color:#0A0B0D;font-weight:700}
.grade2{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:14px 0}@media(max-width:640px){.grade2{grid-template-columns:1fr}}
.campo{display:flex;flex-direction:column;margin:0 0 12px}.campo span{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--s)}.campo b{font-weight:600}
.docs{list-style:none;padding:0;margin:0}.doc{display:grid;grid-template-columns:28px 1fr;gap:2px 8px;padding:9px 0;border-bottom:1px solid var(--l)}
.doc span:nth-child(2){font-weight:600}.doc b{grid-column:2;font-weight:400;font-size:16px;color:var(--s)}.ic{width:22px;height:22px;border-radius:50%;border:2px solid var(--s);grid-row:span 2;margin-top:2px}
.doc.ok .ic{background:var(--az);border-color:var(--az)}.doc.ok b{color:var(--az);font-weight:600}.doc.recebido .ic{border-color:var(--li);background:linear-gradient(90deg,var(--li) 50%,transparent 50%)}
.doc.recebido b{color:var(--li)}.doc.problema .ic{background:var(--am);border-color:var(--am)}.doc.problema b{color:var(--am);font-weight:600}.doc.falta .ic{border-style:dashed;border-color:var(--am)}.doc.falta b{color:var(--am)}
.msg{white-space:pre-line;background:var(--sl);border:1px solid var(--l);border-radius:10px;padding:12px 14px;margin:12px 0;font-size:18px}
.acoes{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.b{font:inherit;font-size:19px;font-weight:600;min-height:56px;padding:12px 22px;border-radius:12px;border:1px solid var(--l);background:var(--sl);color:var(--t);
text-decoration:none;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:transform .08s,background .15s,border-color .15s}
.b:hover{border-color:var(--az)}.b:active,.b.tocado{transform:scale(.96);background:var(--azs);border-color:var(--az)}.b:focus-visible{outline:3px solid var(--az);outline-offset:2px}
.b.zap{background:var(--az);border-color:var(--az);color:#0A0B0D}.b.claude{background:var(--li);border-color:var(--li);color:#0A0B0D}.b.feito{background:var(--azs);border-color:var(--az);color:var(--az)}
@media(max-width:640px){.b{flex:1 1 100%}}.vazio{color:var(--s);font-size:20px}"""

JS = """const abas=[...document.querySelectorAll('nav button')];function abrir(id){abas.forEach(b=>b.setAttribute('aria-selected',b.dataset.aba===id));
document.querySelectorAll('.aba').forEach(s=>s.classList.toggle('ativa',s.id===id));try{localStorage.setItem('aba',id)}catch(e){}}
abas.forEach(b=>b.onclick=()=>abrir(b.dataset.aba));let ini='tarefas';try{ini=localStorage.getItem('aba')||ini}catch(e){}abrir(document.getElementById(ini)?ini:'tarefas');
document.querySelectorAll('.chip.claude').forEach(c=>c.closest('.item').classList.add('claude-item'));
document.querySelectorAll('a.b').forEach(a=>a.addEventListener('click',()=>{a.classList.add('tocado');setTimeout(()=>a.classList.remove('tocado'),350)}));
document.querySelectorAll('[data-copiar]').forEach(b=>b.onclick=async()=>{const t=b.dataset.copiar;
try{await navigator.clipboard.writeText(t)}catch(e){const x=document.createElement('textarea');x.value=t;document.body.append(x);x.select();document.execCommand('copy');x.remove()}
const r=b.textContent;b.textContent='Copiado ✓';b.classList.add('feito');setTimeout(()=>{b.textContent=r;b.classList.remove('feito')},1600)});"""


def main(a):
    global PASTA
    if not a:
        sys.exit(__doc__)
    if "--pasta" in a:
        j = a.index("--pasta")
        PASTA = os.path.abspath(a[j + 1]) if j + 1 < len(a) else ""
        del a[j:j + 2]
    pasta = a[0]
    saida = a[1] if len(a) > 1 else os.path.join(pasta, "painel.html")
    parc, crono = ler(pasta, "parceiros"), ler(pasta, "cronograma")
    temas, pautas = ler(pasta, "linha-editorial"), ler(pasta, "pautas")
    cfg = {r.get("Chave", ""): r.get("Valor", "") for r in ler(pasta, "config")}
    lim = HOJE + datetime.timedelta(days=14)
    t_parc = sorted([p for p in parc if data(v(p, "Data da próxima ação"))], key=lambda p: data(v(p, "Data da próxima ação")))
    t_post = sorted([c for c in crono if (v(c, "Status") or "").lower() != "publicado" and data(v(c, "Data")) and data(v(c, "Data")) <= lim],
                    key=lambda c: data(v(c, "Data")))
    tarefas = sorted([(data(v(p, "Data da próxima ação")), parceiro(p, True)) for p in t_parc]
                     + [(data(v(c, "Data")), post(c, True)) for c in t_post], key=lambda x: x[0])
    crono.sort(key=lambda c: data(v(c, "Data")) or datetime.date.max)
    titulo = "CAAMT · " + (cfg.get("Subseção") or "Subseção")
    abas = [("tarefas", "Tarefas"), ("postagens", "Postagens"), ("parceiros", "Parceiros"), ("temas", "Temas"), ("pautas", "Pautas")]
    corpo = (secao("tarefas", "Tarefas", [h for _, h in tarefas]) + secao("postagens", "Postagens", [post(c) for c in crono])
             + secao("parceiros", "Parceiros", [parceiro(p, False) for p in parc]) + secao("temas", "Temas", [tema(t) for t in temas])
             + secao("pautas", "Pautas", [pauta(p) for p in pautas]))
    with open(saida, "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>%s</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"><style>%s</style></head><body><header><div class="rot">Painel da subseção</div><h1>%s</h1><nav>%s</nav></header><main>%s</main><script>%s</script></body></html>'
                % (e(titulo), CSS, e(titulo), "".join('<button type="button" data-aba="%s">%s</button>' % x for x in abas), corpo, JS))
    print(os.path.abspath(saida))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
