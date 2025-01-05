document.addEventListener("DOMContentLoaded", function () {
    const diagramacaoInput = document.querySelector('input[name="diagramacao"]'); // Campo de diagramação
    const diagramacaoForm = document.getElementById('diagramacaoForm'); // Contêiner do custo da diagramação
    const quantidadePaginasInput = document.getElementById("id_quant_pag"); // Campo de quantidade de páginas
    const custoPorPaginaInput = document.getElementById("id_custo_pag"); // Campo de custo por página
    const custoDiagramacaoInput = document.getElementById("id_custo_diagramacao"); // Campo de custo da diagramação
    const precoOutput = document.getElementById("preco"); // Campo de exibição do preço total

    // Atualiza a visibilidade ao carregar a página
    toggleDiagramacao(diagramacaoInput.checked);

    // Escuta mudanças no campo de diagramação
    diagramacaoInput.addEventListener("change", function () {
        toggleDiagramacao(this.checked);
    });

    // Escuta mudanças nos campos que afetam o preço
    quantidadePaginasInput.addEventListener("input", calculatePrice);
    custoPorPaginaInput.addEventListener("input", calculatePrice);
    custoDiagramacaoInput.addEventListener("input", calculatePrice);

    // Função para alternar visibilidade do custo de diagramação
    function toggleDiagramacao(isChecked) {
        if (isChecked) {
            diagramacaoForm.classList.remove("hidden");
        } else {
            diagramacaoForm.classList.add("hidden");
            custoDiagramacaoInput.value = ""; // Limpa o valor
        }
        calculatePrice(); // Atualiza o preço
    }

    // Função para calcular o preço total
    function calculatePrice() {
        // Obtém os valores dos campos
        const quantidadePaginas = parseFloat(quantidadePaginasInput.value) || 0;
        const custoPorPagina = parseFloat(custoPorPaginaInput.value) || 0;
        const custoDiagramacao = parseFloat(custoDiagramacaoInput.value) || 0;
        const diagramacaoAtiva = diagramacaoInput.checked; // Se o campo de diagramação estiver marcado

        // Calcula o preço base
        let total = quantidadePaginas * custoPorPagina;

        // Se a diagramação estiver ativada, adiciona o custo da diagramação
        if (diagramacaoAtiva) {
            total += custoDiagramacao;
        }

        // Atualiza a exibição do preço total no HTML
        precoOutput.textContent = total.toFixed(2); // Exibe o valor com duas casas decimais
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const tipoSelect = document.getElementById("tipo");
    const tabela = document.getElementById("resultadoTabela");
    const mediaPaginas = document.getElementById("mediaPaginas");
    const mediaCustoPagina = document.getElementById("mediaCustoPagina");
    const mediaDiagramacao = document.getElementById("mediaDiagramacao");
    const mediaTotal = document.getElementById("mediaTotal");
    const quantidade = document.getElementById("quantidade");

    tipoSelect.addEventListener("change", function () {
        const tipo = tipoSelect.value;

        if (tipo) {
            fetch(`/calcular-medias/?tipo=${tipo}`)
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error("Erro ao buscar os dados.");
                    }
                })
                .then((data) => {
                    tabela.style.display = "table";

                    mediaPaginas.textContent = data.media_paginas;
                    mediaCustoPagina.textContent = data.media_custo_pagina;
                    mediaDiagramacao.textContent = data.media_diagramacao;
                    mediaTotal.textContent = data.media_total;
                    quantidade.textContent = data.quantidade;
                })
                .catch((error) => {
                    alert(error.message);
                    tabela.style.display = "none";
                });
        } else {
            tabela.style.display = "none";
        }
    });
});