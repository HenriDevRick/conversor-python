# Arquitetura

## Frontend estático

`index.html`, `css/` e `js/` formam a aplicação publicada pelo GitHub Pages.
O frontend envia o PDF para a URL configurada em `js/config.js`.

## Backend

O backend em `backend/` usa FastAPI e `pdf2docx`. Ele precisa ser executado em
um serviço com runtime Python. O GitHub Pages não executa esse código.

## Limitação da hospedagem

Não é possível converter PDF para DOCX com fidelidade usando somente HTML,
CSS e JavaScript do navegador. Para conversão real, publique o backend em um
serviço separado e configure sua URL HTTPS em `js/config.js`.