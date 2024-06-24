import os
import pandas as pd
import sqlite3
from datetime import datetime
from io import StringIO

#Definir caminho do arquivo JSONL
jsonl_path = os.path.abspath('data/data.jsonl')

#Ler os dados do arquivo JSONL
with open(jsonl_path, 'r', encoding='utf-8') as file:
    jsonl_data = file.read()

df = pd.read_json(StringIO(jsonl_data), lines=True)

#Setar o Pandas para mostrar todas as colunas
pd.options.display.max_columns = None

#Adicionar a coluna _source com um valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/bicicleta-mtb#D[A:bicicleta%20mtb]"

#Adicionar a coluna _data_coleta com a data e hora atuais
df['_data_coleta'] = datetime.now()

#Tratar os valores nulos para colunas numéricas e de texto
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

#Remover os parênteses das colunas `reviews_amount`
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

#Tratar os preços como floats e calcular os valores totais
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

#Remover as colunas antigas de preços
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

#Conectar ao banco de dados SQLite
conn = sqlite3.connect('data/quotes.db')

#Salvar o DataFrame no banco de dados SQLite
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

#Fechar a conexão com o banco de dados
conn.close()

print(df.head())