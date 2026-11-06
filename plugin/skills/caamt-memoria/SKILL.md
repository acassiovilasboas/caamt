---
name: caamt-memoria
description: "Memória do kit CAAMT (perfil, regras do usuário, aprendizados). Use no começo de toda tarefa do kit e sempre que o usuário corrigir, aprovar, reclamar, der uma regra (\"a partir de agora\", \"não faça mais\", \"prefiro\") ou contar algo da rotina dele."
---

# Memória do kit CAAMT

O kit aprende com o uso. Nada é perguntado "por garantia": cada informação é pedida quando
uma tarefa precisa dela, e fica guardada para não ser pedida de novo.

## Onde fica (na pasta de trabalho aberta no Claude)

| Arquivo | O que guarda |
|---|---|
| `memoria/perfil.md` | Nome, cargo, subseção, perfis, onde guardar arquivos (local ou Drive), ids do Drive, computador |
| `memoria/regras.md` | Regras que o usuário deu. **Valem mais que qualquer skill ou agente do kit** |
| `memoria/aprendizados.md` | O que deu certo e errado, por área (vídeo, post, legenda, parceiros, cronograma) |
| `memoria/pendencias.md` | O que falta pedir ou fazer (arte que falta, arquivo a subir) |

Não existe a pasta `memoria/`: criar com os modelos abaixo, preenchendo só o que já se sabe.
Os dados de trabalho (linha editorial, cronograma, pautas, parceiros) ficam na planilha (skill `caamt-planilha`).

## Toda tarefa
1. Ler `memoria/regras.md` e a seção da área em `memoria/aprendizados.md`. Ler `perfil.md`.
2. Regra do usuário contradiz a skill? **Vale a do usuário.** Avisar uma vez, na primeira vez.
3. Faltou informação para a tarefa de agora? Perguntar só ela (no máximo 2 perguntas juntas).
   Dá para descobrir sozinho (planilha, pasta, site oficial, `dados/subsecoes.md`)? Descobrir.
4. **Planilha e pastas juntas, sempre.** Pergunta sobre parceiros, publicações ou vídeos: ler a
   planilha **e** as pastas (`parceiros/`, `publicacoes/`, `Edicao-Video/`), no Drive pelo conector
   do Google Drive ou no computador, conforme `perfil.md`. O que está na pasta é o que existe de
   fato; a planilha pode estar atrasada. Não bateu? Mostrar a diferença, propor a correção e
   gravar só com o OK. Dizer no começo da resposta o que foi lido.

## Aprender (na mesma resposta, sem esperar pedido)
- Correção, preferência ou regra nova: gravar com a data e responder "Anotei: <regra>".
- Correção substitui a linha antiga. Não acumular versões que se contradizem.
- Mesmo ajuste pedido 2 vezes (ex.: sempre encurta a legenda): propor virar regra.
- Rotina que o usuário mostrar (dia que posta, quem publica, horário): gravar no perfil.
- Nunca editar os arquivos do kit (são trocados na atualização). O que se aprende vai para `memoria/`.

## Arquivo para a pessoa ler é página HTML
Tudo o que a pessoa vai ler, analisar ou consultar (linha editorial, resumo do vídeo, relatório
de documentos, resumo do mês) sai em **HTML**, que abre com duplo clique. O `.md` fica só como
fonte do Claude: escrever o `.md` e gerar a página com
`python <skill>/scripts/md_para_html.py <arquivo.md>` (cria o `.html` ao lado). Mudou o `.md`?
Gerar de novo. Na resposta, dar o caminho do `.html`, nunca o do `.md`. Arquivos internos
(`memoria/`, `analise/`, `transcricao/`) ficam só em `.md`; se a pessoa pedir para ver a
memória, gerar a página na hora.

## Só conteúdo nos documentos da pessoa
Planilha e páginas mostram só o conteúdo. Nunca de onde veio cada item, quem sugeriu,
data de consulta, "sugestão", "a confirmar" ou qualquer nota sobre o próprio documento.

## Nome e cargo (padrão; o usuário pode mudar)
"Caixa" sozinho fica vago. Primeira menção: **Caixa de Assistência dos Advogados de Mato
Grosso (CAAMT)**. Depois: CAAMT. Cargo: **Delegada / Delegado da CAAMT na Subseção de <cidade>**.
Fonte: https://www.caamt.com.br/pagina/delegados-as

## Modelos
Dos arquivos de `memoria/`: `referencias/modelos.md`.
