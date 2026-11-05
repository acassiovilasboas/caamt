# Changelog

## 1.0.1 (05/11/2026)
Correções da revisão de três subagentes: scripts, aderência ao pedido e questionador.
- Agentes de vídeo leem `memoria/regras.md`: a regra do usuário chega a eles.
- Uma árvore só no Drive (`CAAMT-<Subseção>/...`): pastas só pelo script, o conector só cria arquivo.
- Planilha única "CAAMT – <Subseção>" com 5 abas. Sem conector do Sheets, nunca regravar a planilha inteira.
- Preferência do usuário só em `memoria/regras.md`, não na aba Config.
- Primeira conversa: cria `CLAUDE.md` na pasta (força a leitura da memória); funciona sem Python; linha editorial sem agente.
- Artes pedidas só quando a tarefa precisar; "legenda" e "capa" sem disputa entre skills; uma `marca/` só.
- `drive_upload.py`: retoma o envio depois de queda de internet ou erro 5xx; compara MD5 antes de pular arquivo.
- `varrer_pasta.py`: acha RG.pdf, CNH.jpg; `post_convenio.py`: 3 descontos cabem, nunca sobrescreve arte.
- Frontmatter YAML entre aspas (3 arquivos não carregavam a descrição).
- Colab: avisa que é a única parte que exige o app do Drive.
- Licença PolyForm Noncommercial 1.0.0 (gratuita, sem uso comercial) e ícone do plugin.

## 1.0.0 (05/11/2026)
Primeira versão do kit único. Junta o `edicao-video` 1.0.6 e o rascunho `caixa-parceiros` 0.1.0.
- Skills especialistas: caamt-memoria, caamt-inicio, caamt-arquivos, caamt-linha-editorial,
  caamt-cronograma, caamt-criativo, caamt-legenda, caamt-parceiros, caamt-documentos,
  caamt-linktree, caamt-instagram e edicao-video.
- Agentes: video-audio-fala, video-catalogador, video-editor-montagem, video-revisor,
  perfis-instagram, pauta-pesquisador, documentos-conferente.
- Memória na pasta de trabalho (`memoria/`): regra do usuário vale mais que o kit; nada de
  questionário no começo, cada dado é pedido quando a tarefa precisa.
- Envio de vídeo, imagem e PDF ao Google Drive pelo Claude (`drive_upload.py`, permissão
  `drive.file`), sem o app do Drive. Escolha entre Drive e pasta do computador.
- Linha editorial começa pelos perfis de Instagram conhecidos; cronograma com eventos
  (antes, no dia, depois) e pautas com fonte.
- Vídeo: nomes dos passos em linguagem do negócio, 2 versões, sincronia de 2 câmeras pelo som,
  estilo a partir de link público. Post "Convênio Disponível" por script.
- Parceiros: etapa Prospecção, pasta por parceiro, mensagem de convencimento, conferência dos
  documentos na pasta.
- Nome e cargo: "Caixa de Assistência dos Advogados de Mato Grosso (CAAMT)" e "Delegada /
  Delegado da CAAMT na Subseção de <cidade>".

Não testado com conta real: login do `drive_upload.py` no Google, publicação no Instagram pela
API da Meta, edição do Linktree pelo Chrome.
