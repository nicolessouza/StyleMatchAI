from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def ranking(df_classificacao, df_img_embeddings, img_embedding):
    """
    Função que recebe df_classificacao, df_img_embeddings e o embedding da imagem e retorna um df ordenado por similaridade
    com o embedding da imagem
    """

    # Puxando os embeddings das imagens para df_classificacao
    df_classificacao = pd.merge(df_classificacao, df_img_embeddings, on='id_produto', how='inner')

    # Pegando as colunas que tem emb_img 
    emb_cols = [col for col in df_img_embeddings.columns if 'emb_img' in col]

    # Calcula a similaridade entre o embedding da imagem e os embeddings das imagens de df_classificacao
    sim = cosine_similarity(df_classificacao[emb_cols].values, img_embedding[emb_cols].values)
    
    # Adiciona a coluna de similaridade no df_img_embeddings
    df_classificacao['sim'] = sim
    
    # Ordena o df_classificacao por similaridade
    df_classificacao = df_classificacao.sort_values(by='sim', ascending=False)
    
    # Retorna o df_classificacao
    return df_classificacao