"""Ponto de entrada da aplicação web."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.api.conversao import router as conversao_router
from backend.app.core.config import DIRETORIO_FRONTEND, ORIGENS_PERMITIDAS

app = FastAPI(title="Conversor de PDF para DOCX")

app.add_middleware(
	CORSMiddleware,
	allow_origins=ORIGENS_PERMITIDAS,
	allow_methods=["POST"],
	allow_headers=["*"],
)
app.include_router(conversao_router)


app.mount("/", StaticFiles(directory=DIRETORIO_FRONTEND, html=True), name="frontend")
