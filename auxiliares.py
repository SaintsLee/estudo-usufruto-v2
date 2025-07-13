import pandas as pd
import streamlit as st
import gdown

# Armazenamento em cache da base de dados a ser apresentada no dashboard
@st.cache_data
def load_data():
    # ID do arquivo no Google Drive
    #file_id_1 = "1r9ZmWRLVhZhhjGrWO-u1U0rEdNkxK8JD"
    #url_1 = f"https://drive.google.com/uc?id={file_id_1}"
    ## Baixando o arquivo do Google Drive
    #output_1 = "dados_completos_brotli.parquet"
    #gdown.download(url_1, output_1, quiet=False)
    #dados_completos = pd.read_parquet(output_1)
    dados_completos = pd.read_parquet("carteiras.parquet")

    
    # ID do arquivo no Google Drive
    #file_id_2 = "1zeuirY7WnEAqSDiVCM0SK3ZTkG7W49li"
    #url_2 = f"https://drive.google.com/uc?id={file_id_2}"
    #
    ## Baixando o arquivo do Google Drive
    #output_2 = "dados_completos__retornos_brotli.parquet"
    #gdown.download(url_2, output_2, quiet=False)
    ## Carregar o arquivo no pandas
    #dados_completos_retornos = pd.read_parquet(output_2)
    dados_completos_retornos = pd.read_parquet("sobrevivencia.parquet")
    
    return dados_completos, dados_completos_retornos

# Armazenamento em cache da criação do dataframe ajustado para as carteiras
def apresenta_carteiras():
    # Quais carteiras estão sendo analisadas
    tipos_carteiras = ["Conservadora", "Moderada", "Arrojada", "Agressiva"]

    # Classes dos ativos de cada carteira
    classe_ativos_conservadora = ["Renda Fixa - CDI",
                                  "Renda Fixa - CDI"]

    classe_ativos_moderada = ["Renda Fixa - CDI",
                              "Renda Fixa - CDI",
                              "Renda Fixa - Inflação",
                              "Renda Fixa - Inflação",
                              "Renda Fixa - Pré",
                              "Renda Variável - Imobiliário"]

    classe_ativos_arrojada = ["Renda Fixa - CDI",
                              "Renda Fixa - CDI",
                              "Renda Fixa - Inflação",
                              "Renda Fixa - Inflação",
                              "Renda Fixa - Pré",
                              "Renda Variável - Imobiliário",
                              "Renda Variável - Ações BR",
                              "Renda Fixa - Exterior",
                              "Renda Fixa - Exterior",
                              "Renda Variável - Ações Global",
                              "Ouro"]

    classe_ativos_agressiva = ["Renda Fixa - CDI",
                               "Renda Fixa - CDI",
                               "Renda Fixa - Inflação",
                               "Renda Fixa - Inflação",
                               "Renda Fixa - Pré",
                               "Renda Variável - Imobiliário",
                               "Renda Variável - Ações BR",
                               "Renda Fixa - Exterior",
                               "Renda Fixa - Exterior",
                               "Renda Variável - Ações Global",
                               "Ouro"]

    # Pesos dos ativos de cada carteira
    pesos_carteira_conservadora = [0.3,
                                   0.7]

    pesos_carteira_moderada = [
                               0.4, 0.4, 0.15, 0.05]

    pesos_carteira_arrojada = [
                               0.25, 0.25, 0.15, 0.125, 0.025, 0.025, 0.10, 0.025, 0.05]

    pesos_carteira_agressiva = [
                               0.15, 0.15, 0.10, 0.25, 0.025, 0.025, 0.175, 0.025, 0.1]

    # Ativos de cada carteira
    ativos_carteira_conservadora = ["CDI",
                                    "TEVADI"]

    ativos_carteira_moderada = [
                                "TEVADI", "IMAB-5", "IFRM-P2", "IFIX"]

    ativos_carteira_arrojada = [
                                "TEVADI", "IMAB-5", "IFRM-P2", "IBRX", "BND", "BNDX",
                                "MSCI-World", "IAU", "IFIX"]

    ativos_carteira_agressiva = [
                                "TEVADI", "IMAB-5", "IFRM-P2", "IBRX", "BND", "BNDX",
                                "MSCI-World", "IAU", "IFIX"]

    # Colunas para o dataframe
    colunas_carteiras = ["Tipo", "Classe", "Ativos", "Pesos"]

    # Dados consolidados para o Treemap
    dados_consolidados_carteiras = [
        {
            colunas_carteiras[0]: tipos_carteiras[0],
            colunas_carteiras[1]: classe_ativos_conservadora,
            colunas_carteiras[2]: ativos_carteira_conservadora,
            colunas_carteiras[3]: pesos_carteira_conservadora
        },
        {
            colunas_carteiras[0]: tipos_carteiras[1],
            colunas_carteiras[1]: classe_ativos_moderada,
            colunas_carteiras[2]: ativos_carteira_moderada,
            colunas_carteiras[3]: pesos_carteira_moderada
        },
        {
            colunas_carteiras[0]: tipos_carteiras[2],
            colunas_carteiras[1]: classe_ativos_arrojada,
            colunas_carteiras[2]: ativos_carteira_arrojada,
            colunas_carteiras[3]: pesos_carteira_arrojada
        },
        {
            colunas_carteiras[0]: tipos_carteiras[3],
            colunas_carteiras[1]: classe_ativos_agressiva,
            colunas_carteiras[2]: ativos_carteira_agressiva,
            colunas_carteiras[3]: pesos_carteira_agressiva
        },
    ]

    linhas_aux = []
    for carteira in dados_consolidados_carteiras:
        tipo = carteira["Tipo"]
        for classe, ativo, peso in zip(carteira["Classe"], carteira["Ativos"], carteira["Pesos"]):
            linhas_aux.append({"Tipo": tipo, "Classe": classe, "Ativos": ativo, "Pesos": peso * 100})

    df_carteiras = pd.DataFrame(linhas_aux)

    # Definir a ordem personalizada para a coluna "Tipo"
    ordem_tipos = ["Conservadora", "Moderada", "Arrojada", "Agressiva"]
    df_carteiras["Tipo"] = pd.Categorical(df_carteiras["Tipo"], categories=ordem_tipos, ordered=True)

    df_carteiras["Risco"] = df_carteiras["Tipo"].apply(lambda x: 1 if x == "Conservadora" else
    2 if x == "Moderada" else
    3 if x == "Arrojada" else
    4)
    return df_carteiras
