import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app


class ApiConversorTestes(unittest.TestCase):
    def setUp(self):
        self.cliente = TestClient(app)

    def test_rejeita_arquivo_que_nao_e_pdf(self):
        resposta = self.cliente.post(
            "/api/converter",
            files={"arquivo": ("relatorio.txt", b"conteudo", "text/plain")},
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.json()["detail"], "Envie um arquivo PDF.")

    @patch("backend.app.api.conversao.converter_pdf")
    def test_retorna_docx_convertido_para_download(self, converter_mock):
        def conversao_falsa(caminho_pdf):
            caminho_docx = caminho_pdf.removesuffix(".pdf") + ".docx"
            with open(caminho_docx, "wb") as arquivo:
                arquivo.write(b"DOCX DE TESTE")
            return caminho_docx

        converter_mock.side_effect = conversao_falsa
        resposta = self.cliente.post(
            "/api/converter",
            files={"arquivo": ("relatorio.pdf", b"%PDF-TESTE", "application/pdf")},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.content, b"DOCX DE TESTE")
        self.assertIn("relatorio.docx", resposta.headers["content-disposition"])
        converter_mock.assert_called_once()

    def test_rejeita_conteudo_que_nao_e_pdf(self):
        resposta = self.cliente.post(
            "/api/converter",
            files={"arquivo": ("relatorio.pdf", b"texto comum", "application/pdf")},
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(
            resposta.json()["detail"],
            "O conteúdo enviado não é um PDF válido.",
        )

    def test_rejeita_arquivo_maior_que_o_limite(self):
        conteudo = b"%PDF-" + b"x" * (10 * 1024 * 1024)
        resposta = self.cliente.post(
            "/api/converter",
            files={"arquivo": ("relatorio.pdf", conteudo, "application/pdf")},
        )

        self.assertEqual(resposta.status_code, 413)
        self.assertEqual(
            resposta.json()["detail"],
            "O arquivo excede o limite de 10 MiB.",
        )


if __name__ == "__main__":
    unittest.main()
