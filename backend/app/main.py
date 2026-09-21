"""Ponto de entrada da aplicação web."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.api.conversao import router as conversao_router
from backend.app.core.config import DIRETORIO_FRONTEND

app = FastAPI(title="Conversor de PDF para DOCX")

app.include_router(conversao_router)


app.mount("/", StaticFiles(directory=DIRETORIO_FRONTEND, html=True), name="frontend")
