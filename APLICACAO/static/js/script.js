// criando variável global para armazenar o embedding da imagem
var img_embedding = null;

function uploadImage() {
    var fileInput = document.getElementById('imageInput');
    var formData = new FormData();
    var image = fileInput.files[0];

    // Adiciona a imagem ao formulário
    formData.append('image', image);
    // Adiciona o grupo selecionado ao formulário
    var grupo = document.getElementById('grupo_selecionado').value;
    formData.append('grupo_produto', grupo);

    // adiciona a imagem ao fundo do preview
    var imagePreview = document.getElementById('imagePreview');
    imagePreview.style.backgroundImage = `url(${URL.createObjectURL(image)})`;
    // add loading class
    imagePreview.classList.add('loading');
    document.getElementById('upload-image-text').textContent = 'Classificando produto...';

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
        img_embedding = data['img_embedding'];
        classificacao = data['classificacao_front']
        grupo_produto = data['grupo_produto'];
        croppedImageBase64 = data['image'];

        imagePreview = document.getElementById('cropped_image');
        imagePreview.style.backgroundImage = `url(data:image/png;base64,${croppedImageBase64})`;


        setTimeout(() => {
            // Remove a classe de loading
            document.getElementById('imagePreview').classList.remove('loading');
            document.getElementById('imagePreview').classList.add('image-uploaded');
            document.getElementById('upload-image-text').textContent = 'Mudar imagem';
        }, 100);


        // classificacao é um dicionário com cada classificacao de cada atributo do grupo
        let delay = 0; // Tempo inicial de delay
        Object.entries(classificacao).forEach(([atributo, valor]) => {
            setTimeout(() => {
                var checkbox = document.getElementById('filtrar_por_' + atributo);
                var select = document.getElementById('filtro_' + atributo);
        
                if (checkbox) {
                    // se o atributo tiver na lista negra nao marca o checkbox
                    var black_list = ['blusa_comprimento_blusa', 'vestido_decote_ou_gola', 'blusa_decote_ou_gola']

                    if (black_list.includes(atributo)) {
                        checkbox.checked = false;
                    } else {
                        checkbox.checked = true;
                    }
                }
                if (select) {
                    select.value = valor;
                }
            }, delay);

            delay += 500; // Incrementa o delay para o próximo atributo
        });   
        
        // Remove a classe disabled do botão de busca
        setTimeout(() => {
            var searchButton = document.getElementById('pesquisar_btn');
            searchButton.classList.remove('disabled');
        }, delay);

    });
}

function search() {
    var grupo = document.getElementById('grupo_selecionado').value;
    var sent_data = {};

    var filtros = document.getElementsByClassName("filtro_de_busca");

    for (var i = 0; i < filtros.length; i++) {
        if (filtros[i].type === 'checkbox') {
            sent_data[filtros[i].name] = filtros[i].checked;
        } else if (filtros[i].type === 'select-one' || filtros[i].type === 'text') {
            sent_data[filtros[i].name] = filtros[i].value;
        }
    }

    sent_data = {
        "query": sent_data,
        "img_embedding": img_embedding,
        "grupo_produto": grupo
    };

    // Tirar a classe hidden da div #results-section-container
    var resultsSectionContainer = document.getElementById('results-section-container');

    if (resultsSectionContainer.classList.contains('hidden')) {
        resultsSectionContainer.classList.remove('hidden');

    }


    console.log('Dados enviados:', sent_data);

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Especifica o tipo do conteúdo como JSON
        },
        body: JSON.stringify(sent_data) // Converte os dados para JSON antes de enviar
    }).then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
        var resultados = data['resultados'];

        // se resultados for uma lista vazia, retorna aviso
        if (resultados.length === 0) {
            console.log('Nenhum resultado encontrado');

            // alerta de que nenhum resultado foi encontrado
            window.alert('Nenhum resultado encontrado! Tente novamente com outros filtros');
        }

        

        var resultadosDiv = document.getElementById('resultsSection');
        resultadosDiv.innerHTML = '';
        // adicionando um atributo com o grupo para o valor dos resultados
        resultadosDiv.setAttribute('grupo', grupo);

        resultados.forEach(result => {
            var resultDiv = document.createElement('div');
            resultDiv.className = 'result';

            var img = document.createElement('img');
            img.src = result['link'];

            var info = document.createElement('div');
            info.className = 'info-produto';

            var id_produto = document.createElement('h5');
            id_produto.className = 'id_produto';
            id_produto.textContent = result['id_produto'];
            info.appendChild(id_produto);

            // para cada atributo dentro do resultado, criar um parágrafo com o nome do atributo e o valor
            Object.entries(result).forEach(([atributo, valor]) => {
                // inserir + uma verificao: se atributo nao conter 'emb'
                if (atributo !== 'id_produto' && atributo !== 'link' && !atributo.includes('emb') && !atributo.includes('sim')) {
                    var p = document.createElement('p');
                    p.textContent = atributo.replace('_', ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase()) + ': ' + valor;
                    info.appendChild(p);
                }
            });

            resultDiv.appendChild(img);
            resultDiv.appendChild(info);
            resultadosDiv.appendChild(resultDiv);

            // Scrolla para a seção de resultados
            resultsSectionContainer.scrollIntoView({behavior: "smooth"});
        });
    });
}

modelagem_atributos = {
    'blusa': {
        'blusa_comprimento_blusa': ['CURTA', 'LONGA', 'TOP'],
        'blusa_comprimento_manga': ['MANGA_LONGA', 'ALCA', 'SEM_MANGA', 'MANGA_MEDIA', 'MANGA_CURTA'],
        'blusa_decote': ['V', 'CORACAO', 'RETO', 'UM_OMBRO_SO', 'REDONDO', 'FRENTE_UNICA', 'OMBRO_A_OMBRO', 'TOMARA_QUE_CAIA', 'GOLA_ALTA', 'GOLA_POLO', 'DEGAGE'],
        },
    'calca': {
        'calca_comprimento_calca': ['CALCANHAR', 'CANELA'],
        'calca_modelagem_calca': ['PANTALONA', 'SOLTA', 'RETA', 'JUSTA', 'FLARE'],
        },
    'vestido': {
        'vestido_tipo_manga': ['MANGA_LONGA', 'ALCA', 'MANGA_CURTA', 'SEM_MANGA', 'MANGA_MEDIA'],
        'vestido_comprimento_saia': ['CURTA', 'MIDI', 'LONGA'],
        'vestido_decote_ou_gola': ['V', 'CORACAO', 'RETO', 'UM_OMBRO_SO', 'REDONDO', 'FRENTE_UNICA', 'OMBRO_A_OMBRO', 'TOMARA_QUE_CAIA'],
        'vestido_modelagem_saia': ['SOLTA', 'RETA', 'JUSTA'],
        },
    'saia': {
        'saia_comprimento_saia': ['CURTA', 'MIDI', 'LONGA'],
        'saia_modelagem_saia': ['RETA', 'SOLTA', 'JUSTA'],
        },
    'short': {
        'short_comprimento_short': ['LONGO', 'CURTO'],
        'short_modelagem_short': ['RETO', 'SOLTO'],
        }
    }

function updateAtributos() {
    var grupo = document.getElementById('grupo_selecionado').value;
    var atributos_modelagem = modelagem_atributos[grupo];

    var modelagemDiv = document.getElementById('pilar_modelagem');
    modelagemDiv.innerHTML = '<h4>Modelagem</h4>';

    // Para cada atributo da modelagem, criar um div com um checkbox e um select
    for (var atributo in atributos_modelagem) {
        // Criar o div do atributo
        var attributeDiv = document.createElement('div');
        attributeDiv.className = 'attribute';
        attributeDiv.id = 'atributo_' + atributo;

        // Criar o checkbox + select (o wrapper)
        var checkboxWrapper = document.createElement('div');
        checkboxWrapper.className = 'checkbox-wrapper-dramatico';
        
        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'filtrar_por_' + atributo;
        checkbox.name = 'filtrar_por_' + atributo;
        checkbox.className = 'filtro_de_busca';

        // Criar seletor de valores para o atributo
        var div_seletor = document.createElement('div');
        div_seletor.className = 'riscar_no_check';
        
        var select = document.createElement('select');
        select.name = atributo;
        select.id = 'filtro_' + atributo;
        select.className = 'filtro_de_busca';

        // Cria a opção com o nome do atributo
        var option = document.createElement('option');
        option.value = "qualquer";
        option.text = "Qualquer " + atributo.replace('_', ' ').toLowerCase();
        select.appendChild(option);

        for (var i = 0; i < atributos_modelagem[atributo].length; i++) {
            var option = document.createElement('option');
            option.value = atributos_modelagem[atributo][i];
            // Substitui o underline por espaço e deixa capitalizado
            option.text = atributos_modelagem[atributo][i].replace('_', ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
            select.appendChild(option);
        }

        div_seletor.appendChild(select);
        checkboxWrapper.appendChild(checkbox);
        checkboxWrapper.appendChild(div_seletor);
        attributeDiv.appendChild(checkboxWrapper);
        modelagemDiv.appendChild(attributeDiv);
    }
}

updateAtributos();
