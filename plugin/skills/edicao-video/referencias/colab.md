# Google Colab (GPU grátis) sem atrito

O Colab gratuito costuma dar uma GPU NVIDIA T4. Ganho real: **transcrição** (Whisper
na GPU) e **gravação do vídeo final** (NVENC). Os filtros de imagem (tonemap, legenda)
rodam na CPU do Colab, que é fraca (2 núcleos): em PC bom o local pode empatar.
Por isso a decisão vem do `teste_velocidade.py` dos dois lados, não de achismo.

Limites (o Google não publica números exatos; consultado em 01/11/2026): sessão até
~12 h, desliga se ficar parada, GPU não garantida em horário de pico. Nunca prometer
prazo ao usuário com base só no Colab; ter o local como plano B.

Medido em 03/11/2026, na T4 grátis, comparando com um notebook de 8 núcleos (GeForce MX150, sem NVENC):

| | Colab T4 | Notebook (CPU) |
|---|---|---|
| Gravar o vídeo (teste sintético) | 1,42x tempo real (NVENC) | 1,11x (libx264) |
| CPU do Colab sem NVENC | 0,36x | - |
| Transcrever 16 s de fala | 5 s, modelo medium, sem erro | 8 s, modelo small, errou um nome próprio |

Conclusão: em PC razoável, local basta. O Colab vale a pena para PC fraco, vídeo longo
ou quando a transcrição precisar de mais precisão. Lembrar que mandar e baixar o vídeo
pelo Drive também leva tempo.

## Como o Claude conversa com o Colab

Tudo passa pela pasta `Edicao-Video/_colab/` do Google Drive:
1. Aqui: `python <skill>/scripts/colab_job.py enviar <nome> "<comando>" ...` grava a
   tarefa em `_colab/fila/`. Os arquivos (brutos, projeto) têm de estar dentro do Drive.
2. No Colab: o notebook roda `colab_worker.py`, que prepara tudo (faster-whisper, FFmpeg
   com NVENC), executa a fila e grava o resultado em `_colab/feito/`.
3. Aqui: `colab_job.py status <id>` (resumo curto). Os arquivos gerados aparecem no
   Drive sozinhos.

Se o MCP `colab-mcp` estiver disponível na sessão, o Claude pode abrir e rodar o
notebook ele mesmo (`open_colab_browser_connection`); o usuário só autoriza o Drive
na janela do Google. Sem o MCP, o usuário abre o notebook e clica "Executar tudo".

## Preparar uma vez

1. Google Drive para computador instalado e logado (ver `instalacao.md`). **O Colab é a única parte do kit que exige o app do Drive:** dizer isso antes de oferecer o Colab.
2. `python <skill>/scripts/colab_job.py kit` → copia os scripts e o notebook para
   `Edicao-Video/_kit/`. Repetir depois de atualizar o kit.
3. Opcional (menos cliques): MCP do Colab, precisa do `uv`:
   `claude mcp add colab-mcp --scope user -- uvx git+https://github.com/googlecolab/colab-mcp`
   e reiniciar o Claude. Pedir o "pode" do usuário antes.
4. Abrir `Edicao-Video/_kit/edicao_video_gpu.ipynb` no Drive (duplo clique abre no
   Colab), conferir GPU T4 e Executar tudo. Na 1ª vez o Google pede acesso ao Drive.

## Teste

Rodar o worker com `--teste` (célula: `!python ".../colab_worker.py" --teste --uma-vez`).
Ele grava `_colab/feito/teste_colab.txt` com o resumo do ambiente e a velocidade.
Comparar com o local e anotar no perfil: "Colab Nx tempo real, local Mx".

## Fluxo de um vídeo no Colab

- Transcrição: `colab_job.py enviar transc_<take> "python {scripts}/whisper.py <bruto> <srt>"`.
- Montagem: o `scripts/montar_<nome>.py` do projeto (dentro do Drive) roda igual lá:
  `colab_job.py enviar monta_<nome> "python <projeto>/scripts/montar_<nome>.py"`.
  O codificador NVENC entra sozinho (`ambiente.codificador_args`).
- Enquanto roda, dizer ao usuário o que está acontecendo e quanto falta (estimativa
  do teste). Conferências (quadros, ebur128) podem rodar aqui, sobre o arquivo já sincronizado.

## Quando dá errado

- "Drive não montado" / "sem GPU": pedir para rodar a 1ª célula de novo / trocar o
  tipo de ambiente para GPU T4.
- Tarefa parada na fila: o notebook não está aberto, ou o Drive ainda não sincronizou.
- Sem GPU disponível (pico): fazer local e avisar a diferença de tempo.
