# PROVA – Introdução à Programação (BIA) 
#**Nome completo:** João Guilherme Pires de Andrade  
#**Matrícula:** 202504010 
#**E-mail institucional:** andrade_pires@discente.ufg.br

# Questão 3

import pandas as pd
import numpy as np
import requests
from datetime import date, timedelta
# Montei meus dados de temperatura usando a API open meteo
# Com ela, peguei as temperaturas médias de goiânia em abril
# Formatei a data para que aparecesse somente o dia, na tabela

# Localização de Goiânia
latitude = -16.6864
longitude = -49.2643

# Mês de Abril
start_date = "2025-04-01"
end_date = "2025-04-30"

# Url da API (não precisa de chave)
# Aqui ela está configurada para ver a temperatura da cidade
url = "https://archive-api.open-meteo.com/v1/archive"
params={
    'latitude': latitude,
    'longitude': longitude,
    'current_weather': True,
    'start_date': start_date,
    'end_date': end_date,
    'daily': 'temperature_2m_mean',
    'timezone': 'America/Sao_Paulo'
}

# Pego esses dados com o requests e transformo em json
response =  requests.get(url, params=params)
data = response.json()

# Crio o DataFrame com as colunas certas e formatadas para 'DIA'
df = pd.DataFrame({
    "DIA": pd.to_datetime(data["daily"]["time"]).day,
    "TEMPERATURA": data["daily"]["temperature_2m_mean"]
})

# Aqui estão os comandos básicos de numpy, arredondados para uam casa decimal
print('='*80)
print('Relatório'.center(80))
print('='*80)
print(f'- A média de temperaturas, nesses 30 dias, é de {np.mean(df["TEMPERATURA"]):.1f}°C.')
print(f'- A mediana das temperaturas, nesses 30 dias, é de {np.median(df["TEMPERATURA"]):.1f}°C.')
print(f'- O desvio padrão de temperaturas, nesses 30 dias, é de {np.std(df["TEMPERATURA"]):.1f}')
print(f'- O índice de variação das temperaturas, nesses 30 dias, é de {(np.max(df["TEMPERATURA"]) - np.min(df["TEMPERATURA"])):.1f}')

# Aqui começa a manipulação dos dados do df

# Fiz a adição linha por linha para deixar claro o processo das alternativas b e c
df['DIFERENÇA PARA A MÉDIA']=(df['TEMPERATURA'] - np.mean(df['TEMPERATURA'])).round(1) # Adição da coluna a partir da diferença com a média

# Para fugir de gastar linhas com if e else, usei o .apply() para adicionar uma função lambda
# Que vai percorrer tudo bem mais diretamente e colocar na coluna nova
df['CLASSIFICAÇÃO TÉRMICA'] = df['TEMPERATURA'].apply(
    lambda i: 'Frio' if i < 18 else 'Agradável' if i <= 25 else 'Quente'
)

# Novamente, usei o .apply() para evitar as linhas de if e else, usando o lambda para criar uma função na mesma linha
df['SOBRE A MÉDIA'] = df['DIFERENÇA PARA A MÉDIA'].apply(
    lambda i: 'Acima da média' if i>0 else 'Exatamente na média' if i==0 else 'Abaixo da média'
)

# Aqui faço a contagem dos dias mais frios e dos dias mais quentes.

mais_frios = df.sort_values('TEMPERATURA', ascending=True).head(5)
mais_quentes = df.sort_values('TEMPERATURA', ascending=False).head(5)
# Pesquisando sobre Pandas, descobri esses comandos. O "sort_value" deixa a coluna em ordem crescente (True) ou decrescente (False)
# Com isso, pego os cinco primeiros itens de cada e armazeno nas variáveis!
resultadosQUENTE = ", ".join(f"{int(row.DIA)} ({row.TEMPERATURA}°C)" for _, row in mais_quentes.iterrows())
resultadosFRIO = ", ".join(f"{int(row.DIA)} ({row.TEMPERATURA}°C)" for _, row in mais_frios.iterrows())
print('- Os cinco dias mais quentes registrados são: ', resultadosQUENTE)
print('- Os cinco dias mais frios registrados são: ', resultadosFRIO)
# O comando "row" lê somente a linha da tabela, e o "for _" ignora o índice da linha.
# O join junta as informações do "for" no print após a vírgula.
print('='*80)

# Aqui mostro a tabela completa
print("\n", df)

print("\n- Não houveram dias 'Frios' na tabela.")
print("- Todos os dias 'Quentes' estavam acima da temperatura média.")