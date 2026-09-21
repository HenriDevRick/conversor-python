const formulario = document.querySelector("#formulario-conversao");
const entradaArquivo = document.querySelector("#arquivo-pdf");
const botaoConversao = document.querySelector("#botao-converter");
const nomeArquivo = document.querySelector("#nome-arquivo");
const status = document.querySelector("#status");
const apiBaseUrl = (window.APP_CONFIG?.apiBaseUrl || "").replace(/\/$/, "");

function mostrarStatus(mensagem, tipo = "") {
  status.textContent = mensagem;
  status.className = `status ${tipo}`.trim();
}

entradaArquivo.addEventListener("change", () => {
  const arquivo = entradaArquivo.files[0];
  const arquivoValido = arquivo && arquivo.name.toLowerCase().endsWith(".pdf");

  botaoConversao.disabled = !arquivoValido;
  nomeArquivo.textContent = arquivoValido
    ? arquivo.name
    : "Nenhum arquivo selecionado";
  mostrarStatus(arquivoValido ? "Pronto para converter." : "Selecione um arquivo PDF.");
});

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const arquivo = entradaArquivo.files[0];
  if (!arquivo) {
    return;
  }

  const dados = new FormData();
  dados.append("arquivo", arquivo);
  botaoConversao.disabled = true;
  mostrarStatus("Convertendo seu arquivo...");

  try {
    if (!apiBaseUrl) {
      throw new Error(
        "A conversão exige um backend. Configure apiBaseUrl em js/config.js."
      );
    }

    const resposta = await fetch(`${apiBaseUrl}/api/converter`, {
      method: "POST",
      body: dados,
    });

    if (!resposta.ok) {
      const erro = await resposta.json().catch(() => ({}));
      throw new Error(erro.detail || "Não foi possível converter o arquivo.");
    }

    const documento = await resposta.blob();
    const url = URL.createObjectURL(documento);
    const link = document.createElement("a");
    link.href = url;
    link.download = arquivo.name.replace(/\.pdf$/i, ".docx");
    link.click();
    URL.revokeObjectURL(url);

    mostrarStatus("Conversão concluída. O download foi iniciado.", "sucesso");
  } catch (erro) {
    mostrarStatus(erro.message, "erro");
  } finally {
    botaoConversao.disabled = false;
  }
});