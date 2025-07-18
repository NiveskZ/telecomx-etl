# %%
import requests
import pandas as pd
#%%
# Extração
# Solicitando os dados
url = 'https://raw.githubusercontent.com/ingridcristh/challenge2-data-science/refs/heads/main/TelecomX_Data.json'
response = requests.get(url)

# Transformando em objeto python
dados = response.json()

# Convertendo os dados em um DataFrame do Pandas
df = pd.json_normalize(dados)
df.head()
# %%
