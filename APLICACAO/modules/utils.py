import os

def get_atributos_dict(path: str) -> dict:
    """
    Função que retorna um dicionário com os atributos de cada grupo de produto

    Args:
        path (str): caminho para a pasta onde estão os datasets

    Returns:
        dict: dicionário com os atributos de cada grupo de produto
    """

    # Definindo grupos presentes na aplicação
    grupos = ['vestido', 'blusa', 'calca', 'saia', 'short']

    atributos = []

    # iterando sobre arquivos de datasets e pegando string 
    for file in os.listdir(path):
        if file.endswith('.parquet') and 'subespace_' in file:
            atributos.append(file.split('subespace_')[1].split('.')[0])

    # adicionando na chave '{grupo_produto} os atributos que começam com o nome do grupo de produto
    atributos_dict = {}

    for atributo in atributos:
        grupo_produto = atributo.split('_')[0]
        if grupo_produto in grupos:
            atributos_dict[grupo_produto] = (atributos_dict.get(grupo_produto, []) + [atributo])
        else:
            # Caso o atributo não comece com o nome de um grupo de produto, ele é adicionado a todos os grupos (ex: cor)
            for grupo in grupos:
                atributos_dict[grupo] = (atributos_dict.get(grupo, []) + [atributo])

    return atributos_dict