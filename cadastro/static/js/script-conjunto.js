async function chamarApi(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

async function addEtapa() {
    const container = document.getElementById('etapas-container');

    // Obtenha as opções do backend
    const data = await chamarApi('/api/etapas-choices/'); // Use 'await' para esperar a resposta

    // Construa as opções dinamicamente
    const destinoOptions = data.destino_choices.map(
        ([value, label]) => `<option value="${value}">${label}</option>`
    ).join('');

    const processoOptions = data.processo_choices.map(
        ([value, label]) => `<option value="${value}">${label}</option>`
    ).join('');

    const etapaHTML = `
        <div class="border rounded p-3 mb-3 bg-light position-relative etapa-item">
            <h5 class="mb-3">Nova Etapa</h5>
            <button type="button" class="btn-close position-absolute top-0 end-0" aria-label="Close" onclick="removeItem(this)"></button>
            <div class="row g-2 align-items-end">
                <div class="col-md-3">
                    <label for="descricao" class="form-label">Descrição:</label>
                    <input type="text" name="descricao" class="form-control mb-2">
                </div>
                <div class="col-md-3">
                    <label for="processo" class="form-label">Processo:</label>
                    <select name="processo" class="form-select mb-2">
                        ${processoOptions}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="destino" class="form-label">Destino:</label>
                    <select name="destino" class="form-select mb-2">
                        ${destinoOptions}
                    </select>
                </div>
                <div class="col-md-3">
                    <label for="desvio" class="form-label">Desvio:</label>
                    <select name="desvio" class="form-select mb-2">
                        <option value="almox_qualidade">Almox Qualidade</option>
                    </select>
                </div>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', etapaHTML);
}

async function addRecurso() {
    const container = document.getElementById('recursos-container');
    const recursoCount = container.querySelectorAll('.recurso-item').length; 

    const dataOrigem = await chamarApi('/api/etapas-choices/');

    const origemOptions = dataOrigem.destino_choices.map(
        ([value, label]) => `<option value="${value}">${label}</option>`
    ).join('');

    const recursoHTML = `
        <div class="border rounded p-3 mb-3 bg-light position-relative recurso-item">
            <h5 class="mb-3">Novo Recurso</h5>
            <button type="button" class="btn-close position-absolute top-0 end-0" aria-label="Close" onclick="removeItem(this)"></button>
            <div class="row g-2 align-items-end">
                <div class="col-md-4">
                    <label for="recurso_${recursoCount}" class="form-label">Recurso:</label>
                    <select id="recurso_${recursoCount}" name="recurso" class="form-select mb-2 recurso-select" required>
                        <!-- Options serão carregadas dinamicamente -->
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="quantidade_${recursoCount}" class="form-label">Quantidade:</label>
                    <input type="number" id="quantidade_${recursoCount}" name="quantidade" step="0.01" class="form-control mb-2" required>
                </div>
                <div class="col-md-4">
                    <label for="dep_origem_${recursoCount}" class="form-label">Depósito de Origem:</label>
                    <select id="dep_origem_${recursoCount}" name="dep_origem" class="form-select mb-2">
                        ${origemOptions}
                    </select>
                </div>
                <div class="col-md-4">
                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" 
                            id="flag_romaneio_${recursoCount}" 
                            name="flag_romaneio_${recursoCount}" 
                            value="on" 
                            data-group="group_${recursoCount}">
                        <label class="form-check-label" for="flag_romaneio_${recursoCount}">Flag Romaneio</label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" 
                            id="cx_acess_${recursoCount}" 
                            name="cx_acess_${recursoCount}" 
                            value="on" 
                            data-group="group_${recursoCount}">
                        <label class="form-check-label" for="cx_acess_${recursoCount}">Caixa de acessórios</label>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', recursoHTML);

    // Inicialize o Select2 com carregamento remoto
    const recursoSelect = container.querySelector('.recurso-item:last-child .recurso-select');
    $(recursoSelect).select2({
        theme: 'bootstrap-5',
        ajax: {
            url: '/api/recursos/', // Endpoint para buscar os recursos
            dataType: 'json',
            delay: 250, // Atraso para evitar muitas requisições
            data: function (params) {
                return {
                    search: params.term, // Termo digitado pelo usuário
                    page: params.page || 1 // Página atual para paginação
                };
            },
            processResults: function (data, params) {
                params.page = params.page || 1;

                return {
                    results: data.results.map(item => ({
                        id: item.id, // ID do recurso
                        text: item.id+" - "+item.label // Nome do recurso
                    })),
                    pagination: {
                        more: data.next // Indica se há mais páginas
                    }
                };
            },
            cache: true
        },
        placeholder: 'Selecione um recurso',
        minimumInputLength: 0, // Mostra os primeiros 10 itens ao abrir
        allowClear: true
    });
}

function addPropriedade() {
    const container = document.getElementById('propriedades-container');
    const propriedadeHTML = `
        <div class="border rounded p-3 mb-3 bg-light position-relative propriedade-item">
            <h5 class="mb-3">Nova Propriedade</h5>
            <button type="button" class="btn-close position-absolute top-0 end-0" aria-label="Close" onclick="removeItem(this)"></button>
            <div class="row g-2 align-items-end">
                <div class="col-md-6">
                    <label for="propriedade" class="form-label">Propriedade:</label>
                    <select name="propriedade" class="form-select mb-2">
                        <option value="comprimento">Comprimento</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label for="valor" class="form-label">Valor:</label>
                    <input type="number" name="valor" step="0.01" class="form-control mb-2">
                </div>
            </div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', propriedadeHTML);
}

// Função para remover um item
function removeItem(button) {
    button.parentElement.remove();
}

document.getElementById('formCadastrarConjunto').addEventListener('submit', async function (event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const submitButton = document.getElementById('submitConjunto');
    submitButton.innerText = 'Carregando...';
    submitButton.disabled = true; // Corrigido: 'disabled', não 'disable'

    const formData = new FormData(this); // Captura os dados do formulário padrão

    // Captura os dados dinâmicos
    const recursos = [];
    const recursoItems = document.querySelectorAll('.recurso-item');
    recursoItems.forEach((item, index) => {
        const recurso = item.querySelector(`[name="recurso"]`).value;
        const quantidade = item.querySelector(`[name="quantidade"]`).value;
        const depOrigem = item.querySelector(`[name="dep_origem"]`).value;
        const flagRomaneio = item.querySelector(`[name="flag_romaneio_${index}"]`).checked ? 'on' : 'off';
        const cxAcess = item.querySelector(`[name="cx_acess_${index}"]`).checked ? 'on' : 'off';

        recursos.push({ recurso, quantidade, depOrigem, flagRomaneio, cxAcess });
    });

    const etapas = [];
    const etapaItems = document.querySelectorAll('.etapa-item');
    etapaItems.forEach(item => {
        const descricao = item.querySelector('[name="descricao"]').value;
        const processo = item.querySelector('[name="processo"]').value;
        const destino = item.querySelector('[name="destino"]').value;
        const desvio = item.querySelector('[name="desvio"]').value;

        etapas.push({ descricao, processo, destino, desvio });
    });

    // Monta o payload para envio
    const payload = {
        codigo: formData.get('codigo'),
        nome: formData.get('nome'),
        classe: formData.get('classe'),
        recursos,
        etapas,
    };

    try {
        // Envia os dados via fetch
        const response = await fetch('/cadastrar-conjunto/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Adiciona o token CSRF
            },
            body: JSON.stringify(payload) // Envia os dados como JSON
        });

        if (response.ok) {
            const result = await response.json();
            Swal.fire({
                icon: 'success',
                title: 'Sucesso!',
                text: 'Dados enviados com sucesso!',
            }).then(() => {
                document.getElementById('formCadastrarConjunto').reset(); // Reseta o formulário
            });
        } else {
            const error = await response.json();
            Swal.fire({
                icon: 'error',
                title: 'Erro!',
                text: error.error || 'Erro ao enviar os dados.',
            });
            console.error(error);
        }
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Erro!',
            text: 'Erro na requisição. Verifique a conexão.',
        });
        console.error('Erro na requisição:', error);
    } finally {
        // Restaura o estado do botão após o envio
        submitButton.innerText = 'Salvar';
        submitButton.disabled = false;
    }

});

document.addEventListener('change', function (event) {
    if (event.target.matches('.form-check-input[data-group]')) {
        const group = event.target.getAttribute('data-group'); // Identifica o grupo
        const checkboxes = document.querySelectorAll(`.form-check-input[data-group="${group}"]`);

        checkboxes.forEach(checkbox => {
            if (checkbox !== event.target) {
                checkbox.checked = false; // Desmarca os outros checkboxes do grupo
            }
        });
    }
});
