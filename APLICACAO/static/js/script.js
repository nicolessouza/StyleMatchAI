function uploadImage() {
    var fileInput = document.getElementById('imageInput');
    var formData = new FormData();
    formData.append('image', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        document.getElementById('productGroup').textContent = data.grupo_produto;
        document.getElementById('color').textContent = data.cor;
        document.getElementById('pattern').textContent = data.estampa;
        document.getElementById('fit').textContent = data.modelagem;
        document.getElementById('productAttributes').classList.remove('hidden');
    });
}

function search() {
    var filtro_grupo = document.getElementById('filtro_grupo').value;
    var filtrar_por_grupo = document.getElementById('filtrar_por_grupo').checked;

    const queryDict = {
        "filtro_grupo": filtro_grupo,
        "filtrar_por_grupo": filtrar_por_grupo
    };
    // Fazer a requisição com o método POST
    fetch('/search', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(queryDict),  // Envia o JSON no corpo da requisição
    })
    .then(response => response.json())  // Parse da resposta para JSON
    .then(data => {
        // O que fazer quando a resposta foi recebida
        console.log('Resposta do servidor:', data);
    })
    .catch(error => {
        console.error('Erro ao fazer a busca:', error);
    });
}