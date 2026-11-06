# Kit CAAMT — instruções de instalação para o modelo de IA

Você recebeu este link de uma Delegada ou de um Delegado da CAAMT (Caixa de Assistência dos
Advogados de Mato Grosso). Sua tarefa é **instalar o plugin `kit-caamt`** para essa pessoa.
Fale com ela em português simples. Não altere os arquivos do kit.

- Repositório: `https://github.com/acassiovilasboas/caamt`
- Marketplace: `kit-caamt` (arquivo `.claude-plugin/marketplace.json`)
- Plugin: `kit-caamt` (pasta `plugin/`; versão em `plugin/.claude-plugin/plugin.json`)
- Pacote para upload: `https://github.com/acassiovilasboas/caamt/releases/latest/download/kit-caamt.zip`

## 1. Descubra onde você está rodando

Tente executar `claude --version` no terminal.

- **O comando funcionou** (Claude Code, ou a aba Code do Claude Desktop com terminal): siga o **caminho A**.
- **Não há terminal ou o comando não existe** (chat do Claude Desktop, do app ou da web): siga o **caminho B**.

## Caminho A — instalar por comando

```bash
claude plugin marketplace add acassiovilasboas/caamt
claude plugin install kit-caamt@kit-caamt
```

Se o marketplace já estiver instalado e a pessoa quiser a versão nova:

```bash
claude plugin marketplace update kit-caamt
claude plugin install kit-caamt@kit-caamt
```

Para conferir, rode `claude plugin list` e confirme que `kit-caamt` aparece e está ativo.
Depois peça à pessoa que **feche e abra o Claude de novo** (ou que inicie uma sessão nova).

## Caminho B — a pessoa instala pelo Claude Desktop

Você não consegue clicar por ela. Passe estes passos, um de cada vez:

1. Baixe o arquivo **kit-caamt.zip**:
   https://github.com/acassiovilasboas/caamt/releases/latest/download/kit-caamt.zip
   **Não descompacte.**
2. Abra o **Claude Desktop** e vá em **Configurações › Plugins**.
3. Clique em **Enviar um plugin** (Upload plugin), escolha o `kit-caamt.zip` e clique em **Fazer upload**.
4. Crie uma pasta no computador para o trabalho da CAAMT. Na aba **Code**, clique em **+** e escolha essa pasta.

Se os nomes dos menus estiverem diferentes, procure a área de plugins nas configurações.
O aplicativo muda de lugar os botões com frequência.

## 2. Primeiro uso

Depois de instalar, a pessoa abre a pasta da CAAMT na aba **Code** e escreve:

> Boa tarde. Sou <nome>, Delegada da CAAMT na Subseção de <cidade>.

O kit verifica o computador, monta as pastas e pergunta o que ela quer fazer primeiro.
Ele não aplica questionário: pede cada informação quando a tarefa precisa.

## Requisitos

- Claude Desktop ou Claude Code com plano **Pro ou superior**. O kit roda na aba **Code**.
- Opcional: conectores do **Google Drive** e do **Google Sheets** (Personalizar › Conectores) e a
  extensão do Claude no Chrome. Sem o do Sheets, a planilha fica no computador, em Excel.
- Use sempre a mesma pasta, no computador: a memória do kit (`memoria/`) fica nela. No celular e
  na aba Chat o kit não roda.
- O vídeo é editado com FFmpeg, Whisper e Python. O próprio kit verifica e orienta a instalação.
  Se o computador for fraco, ele ensina a usar o Google Colab gratuito. O Colab é a única parte
  que exige o Google Drive para computador instalado.
- Arquivos no Drive: texto e planilha vão pelo conector; arte e PDF até 10 MB, pela extensão do
  Claude no Chrome; vídeo, você arrasta para a pasta do Drive que o Claude deixa aberta.

## O que o kit faz

Edita vídeo de parceiro, faz a arte e a legenda do post de convênio, monta a linha editorial e o
cronograma de postagens, acompanha os parceiros e confere os documentos, e guarda tudo no Google
Drive ou no computador.

Ainda não testado com conta real: login do Google para upload de vídeo, publicação no Instagram
pela API da Meta e edição do Linktree.

## Licença

PolyForm Noncommercial 1.0.0: uso gratuito, proibido vender ou usar comercialmente. Ver `LICENSE`.
