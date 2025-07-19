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
# Transformação
# Verificando os tipos de dados
df.info()
# %%
# Verificando se possui valores nulos
df.isnull().sum()
# %%
# Verificando se possui valores vazios em alguma coluna.
for col in df.columns:
    print(f"Valores únicos em {col}: {df[col].nunique()}")
    if df[col].nunique() < 10:
        print(df[col].unique())
        print("\n")
# %%
# Contando os valorez vazios.
vazios = df.apply(lambda x: x.astype(str).str.strip() == '').sum()
vazios
# %%
# Calculando Potencial de informação perdida ao remover linhas com churn vazio
print(f"Porcentagem churn vazio: {round(vazios['Churn']/len(df),2)*100}%")
# %%
# Removendo as linhas com Churn vazio
df = df[df['Churn'].str.strip() != '']
len(df)
# %%
# Transformando a coluna "account.Charges.Total" em float e verificando se ainda possui nulos/vazios
df['account.Charges.Total'] = pd.to_numeric(df['account.Charges.Total'],errors='coerce')
total_null = df['account.Charges.Total'].isnull()
total_null.sum()
# %%
# Observando se existe relação onde tenure = 0 com cobrança total nula
(df[total_null]['customer.tenure'] == 0).all()
# %%
# Podemos supor que por se tratar de clientes novos ainda não possuem cobranças
df['account.Charges.Total'] = df['account.Charges.Total'].fillna(0.)
#%%
# Verificando se possui linhas duplicadas
df.duplicated().sum()

# %%
# Criando coluna de contas diárias considerando as cobranças mensais do cliente
df["account.Charges.Day"] = ((df['account.Charges.Monthly'])/30).round(2)

# Criando coluna de contas diárias considerando todas as cobranças do cliente
df["account.Charges.Total.Day"] = ((df['account.Charges.Total']/df['customer.tenure'])/30).round(2)

df.head()
# %%
