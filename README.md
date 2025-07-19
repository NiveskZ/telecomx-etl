# Challenge Telecom X: Análise de Evasão de Clientes
![Static Badge](https://img.shields.io/badge/status-em_desenvolvimento-blue)
Desafio promovido pela Oracle Next Education junto da Alura.

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

Por fim, nessa etapa foi adicionada duas novas colunas:

- ```account.Charges.Day```: estimativa de custo diário com base no valor mensal (```account.Charges.Monthly```), garantindo que até mesmo clientes recentes sejam considerados nas comparações.
- ```account.Charges.Total.Day```: custo diário estimado a partir do total gasto (```account.Charges.Total```) dividido pelos dias correspondentes, permitindo comparações mais justas entre clientes com diferentes períodos de contrato.

Foram convertidas para valores binários (0 e 1) todas as colunas que continham apenas as categorias "Yes" e "No". Colunas com valores adicionais como "No internet service" foram mantidas como categóricas, pois representam mais de duas classes distintas e requerem tratamento diferente na etapa de codificação. 

Como todas as colunas possuem diferenças bem definidas entre si, também foi normalizado os nomes, sendo removido os prefixos ```customer```,```phone```,```internet``` e ```account```