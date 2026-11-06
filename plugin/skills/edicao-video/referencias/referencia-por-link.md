# Estilo de edição a partir de um link

A pessoa manda um vídeo público (YouTube, TikTok, Reels) e diz "quero assim".

1. Só link público. Serve de referência de estilo: não reaproveitar trecho, música nem arte.
2. Baixar uma cópia de estudo em `analise/referencia/` com o `yt-dlp` (gratuito,
   `pip install yt-dlp`, instalar com o "pode"): `yt-dlp -f "mp4[height<=720]" -o ref.mp4 <link>`.
   Não baixou (login, bloqueio)? Pedir para a pessoa mandar o arquivo ou descrever.
3. Medir, sem assistir quadro a quadro:
   - cortes: `ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep pts_time`
     → número de cortes por minuto e duração média dos planos;
   - folha de contato de 12 quadros (320 px), para ver legenda (posição, tamanho, cor, karaokê
     ou não), zoom, texto na tela e troca de câmera.
4. Escrever em `analise/referencia.md` 5 a 8 linhas: ritmo, legenda, zoom, textos, abertura e
   final. Mostrar e aplicar na decupagem.
5. Se a pessoa disser "sempre assim": regra em `memoria/aprendizados.md` (seção Vídeo).
6. Apagar a cópia de estudo ao fim do vídeo (é de outra pessoa).
