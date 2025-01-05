document.addEventListener('DOMContentLoaded', function () {
    const campoFiltro = document.getElementById('campoFiltro');
    const opcoesFiltro = document.getElementById('opcoesFiltro');
    const operadorFiltro = document.getElementById('operadorFiltro');
    const valorFiltroDiv = document.getElementById('valorFiltroDiv');
    const aplicarFiltro = document.getElementById('aplicarFiltro');
    
    // Função para mostrar/esconder os campos
    campoFiltro.addEventListener('change', function () {
        const campoSelecionado = campoFiltro.value;

        if (campoSelecionado === 'tipo' || campoSelecionado === '') {
            opcoesFiltro.style.display = 'none'; // Esconde o grupo de filtros
        } else {
            opcoesFiltro.style.display = 'block'; // Mostra o grupo de filtros
        }
    });

    // Função para aplicar o filtro
    aplicarFiltro.addEventListener('click', function () {
        const campo = campoFiltro.value;
        const operador = operadorFiltro.value;
        const valor = document.getElementById('valorFiltro').value;

        if (!campo) {
            alert('Por favor, selecione um campo para filtrar.');
            return;
        }

        let url = new URL(window.location.href);
        url.searchParams.set('campo', campo);

        if (campo !== 'tipo') {
            url.searchParams.set('operador', operador);
            url.searchParams.set('valor', valor);
        }

        window.location.href = url.toString();
    });

    // Dispara o evento change para ajustar a exibição inicial ao carregar a página
    campoFiltro.dispatchEvent(new Event('change'));
});