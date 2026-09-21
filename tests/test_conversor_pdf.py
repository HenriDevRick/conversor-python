import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from backend.app.services.conversor_pdf import converter_pdf


class ConversorPdfTestes(unittest.TestCase):
    @patch("backend.app.services.conversor_pdf.Converter")
    def test_converte_todas_as_paginas_para_o_mesmo_nome_base(self, classe_conversor):
        conversor = Mock()
        classe_conversor.return_value = conversor

        with tempfile.TemporaryDirectory() as diretorio:
            caminho_pdf = str(Path(diretorio) / "relatorio.pdf")

            caminho_docx = converter_pdf(caminho_pdf)

        self.assertEqual(caminho_docx, str(Path(diretorio) / "relatorio.docx"))
        classe_conversor.assert_called_once_with(caminho_pdf)
        conversor.convert.assert_called_once_with(caminho_docx, start=0, end=None)
        conversor.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
