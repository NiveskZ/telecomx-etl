# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %%
df = pd.read_csv('data/telecomx.csv')
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
fig.suptitle("Quantidade de usuários que deram Churn e não deram Churn por meses de contrato", fontsize=22)

sns.countplot(df, x='tenure', hue='Churn', palette='Set2',ax=ax)
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

g = sns.lmplot(df, x='tenure', y ='Charges_Total_Day',hue='Churn',col='Contract',
               col_order=["Month-to-month","One year","Two year"], palette='Set2')

g.figure.suptitle("Distribuição total gasto por dia e meses de contrato em relação ao tipo de Contrato",fontsize=16)
g.figure.subplots_adjust(top=0.85)

g.set_axis_labels("Tempo de Contrato (meses)", "Gasto Diário (R$)")
g._legend.set_bbox_to_anchor((1.05, 0.5))
g._legend.set_frame_on(False)

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
g.figure.suptitle("Distribuição total gasto por dia e meses de contrato em relação ao tipo de Pagamento",fontsize=16)
g.figure.subplots_adjust(top=0.85)

g.set_axis_labels("Meses de Contrato","Total Gasto por Dia")
g._legend.set_bbox_to_anchor((1.05, 0.5))
g._legend.set_frame_on(False)

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
# Fazendo análises através de matrizes de correlação.
cols_corr = ['n_servicos', 'Charges_Total_Day', 'tenure', 'Churn']
# Criando matriz de correlação
matriz_corr = df[cols_corr].corr()

# Cria uma Máscara para tirar a parte superior da matriz.
mask = np.triu(np.ones_like(matriz_corr,dtype=bool))
cmap = sns.diverging_palette(180,15,as_cmap=True)

# %%
fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(matriz_corr, mask=mask,cmap=cmap, vmax=0.3, center=0,
            square=True, linewidths=.5,cbar_kws={"shrink": .5},
            annot=True, fmt=".2f",ax=ax)

labels = ['Número de Serviços', 'Gasto total Diário', 'Tempo de Contrato','Churn']
tick_positions = np.arange(len(labels)) + 0.5

ax.set_title("Matriz de Correlação",fontsize=24,loc='left')
ax.set_xticks(tick_positions,
               labels=labels,
                rotation=45)
ax.set_yticks(tick_positions,
               labels=labels,
                rotation='horizontal')
plt.tight_layout
plt.show()
# %%
payment_dummies = pd.get_dummies(df['PaymentMethod'], prefix='pay', drop_first=False)
df_corr = pd.concat([payment_dummies,df[['Churn']]], axis=1)

matriz_corr = df_corr.corr()

mask = np.triu(np.ones_like(matriz_corr, dtype=bool))
# %%
fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(matriz_corr, mask=mask,cmap=cmap, vmax=0.3, center=0,
            square=True, linewidths=.5,cbar_kws={"shrink": .5},
            annot=True, fmt=".2f",ax=ax)

ax.set_title("Matriz de Correlação com Métodos de Pagamento",fontsize=24,loc='left')

labels = ['Boleto Bancário', 'Cartão de Crédito',
          'Cheque Eletrônico', 'Cheque Enviado','Churn']
tick_positions = np.arange(len(labels)) + 0.5

ax.set_xticks(tick_positions,
               labels=labels,
                rotation=45)
ax.set_yticks(tick_positions,
               labels=labels,
                rotation='horizontal')

plt.show()
# %%
