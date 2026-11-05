---
name: caamt-criativo
description: "Faz a arte pronta para postar (o \"criativo\") da subseção da CAAMT: post \"Convênio Disponível\" com a foto da placa, post de texto sobre foto de fundo, lembrete de parceiros ativos. Use quando a pessoa pedir arte, post, imagem, capa de post (capa de vídeo é da skill edicao-video), ou quando uma linha do cronograma precisar de arte."
---

# Arte do post

1. **Modelo da subseção:** ler `CAAMT-<Subseção>/marca/MARCA.md` (a mesma marca do vídeo) (cores, fontes, rodapé). O que vem no kit em
   `modelos/barra-do-garcas/` é da Subseção de Barra do Garças: outra subseção usa o dela.
   Faltou o rodapé ou o modelo? Pedir naquele momento e anotar em `memoria/pendencias.md`.
2. **Logo do parceiro:** usar o que a pessoa mandou. Não tem? Procurar no site oficial ou no
   perfil oficial do parceiro, baixar o arquivo, dizer de onde veio e pedir OK. Nunca desenhar
   logo nem texto com gerador de imagem (erra letra e marca).
3. **Tipos:**
   - **Convênio Disponível** (foto com a placa): preencher um `config.json` e rodar
     `python <skill>/scripts/post_convenio.py config.json` (campos no topo do script).
   - **Texto sobre foto de fundo** (ex.: foto da sede da OAB da cidade): foto da pasta
     `coringa/`, da pessoa ou de fonte oficial com crédito; texto curto, rodapé da subseção.
   - **Lembrete de parceiros ativos:** logos e descontos dos parceiros com Etapa
     "Divulgado" na planilha.
   Para os dois últimos, adaptar o `post_convenio.py` (mesmo tamanho 1080x1350 e rodapé),
   copiando-o para a pasta do post. Gerador de imagem por IA só com pedido: consome crédito.
4. **Salvar** em `publicacoes/<AAAA-MM-DD>_<tema>/` com o `config.json` e a fonte das
   fotos. Mostrar a arte. Com o OK, subir (skill `caamt-arquivos`) e pôr o link na linha do
   Cronograma.
5. Ajuste pedido (cor, tamanho, posição) que vale para sempre: `memoria/aprendizados.md`, seção Post.

Conferir antes de entregar: nome do parceiro, percentuais, telefone e @ batem com a planilha.
