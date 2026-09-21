# Conversor de PDF para DOCX

[![Publicação no GitHub Pages](https://github.com/SEU_USUARIO/SEU_REPOSITORIO/actions/workflows/deploy.yml/badge.svg)](https://github.com/SEU_USUARIO/SEU_REPOSITORIO/actions/workflows/deploy.yml)

Frontend estático para conversão de PDF para DOCX. A conversão é preservada no
backend Python com FastAPI e `pdf2docx`, hospedado separadamente.

## Compatibilidade com GitHub Pages

O GitHub Pages serve somente arquivos estáticos. A interface funciona no Pages,
mas a conversão exige um backend externo com HTTPS. Configure-o em `js/config.js`:

```javascript
window.APP_CONFIG = Object.freeze({
	apiBaseUrl: "https://seu-backend.exemplo.com",
});
```

Não coloque segredos nesse arquivo: o JavaScript publicado é visível para visitantes.

## Tecnologias

- HTML, CSS e JavaScript vanilla no frontend.
- FastAPI, Python e `pdf2docx` no backend.
- GitHub Actions e GitHub Pages para publicação estática.

## Execução local

No PowerShell, a partir da raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.app.main:app --reload
```

Depois, acesse `http://127.0.0.1:8000`.

Nesse modo, o backend serve o frontend pela mesma origem e `apiBaseUrl` pode permanecer vazio.

Para instalar também as ferramentas de desenvolvimento:

```powershell
python -m pip install -r backend\requirements-dev.txt
```

## Aplicação desktop legada

Para executar a versão original com CustomTkinter:

```powershell
python -m desktop.conversor_desktop
```

## Testes

```powershell
python -m unittest discover -s tests -v
ruff check backend desktop tests
ruff format --check backend desktop tests
```

## Publicação no GitHub Pages

1. Crie um repositório no GitHub e substitua `SEU_USUARIO/SEU_REPOSITORIO` pelo endereço real no badge.
2. Faça o commit e envie a branch principal:

```powershell
git add .
git commit -m "feat: preparar publicação no GitHub Pages"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

3. Em `Settings > Pages`, selecione `GitHub Actions` como fonte.
4. Acompanhe o workflow em `Actions > Publicar no GitHub Pages`.
5. O site ficará em `https://SEU_USUARIO.github.io/SEU_REPOSITORIO/`.

## Estrutura

```text
.
├── index.html
├── 404.html
├── css/ e js/
├── assets/
├── backend/ e desktop/
├── tests/ e docs/
└── .github/workflows/deploy.yml
```

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) e [LICENSE](LICENSE) para contribuições e licença.

## Limitações atuais

- O upload é limitado a 10 MiB.
- O servidor mantém os arquivos somente durante a conversão e o download.
- Não há banco de dados nem histórico de conversões.