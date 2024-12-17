import pickle
import torch
from .utils import get_atributos_dict
import pandas as pd
from PIL import Image

def get_img_embedding(img, embedding_model):
    """
    Recebe uma imagem e um modelo de embedding e retorna um df com colunas emb_img_{i}
    onde i é o índice do vetor de embedding
    """
    
    # Transformar imagem em embedding
    img_emb = embedding_model.encode(img)

    # Criar DataFrame com embeddings
    df_img_emb = pd.DataFrame([img_emb], columns=[f'emb_img_{i}' for i in range(len(img_emb))])
    return df_img_emb


def get_loc_nos_subespacos(img_embedding, grupo_produto, datasets_path, models_path):
    """
    Recebe um embedding de imagem, um grupo de produto, o caminho para os datasets e o caminho para os modelos
    e retorna o local da imagem nos subespaços de cada atributo do grupo de produto (.transform nos modelos lda)
    """

    dict_atributos = get_atributos_dict(datasets_path)

    # Encontra os subespaços com base no grupo de produto
    atributos = dict_atributos[grupo_produto]

    loc_nos_subespacos = {}

    for atributo in atributos:
        # le os modelos usados pra gerar o subespaço de 'models_path/lda_model_{atributo}.pkl'
        lda_model = pickle.load(open(f'{models_path}/lda_model_{atributo}.pkl', 'rb'))

        # .transform(img_embedding) para encontrar a localização do ponto no subespaço
        loc_nos_subespacos[atributo] = lda_model.transform(img_embedding)

    return loc_nos_subespacos

def get_centroides_mais_proximos(loc_nos_subespacos, grupo_produto, datasets_path):
    """
    Recebe o local da imagem nos subespaços, um grupo de produto, o caminho para os datasets e o caminho para os modelos
    e retorna o centroide mais próximo da imagem
    """

    dict_atributos = get_atributos_dict(datasets_path)

    # Encontra os subespaços com base no grupo de produto
    atributos = dict_atributos[grupo_produto]

    centroide_mais_proximo = {}

    for atributo in atributos:
        # le os subespacos em 'datasets_path/df_subespace_{atributo}.parquet'
        subespaco = pd.read_parquet(f'{datasets_path}/df_subespace_{atributo}.parquet')

        # localização da imagem no subespaço
        loc_atributo = loc_nos_subespacos[atributo]

        # colunas lda
        colunas_lda = [f'EMB_LDA_{i}' for i in range(loc_atributo.shape[1])]

        # pegando os centroides
        centroides = subespaco.loc[subespaco['is_centroid'] == True]
        nomes_centroides = centroides['id_produto'].values
        centroides = centroides[colunas_lda].values

        # pegando as distâncias dos centroides
        centroides = torch.tensor(centroides, dtype=torch.float32)
        loc_atributo = torch.tensor(loc_atributo, dtype=torch.float32)

        euclidean_dist = torch.cdist(loc_atributo, centroides, p=2)

        # obtendo o centroide mais próximo
        centroide_mais_proximo[atributo] = nomes_centroides[euclidean_dist.argmin()]           

    return centroide_mais_proximo

def get_classificacao_img(img: Image, grupo_produto: str, datasets_path: str, models_path: str,  emb_model: object) -> dict:
    """
    Retorna a classificação da imagem.
    
    Args:
        img: Imagem a ser classificada.
        grupo_produto: Grupo de produto ao qual a imagem pertence.
        datasets_path: Caminho para a pasta onde estão os datasets.
        emb_model: Modelo de embedding a ser utilizado.

    Returns:
        dict: Dicionário contendo a classificação da imagem.

        output = {
        classificao: {atributo: valor},
        img_embedding: [array],
        loc_nos_subespacos: {nome do subespaco: array}
        }
    """

    # ETAPA 1: Embedding da imagem
    img_embedding = get_img_embedding(img, emb_model)

    # ETAPA 2: Pegando a localização da imagem em cada subespaço dado o grupo de produto
    loc_nos_subespacos = get_loc_nos_subespacos(img_embedding, grupo_produto, datasets_path, models_path)

    # ETAPA 3: Classificação da imagem
    classificacao = get_centroides_mais_proximos(loc_nos_subespacos, grupo_produto, datasets_path)

    # ----------------- Ajustes pontuais na saída -----------------

    # Ajustes pontuais na saída: classificacao_front
    classificacao_front = classificacao.copy()

    # Se estampado == CLUSTER_False, então estampa = 'LISO'
    if classificacao['estampado'] == 'CLUSTER_False':
        classificacao_front['estampa'] = 'liso'
        print("LISO")

    # Tirando chave estampado da classificação
    classificacao_front.pop('estampado')

    # Se grupo for 'vestido', ajustar atributos
    if grupo_produto == 'vestido':  
        # Ajustes nas mangas do vestido
        # Se possui manga, usa a manga
        if classificacao['vestido_contem_manga'] == 'CLUSTER_True':
            classificacao_front['vestido_tipo_manga'] = classificacao['vestido_comprimento_manga']
            print("COM MANGA")
        # Se não possui manga, mas possui alça, usa alça
        elif classificacao['vestido_contem_alca'] == 'CLUSTER_True':
            classificacao_front['vestido_tipo_manga'] = 'ALCA'
            print("ALCA")
        # Se não possui manga nem alça, então é sem manga
        elif classificacao['vestido_contem_manga'] == 'CLUSTER_False':
            classificacao_front['vestido_tipo_manga'] = 'SEM_MANGA'
            print("SEM MANGA")

        # Retirar atributo: vestido_comprimento_manga, vestido_contem_alca, vestido_contem_manga
        classificacao_front.pop('vestido_comprimento_manga')
        classificacao_front.pop('vestido_contem_alca')
        classificacao_front.pop('vestido_contem_manga')

        # --------------------------------------------------------

    output = {
        'classificacao': classificacao,
        'classificacao_front': classificacao_front,
        'img_embedding': img_embedding,
        'loc_nos_subespacos': loc_nos_subespacos
    }

    return output