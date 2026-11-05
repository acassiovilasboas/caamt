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
  linha-editorial.md
```
Local: dentro da pasta de trabalho. Drive: `Meu Drive/CAAMT-<Subseção>/`.

## Planilha "CAAMT – <Subseção>" (abas Parceiros, Cronograma, Pautas, Config, Histórico)
- Drive: Google Planilhas pelos conectores do Google Drive e do Google Sheets (como criar: `caamt-parceiros/referencias/planilha.md`).
- Local: um CSV por aba em `planilha/` (UTF-8 com BOM, abre no Excel).
- Sempre ler antes de gravar e gravar **só as células que mudaram**. A pessoa pode editar à
  mão: o que ela escreveu vale.

## Mandar arquivo para o Drive (o Claude faz)
1. **Texto, planilha, Markdown**: pelo conector do Google Drive (`create_file`).
2. **Vídeo, imagem, PDF**: o conector não serve (o arquivo teria de passar inteiro pela
   conversa; um vídeo de 34 MB não subiu no teste de 04/11/2026). Usar o script, que fala
   direto com o Google:
   `python <skill>/scripts/drive_upload.py enviar <arquivo> --pasta "CAAMT-<Subseção>/<subpasta>"`
   Ele cria as pastas que faltam, não sobe duas vezes o mesmo arquivo e imprime o link.
3. `login` espera a pessoa no navegador por até 5 min: rodar em segundo plano ou com tempo
   limite de 10 min. `drive_upload.py status` diz se já está configurado. Não está: mostrar
   `referencias/permissoes-google.md` (10 minutos, uma vez) e, até lá, guardar local e anotar
   em `memoria/pendencias.md` o que falta subir.
4. **Pastas no Drive: só o script cria** (`drive_upload.py pasta "<caminho>"`); o conector nunca cria
   pasta, só arquivo de texto dentro de pasta já criada (pelo id). Com a permissão `drive.file`, o script só enxerga as pastas que **ele** criou.
   No modo Drive, a pasta `CAAMT-<Subseção>` é criada pelo script (`drive_upload.py pasta
   "CAAMT-<Subseção>"`), e o id vai para o perfil. O conector acha tudo pelo id.
5. Documento que chega no WhatsApp: no celular, Compartilhar › Drive › pasta do parceiro.

## Nunca
Apagar arquivo, mudar compartilhamento ou deixar pasta pública sem pedido.
