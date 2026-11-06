# Changelog

## 1.0.5 (06/11/2026)
- Linha editorial sem a coluna de exemplo: nada sobre os perfis consultados em planilha, painel ou página.
- Contato com o desenvolvedor só depois de cinco tentativas (ou pedido da pessoa).

## 1.0.4 (06/11/2026)
- Documentos da pessoa só com conteúdo: sai a coluna Origem da Linha editorial, as marcas
  "sugestão" e o "Gerado de" das páginas. "Exemplo real" vira "Exemplo (link)".
- Temas de partida só com o que foi visto nos perfis (inclui "Quarta de Lei", do @oab_bg).

## 1.0.3 (06/11/2026)
- `caamt-painel`: painel da subseção no navegador (Hoje, Postagens, Parceiros, Temas, Pautas), letras
  grandes, botões de WhatsApp com a mensagem pronta, copiar e abrir pasta ou arte. Só dado real.
- `caamt-agenda`: lembrete na agenda da pessoa (Google Agenda ou outra com conector), um evento por
  prazo, atualizado quando a data muda.
- `caamt-suporte`: contato com o desenvolvedor pelo WhatsApp, só em último caso.
- Planilha: colunas Pasta (link) e Evento na agenda; coluna nova entra no fim sem mexer no resto;
  nunca grava dado de exemplo.
- Ritmo medido dos perfis do Instagram e método de medição (`caamt-instagram/referencias/medir-ritmo.md`).

## 1.0.2 (06/11/2026)
- Nova skill `caamt-planilha`: única dona da planilha "CAAMT – <Subseção>". Ela nasce na conversa,
  quando for útil, com a pergunta Drive ou computador nesse momento. Abas: Linha editorial,
  Cronograma, Pautas, Parceiros, Config, Histórico. Modo computador com `planilha_local.py`
  (grava só as células citadas, registra o Histórico e gera `planilha/ver.html`).
- Linha editorial vira aba da planilha, com Frequência (fixa ou por demanda; convênio
  disponível é por demanda) e Origem de cada tema.
- Primeira conversa sem menu: cumprimenta, mostra o que achou e oferece um passo concreto.
- Todo arquivo para a pessoa ler sai em HTML (`md_para_html.py`).
- Sem resto de palestra, testes ou outros projetos no kit.

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
