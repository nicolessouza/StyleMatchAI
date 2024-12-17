from flask import Flask, request, render_template, jsonify, send_from_directory
from modules.classificacao import get_classificacao_img
from modules.segmentation import get_cropped_image_from_pil
from modules.ranking import ranking
from modules.filtragem import search_products
from transformers import pipeline
from PIL import Image
import base64
from io import BytesIO
import pandas as pd

app = Flask(__name__)

# Carregar o modelo SentenceTransformer para imagens
print('Carregando modelos...')
from sentence_transformers import SentenceTransformer, util
# We use the original clip-ViT-B-32 for encoding images
img_model = SentenceTransformer('clip-ViT-B-32')
pipe = pipeline("image-segmentation", model="sayeed99/segformer_b3_clothes")
print('Modelos carregados')

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')


def image_to_base64(image):
    """
    Converte uma imagem PIL para uma string Base64.
    
    Parâmetros:
        image (PIL.Image): A imagem que será convertida.
    
    Retorna:
        str: A string Base64 da imagem.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")  # Use PNG ou outro formato suportado
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def process_image(file, grupo_produto):
    # carregar a imagem
    img = Image.open(file)

    # Segmenta a imagem com base no grupo de produto
    cropped_image, bounding_box = get_cropped_image_from_pil(img, grupo_produto, pipe)

    # Classifica a imagem recortada
    classificacao = get_classificacao_img(
        img=cropped_image,
        grupo_produto=grupo_produto,
        datasets_path='./modules/datasets',
        models_path='./modules/models',
        emb_model=img_model
    )

    classificacao_back = classificacao['classificacao']
    classificacao_front = classificacao['classificacao_front']
    img_embedding = classificacao['img_embedding']

    # em todos os valores, apaga CLUSTER_ por ''
    for key, value in classificacao_front.items():
        classificacao_front[key] = value.replace('CLUSTER_', '')
    
    return {
        'classificacao_back': classificacao_back,
        'classificacao_front': classificacao_front,
        'image': image_to_base64(cropped_image),
        'img_embedding': img_embedding.values.tolist(),
        'grupo_produto': grupo_produto
    }
    

# Rota para o upload de imagens
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    grupo_produto = request.form['grupo_produto']
    if file:
        # Supõe que você tem uma função no seu módulo para processar a imagem
        # e retornar os atributos necessários como grupo de produto, cor, etc.
        
        return jsonify(process_image(file, grupo_produto))
    return jsonify({'error': 'Falha ao carregar a imagem'}), 400

# Rota para a busca de produtos
@app.route('/search', methods=['POST'])
def search():
    print("Requisição de busca recebida")
    data = request.get_json()  # Recebe o JSON do corpo da requisição
    grupo_produto = data['grupo_produto']
    query_dict = data['query']
    img_embedding = data['img_embedding'][0]
    
    # transformando img_embedding em dataframe com as colunas emb_img_{i}
    df_emb = pd.DataFrame([img_embedding], columns=[f'emb_img_{i}' for i in range(len(img_embedding))])
    
    # Procura os produtos
    produtos_encontrados = []
    df_classificacao = search_products(query_dict, './modules/datasets', grupo_produto)
    df_img_embeddings = pd.read_parquet('./modules/datasets/img_embeddings.parquet')

    # Quando df_classificao for vazio, retorna um aviso de que não foram encontrados produtos
    if df_classificacao.empty:
        return jsonify({
            'seu input': query_dict,
            'resultados': []
        })

    # Rankeia os produtos por similaridade de embedding
    df_classificacao_rankeada = ranking(df_classificacao, df_img_embeddings, df_emb)

    # transforma cada linha do dataframe em um dicionário de produto
    produtos_encontrados = []
    for index, row in df_classificacao_rankeada.iterrows():
        product = {}
        for column in df_classificacao_rankeada.columns:
            product[column] = row[column]
        produtos_encontrados.append(product)

        if len(produtos_encontrados) >= 15:
            break

    dict_resposta = {
        'seu input': query_dict,
        'resultados': produtos_encontrados
    }

    return jsonify(dict_resposta)

# Rota para servir arquivos CSS, JS e imagens de background
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
