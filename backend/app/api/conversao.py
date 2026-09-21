"""Endpoint HTTP responsável pela conversão de PDF para DOCX."""

import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from backend.app.core.config import (
    TAMANHO_BLOCO_UPLOAD,
    TAMANHO_MAXIMO_UPLOAD,
)
from backend.app.services.conversor_pdf import converter_pdf

router = APIRouter()


def remover_diretorio(caminho: str) -> None:
    """Remove os arquivos temporários gerados durante uma conversão."""
    shutil.rmtree(caminho, ignore_errors=True)


@router.post("/api/converter")
async def converter_arquivo(
    tarefas_em_segundo_plano: BackgroundTasks,
    arquivo: UploadFile = File(...),  # noqa: B008
) -> FileResponse:
    """Recebe um PDF, converte-o e retorna o DOCX para download."""
    nome_original = Path(arquivo.filename or "").name

    if not nome_original or Path(nome_original).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Envie um arquivo PDF.")

    diretorio_temporario = Path(tempfile.mkdtemp(prefix="conversor_"))
    caminho_pdf = diretorio_temporario / nome_original

    try:
        with caminho_pdf.open("wb") as arquivo_destino:
            total_recebido = 0
            cabecalho = b""

            while bloco := await arquivo.read(TAMANHO_BLOCO_UPLOAD):
                if not cabecalho:
                    cabecalho = bloco[:5]

                total_recebido += len(bloco)
                if total_recebido > TAMANHO_MAXIMO_UPLOAD:
                    raise HTTPException(
                        status_code=413,
                        detail="O arquivo excede o limite de 10 MiB.",
                    )

                arquivo_destino.write(bloco)

        if cabecalho != b"%PDF-":
            raise HTTPException(
                status_code=400,
                detail="O conteúdo enviado não é um PDF válido.",
            )

        caminho_docx = converter_pdf(str(caminho_pdf))
    except HTTPException:
        remover_diretorio(str(diretorio_temporario))
        raise
    except Exception as erro:
        remover_diretorio(str(diretorio_temporario))
        raise HTTPException(
            status_code=500,
            detail=f"Ocorreu um erro na conversão: {erro}",
        ) from erro
    finally:
        await arquivo.close()

    tarefas_em_segundo_plano.add_task(
        remover_diretorio,
        str(diretorio_temporario),
    )

    nome_saida = f"{Path(nome_original).stem}.docx"
    return FileResponse(
        path=caminho_docx,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=nome_saida,
        background=tarefas_em_segundo_plano,
    )
