---
name: caamt-arquivos
description: "Onde guardar e como organizar os arquivos do kit CAAMT (pasta do computador ou Google Drive), a planilha de trabalho e o envio de arquivos ao Drive pelo próprio Claude. Use ao salvar, subir, organizar ou achar arquivo, ao criar a planilha, ou quando o usuário falar em Drive, pasta, upload ou \"mandar para a nuvem\"."
---

# Arquivos e Google Drive

## Escolha (perguntar na primeira vez que for salvar algo; gravar em `memoria/perfil.md`)
"Guardo os arquivos no seu Google Drive ou nesta pasta do computador?" A pessoa pode trocar
quando quiser. Na troca, copiar o que existe; nunca apagar o original sem pedir.

## Estrutura (igual nos dois lugares; a pessoa pode mudar, e a mudança vai para `memoria/regras.md`)
```
CAAMT-<Subseção>/
  parceiros/<Parceiro>/          documentos recebidos (um parceiro por pasta)
  publicacoes/<AAAA-MM-DD>_<tema>/  artes, legenda, fonte das fotos
  Edicao-Video/                  vídeos (skill edicao-video)
  marca/                         logos, molduras, rodapé, MARCA.md
  coringa/                       fotos da OAB, da sede, dos delegados, do quadro social
```
Local: dentro da pasta de trabalho. Drive: `Meu Drive/CAAMT-<Subseção>/`.

## Planilha
Toda leitura e gravação passa pela skill `caamt-planilha` (Drive ou `planilha/` no computador).

## Mandar arquivo para o Drive (o Claude faz)
1. **Texto, planilha, Markdown**: pelo conector do Google Drive (`create_file`).
2. **Imagem e PDF até 10 MB, com a extensão Claude no Chrome:** abrir no Chrome a pasta de
   destino do Drive, criar um campo de arquivo na página, pôr o arquivo nele (`file_upload`) e
   soltá-lo na área vazia da lista. Nunca soltar em cima de uma pasta da lista: o arquivo cai
   dentro dela. Depois, conferir pelo conector que o arquivo está na pasta certa e com o mesmo
   tamanho. Errou a pasta? Mover para a certa e avisar.
3. **Arquivo grande (vídeo) ou sem a extensão do Chrome: a pessoa arrasta.** O conector não
   leva arquivo grande (ele teria de passar inteiro pela conversa). O Claude prepara tudo:
   cria a pasta de destino pelo conector, se faltar, e roda
   `python <skill>/scripts/abrir_para_arrastar.py <link da pasta> <arquivo>`, que abre a pasta
   do Drive no navegador e o arquivo selecionado no computador. A mensagem é uma linha:
   "Abri a pasta do Drive e o arquivo: é só arrastar o arquivo para a pasta." Depois, conferir
   pelo conector que chegou (nome e tamanho) e pôr o link na planilha. Não chegou (a pessoa
   deixou para depois): anotar em `memoria/pendencias.md` o arquivo e a pasta, e lembrar na
   próxima conversa.
4. **Pastas no Drive:** pelo conector (pasta = `contentMimeType`
   `application/vnd.google-apps.folder`, dentro da pasta-mãe pelo id). A pasta `CAAMT-<Subseção>`
   é criada uma vez e o id vai para `memoria/perfil.md`.
5. Documento que chega no WhatsApp: no celular, Compartilhar › Drive › pasta do parceiro.

## Nunca
Apagar arquivo, mudar compartilhamento ou deixar pasta pública sem pedido.
