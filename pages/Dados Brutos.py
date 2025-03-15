import streamlit as st
import pandas as pd
import requests

st.title('Dados Brutos')

url = 'https://labdados.com/produtos'

reponse = requests.get(url)
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

st.dataframe(dados)