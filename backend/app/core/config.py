"""Configurações compartilhadas pelo backend."""

from pathlib import Path

TAMANHO_MAXIMO_UPLOAD = 10 * 1024 * 1024
TAMANHO_BLOCO_UPLOAD = 1024 * 1024
DIRETORIO_FRONTEND = Path(__file__).resolve().parents[3]
