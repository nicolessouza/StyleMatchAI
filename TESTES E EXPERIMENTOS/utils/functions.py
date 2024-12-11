from PIL import Image
from matplotlib import pyplot as plt
import pandas as pd
import torch
from sklearn.decomposition import PCA
import plotly.graph_objs as go
import random

# Dicionário de cores ajustado para cada valor de COR_PREDOMINANTE
color_dict = {
    'OFF WHITE': '#FFFFFF',       # Tom neutro claro
    'PRETO': '#000000',           # Preto puro
    'AZUL': '#1f77b4',            # Azul padrão
    'MULTICOLORIDO': '#808080',    # Cinza (para representar múltiplas cores de forma neutra)
    'VERDE': '#2ca02c',           # Verde padrão
    'ROSA': '#ff69b4',            # Rosa vibrante
    'BEGE': '#D2B48C',            # Bege suave
    'AMARELO': '#ffdd57',         # Amarelo claro
    'VERMELHO': '#d62728',        # Vermelho escuro
    'LARANJA': '#ff7f0e',         # Laranja padrão
    'LILÁS': '#dda0dd',           # Lilás suave
    'ROXO': '#9467bd',            # Roxo médio
    'BRANCO': '#FFFFFF',          # Branco puro
    'MARROM': '#8B4513',          # Marrom escuro
    'CINZA': '#808080',           # Cinza médio
    'VINHO': '#800000',           # Vinho escuro
    'DOURADO': '#FFD700',         # Dourado puro
    'JEANS': '#000080'            # Azul marinho
}


# Função que gera PCA para os embeddings
def apply_pca(embeddings, n_components=2, modelo_pca=None):
    """
    Função para gerar uma redução de dimensionalidade PCA para os embeddings.
    
    Args:
        embeddings (ndarray): Conjunto de embeddings.
        n_components (int): Número de componentes principais.
    
    Returns:
        PCA: Objeto PCA treinado.
        ndarray: Embeddings transformados.
    """
    if modelo_pca is not None:
        print("Usando modelo PCA fornecido.")
        return modelo_pca.transform(embeddings), modelo_pca
    else:
        # Inicializando e treinando o PCA
        print("Treinando um novo modelo PCA.")
        pca = PCA(n_components=n_components)
        embeddings_pca = pca.fit_transform(embeddings)
        return embeddings_pca, pca
    
def normalize_embeddings(embeddings_set1, embeddings_set2):
    """
    Normaliza os valores de embeddings_set1 para coincidir com o intervalo de embeddings_set2.
    
    Args:
        embeddings_set1 (ndarray): Embeddings que serão normalizados.
        embeddings_set2 (ndarray): Embeddings cujos intervalos serão usados como referência.
    
    Returns:
        ndarray: Embeddings_set1 normalizado.
    """
    embeddings_normalized = embeddings_set1.copy()
    for i in range(embeddings_normalized.shape[1]):
        min_value_set2 = embeddings_set2[:, i].min()
        max_value_set2 = embeddings_set2[:, i].max()
        min_value_set1 = embeddings_normalized[:, i].min()
        max_value_set1 = embeddings_normalized[:, i].max()
        
        embeddings_normalized[:, i] = (
            (embeddings_normalized[:, i] - min_value_set1) /
            (max_value_set1 - min_value_set1) *
            (max_value_set2 - min_value_set2) + min_value_set2
        )
    return embeddings_normalized


def find_top_similar(
    embeddings_set1,  # Primeiro conjunto de embeddings (ex.: roupas ou cores)
    embeddings_set2,  # Segundo conjunto de embeddings (ex.: roupas ou cores)
    n_top: int = 3  # Número de correspondências similares a retornar
):
    """
    Função para encontrar os índices e distâncias dos `n_top` embeddings mais similares para cada entrada em embeddings_set1.
    
    Args:
        embeddings_set1 (ndarray): Conjunto 1 de embeddings (ex.: roupas ou cores).
        embeddings_set2 (ndarray): Conjunto 2 de embeddings (ex.: roupas ou cores).
        normalize (bool): Indica se é necessário normalizar os embeddings.
        n_top (int): Número de top similares a serem retornados.
    
    Returns:
        list of tuples: Lista onde cada entrada é um tuple com:
                        - Índices dos `n_top` mais similares no embeddings_set2.
                        - Distâncias correspondentes dos `n_top` mais similares.
    """
    
    # Convertendo para tensores do PyTorch
    embeddings_set1 = torch.tensor(embeddings_set1, dtype=torch.float32)
    embeddings_set2 = torch.tensor(embeddings_set2, dtype=torch.float32)
    
    # Calculando a distância euclidiana
    euclidean_dist = torch.cdist(embeddings_set1, embeddings_set2, p=2)
    
    # Encontrando os índices e distâncias mais similares
    results = []
    for distances in euclidean_dist:
        if isinstance(distances, torch.Tensor):
            distances = distances.cpu().numpy()
        
        # Obter os `n_top` índices com menores distâncias
        sorted_indices = distances.argsort()[:n_top]
        sorted_distances = distances[sorted_indices]
        results.append((sorted_indices.tolist(), sorted_distances.tolist()))
    
    return results


def plot_image(image_path):
    """
    Plota uma imagem a partir de um caminho fornecido.
    """
    image = Image.open(image_path)
    plt.imshow(image)
    plt.axis('off')
    plt.show()

# Função para plotar os componentes reduzidos com cores definidas por um dicionário
def plot_cores(df, cor_column='COR_PREDOMINANTE', reducer='LDA', color_dict=None, show=True):
    """
    Plota os componentes reduzidos colorindo os pontos com base em um dicionário de cores.
    """

    # Setando componente x e y conforme o reducer
    component_x, component_y = f'EMB_{reducer}_0', f'EMB_{reducer}_1'

    # Filtrando apenas as linhas que possuem valores válidos (sem NaN) nos componentes
    df_plot = df.dropna(subset=[component_x, component_y, cor_column])

    # Se o dicionário de cores não for fornecido, gerar um dicionário de cores padrão
    if color_dict is None:
        unique_colors = df_plot[cor_column].unique()
        color_dict = {color: plt.cm.tab20(i / len(unique_colors)) for i, color in enumerate(unique_colors)}

    # Removendo linhas com cores não mapeadas no dicionário de cores
    df_plot = df_plot[df_plot[cor_column].isin(color_dict.keys())]

    # Iterar por cada cor e plotar os pontos
    for cor, color_value in color_dict.items():
        subset = df_plot[df_plot[cor_column] == cor]
        
        # Adicionar borda preta se a cor for branca
        edge_color = 'black' if color_value == '#FFFFFF' else color_value

        plt.scatter(
            subset[component_x],
            subset[component_y],
            color=color_value,
            edgecolor=edge_color,  # Define a cor da borda
            linewidth=0.5 if color_value in ['#FFFFFF', '#F8F4E3'] else 0,  # Define a largura da borda para pontos brancos
            alpha=0.7,
            label=cor
        )

    # Botando a legenda deslocada para fora do gráfico
    plt.legend(title="COR_PREDOMINANTE", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel(component_x)
    plt.ylabel(component_y)
    plt.title(f"Componentes {reducer} com cores de {cor_column}")
    if show:
        plt.show()

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from umap.umap_ import UMAP

# Função que aplica LDA: recebe um df, as colunas desse df que contêm os embeddings e o número de componentes que se deseja obter
def apply_lda(df, colunas, n_components=2, lda=None, column_target='COR_PREDOMINANTE'):
    """
    Aplica LDA nos embeddings para redução de dimensionalidade com base na coluna passada como target,
    ignorando valores nulos na coluna de target e retornando um novo DataFrame com as colunas desejadas.
    """
    df_filtered = df.copy()

    if not lda:
        # Inicializando o modelo LDA
        lda = LinearDiscriminantAnalysis(n_components=n_components)

        # Filtrando os dados para remover nulos na coluna 'COR_PREDOMINANTE'
        df_filtered = df_filtered.dropna(subset=[f'{column_target}'])

        # Treinando o modelo e transformando os dados
        componentes = lda.fit_transform(df_filtered[colunas], df_filtered[f'{column_target}'])

        # Criando um novo DataFrame com as colunas desejadas
        df_lda = df_filtered[['id_produto', f'{column_target}']].copy()

    else:
        componentes = lda.transform(df_filtered[colunas])

        # Criando um novo DataFrame com as colunas desejadas
        df_lda = df_filtered[['id_produto']].copy()

    for i in range(n_components):
        df_lda[f'EMB_LDA_{i}'] = componentes[:, i]

    return df_lda, lda

def apply_umap(df, colunas, n_components=2, umap=None):
    """
    Aplica UMAP nos embeddings para redução de dimensionalidade
    """

    if umap is None:
        # Removendo linhas com valores nulos para treinar o modelo

        # Inicializando o modelo t-SNE
        umap = UMAP(n_components=n_components, random_state=42)

        # Treinando o modelo e transformando os dados
        componentes = umap.fit_transform(df[colunas])

        # Criando um novo DataFrame com as colunas desejadas
        df_umap = df[['id_produto']].copy() 
    else:
        # Transformando os dados
        componentes = umap.transform(df[colunas])

        # Criando um novo DataFrame com as colunas desejadas
        df_umap = df[['id_produto']].copy()

    for i in range(n_components):
        df_umap[f'EMB_UMAP_{i}'] = componentes[:, i]

    return df_umap, umap

import plotly.graph_objects as go

def plot_clusters_with_centroids(
    df_combined, 
    target_column, 
    embedding_columns, 
    color_dict=None, 
    title="Visualização de Clusters com Centróides", 
    umap_params=None
):
    """
    Cria um gráfico de dispersão interativo com os clusters e seus centróides.
    
    Parâmetros:
    - df_combined: DataFrame contendo os dados originais e os centróides.
    - target_column: Nome da coluna que contém as categorias dos clusters.
    - embedding_columns: Lista com os nomes das colunas de embeddings.
    - color_dict: Dicionário com as cores específicas para cada categoria. Default: cores automáticas.
    - title: Título do gráfico. Default: "Visualização de Clusters com Centróides".
    - apply_umap: Booleano indicando se UMAP deve ser aplicado. Default: False.
    - umap_params: Dicionário com parâmetros para o UMAP. Default: None.
    
    Retorna:
    - Objeto Figure do Plotly.
    """
    # Aplicar UMAP se solicitado
    if apply_umap:
        umap_params = umap_params or {'n_neighbors': 15, 'n_components': 2, 'random_state': 42}
        umap = UMAP(**umap_params)
        
        embeddings = df_combined[embedding_columns].values
        umap_embeddings = umap.fit_transform(embeddings)

        # Adicionar os embeddings reduzidos ao DataFrame
        df_combined['UMAP_0'] = umap_embeddings[:, 0]
        df_combined['UMAP_1'] = umap_embeddings[:, 1]

        # Ajustar as colunas para o gráfico
        embedding_columns = ['UMAP_0', 'UMAP_1']

    # Separar dados originais e centróides
    df_original = df_combined[df_combined['is_centroid'] == False].copy()
    df_original['Tipo'] = 'Original'

    df_centroids = df_combined[df_combined['is_centroid'] == True].copy()
    df_centroids['Tipo'] = 'Centróide'

    # Gerar um dicionário de cores se não fornecido
    if color_dict is None:
        categorias = df_original[target_column].unique()
        # Setando paleta de cores do tableau
        color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
            '#ff9896', '#aec7e8', '#ffbb78', '#98df8a'
        ]
        color_dict = {categoria: color_palette[i % len(color_palette)] for i, categoria in enumerate(categorias)}

    # Criação do gráfico com Plotly
    fig = go.Figure()

    # Adicionar os pontos dos dados originais por categoria
    for categoria, cor in color_dict.items():
        subset = df_original[df_original[target_column] == categoria]
        fig.add_trace(go.Scatter(
            x=subset[embedding_columns[0]],
            y=subset[embedding_columns[1]],
            mode='markers',
            marker=dict(color=cor, size=8, line=dict(width=1, color='black')),
            name=f'{categoria}',
            hoverinfo='text',
            text=subset['id_produto']
        ))

    # Adicionar os centróides com cor fixa
    fig.add_trace(go.Scatter(
        x=df_centroids[embedding_columns[0]],
        y=df_centroids[embedding_columns[1]],
        mode='markers',
        marker=dict(color='red', symbol='x', size=10, line=dict(width=0.5)),
        name='Centróides',
        hoverinfo='text',
        text=df_centroids['id_produto']
    ))

    # Configuração do layout
    fig.update_layout(
        title=title,
        xaxis_title=f'{embedding_columns[0]}',
        yaxis_title=f'{embedding_columns[1]}',
        legend_title='Legenda',
        template='plotly_white',
        hovermode='closest'
    )

    # Mostrar o gráfico
    return fig

def calcular_centroides(df, colunas, target_column):
    """
    Calcula os centróides para cada categoria em 'target_column' com base nas colunas fornecidas.
    Retorna um DataFrame com os centróides e a categoria correspondente.
    """
    
    # 1. Calcular os centróides para cada {target_column}
    df_centroides = df.drop(columns={'id_produto'}).groupby(f'{target_column}').mean().reset_index()

    # 2. Adicionar a coluna 'id_produto' aos centróides
    df_centroides['id_produto'] = df_centroides[f'{target_column}'].apply(lambda x: f'CLUSTER_{x}')

    # 3. Adicionar uma coluna para identificar os centróides
    df_centroides['is_centroid'] = True
    
    df['is_centroid'] = False  # Para os dados originais

    # 4. Concatenar os dados originais com os centróides
    df_combined = pd.concat([df, df_centroides], ignore_index=True)

    return df_combined