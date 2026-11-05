"""Gera uma galeria HTML local (abre no navegador, sem servidor) a partir de um JSON de itens.

Cada projeto monta o seu JSON (nomes legíveis, grupos, situação) e chama este script. Os vídeos
tocam pela prévia leve (previa_videos.py); o caminho do original aparece para abrir no VLC.
Seleção e anotações ficam no navegador (localStorage) e podem ser copiadas.

JSON de entrada:
{
  "titulo": "Vídeos · Projeto",
  "abas": [
    {"nome": "Criativos prontos",
     "grupos": [
       {"nome": "Topo do funil", "nota": "texto curto opcional",
        "subgrupos": [
          {"nome": "O que eu faria toda semana", "nota": "...",
           "itens": [
             {"id": "único", "titulo": "Versão base", "detalhe": "o que muda",
              "video": "caminho relativo ao HTML", "poster": "jpg relativo (opcional)",
              "original": "caminho do arquivo original", "etiquetas": ["revisado", "38 s"],
              "situacao": "ok|pendente|nao|antigo",
              "fps": 30, "meta": [["Exercício", "..."], ["Melhores trechos", "..."]]}]}]}]}]}

Opcionais por item: "situacao_texto" troca o rótulo da situação mantendo a cor (ex.: "no ar",
"pausado", "não subido", para aba de campanha); "link" põe um botão que abre a publicação
original (texto em "link_texto", padrão "Abrir no Instagram"), junto do vídeo local. Sem vídeo
local: "embed" (ex.: https://www.instagram.com/reel/<código>/embed/) toca dentro de um iframe;
sem os dois, "poster" vira imagem que abre o link.

Âncoras: "ancora" opcional em grupo, subgrupo e item (padrão: o nome ou o id em minúsculas, com
hífen). Abrir VER_VIDEOS.html#ancora troca para a aba certa, rola até o ponto e o destaca. A busca
procura no texto do cartão e no nome da aba, do grupo e do subgrupo, em todas as abas, sem acento.

Uso: python galeria_videos.py dados.json saida.html
"""
import html
import json
import re
import sys
import unicodedata

COR = {"ok": "#2f7d4f", "pendente": "#b7791f", "nao": "#b23b3b", "antigo": "#777"}
ROTULO = {"ok": "pode publicar", "pendente": "revisão pendente", "nao": "não publicar",
          "antigo": "versão antiga"}

CSS = """
:root{--bg:#f6f5f1;--card:#fff;--tx:#222;--mu:#666;--ln:#e3e0d8;--ac:#c2185b}
@media (prefers-color-scheme:dark){:root{--bg:#1b1a18;--card:#26241f;--tx:#eee;--mu:#aaa;--ln:#3a372f}}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,Segoe UI,sans-serif;background:var(--bg);color:var(--tx)}
header{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--ln);padding:10px 16px}
h1{font-size:18px;margin:0 0 8px}nav button{border:1px solid var(--ln);background:var(--card);color:var(--tx);
padding:6px 12px;border-radius:999px;margin:0 4px 4px 0;cursor:pointer}nav button[aria-selected=true]{background:var(--ac);color:#fff;border-color:var(--ac)}
#busca{width:min(420px,100%);padding:6px 10px;border:1px solid var(--ln);border-radius:8px;background:var(--card);color:var(--tx)}
.barra{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:6px}.barra small{color:var(--mu)}
main{padding:12px 16px 60px}section.g>h2{font-size:17px;margin:22px 0 4px}section.g>p,.sg>p{color:var(--mu);margin:0 0 8px;font-size:14px}
.sg>h3{font-size:15px;margin:14px 0 6px}.grade{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.c{background:var(--card);border:1px solid var(--ln);border-radius:10px;padding:8px;font-size:13px}
.c video{width:100%;aspect-ratio:9/16;background:#000;border-radius:6px}.c b{display:block;margin:6px 0 2px;font-size:14px}
.c .d{color:var(--mu);margin:2px 0}.pill{display:inline-block;padding:1px 8px;border-radius:999px;font-size:11px;margin:2px 2px 0 0;border:1px solid var(--ln)}
.sit{color:#fff;border:0}.c textarea{width:100%;height:38px;margin-top:4px;font:inherit;background:var(--bg);color:var(--tx);border:1px solid var(--ln);border-radius:6px}
.c code{font-size:11px;word-break:break-all;color:var(--mu);cursor:copy}.oculto{display:none}
.c details{margin-top:4px}.c summary{cursor:pointer;color:var(--ac);font-size:12px}.meta{margin:4px 0 0;display:grid;gap:3px}
.meta div{font-size:12px}.meta b{display:inline;font-size:12px;margin:0;color:var(--mu)}.abrir{margin-top:4px;width:100%}
button{font:inherit;cursor:pointer}.abrir,#m button{border:1px solid var(--ln);background:var(--card);color:var(--tx);border-radius:6px;padding:4px 8px}
#m{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:20;display:none;overflow:auto}
#m .in{display:grid;grid-template-columns:minmax(0,1fr) minmax(260px,380px);gap:14px;max-width:1300px;margin:0 auto;padding:12px 16px}
@media(max-width:800px){#m .in{grid-template-columns:1fr}}
#mv{width:100%;max-height:78vh;background:#000;border-radius:8px}#m .pn{background:var(--card);color:var(--tx);border-radius:10px;padding:12px;font-size:13px;min-width:0}
#tl{width:100%}#tc{font-family:ui-monospace,Consolas,monospace;color:#fff;font-size:13px}.ctl{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
#mn{width:100%;height:120px;font:inherit;background:var(--bg);color:var(--tx);border:1px solid var(--ln);border-radius:6px}
#mt{color:#fff;margin:0 0 6px;font-size:15px}.atalhos{color:var(--mu);font-size:12px}
.lk{display:flex;align-items:center;justify-content:center;width:100%;aspect-ratio:9/16;background:#000;border-radius:6px;overflow:hidden;color:#aaa}
.lk{border:0}.lk img{width:100%;height:100%;object-fit:cover}a.abrir{display:block;text-align:center;text-decoration:none;box-sizing:border-box}
[id]{scroll-margin-top:150px}.alvo{outline:3px solid var(--ac);outline-offset:3px}
a.anc{color:var(--mu);text-decoration:none;font-weight:400;margin-left:6px;font-size:.85em}a.anc:hover{color:var(--ac)}
.indice{background:var(--card);border:1px solid var(--ln);border-radius:10px;padding:8px 12px;margin:8px 0;font-size:13px}
.indice summary{cursor:pointer;font-weight:600}.indice ul{margin:6px 0 0;padding-left:18px}.indice li{margin:2px 0}
.indice a{color:var(--tx)}.indice a:hover{color:var(--ac)}.indice ul ul{margin:2px 0 4px}.indice ul ul a{color:var(--mu)}
body.buscando .aba{display:block!important}body.buscando .indice{display:none}
"""

JS = """
const K='galeria:'+document.title;let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
function salva(){try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
document.querySelectorAll('[data-sel]').forEach(c=>{c.checked=!!(st[c.dataset.sel]||{}).s;c.onchange=()=>{(st[c.dataset.sel]??={}).s=c.checked;salva()}});
document.querySelectorAll('[data-nota]').forEach(t=>{t.value=(st[t.dataset.nota]||{}).n||'';t.oninput=()=>{(st[t.dataset.nota]??={}).n=t.value;salva()}});
document.querySelectorAll('code').forEach(c=>c.onclick=()=>navigator.clipboard.writeText(c.textContent));
function aba(i){document.querySelectorAll('nav button').forEach((b,j)=>b.setAttribute('aria-selected',i==j));
document.querySelectorAll('.aba').forEach((a,j)=>a.classList.toggle('oculto',i!=j));try{localStorage.setItem(K+':aba',i)}catch(e){}}
document.querySelectorAll('nav button').forEach((b,i)=>b.onclick=()=>aba(i));let a0=0;try{a0=+localStorage.getItem(K+':aba')||0}catch(e){}aba(a0);
const sa=s=>s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
document.querySelectorAll('.c').forEach(c=>c.dataset.txt=sa((c.dataset.ctx||'')+' '+c.textContent));
function buscar(){const q=sa(document.getElementById('busca').value.trim());document.body.classList.toggle('buscando',!!q);let n=0;
document.querySelectorAll('.c').forEach(c=>{const v=!q||q.split(/\\s+/).every(t=>c.dataset.txt.includes(t));c.classList.toggle('oculto',!v);if(v&&q)n++});
document.querySelectorAll('.sg').forEach(s=>s.classList.toggle('oculto',!!q&&!s.querySelector('.c:not(.oculto)')));
document.querySelectorAll('section.g').forEach(s=>s.classList.toggle('oculto',!!q&&!s.querySelector('.c:not(.oculto)')));
document.querySelectorAll('.aba').forEach(a=>a.classList.toggle('vazia',!!q&&!a.querySelector('.c:not(.oculto)')));
document.getElementById('st').textContent=q?n+' encontrados em todas as abas':''}
document.getElementById('busca').oninput=buscar;
function ir(h){if(!h)return;let el=null;try{el=document.getElementById(decodeURIComponent(h))}catch(e){}if(!el)return;
const b=document.getElementById('busca');if(b.value){b.value='';buscar()}
const ab=[...document.querySelectorAll('.aba')].indexOf(el.closest('.aba'));if(ab>=0)aba(ab);
document.querySelectorAll('.alvo').forEach(x=>x.classList.remove('alvo'));el.classList.add('alvo');setTimeout(()=>el.scrollIntoView({block:'start'}),0)}
window.addEventListener('hashchange',()=>ir(location.hash.slice(1)));ir(location.hash.slice(1));
let cur=null,fps=30;const mv=document.getElementById('mv'),tl=document.getElementById('tl');
function fmt(t){t=t||0;const m=Math.floor(t/60),s=t-m*60;return m+':'+(s<10?'0':'')+s.toFixed(3)}
function upd(){document.getElementById('tc').textContent=fmt(mv.currentTime)+'  ·  quadro '+Math.round(mv.currentTime*fps)+'  ·  total '+fmt(mv.duration);if(mv.duration)tl.value=mv.currentTime/mv.duration*1000}
function abrir(id){const c=document.querySelector('.c[data-id="'+CSS.escape(id)+'"]');cur=id;fps=+c.dataset.fps||30;
document.getElementById('mt').textContent=c.querySelector('b').textContent+'  ('+fps+' qps)';mv.src=c.querySelector('video').getAttribute('src');vel(1);
const me=c.querySelector('.meta');document.getElementById('mmeta').innerHTML=me?me.innerHTML:'';document.getElementById('mo').textContent=c.dataset.orig||'';
document.getElementById('mn').value=(st[id]||{}).n||'';document.getElementById('m').style.display='block'}
function fechar(){mv.pause();document.getElementById('m').style.display='none';
if(cur){const t=document.querySelector('[data-nota="'+CSS.escape(cur)+'"]');if(t)t.value=(st[cur]||{}).n||''}cur=null}
function tocar(){mv.paused?mv.play():mv.pause()}
function quadro(n){mv.pause();mv.currentTime=Math.max(0,Math.min(mv.duration||0,mv.currentTime+n/fps+0.0001))}
function pulo(s){mv.currentTime=Math.max(0,Math.min(mv.duration||0,mv.currentTime+s))}
function vel(v){mv.playbackRate=v;document.getElementById('vv').textContent=v+'x'}
function nota(){(st[cur]??={}).n=document.getElementById('mn').value;salva()}
function marca(k){const mn=document.getElementById('mn'),t=fmt(mv.currentTime);
mn.value+=k=='ini'?(mn.value&&!mn.value.endsWith('\\n')?'\\n':'')+t+' - ':t+'\\n';nota()}
document.getElementById('mn').addEventListener('input',nota);
['timeupdate','seeked','loadedmetadata'].forEach(ev=>mv.addEventListener(ev,upd));
tl.addEventListener('input',()=>{if(mv.duration)mv.currentTime=tl.value/1000*mv.duration});
document.addEventListener('keydown',e=>{if(!cur||e.target.tagName=='TEXTAREA'||(e.target.tagName=='INPUT'&&e.target.type!='range'))return;const k=e.key;
if(k==',')quadro(-1);else if(k=='.')quadro(1);else if(k=='ArrowLeft')pulo(e.shiftKey?-10:-1);else if(k=='ArrowRight')pulo(e.shiftKey?10:1);
else if(k==' ')tocar();else if(k=='i'||k=='I')marca('ini');else if(k=='o'||k=='O')marca('fim');else if(k=='Escape')fechar();else return;e.preventDefault()});
document.getElementById('m').addEventListener('click',e=>{if(e.target.id=='m')fechar()});
function copiar(){const l=[];document.querySelectorAll('.c').forEach(c=>{const id=c.dataset.id,s=st[id]||{};
if(s.s||s.n)l.push((s.s?'[x] ':'[ ] ')+c.querySelector('b').textContent+' | '+(c.dataset.orig||'')+(s.n?' | '+s.n:''))});
navigator.clipboard.writeText(l.join('\\n'));document.getElementById('st').textContent=l.length+' copiados'}
"""


MODAL = """<div id="m"><div class="in"><div><p id="mt"></p><video id="mv" playsinline></video>
<input id="tl" type="range" min="0" max="1000" value="0" aria-label="linha do tempo"><div id="tc"></div>
<div class="ctl"><button onclick="quadro(-1)">◀ quadro</button><button onclick="tocar()">▶ / ❚❚</button><button onclick="quadro(1)">quadro ▶</button>
<button onclick="pulo(-1)">-1 s</button><button onclick="pulo(1)">+1 s</button><button onclick="vel(0.25)">0,25x</button><button onclick="vel(0.5)">0,5x</button>
<button onclick="vel(1)">1x</button><button onclick="vel(2)">2x</button><span id="vv" style="color:#fff;align-self:center"></span>
<button onclick="marca('ini')">Marcar início (I)</button><button onclick="marca('fim')">Marcar fim (O)</button><button onclick="fechar()">Fechar (Esc)</button></div>
<p class="atalhos" style="color:#ccc">Atalhos: vírgula/ponto = quadro a quadro · ←/→ = 1 s (Shift = 10 s) · espaço = tocar/pausar · I/O = marcar trecho · Esc = fechar</p></div>
<div class="pn"><b>Anotação (trechos marcados entram aqui)</b><textarea id="mn"></textarea><div id="mmeta" class="meta"></div>
<p class="atalhos">Original: <code id="mo"></code></p></div></div></div>"""


def e(s):
    return html.escape(str(s or ""))


def slug(s):
    s = unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "x"


def anc(a):
    return f'<a class="anc" href="#{e(a)}" title="link direto">#</a>'


def card(it, ctx=""):
    sit = it.get("situacao")
    pills = "".join(f'<span class="pill">{e(t)}</span>' for t in it.get("etiquetas", []))
    if sit:
        rot = it.get("situacao_texto") or ROTULO[sit]
        pills = f'<span class="pill sit" style="background:{COR[sit]}">{e(rot)}</span>' + pills
    poster = f' poster="{e(it["poster"])}"' if it.get("poster") else ""
    orig = f'<code title="clique para copiar">{e(it["original"])}</code>' if it.get("original") else ""
    i = e(it["id"])
    meta = ""
    if it.get("meta"):
        meta = ('<details><summary>Metadados</summary><div class="meta">'
                + "".join(f"<div><b>{e(k)}:</b> {e(v)}</div>" for k, v in it["meta"] if v not in (None, "", [])) + "</div></details>")
    link_txt = e(it.get("link_texto") or "Abrir no Instagram")
    link = f'<a class="abrir" href="{e(it["link"])}" target="_blank" rel="noopener">{link_txt}</a>' if it.get("link") else ""
    if it.get("video"):
        midia = f'<video controls preload="none" src="{e(it["video"])}"{poster}></video>'
        botao = '<button class="abrir" onclick="abrir(this.closest(&quot;.c&quot;).dataset.id)">Abrir quadro a quadro</button>' + link
    elif it.get("embed"):
        midia = f'<iframe class="lk" src="{e(it["embed"])}" loading="lazy" allowfullscreen></iframe>'
        botao = link
    else:
        img = f'<img src="{e(it["poster"])}" alt="" loading="lazy">' if it.get("poster") else '<span class="sem">sem prévia</span>'
        midia = f'<a class="lk" href="{e(it.get("link"))}" target="_blank" rel="noopener">{img}</a>'
        botao = link
    a = it.get("ancora") or slug(it["id"])
    return (f'<div class="c" id="{e(a)}" data-id="{i}" data-ctx="{e(ctx)}" data-orig="{e(it.get("original"))}" data-fps="{e(it.get("fps", 30))}">'
            f'{midia}<b>{e(it["titulo"])}{anc(a)}</b><div class="d">{e(it.get("detalhe"))}</div>{pills}'
            f'{botao}{meta}{orig}'
            f'<label><input type="checkbox" data-sel="{i}"> marcar</label>'
            f'<textarea data-nota="{i}" placeholder="anotação"></textarea></div>')


def main(entrada, saida):
    d = json.load(open(entrada, encoding="utf-8"))
    nav, corpo = [], []
    for ab in d["abas"]:
        nav.append(f'<button role="tab">{e(ab["nome"])}</button>')
        partes = [f'<div class="aba">']
        if ab.get("nota"):
            partes.append(f'<p>{e(ab["nota"])}</p>')
        indice = []
        for g in ab["grupos"]:
            ga = g.get("ancora") or slug(g["nome"])
            sub = "".join(f'<li><a href="#{e(sg.get("ancora") or slug(ga + "-" + sg["nome"]))}">{e(sg["nome"])}</a></li>'
                          for sg in g["subgrupos"])
            indice.append(f'<li><a href="#{e(ga)}">{e(g["nome"])}</a><ul>{sub}</ul></li>')
        if len(ab["grupos"]) > 1:
            partes.append(f'<details class="indice" open><summary>Sumário</summary><ul>{"".join(indice)}</ul></details>')
        for g in ab["grupos"]:
            ga = g.get("ancora") or slug(g["nome"])
            partes.append(f'<section class="g" id="{e(ga)}"><h2>{e(g["nome"])}{anc(ga)}</h2>'
                          + (f'<p>{e(g["nota"])}</p>' if g.get("nota") else ""))
            for sg in g["subgrupos"]:
                sa = sg.get("ancora") or slug(ga + "-" + sg["nome"])
                partes.append(f'<div class="sg" id="{e(sa)}"><h3>{e(sg["nome"])}{anc(sa)}</h3>'
                              + (f'<p>{e(sg["nota"])}</p>' if sg.get("nota") else ""))
                ctx = f'{ab["nome"]} {g["nome"]} {sg["nome"]}'
                partes.append('<div class="grade">' + "".join(card(it, ctx) for it in sg["itens"]) + "</div></div>")
            partes.append("</section>")
        partes.append("</div>")
        corpo.append("".join(partes))
    doc = (f'<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{e(d["titulo"])}</title><style>{CSS}</style><header><h1>{e(d["titulo"])}</h1><nav>{"".join(nav)}</nav>'
           f'<div class="barra"><input id="busca" placeholder="buscar: vídeo, campanha, conjunto (ex.: OF-03, CV1, oferta)"><button onclick="copiar()">Copiar marcados e anotações</button>'
           f'<small id="st"></small><small>{e(d.get("nota"))}</small></div></header><main>{"".join(corpo)}</main>{MODAL}<script>{JS}</script></html>')
    open(saida, "w", encoding="utf-8").write(doc)
    n = sum(len(sg["itens"]) for ab in d["abas"] for g in ab["grupos"] for sg in g["subgrupos"])
    print(f"{saida}: {n} vídeos")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
