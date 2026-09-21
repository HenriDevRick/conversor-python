"""Serviço responsável pela conversão de arquivos PDF para DOCX."""

import os

from pdf2docx import Converter


def converter_pdf(caminho_pdf: str) -> str:
    """Converte um PDF para DOCX e retorna o caminho do arquivo gerado."""
    caminho_docx = os.path.splitext(caminho_pdf)[0] + ".docx"

    conversor = Converter(caminho_pdf)
    conversor.convert(caminho_docx, start=0, end=None)
    conversor.close()

    return caminho_docx
