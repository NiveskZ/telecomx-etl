# Challenge Telecom X: Análise de Evasão de Clientes
![Static Badge](https://img.shields.io/badge/status-complete-green)

Desafio promovido pela Oracle Next Education junto da Alura.

## Ferramentas utilizadas
- requests
- Python
- Pandas
- Numpy
- Matplotlib
- Seaborn

## Objetivos
Meu desafio aqui é agir como um assistente de análise de dados em um projeto de **Churn de Clientes** dentro da empresa Telecom X. Para isso irei aplicar os conceitos de ETL e fazer a Coleta, tratamento e análise dos dados.

### Extração dos Dados
Os dados foram importados da **API da Telecom X**, disponível em formato **JSON** [aqui](https://github.com/ingridcristh/challenge2-data-science/blob/main/TelecomX_Data.json)

Para entender as informações de cada coluna temos também o dicionario disponibilizado [aqui](https://github.com/ingridcristh/challenge2-data-science/blob/main/TelecomX_dicionario.md)

### Transformação dos Dados 
Como o objetivo da análise é prever o Churn de clientes, todas as transformações foram realizadas com essa variável em mente. Durante a etapa de exploração dos dados, foram identificadas as seguintes inconsistências:

- Valores vazios na coluna ```Churn```
- Valores vazios na coluna ```account.Charges.Total```
- A coluna ```account.Charges.Total``` estava com o tipo ```object``` ao invés de um tipo numérico (```float```)

Para o tratamento dessas inconsistências, foram avaliados os possíveis impactos de cada decisão.

No caso da coluna ```Churn``` , por se tratar da variável alvo da modelagem, não faria sentido manter registros com valores ausentes. Para garantir que a remoção dessas linhas não comprometesse a representatividade da base, foi calculado o percentual de perda, que foi de apenas 3%. Dado o baixo impacto, optou-se por eliminar essas observações.

Na coluna ```account.Charges.Total``` , inicialmente foi realizada a conversão do tipo ```object``` para ```float```. Em seguida, investigou-se a causa dos valores ausentes. Observou-se que todas as linhas com ```NaN``` nesta coluna apresentavam ```customer.tenure = 0```, o que sugere que se tratam de clientes recém-contratados que ainda não acumularam cobrança. Diante disso, optou-se por preencher esses valores com ```0```, facilitando visualizações e análises futuras sem distorcer os resultados. 

Foram convertidas para valores binários (0 e 1) todas as colunas que continham apenas as categorias "Yes" e "No". Colunas com valores adicionais como "No internet service" foram mantidas como categóricas, pois representam mais de duas classes distintas e requerem tratamento diferente na etapa de codificação. 

Como todas as colunas possuem diferenças bem definidas entre si, também foi normalizado os nomes, sendo removido os prefixos ```customer```,```phone```,```internet``` e ```account```.

Por fim, nessa etapa foi adicionada Três novas colunas:

- ```Charges_Day```: estimativa de custo diário com base no valor mensal (```account.Charges.Monthly```), garantindo que até mesmo clientes recentes sejam considerados nas comparações.
- ```Charges_Total_Day```: custo diário estimado a partir do total gasto (```account.Charges.Total```) dividido pelos dias correspondentes, permitindo comparações mais justas entre clientes com diferentes períodos de contrato.
- ```n_servicos```: Quantidade de serviços assinados pelo cliente.

### Carga e Análise

Tendo uma tabela final onde podemos trabalhar em cima para tirar insights, a primeira coisa feita foi analisar a taxa de churn em relação ao total para entendermos o quão grave é a situação.

![Clientes que deram Churn X Clientes que não deram Churn](https://raw.githubusercontent.com/NiveskZ/telecomx-etl/refs/heads/main/imgs/chrun-pie.png)

Como podemos ver, mais de 1/4 dos clientes deram Churn, o que é preocupante. Logo o próximo passo é tentar enteder possíveis causas para isso.

![Quantidade de usuários que deram Churn e não deram Churn por meses de contrato](https://raw.githubusercontent.com/NiveskZ/telecomx-etl/refs/heads/main/imgs/relacao-churn-tenure.png)

E avaliando a Taxa de cancelamento.

![Taxa de Churn por Total de Meses de Contrato do Cliente](https://github.com/NiveskZ/telecomx-etl/blob/main/imgs/taxa-churn-tenure.png?raw=true)

Nos gráficos acima conseguimos visualizar que boa parte dos clientes que dão Churn possuem uma quantidade menor de meses de contrato, já quem está mais tempo com a empresa tende a não fazer o cancelamento dos serviços. Vamos tentar averiguar se possui alguma relação com os gastos do cliente.

![Distribuição de total gasto por número de clientes](https://raw.githubusercontent.com/NiveskZ/telecomx-etl/refs/heads/main/imgs/influencia-gasto-cliente.png)

Apesar de Comportamentos similares, no primeiro gráfico (superior esquerdo) podemos notar que reforça nossa tese de clientes mais novos darem Churn com mais frequência, pois a maioria não passa de R$ 2000,00 Gasto durante todo o tempo de contrato com a empresa. Por outro lado, podemos notar que existe um descontentamento com o serviço, pois ao olhar pro gasto mensal o cliente costuma gastar entre 70-110 por mês antes de cancelar o contrato.

Além disso, podemos ver que ao analisar o gasto por dia ao longo do tempo, o valor mensal diferencia em relação ao valor total, o que demonstra uma possível diferença de perfil de cliente com tipos de contrato diferente.

![Relação entre Total Gasto e Total Gasto por Dia](https://raw.githubusercontent.com/NiveskZ/telecomx-etl/refs/heads/main/imgs/total-gasto-contrato.png)

Pela distribuição acima, fica claro que o Churn está muito relacionado com o valor dos serviços e também com o tipo de contrato, é muito mais comum ter Cancelamentos em contratos do tipo mensal.

Além disso, conseguimos notar uma relação entre os clientes mais velhos, estes ou consomem mais serviços ou estão dispostos a pagar mais caro para manter a fidelidade.

![Distribuição por gasto diário, status de churn e comparação por tipo de contrato](https://github.com/NiveskZ/telecomx-etl/blob/main/imgs/boxplot.png?raw=true)

Aqui confirma nossa hipótese de que uma média maior de gasto diário tem grande influência no cancelamento de serviços, porém também vemos que clientes com contrato mais longos tendem a dar Churn quando tem uma diferença muito maior no gasto diário em relação a quem não da Churn.

Por último, vamos avaliar se possui alguma influência relacionada ao método de pagamento
![Distribuição total gasto por dia e meses de contrato em relação ao tipo de Pagamento](https://github.com/NiveskZ/telecomx-etl/blob/main/imgs/total-gasto-tipo-pagamento.png?raw=true)

Apesar de trazer pouca informação, ele reforça que os valores precisam ser ajustados para contenção de clientes e demonstra que formas de pagamentos automáticos possuem clientes mais fiéis. Além disso, Cheques eletrônicos possui uma distribuição muito maior de clientes que cancelam o serviço. Isso pode se dar por fatores como:

- Cliente esquecer de renovar.
- Problemas de comunicação entre a empresa e o cliente.
- Dificuldades de acesso.

Talvez seja uma boa ideia entender possíveis problemas operacionais relacionadas a essa forma de pagamento. O gráfico abaixo reforça nossa tese:
![Quantidade de Churn X Forma de Pagamento](https://github.com/NiveskZ/telecomx-etl/blob/main/imgs/churn-tipo-pagamento.png?raw=true)

Olhando agora para matriz de correlação entre Churn, número de serviços do cliente, meses de contrato e Gasto total diário:
![Matriz de Correlação](https://github.com/NiveskZ/telecomx-etl/blob/main/imgs/matriz-corr.png?raw=true)

Realmente a maior relação com cancelamento de serviço é Gasto total diário, em contra partida vemos que quanto maior o tempo de contrato menor a chance de cancelamento. Vamos tentar visualizar a mesma coisa na forma de pagamento:

![Matriz de Correlação](https://github.com/NiveskZ/telecomx-etl/blob/main/imgs/corr-churn-pagamento.png?raw=true)

Observe que o Cheque eletrônico se destaca por muito, tendo uma alta relação com o Churn positivo, por outro lado, as outras formas de pagamento quase não tem relação.

### Conclusão

Tendo feitas todas as observações dessa análise, seria recomendado a empresa Telecom X tomar as seguintes medidas.

Em relação a forma de pagamento:

- Avaliar possiveis problemas em relação a forma de pagamento por Cheque eletrônico.
- Buscar feedbacks dos clientes sobre possiveis dificuldades na hora de pagar.
- Fazer propostas de pagamentos a longo prazo com descontos.

Em relação aos preços dos produtos:

- Reavaliar preços de custo e venda.
- Entender o perfil do público alvo e oferecer vantagens.
- Trazer promoções sedutoras, principalmente em planos anuais.

Note que o número de serviços usados pelo cliente tem pouca influência no cancelamento, então oferecer outros serviços da empresa como vantagens ou sob preços promocionais pode aumentar a retenção e garantir clientes fiéis.