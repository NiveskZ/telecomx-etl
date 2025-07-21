# %%
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
# Padronizando colunas binárias para 0 caso Não e 1 caso Sim

# Pega estritamente as colunas que tenham apenas valores "Yes" e "No"
cols_yes_no = [col for col in df.columns if df[col].isin(["Yes","No"]).all()] 

df[cols_yes_no] = df[cols_yes_no].replace({"Yes":1,"No":0})

df.head()
# %%
# Removendo prefixos dos nomes
df.rename(columns={
    col:col.split('.',1)[1].replace('.','_') for col in df.columns if '.' in col
}, inplace=True)
df.columns
# %%
# Carga e Análise
df.describe()
# %%
fig, ax = plt.subplots(figsize=(10,6))

ax.pie(df['Churn'].value_counts(),
             labels=['Não Deu Churn', 'Deu Churn'],
             autopct='%1.1f%%', explode=(0,0.1))
ax.set_title("Clientes que deram Churn X Clientes que não deram Churn")
# %%
df.head()
# %%
fig, ax = plt.subplots(figsize=(15,5))

ax = sns.countplot(df, x='tenure', hue='Churn')
ax.set_xticks(range(1,df['tenure'].max(), 10))

# %%
fig, axs = plt.subplots(2,2,figsize=(10,6))

sns.histplot(df,x='Charges_Total',hue='Churn',ax=axs[0,0])
sns.histplot(df,x='Charges_Day',hue='Churn',ax=axs[0,1])
sns.histplot(df,x='Charges_Monthly',hue='Churn',ax=axs[1,0])
sns.histplot(df,x='Charges_Total_Day',hue='Churn',ax=axs[1,1])
# %%
fig, axs = plt.subplots(2,2,figsize=(10,6))

sns.boxplot(df,y='Charges_Total',x='Churn',ax=axs[0,0])
sns.boxplot(df,y='Charges_Day',x='Churn',ax=axs[0,1])
sns.boxplot(df,y='Charges_Monthly',x='Churn',ax=axs[1,0])
sns.boxplot(df,y='Charges_Total_Day',x='Churn',ax=axs[1,1])
# %%
sns.lmplot(df, x='Charges_Total', y ='Charges_Total_Day',hue='Churn',col='Contract')
# %%
sns.lmplot(df, x='tenure', y ='Charges_Total_Day',hue='Churn',col='PaymentMethod')
# %%
