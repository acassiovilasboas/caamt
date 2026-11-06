# -*- coding: utf-8 -*-
"""Painel da subseção no navegador, a partir dos CSV da planilha (local ou espelho do Drive).

  python painel.py <pasta com os .csv> [saida.html]

Mostra só o que existe na planilha. Nada de exemplo: aba vazia aparece vazia.
"""
import csv
import datetime
import html
import json
import os
import re
import sys
import urllib.parse

HOJE = datetime.date.today()


def ler(pasta, aba):
    p = os.path.join(pasta, aba + ".csv")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


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


def zap(numero, texto):
    d = re.sub(r"\D", "", numero or "")
    if len(d) in (10, 11):
        d = "55" + d
    if len(d) < 12:
        return ""
    return "https://wa.me/%s?text=%s" % (d, urllib.parse.quote(texto or ""))


def nome_link(url):
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    if "drive.google" in host or "docs.google" in host:
        return "Google Drive"
    return host or "Abrir"


def botao_link(url, rotulo, classe="b"):
    url = (url or "").strip()
    if not url:
        return ""
    if not re.match(r"https?://", url):
        url = "file:///" + url.replace("\\", "/").lstrip("/")
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (classe, html.escape(url, quote=True), rotulo)


def botao_copiar(texto, rotulo):
    if not (texto or "").strip():
        return ""
    return '<button class="b" data-copiar="%s">%s</button>' % (html.escape(texto.strip(), quote=True), rotulo)


def chip(texto, tipo):
    return '<span class="chip %s">%s</span>' % (tipo, e(texto)) if (texto or "").strip() else ""


def quando(d):
    if not d:
        return ""
    dias = (d - HOJE).days
    if dias < 0:
        return chip("Venceu há %d dia%s" % (-dias, "s" if dias < -1 else ""), "atraso")
    if dias == 0:
        return chip("Hoje", "hoje")
    if dias == 1:
        return chip("Amanhã", "logo")
    return chip(d.strftime("%d/%m"), "logo" if dias <= 7 else "")


def card_parceiro(p):
    msg = p.get("Próxima mensagem", "")
    z = zap(p.get("WhatsApp/Telefone", ""), msg)
    falta = (p.get("Falta") or "").strip()
    return ('<article class="card"><h3>%s</h3><p class="linha">%s %s %s</p>%s<div class="acoes">%s%s%s</div></article>'
            % (e(p.get("Parceiro")), chip(p.get("Etapa"), "etapa"), quando(data(p.get("Data da próxima ação"))),
               chip("Falta: " + falta, "falta") if falta else "",
               '<p class="grande">%s</p>' % e(p.get("Próxima ação")) if (p.get("Próxima ação") or "").strip() else "",
               ('<a class="b zap" href="%s" target="_blank" rel="noopener">WhatsApp</a>' % html.escape(z, quote=True)) if z and msg.strip() else "",
               botao_copiar(msg, "Copiar mensagem"), botao_link(p.get("Pasta (link)"), "Abrir pasta")))


def card_post(c):
    st = (c.get("Status") or "ideia").strip()
    return ('<article class="card"><h3>%s</h3><p class="linha">%s %s %s %s</p>%s<div class="acoes">%s%s%s%s%s</div></article>'
            % (e(c.get("Pauta") or c.get("Tema")), quando(data(c.get("Data"))) if st != "publicado" else chip(c.get("Data"), ""),
               chip(c.get("Tema"), "etapa"), chip(c.get("Formato"), ""), chip(st, "ok" if st == "publicado" else "pronto" if st == "pronto" else ""),
               '<p class="texto">%s</p>' % e(c.get("Legenda")) if (c.get("Legenda") or "").strip() else "",
               botao_link(c.get("Arte (link)"), "Abrir arte"), botao_copiar(c.get("Legenda"), "Copiar legenda"),
               botao_copiar(c.get("Hashtags"), "Copiar hashtags"), botao_copiar(c.get("Primeiro comentário"), "Copiar 1º comentário"),
               botao_link(c.get("Fonte"), nome_link(c.get("Fonte") or "")) if re.match(r"https?://", c.get("Fonte") or "") else ""))


def card_tema(t):
    return ('<article class="card"><h3>%s</h3><p class="linha">%s %s</p>%s</article>'
            % (e(t.get("Tema")), chip(t.get("Frequência"), "etapa"), chip(t.get("Dia sugerido"), ""),
               '<p class="grande">%s</p>' % e(t.get("Para quê")) if (t.get("Para quê") or "").strip() else ""))


def card_pauta(p):
    return ('<article class="card"><h3>%s</h3><p class="linha">%s %s</p>%s<div class="acoes">%s</div></article>'
            % (e(p.get("Título")), chip(p.get("Tema"), "etapa"), chip(p.get("Data"), ""),
               '<p class="texto">%s</p>' % e(p.get("Resumo")) if (p.get("Resumo") or "").strip() else "",
               botao_link(p.get("Fonte"), nome_link(p.get("Fonte") or "")) if (p.get("Fonte") or "").strip() else ""))


def secao(id_, titulo, cards):
    corpo = "".join(cards) or '<p class="vazio">Nada aqui ainda.</p>'
    return '<section id="%s" class="aba"><h2>%s <small>%d</small></h2><div class="grade">%s</div></section>' % (id_, titulo, len(cards), corpo)


CSS = """:root{--f:#F4F5F1;--p:#fff;--t:#14211C;--s:#4B5A52;--l:#D5DAD2;--v:#0F2A23;--a:#E2A93B;--z:#1F7A4D;--r:#B3261E}
@media (prefers-color-scheme:dark){:root{--f:#0E1A16;--p:#15241F;--t:#EEF1EC;--s:#B4C0B8;--l:#2C3E37;--z:#2FA36A;--r:#F2766B}}
*{box-sizing:border-box}body{margin:0;background:var(--f);color:var(--t);font:20px/1.45 system-ui,"Segoe UI",Roboto,Arial,sans-serif}
header{background:var(--v);color:#EEF1EC;padding:18px 16px;position:sticky;top:0;z-index:2}
header h1{margin:0 0 12px;font-size:26px}nav{display:flex;gap:8px;flex-wrap:wrap}
nav button{font:inherit;font-size:19px;padding:10px 16px;border-radius:999px;border:2px solid #EEF1EC55;background:transparent;color:#EEF1EC;cursor:pointer}
nav button[aria-selected=true]{background:var(--a);border-color:var(--a);color:#14211C;font-weight:700}
main{max-width:1100px;margin:0 auto;padding:16px}.aba{display:none}.aba.ativa{display:block}
h2{font-size:30px;margin:8px 0 16px}h2 small{font-size:20px;color:var(--s);font-weight:400}
.grade{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.card{background:var(--p);border:1px solid var(--l);border-radius:16px;padding:18px}
.card h3{margin:0 0 8px;font-size:24px;line-height:1.25}.linha{margin:0 0 10px;display:flex;flex-wrap:wrap;gap:6px}
.grande{margin:0 0 12px;font-size:21px}.texto{margin:0 0 12px;white-space:pre-line;color:var(--s);font-size:18px;max-height:9.5em;overflow:auto}
.chip{display:inline-block;padding:3px 12px;border-radius:999px;background:var(--f);border:1px solid var(--l);font-size:17px}
.chip.etapa{border-color:var(--v)}.chip.atraso{background:var(--r);border-color:var(--r);color:#fff;font-weight:700}
.chip.hoje{background:var(--a);border-color:var(--a);color:#14211C;font-weight:700}.chip.logo{border-color:var(--a);font-weight:600}
.chip.falta{border-style:dashed}.chip.ok{background:var(--z);border-color:var(--z);color:#fff}.chip.pronto{border-color:var(--z)}
.acoes{display:flex;flex-wrap:wrap;gap:8px}.b{font:inherit;font-size:18px;min-height:48px;padding:10px 16px;border-radius:12px;border:2px solid var(--v);
background:var(--p);color:var(--t);text-decoration:none;cursor:pointer;display:inline-flex;align-items:center}
.b:hover,.b:focus-visible{background:var(--v);color:#fff;outline:none}.b.zap{background:var(--z);border-color:var(--z);color:#fff;font-weight:700}
.vazio{color:var(--s);font-size:22px}.aviso{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:var(--v);color:#fff;
padding:12px 22px;border-radius:999px;font-size:19px;opacity:0;transition:.2s}.aviso.on{opacity:1}"""

JS = """const abas=[...document.querySelectorAll('nav button')];function abrir(id){abas.forEach(b=>b.setAttribute('aria-selected',b.dataset.aba===id));
document.querySelectorAll('.aba').forEach(s=>s.classList.toggle('ativa',s.id===id));try{localStorage.setItem('aba',id)}catch(e){}}
abas.forEach(b=>b.onclick=()=>abrir(b.dataset.aba));let ini='hoje';try{ini=localStorage.getItem('aba')||ini}catch(e){}abrir(document.getElementById(ini)?ini:'hoje');
const av=document.querySelector('.aviso');document.querySelectorAll('[data-copiar]').forEach(b=>b.onclick=async()=>{
try{await navigator.clipboard.writeText(b.dataset.copiar)}catch(e){const t=document.createElement('textarea');t.value=b.dataset.copiar;document.body.append(t);t.select();document.execCommand('copy');t.remove()}
av.textContent='Copiado';av.classList.add('on');setTimeout(()=>av.classList.remove('on'),1400)});"""


def main(a):
    if not a:
        sys.exit(__doc__)
    pasta = a[0]
    saida = a[1] if len(a) > 1 else os.path.join(pasta, "painel.html")
    parc, crono = ler(pasta, "parceiros"), ler(pasta, "cronograma")
    temas, pautas = ler(pasta, "linha-editorial"), ler(pasta, "pautas")
    cfg = {r.get("Chave", ""): r.get("Valor", "") for r in ler(pasta, "config")}
    limite = HOJE + datetime.timedelta(days=7)
    hoje_p = [p for p in parc if data(p.get("Data da próxima ação")) and data(p.get("Data da próxima ação")) <= limite]
    hoje_c = [c for c in crono if (c.get("Status") or "") != "publicado" and data(c.get("Data")) and data(c.get("Data")) <= limite]
    hoje_p.sort(key=lambda p: data(p.get("Data da próxima ação")))
    hoje_c.sort(key=lambda c: data(c.get("Data")))
    crono.sort(key=lambda c: data(c.get("Data")) or datetime.date.max)
    titulo = "CAAMT · " + (cfg.get("Subseção") or "Subseção")
    abas = [("hoje", "Hoje"), ("postagens", "Postagens"), ("parceiros", "Parceiros"), ("temas", "Temas"), ("pautas", "Pautas")]
    nav = "".join('<button data-aba="%s">%s</button>' % x for x in abas)
    corpo = (secao("hoje", "Hoje e próximos 7 dias", [card_parceiro(p) for p in hoje_p] + [card_post(c) for c in hoje_c])
             + secao("postagens", "Postagens", [card_post(c) for c in crono])
             + secao("parceiros", "Parceiros", [card_parceiro(p) for p in parc])
             + secao("temas", "Temas", [card_tema(t) for t in temas])
             + secao("pautas", "Pautas", [card_pauta(p) for p in pautas]))
    with open(saida, "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,'
                'initial-scale=1"><title>%s</title><style>%s</style></head><body><header><h1>%s</h1><nav>%s</nav></header>'
                '<main>%s</main><div class="aviso" role="status"></div><script>%s</script></body></html>'
                % (e(titulo), CSS, e(titulo), nav, corpo, JS))
    print(os.path.abspath(saida))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
