import streamlit as st
import pandas as pd
import requests
from cogs import download

st.title('Dados Brutos')

url = 'https://labdados.com/produtos'

response = requests.get(url)

# Tratamento de erro da API 
if response.status_code != 200:
    st.error(f'Erro ao buscar os dados: {response.status_code}')
    st.stop()
try:
    dados = pd.DataFrame.from_dict(response.json())

except requests.exceptions.JSONDecodeError:
    st.error('Erro ao decodificar a resposta JSON. A API pode estar fora do ar')
    st.stop()

dados = pd.DataFrame.from_dict(reponse.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')

with st.sidebar.expander('Nome do Produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())

with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0, 5000))

with st.sidebar.expander('Data da Compra'):
    data_compra = st.sidebar.date_input('Selecione a Data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione o vendedor', dados['Vendedor'].unique(), dados['Vendedor'].unique())

with st.sidebar.expander('Local da Compra'):
    local = st.multiselect('Selecione o Estado', dados['Local da compra'].unique(), dados['Local da compra'].unique())

with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())

with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0,250, (0,250))

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra',1,5, value = (1,5))

with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento',dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())

with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1,24))

query = '''
Produto in @produtos and \
`Categoria do Produto` in @categoria and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedor and \
`Local da compra` in @local and \
@avaliacao[0]<= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
'''
dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas = :blue[{dados_filtrados.shape[1]}] colunas')

st.markdown('Escreva um nome para o arquivo')
coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value = 'dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Fazer o Download da Tabela em CSV', data = download.converte_csv(dados_filtrados), file_name= nome_arquivo, mime = 'text/csv', on_click = download.mensagem_sucesso)