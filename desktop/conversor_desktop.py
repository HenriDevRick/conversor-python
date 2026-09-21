import os
import threading
from tkinter import filedialog, messagebox

import customtkinter as ctk

from backend.app.services.conversor_pdf import converter_pdf

# Configuração do tema da interface
ctk.set_appearance_mode("System")  # Segue o tema do sistema (Claro/Escuro)
ctk.set_default_color_theme("blue")


class ConversorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela
        self.title("Conversor de PDF para DOCX")
        self.geometry("500x350")
        self.resizable(False, False)

        # Variáveis de Estado
        self.pdf_path = ""

        # Layout da Interface
        self.criar_widgets()

    def criar_widgets(self):
        # Título Principal
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Conversor PDF para Word",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.lbl_titulo.pack(pady=(20, 10))

        # Subtítulo
        self.lbl_subtitulo = ctk.CTkLabel(
            self,
            text="Selecione um arquivo PDF para converter para .docx",
            font=ctk.CTkFont(size=12),
        )
        self.lbl_subtitulo.pack(pady=(0, 20))

        # Botão para Selecionar Arquivo
        self.btn_selecionar = ctk.CTkButton(
            self,
            text="Selecionar PDF",
            command=self.selecionar_arquivo,
            width=200,
            height=40,
        )
        self.btn_selecionar.pack(pady=10)

        # Rótulo com o Nome do Arquivo Selecionado
        self.lbl_arquivo = ctk.CTkLabel(
            self, text="Nenhum arquivo selecionado", text_color="gray", wraplength=400
        )
        self.lbl_arquivo.pack(pady=10)

        # Barra de Progresso (Oculta por padrão)
        self.progress_bar = ctk.CTkProgressBar(self, width=350)
        self.progress_bar.set(0)

        # Botão de Conversão
        self.btn_converter = ctk.CTkButton(
            self,
            text="Converter para DOCX",
            command=self.iniciar_conversao,
            fg_color="green",
            hover_color="darkgreen",
            width=200,
            height=40,
            state="disabled",
        )
        self.btn_converter.pack(pady=15)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Escolha o PDF", filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if caminho:
            self.pdf_path = caminho
            nome_arquivo = os.path.basename(caminho)
            self.lbl_arquivo.configure(
                text=f"Selecionado: {nome_arquivo}", text_color="white"
            )
            self.btn_converter.configure(state="normal")

    def iniciar_conversao(self):
        # Desabilita botões durante o processo
        self.btn_selecionar.configure(state="disabled")
        self.btn_converter.configure(state="disabled")

        # Exibe a barra de progresso em modo indeterminado
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()

        # Executa a conversão em uma thread separada para não travar a interface
        thread = threading.Thread(target=self.converter_pdf)
        thread.start()

    def converter_pdf(self):
        try:
            caminho_docx = converter_pdf(self.pdf_path)

            # Notifica sucesso
            self.after(0, lambda: self.finalizar_sucesso(caminho_docx))

        except Exception as erro:  # noqa: BLE001
            # Notifica erro
            mensagem_erro = str(erro)
            self.after(0, lambda: self.finalizar_erro(mensagem_erro))

    def finalizar_sucesso(self, caminho_docx):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.btn_selecionar.configure(state="normal")
        self.btn_converter.configure(state="normal")

        messagebox.showinfo(
            "Sucesso!", f"Arquivo convertido com sucesso!\n\nSalvo em:\n{caminho_docx}"
        )

    def finalizar_erro(self, mensagem_erro):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.btn_selecionar.configure(state="normal")
        self.btn_converter.configure(state="normal")

        messagebox.showerror("Erro na Conversão", f"Ocorreu um erro:\n{mensagem_erro}")


if __name__ == "__main__":
    app = ConversorApp()
    app.mainloop()
