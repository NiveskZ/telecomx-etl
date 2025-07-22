# %%
import requests
import numpy as np
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
# Avaliando Porcentagem de Churn 
cores = sns.color_palette('Set2')
fig, ax = plt.subplots(figsize=(10,6))

ax.pie(df['Churn'].value_counts(),
             labels=['Não', 'Sim'],
             autopct='%1.1f%%', explode=(0,0.1),colors=cores)
ax.set_title("Clientes que deram Churn X Clientes que não deram Churn")

plt.tight_layout()
plt.show()
# %%
fig, ax = plt.subplots(figsize=(15,5))
fig.suptitle("Quantidade de usuários que deram Churn e não deram Churn por meses de contrato")

sns.countplot(df, x='tenure', hue='Churn',ax=ax)
ax.set_xticks(range(0,df['tenure'].max(), 10))
ax.set_xlabel("Meses de Contrato")
ax.set_ylabel("Número de Usuários")

plt.tight_layout()
plt.show()
# %%
# Avaliando influência do preço de cobrança.
fig, axs = plt.subplots(2,2,figsize=(10,6))
fig.subplots_adjust(wspace=0.3,hspace=0.5)

sns.histplot(df,x='Charges_Total',hue='Churn',ax=axs[0,0],palette={0:'green',1:'blue'})
axs[0,0].set_title('Churn por total gasto')
axs[0,0].set_xlabel('Total Gasto Pelo Cliente')

sns.histplot(df,x='Charges_Day',hue='Churn',ax=axs[0,1],palette={0:'green',1:'blue'})
axs[0,1].set_title('Churn por total gasto diário')
axs[0,1].set_xlabel('Total Gasto Pelo Cliente por Dia')

sns.histplot(df,x='Charges_Monthly',hue='Churn',ax=axs[1,0],palette={0:'green',1:'blue'})
axs[1,0].set_title('Churn por gasto mensal')
axs[1,0].set_xlabel('Gasto Mensal do Cliente')

sns.histplot(df,x='Charges_Total_Day',hue='Churn',ax=axs[1,1],palette={0:'green',1:'blue'})
axs[1,1].set_title('Churn por gasto diário mensal')
axs[1,1].set_xlabel('Gasto Mensal do Cliente por Dia')

for ax in axs.ravel():
    ax.set_ylabel("Qtd. de Clientes")

plt.tight_layout()
plt.show()
# %%

# %%

g = sns.lmplot(df, x='Charges_Total', y ='Charges_Total_Day',hue='Churn',col='Contract',
               col_order=["Month-to-month","One year","Two year"], palette='Set2')

g.figure.suptitle("Relação entre Total Gasto e Total Gasto por Dia",fontsize=16)
g.figure.subplots_adjust(top=0.85)

plt.tight_layout()
plt.show()
# %%
fig, ax = plt.subplots(figsize=(10,6))
fig.suptitle("Quantidade de Churn X Forma de Pagamento")

sns.histplot(df,x='PaymentMethod', hue='Churn',palette={0:'green',1:'blue'},ax=ax)
ax.set_xlabel("Forma de Pagamento")
ax.set_ylabel("Número de Usuários")

plt.tight_layout()
plt.show()
# %%
# Calculando a taxa de churn por meses ativos
churn_tenure = df.groupby(['tenure','Churn']).size().unstack(fill_value=0)

churn_tenure['taxa_churn'] = (churn_tenure.get(1,0)/churn_tenure.sum(axis=1)) * 100

churn_tenure[['taxa_churn']]

churn_tenure.reset_index(inplace=True)
# %%

fig,ax = plt.subplots(figsize=(10,5))

sns.lineplot(data=churn_tenure,
             x='tenure',
             y='taxa_churn',
             ax=ax)

ax.set_title("Taxa de Churn por Total de Meses de Contrato do Cliente",loc='left',fontsize=16)
ax.set_xlabel("Meses de Contrato Ativo")
ax.set_ylabel("Taxa de Churn de cliente")

plt.tight_layout()
plt.show()
# %%
g = sns.lmplot(df, x='tenure', y ='Charges_Total_Day',hue='Churn',
               col='PaymentMethod',palette='Set2')
g.set_axis_labels("Meses de Contrato","Total Gasto por Dia")

plt.tight_layout()
plt.show()
# %%
fig, axs = plt.subplots(2,1,figsize=(6,8))
fig.subplots_adjust(hspace=0.3)

sns.boxplot(df,y='Charges_Total_Day',x='Churn', hue='Churn',
            palette='Set2',ax=axs[0])
axs[0].set_title("Distribuição do gasto diário por status de Churn")

sns.boxplot(df,y='Charges_Total_Day',
            x='Churn', hue='Contract',
            palette='Set2',
            ax=axs[1])
axs[1].set_title("Gasto diário por Churn e tipo de contrato")
axs[1].legend(title='Contrato', bbox_to_anchor=(1.05, 1), loc='upper left')

for ax in axs.ravel():

    ax.set_ylabel('Total Gasto Diário')

plt.tight_layout()
plt.show()
# %%
# Lista das colunas de serviço, incluindo a InternetService
servicos_cols = ['PhoneService','MultipleLines','InternetService',
                 'OnlineSecurity','OnlineBackup','DeviceProtection',
                 'TechSupport','StreamingTV','StreamingMovies']

# Criar cópia para não alterar o original
df_servicos = df[servicos_cols].copy()

# Para colunas binárias simples, mapeia Yes->1, No->0
binario_map = {'Yes':1, 'No':0}

for col in servicos_cols:
    if col == 'InternetService':
        # Considera que o cliente tem internet se o valor não for 'No'
        df_servicos[col] = df_servicos[col].apply(lambda x: 0 if x == 'No' else 1)
    else:
        df_servicos[col] = df_servicos[col].map(binario_map)

# Agora soma linha a linha para contar quantos serviços o cliente tem
df['n_servicos'] = df_servicos.sum(axis=1)
df.head()
# %%
corr = ['n_servicos',"Charges_Total_Day","tenure","Churn"]
matriz_corr = df[corr].corr()

mask = np.triu(np.ones_like(matriz_corr,dtype=bool))

fig, ax = plt.subplots(figsize=(11, 9))

cmap = sns.diverging_palette(180,15,as_cmap=True)

sns.heatmap(matriz_corr, mask=mask,cmap=cmap, vmax=0.3, center=0,
            square=True, linewidths=.5,cbar_kws={"shrink": .5},
            annot=True, fmt=".2f",ax=ax)

ax.set_title("Matriz de Correlação",fontsize=18,loc='left')
ax.set_xticks([0.5,1.5,2.5,3.5],
               labels=['Número de Serviços', 'Gasto total Diário', 'Tempo de Contrato','Churn'],
                rotation='horizontal')
ax.set_yticks([0.5,1.5,2.5,3.5],
               labels=['Número de Serviços', 'Gasto total Diário', 'Tempo de Contrato','Churn'],
                rotation='horizontal')
# %%
