document.getElementById('formCadastrarClasse').addEventListener('submit', async (event) => {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const url = "{% url 'cadastrar_classe' %}";

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}', // Certifique-se de que o token CSRF é gerado corretamente
            },
            body: formData, // Envia os dados como multipart/form-data
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('responseMessage').textContent = 'Formulário enviado com sucesso!';
        } else {
            document.getElementById('responseMessage').textContent = `Erro: ${data.error || 'Algo deu errado.'}`;
        }
    } catch (error) {
        document.getElementById('responseMessage').textContent = 'Erro de conexão.';
    }
});
