---
name: edicao-video
description: "Edição de vídeo curto (Reels, Stories, anúncio, vídeo de parceiro) controlada pelo Claude com FFmpeg, Whisper e Python, no computador do usuário ou na GPU grátis do Google Colab. Cortes, zoom, B-roll, limpeza de áudio, legenda karaokê, selos, CTA, capa, organização dos vídeos no Google Drive e documento de marca de cada projeto. Usar sempre que o pedido envolver editar, montar, legendar, cortar, transcrever ou fazer capa de vídeo, organizar vídeos, ou criar/atualizar a marca de um projeto."
---

# Edição de vídeo

O segredo não é um comando: é a ordem de trabalho. Analisar antes de montar,
decidir com o usuário o que é dele, montar por script com listas editáveis,
conferir com evidência, e revisão por quem não editou.

`<skill>` = pasta onde este arquivo está. Scripts em `<skill>/scripts/`.

## Antes de tudo (toda sessão, custa quase nada)

1. **Kit CAAMT:** a memória é a da pasta de trabalho (skill `caamt-memoria`):
   `memoria/perfil.md`, `memoria/regras.md` e a seção Vídeo de `memoria/aprendizados.md`.
   **Regra do usuário vale mais que este arquivo.** Sem `memoria/`, usar `~/.edicao-video/`.
   Pergunta sobre vídeos (o que existe, o que falta, qual versão): ler a pasta `Edicao-Video/`
   no Drive (conector) ou no computador, não só a planilha (regra 4 de `caamt-memoria`).
   Computador ainda não medido: `referencias/primeiro-uso.md` (só mede; não faz questionário).
2. `python <skill>/scripts/ambiente.py` → ler só o resumo de 6 linhas que ele
   imprime (usa cache de 30 dias). Com `--refazer` quando uma ferramenta falhar,
   o usuário instalar algo ou trocar de computador.
3. Se o projeto tem `CLAUDE.md`/`AGENTS.md` com padrão de vídeo próprio, **o do
   projeto vale** onde houver conflito.

## Onde processar (local ou Colab)

**O usuário manda.** Pediu Colab (agora ou no perfil: `Processar em: colab`), então é Colab:
nada pesado roda neste computador. Isso inclui transcrição, prévia, extração de muitos quadros
e teste de cadeia de áudio. Aqui só ficam leitura de metadado (`ffprobe`), conversa e
decupagem. Se faltar algo para o Colab, como o Drive para computador, preparar isso primeiro
seguindo `referencias/colab.md`. Nunca voltar para o processamento local sem o usuário autorizar.
Pediu local, então é local. Pedido explícito vale mais que a recomendação do `ambiente.py`.

Sem pedido, decidir pelo resumo do `ambiente.py`, sem perguntar de novo o que o perfil já diz:
- "editar neste computador": tudo local.
- "usar o Colab": transcrição e gravação final no Colab, o resto (decisões,
  decupagem, conferência) aqui. Seguir `referencias/colab.md`.
- Vídeo longo (> 3 min de bruto) num PC lento: oferecer o Colab uma vez, com a
  estimativa de tempo dos dois lados, e anotar a escolha no perfil.
Nunca deixar o usuário esperando sem dizer quanto falta. Ao fim, uma linha em
`~/.edicao-video/historico.md` (data, projeto, onde rodou, minutos), que calibra
as próximas estimativas.

## Passo 0: documento de marca do projeto

Todo valor de marca (cor, fonte, logo, CTA, público, tom) sai de
`marca/MARCA.md` + `marca/marca.json` do projeto (kit CAAMT: a `marca/` única da raiz `CAAMT-<Subseção>/`), nunca da memória nem do código.
Não existe: criar seguindo `referencias/documento-de-marca.md`. Existe: ler e
atualizar só o item que o usuário mudou.

## Objetivo antes do roteiro (regra de negócio)

Antes de propor qualquer corte, deixar escrito em 3 linhas:
- **quem publica**,
- **para quem**,
- **qual é a notícia**.

Quem aparece no vídeo não é necessariamente quem anuncia. Se houver receita para esse tipo de
vídeo (`~/.edicao-video/receitas/` ou `referencias/receitas/`), segui-la. Não deu para saber
pelo perfil, pela marca ou pela receita? Perguntar antes de cortar.

- **Vídeo de parceiro da CAAMT (Caixa de Assistência dos Advogados de Mato Grosso):** quem
  publica é a CAAMT, pela subseção, o público é a advocacia, e a notícia é a **nova parceria e
  o benefício**. O parceiro é o assunto, não o
  anunciante. Seguir `referencias/receitas/parceiro-caixa.md` e o modelo `modelos/caamt/`
  (molduras, rodapé e cores).

## Ordem de trabalho de um vídeo

Mostrar o andamento com nomes do negócio, não técnicos: "Entender a nova parceria",
"Ouvir e transcrever a fala", "Escolher os melhores trechos", "Montar com a moldura da
CAAMT", "Fazer a capa", "Revisar", "Entregar".

1. **Ler**: marca, `referencias/padrao-tecnico.md`, `referencias/licoes.md`,
   `~/.edicao-video/licoes.md` (lições deste usuário) e a edição anterior do projeto.
2. **Pasta do vídeo** (estrutura em `referencias/primeiro-uso.md`, item Pastas):
   `brutos/ analise/ transcricao/ tmp/ final/ capas/ cartelas/ LEIA-ME.md`.
   Renomear bruto só com autorização, mantendo o nome original na frente.
3. **Em paralelo**, dois subagentes (passar a eles o caminho `<skill>`):
   - `video-audio-fala`: transcrição por palavra conferida, pausas, versão
     enxuta, diagnóstico de eco/ruído, amostras A/B (`scripts/cadeias_audio.py`).
   - `video-catalogador`: cada take, melhores trechos, rosto, defeitos, cor/luz.
4. **Parar e mostrar ao usuário** o que depende dele: cadeia de áudio (ele ouve),
   valor sem fonte, palavra em dúvida, take principal. Não montar antes.
   **Sempre perguntar qual moldura ou arte usar:** listar o que existe em `marca/logos/`
   (molduras, rodapé, vinheta), cada uma com uma linha do que é. Mostrar uma folha com as
   miniaturas, gerada por Pillow sobre fundo neutro. Opções: usar uma delas no vídeo inteiro,
   só no cartão final, ou nenhuma. A escolha vale só para este vídeo. Se a pessoa disser
   "sempre essa", gravar a escolha no MARCA.md.
   **Mais de uma câmera:** `python <skill>/scripts/sincronizar_cameras.py <base> <outra>` dá o
   atraso; a decupagem alterna os takes já alinhados (ARQ e PLANOS do `montar_video.py`).
   **Exemplo de estilo por link** (YouTube, TikTok, Reels público): `referencias/referencia-por-link.md`.
5. **Decupagem** em tabela (tempo final, fonte no bruto, enquadramento, fala, texto).
6. **`video-editor-montagem`** copia `scripts/montar_video.py` para o projeto,
   preenche as listas e roda. Capa com `scripts/capa.py`, cartão final com `scripts/cartelas.py`.
7. **`video-revisor`** (não editou): devolve só o que afeta o resultado.
8. **Capa (sempre, faz parte da entrega).** Por padrão, `scripts/capa.py` faz assim:
   - usa um quadro do próprio vídeo, com sorriso de verdade (indicado pelo catalogador);
   - põe o gancho em caixa na cor da marca;
   - põe por cima a arte da subseção escolhida (`RODAPE`), com os logos subidos até caberem no
     recorte 4:5 do feed.
   Mostrar a capa inteira e o recorte 4:5 lado a lado. Se o usuário sugerir outra capa (uma
   foto, uma arte pronta, outro quadro), usar a dele (`CAPA_DO_USUARIO`) e só aplicar texto e
   rodapé se ele quiser.
   **Versões:** entregar 2 versões diferentes (ex.: cortes ou legenda diferentes), salvo
   regra do usuário ("só uma"). Dizer em uma linha o que muda entre elas.
9. **Registrar** no `LEIA-ME.md` da pasta: decupagem, decisões, dúvidas, quem revisou. Kit
   CAAMT: gerar também `LEIA-ME.html` (`caamt-memoria/scripts/md_para_html.py`) e dar esse caminho.
10. **Entregar onde o usuário escolher** (seção "Entrega").

Tarefa pequena (cortar um trecho, trocar legenda, gerar capa, converter): fazer
direto, sem subagentes. Prompt pronto para vídeo novo: `referencias/prompt-sessao.md`.

## Organização e página dos vídeos (padrão, sempre)

- **Todo vídeo mora em `Edicao-Video/<Projeto>/<AAAA-MM-DD>_<nome>/`**, no lugar que o
  usuário escolheu (skill `caamt-arquivos`: pasta do computador ou Google Drive). Vale para vídeo que chegou por WhatsApp,
  Downloads ou Drive: copiar o bruto para `brutos/`, sem apagar o original.
- **Vídeo que só existe no Drive** (sem cópia no computador): não baixar sem pedir. Anotar em
  `<pasta do vídeo>/drive.json` (`[{"titulo": "...", "drive_id": "<id>"}]`, com o id achado pelo
  conector do Google Drive) para ele aparecer na página tocando pelo player do Drive.
- **Página `Edicao-Video/VER_VIDEOS.html`:** rodar `python <skill>/scripts/galeria_projeto.py
  <Edicao-Video>` ao organizar um vídeo novo e ao terminar cada versão. Em seguida, dizer ao
  usuário o caminho da página: ela abre com duplo clique. A página mostra prontos, brutos e
  vídeos do Drive por projeto, com busca, marcação de trechos e anotação. Vídeo que o
  navegador já toca entra direto. Os outros ganham uma prévia leve, feita uma vez só (no
  Colab, se o perfil disser `Processar em: colab`).
- O vídeo do Drive embutido na página só toca para quem estiver logado numa conta do Google
  com acesso ao arquivo. Para mostrar a outra pessoa, mandar o link do Drive, sem mudar o
  compartilhamento do arquivo sem pedir.

## Entrega (o usuário escolhe; perguntar na primeira entrega e gravar no perfil; kit CAAMT: `caamt-arquivos`)

Duas opções. Nenhuma limita a outra: dá para mudar a qualquer hora.
- **Computador.** Tudo fica em `Edicao-Video/` local. Funciona sem conta Google. (Kit CAAMT: perguntar uma vez, pela skill `caamt-arquivos`.)
- **Google Drive pelo conector, sem instalar o app do Drive:**
  1. A pasta do vídeo no Drive é `CAAMT-<Subseção>/Edicao-Video/<AAAA-MM-DD>_<nome>/`, criada **pelo script** (`drive_upload.py pasta`), nunca pelo conector.
     Gravar o link no `LEIA-ME.md`.
  2. **Arquivo grande (vídeo) não passa pelo conector** (o arquivo teria de passar inteiro
     pela conversa). O Claude sobe pelo script do kit, sem instalar o app do Drive:
     `python <caamt-arquivos>/scripts/drive_upload.py enviar <vídeo> --pasta "CAAMT-<Subseção>/Edicao-Video/<AAAA-MM-DD>_<nome>/final"`.
     Ainda não configurado: `caamt-arquivos/referencias/permissoes-google.md`; até lá, dar o
     caminho do arquivo para o usuário arrastar no Drive.
  3. Depois que o arquivo estiver no Drive, conferir pelo conector (listar a pasta) e anotar
     no `drive.json` da pasta do vídeo, para a página VER_VIDEOS mostrar.
- Nunca apagar a cópia local sem pedir. Nunca mudar o compartilhamento no Drive sem pedir.

## Memória viva (a skill aprende com o usuário)

Três camadas, cada uma no seu lugar. **Nunca editar os arquivos desta skill** (são
substituídos quando o kit é atualizado); o que se aprende vai para `~/.edicao-video/`:

| O que se aprendeu | Onde grava |
|---|---|
Kit CAAMT: as camadas abaixo ficam em `memoria/` da pasta de trabalho (`caamt-memoria`);
`~/.edicao-video/` só sem o kit.

| Preferência ou jeito do usuário (nível de explicação, horário, aprova por áudio, não gosta de X) | `~/.edicao-video/perfil.md` |
| Lição de edição que vale para qualquer vídeo dele ("legenda menor", "nunca música") | `~/.edicao-video/licoes.md` (tabela: lição, data) |
| Regra de uma marca/projeto (cor, CTA, logo, tom) | `marca/MARCA.md` do projeto |
| Tarefa repetida que ganhou um jeito próprio (ex.: "vídeo de parceiro da CAAMT") | `~/.edicao-video/receitas/<nome>.md`: passos, valores, exemplo aprovado |

**Artes da marca crescem com o uso.** Pedir só quando a tarefa precisar (nunca em lista na primeira conversa) as que o usuário tiver
(logos, rodapé, molduras, capas, vinheta, modelo de post). Depois:
- arquivo de arte que chegar em qualquer conversa: salvar em `marca/logos/` do projeto,
  registrar no `MARCA.md` (o que é, quando usar, data) e confirmar em uma linha;
- tarefa que precisa de uma arte que ainda falta: pedir naquele momento, dizendo para que serve.
  Enquanto não chega, seguir sem ela e avisar, sem inventar e sem usar a de outra subseção;
- arte nova que substitui uma antiga: trocar no `MARCA.md` e manter a antiga com a data, até o
  usuário mandar apagar.

Regras:
- Gravar **na mesma resposta** em que o usuário corrigiu, aprovou ou reclamou. Uma linha, com data.
- Correção substitui a linha antiga (não acumular versões contraditórias).
- Antes de um pedido que tem receita, ler a receita e seguir; perguntar só o que mudou.
- Lição do usuário que contradiz `referencias/licoes.md`: vale a do usuário, e avisar uma vez.
- O perfil manda no tom: iniciante recebe passo a passo curto e sem termo técnico;
  avançado recebe só a decisão.
- Atualização do kit: quando o usuário disser "atualizar a skill", rodar
  `/plugin update kit-caamt` (ou repetir a instalação do README). Os arquivos de
  `~/.edicao-video/` continuam.

## Economia de tokens (obrigatório)

- Ler resumos, não arquivos crus: `ambiente.py` (6 linhas), `colab_job.py status`,
  saídas curtas dos scripts. Não abrir `ambiente.json` inteiro.
- Imagem: folha de contato pequena (até 12 quadros, 320 px de largura) em vez de
  quadro a quadro; quadro grande só para decidir capa ou conferir texto.
- Transcrição uma vez por bruto, guardada em `transcricao/`; reusar. Janela isolada
  só para o trecho em dúvida.
- Análise de cada vídeo fica em `analise/*.md`: sessão nova lê o `.md`, não reanalisa.
- Subagentes só no fluxo completo de vídeo com fala; nunca dois revisores.
- Saída longa de FFmpeg: `-v error` e só o fim do erro.

## Ferramentas

- FFmpeg completo (filtros `subtitles`, `zscale`, `ebur128`; `whisper` no 8.0+), Python 3.10+
  com Pillow e numpy. Instalação: `referencias/instalacao.md`.
- Transcrição: `scripts/whisper.py` escolhe sozinho o motor (GPU no Colab, filtro do
  FFmpeg com modelo baixado por `scripts/baixar_modelo.py`, ou faster-whisper).
- Gravação final: `ambiente.codificador_args()` usa a placa de vídeo quando o teste
  real passou (NVENC no Colab, VideoToolbox no Mac), senão libx264.
- Página dos vídeos: `scripts/galeria_projeto.py` (padrão, monta tudo sozinho). Por baixo,
  `galeria_videos.py dados.json saida.html` (motor, formato no topo) e `previa_videos.py`
  (prévias leves), para quem precisar de uma página sob medida.
- Opcionais, se o usuário tiver: CapCut (MCP `capcut`) para terminar à mão; gerador de
  imagem por IA. Consome crédito: perguntar antes.

## Regras fixas

- Não inventar o que a pessoa falou: transcrição conferida; o resto marcado "inferido".
- Valor, número ou afirmação na tela só com fonte no projeto ou aprovação do usuário.
- Não alterar brutos. Não subir, publicar nem ativar nada sem pedido.
- Vídeo assistido e legenda revisada por um humano antes de publicar.
- Dizer quem revisou. Se foi só quem editou: "review pendente".
