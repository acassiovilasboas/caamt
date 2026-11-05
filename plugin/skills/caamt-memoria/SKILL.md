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
Os dados de trabalho (parceiros, cronograma, pautas) ficam na planilha (skill `caamt-arquivos`).

## Toda tarefa
1. Ler `memoria/regras.md` e a seção da área em `memoria/aprendizados.md`. Ler `perfil.md`.
2. Regra do usuário contradiz a skill? **Vale a do usuário.** Avisar uma vez, na primeira vez.
3. Faltou informação para a tarefa de agora? Perguntar só ela (no máximo 2 perguntas juntas).
   Dá para descobrir sozinho (planilha, pasta, site oficial, `dados/subsecoes.md`)? Descobrir.

## Aprender (na mesma resposta, sem esperar pedido)
- Correção, preferência ou regra nova: gravar com a data e responder "Anotei: <regra>".
- Correção substitui a linha antiga. Não acumular versões que se contradizem.
- Mesmo ajuste pedido 2 vezes (ex.: sempre encurta a legenda): propor virar regra.
- Rotina que o usuário mostrar (dia que posta, quem publica, horário): gravar no perfil.
- Nunca editar os arquivos do kit (são trocados na atualização). O que se aprende vai para `memoria/`.

## Nome e cargo (padrão; o usuário pode mudar)
"Caixa" sozinho fica vago. Primeira menção: **Caixa de Assistência dos Advogados de Mato
Grosso (CAAMT)**. Depois: CAAMT. Cargo: **Delegada / Delegado da CAAMT na Subseção de <cidade>**.
Fonte: https://www.caamt.com.br/pagina/delegados-as

## Modelos

`perfil.md`
```
# Perfil
- Nome / tratamento:
- Cargo: Delegada|Delegado da CAAMT na Subseção de <cidade> | cidades atendidas:
- Perfis: pessoal @ | subseção @ | CAAMT @caamt1
- Guardar arquivos em: (perguntar na primeira vez que precisar) local | drive
- Drive: pasta raiz id= | planilha id=
- Computador: (do ambiente.py, quando editar vídeo)
- Rotina: (preencher com o uso)
```
`regras.md`: tabela `Regra | Vale para | Dada em`.
`aprendizados.md`: uma seção por área; em cada uma, tabela `O que | Origem | Data`.
