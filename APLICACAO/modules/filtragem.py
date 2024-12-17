import pandas as pd

def search_products (dict_busca, path_datasets, grupo_produto):
    # quais filtros foram selecionados? (filtar_por_{atributo} == True)
    filtros = [k for k, v in dict_busca.items() if 'filtrar_por_' in k and v == True]

    # replace filtrar_por por '' e transforma em lista
    filtros = [filtro.replace('filtrar_por_', '') for filtro in filtros]

    # Lendo df_classificacao
    df_classificacao = pd.read_parquet(f'{path_datasets}/df_classificacao.parquet')

    # Filtrando df_classificacao para o grupo de produto selecionado
    df_classificacao = df_classificacao[df_classificacao['grupo_produto'] == grupo_produto]
    
    print(f"linhas: {df_classificacao.shape[0]}")

    # Filtrando df_classificacao para que coincida com todos os filtros selecionados
    for filtro in filtros:
        print("filtrando por", filtro, " == ", dict_busca[filtro])
        df_classificacao = df_classificacao[df_classificacao[filtro] == dict_busca[filtro]]
        print(f"linhas: {df_classificacao.shape[0]}")

    
    # Tirando colunas completamente nulas
    df_classificacao = df_classificacao.dropna(axis=1, how='all')

    return df_classificacao