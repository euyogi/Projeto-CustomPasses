
<img alt="Header" width=100% src="https://capsule-render.vercel.app/api?type=waving&color=0000ff&height=100&section=header">

# Projeto-CustomPasses

A carteira do Google não deixa personalizar os cartões que adicionamos. Então, fiz esse
projeto para personalizar os meus cartões (passe da biblioteca, carteirinha estudantil, entre outros que
possam ser representados com um QR Code.)

Ademais, pode servir de base para implementação da API da carteira da Google para integrar com seu negócio.
Aqui, utilizei o cartão genérico, mas há vários tipos (embarque, ingresso, identidade, etc...)

Mais informações em: https://developers.google.com/wallet?hl=pt-br.

<h2>Para testar:</h2>

Abrir <a href="custompasses.vercel.app">Projeto-CustomPasses</a>.

Detalhe: Ao abrir o cartão o título conterá [SOMENTE TESTE] antes, confira os exemplos abaixo.

<h2>Tela Inicial:</h2>

<p align="center">
  <img alt="Imagem da tela inicial" width=80% src="https://github.com/euyogi/Projeto-CustomPasses/assets/46427886/dec82306-7d96-49cb-85aa-19afc4aafaca">
</p>

Como você pode ver basta inserir os dados que você quer no seu cartão e clicar em adicionar, você será redirecionado para
a carteira da google perguntando se você quer adicionar o cartão.

<h2>Exemplos de cartões:</h2>

<p align="center">
  <img alt="Imagem de um cartão" width=25% src="https://github.com/euyogi/Projeto-CustomPasses/assets/46427886/4518d202-2841-43b1-b4de-104a1dbef7cc">
  <img alt="Imagem de um cartão" width=30% src="https://github.com/euyogi/Projeto-CustomPasses/assets/46427886/5addd044-bc92-4157-ace7-2e8583dac001b">
  <img alt="Imagem de um cartão" width=25.5% src="https://github.com/euyogi/Projeto-CustomPasses/assets/46427886/58cf1010-0aad-42f0-ba00-ea760b78ced6">
</p>

A logo é a imagem do google no canto superior esquerdo e a imagem é a imagem na parte inferior do cartão escrito #GoogleIO.

<h2>Para testar localmente:</h2>

Necessário: Python

Baixe e extraia o .zip com os arquivos.

Cole a chave da API no arquivo KEY.json, no arquivo tem mais informações para iniciar o uso da API e baixar a chave.
Em seguida, cole a sua issuer_id na variável `ISSUER_ID` no arquivo app.py, também mais informações para pegar esse id no arquivo.
Também é preferível mudar o url 'origins' no arquivo generic.py na linha 174 para o do seu website.

Instale as bibliotecas necessárias com `pip install -r requirements.txt`

Rode com `flask run` e abra o link dado, provavelmente http://127.0.0.1:5000.

<p align="center">Feito por: Yogi Nam de Souza Barbosa</p>

<img alt="Footer" width=100% src="https://capsule-render.vercel.app/api?type=waving&color=0000ff&height=100&section=footer">
