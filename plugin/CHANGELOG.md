# Changelog

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
