# Ligar o envio automático ao Google Drive (uma vez, ~10 minutos)

Por quê: o conector do Google Drive no Claude lê e cria arquivos de texto, mas não sobe vídeo
nem imagem. Para subir sem instalar o Google Drive para computador, o kit usa um script que
fala direto com o Google. Para isso, o Google pede que você crie uma "chave de app" na sua
própria conta. Você faz os cliques e o login; o Claude não vê sua senha.

**Permissão pedida:** `drive.file`. O kit só vê e mexe nos arquivos e pastas que ele mesmo
criou no seu Drive. Seus outros arquivos ficam fora do alcance dele. O Google classifica essa
permissão como não sensível ([Google, escopos do Drive](https://developers.google.com/workspace/drive/api/guides/api-specific-auth), consultado em 05/11/2026).

## Passos (os nomes dos botões podem mudar; procure pelo sentido)
1. Abra https://console.cloud.google.com com a sua conta Google e crie um projeto
   (ex.: "Kit CAAMT").
2. **APIs e serviços › Biblioteca** › procure **Google Drive API** › **Ativar**.
3. **Google Auth Platform** (ou "Tela de consentimento OAuth") › **Começar**:
   nome do app "Kit CAAMT", seu e-mail, público **Externo**.
4. **Acesso a dados** (ou "Escopos") › adicionar `https://www.googleapis.com/auth/drive.file`.
5. **Público**: clique em **Publicar app** (fica "Em produção"). Se preferir deixar em
   **Teste**, adicione seu e-mail como usuário de teste, mas aí o acesso vence a cada 7 dias
   e é preciso refazer o login.
6. **Clientes** (ou "Credenciais") › **Criar cliente** › tipo **App para computador** ›
   **Baixar JSON**.
7. No Claude, diga: "configurei, o arquivo está em <caminho>". O Claude roda:
   `drive_upload.py configurar <arquivo.json>` e depois `drive_upload.py login`, que abre o
   navegador para você entrar e autorizar.

O Google pode mostrar o aviso "app não verificado". É o seu próprio app: clique em
"Avançado" › "Acessar Kit CAAMT". Para cancelar o acesso a qualquer momento:
https://myaccount.google.com/permissions

Onde fica a chave: `~/.kit-caamt/` no seu computador. Não compartilhe essa pasta.
