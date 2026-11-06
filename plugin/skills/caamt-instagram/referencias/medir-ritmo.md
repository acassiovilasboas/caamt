# Medir o ritmo de um perfil público do Instagram

Sem API e sem login extra: no Chrome da própria pessoa (extensão Claude no Chrome), abrir
`https://www.instagram.com/<perfil>/` e rodar o código abaixo no console da página. Ele rola a
grade, lê os links dos posts e tira a data de cada um do próprio código do post (o "DfIfVxlGADY"
de `/p/DfIfVxlGADY/`: os primeiros bits do número do post são o horário em que ele foi publicado).
Conferido abrindo um post: a data bate com a que o Instagram mostra.

```js
(async()=>{const A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
const dt=c=>{let id=0n;for(const x of c.slice(0,11))id=id*64n+BigInt(A.indexOf(x));return new Date(Number(id>>23n)+1314220021721)};
for(let i=0;i<4;i++){window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,1800))}
const m=new Map();document.querySelectorAll('a[href*="/p/"],a[href*="/reel/"]').forEach(a=>{const h=a.getAttribute('href');
const c=h.split('/').filter(Boolean).pop();if(!m.has(c))m.set(c,{d:dt(c),reel:h.includes('/reel/'),texto:(a.querySelector('img')?.alt||'').slice(0,90)})});
return [...m.values()].sort((a,b)=>b.d-a.d).map(p=>p.d.toISOString().slice(0,10)+(p.reel?' Reels ':' ')+p.texto).join('\n')})()
```

Como ler o resultado:
- Posts fixados no topo do perfil são antigos: não contam no ritmo.
- Ritmo = posts dos últimos 60 dias ÷ 8,6 semanas. Se todos os posts lidos estão dentro dos 60
  dias, a grade não carregou tudo: contar pelo período real (do mais antigo lido até hoje).
- O texto vem do "alt" da imagem (começo da legenda): serve para agrupar por tema.
- Não guardar nome de pessoa que aparece em nota de pesar ou foto.
