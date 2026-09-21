"""Configurações compartilhadas pelo backend."""

import os
from pathlib import Path

TAMANHO_MAXIMO_UPLOAD = 10 * 1024 * 1024
TAMANHO_BLOCO_UPLOAD = 1024 * 1024
DIRETORIO_FRONTEND = Path(__file__).resolve().parents[3]
ORIGENS_PERMITIDAS = [
	origem.strip()
	for origem in os.getenv(
		"CORS_ORIGINS",
		"http://127.0.0.1:8000,http://localhost:8000,"
		"https://henridevrick.github.io",
	).split(",")
	if origem.strip()
]
