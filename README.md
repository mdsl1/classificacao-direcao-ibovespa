# Classificação da Direção Futura do Ibovespa

Projeto acadêmico de aprendizado de máquina para classificar se o
**Ibovespa estará em alta ou em queda daqui a cinco pregões**,
utilizando somente informações conhecidas até a data da previsão.

> **Status:** Em desenvolvimento\
> **Período dos dados:** 2010--2025\
> **Ativo:** Ibovespa (`^BVSP`)\
> **Frequência:** diária\
> **Horizonte de previsão:** 5 pregões

------------------------------------------------------------------------

## 1. Objetivo

O objetivo do projeto é desenvolver e avaliar modelos de **Aprendizado
de Máquina** capazes de classificar a direção futura do Ibovespa em um
horizonte de cinco pregões.

O problema será tratado como uma **classificação binária**:

-   **Alta**
-   **Queda**

A classificação será feita comparando o fechamento do Ibovespa na data
da previsão com o fechamento cinco pregões depois.

De forma simplificada:

``` text
Informações disponíveis até T
            ↓
          MODELO
            ↓
       Fechamento T+5
            ↓
      ┌───────────────┐
      │               │
      ↓               ↓
    ALTA           QUEDA
```

Exemplo:

``` text
Fechamento em T     = 150.000 pontos
Fechamento em T+5   = 152.000 pontos
Resultado           = ALTA
```

ou:

``` text
Fechamento em T     = 150.000 pontos
Fechamento em T+5   = 148.000 pontos
Resultado           = QUEDA
```

O projeto **não tem como objetivo prever exatamente o preço futuro do
Ibovespa**, mas sim classificar sua direção.

------------------------------------------------------------------------

# 2. Dados

### Ativo

-   **Nome:** Ibovespa
-   **Ticker:** `^BVSP`
-   **Mercado:** B3
-   **Frequência:** diária

### Período

-   **Início:** 2010
-   **Fim:** 2025

Os dados serão obtidos inicialmente por meio do Yahoo Finance.

------------------------------------------------------------------------

# 3. Problema de classificação

Para cada data `T`, o modelo receberá informações disponíveis até aquele
momento.

O alvo será determinado pelo comportamento do índice cinco pregões
depois:

``` text
Close(T+5) > Close(T) → ALTA
Close(T+5) < Close(T) → QUEDA
```

A definição exata do tratamento de eventuais casos em que os valores
sejam iguais deverá ser estabelecida durante a preparação dos dados.

### Regra fundamental

Nenhuma informação posterior à data `T` poderá ser utilizada como
variável de entrada para realizar a previsão.

Isso é essencial para evitar **vazamento de dados (data leakage)**.

------------------------------------------------------------------------

# 4. Modelos

Serão implementados e comparados três modelos de classificação:

1.  **Regressão Logística**
2.  **Árvore de Decisão**
3.  **Random Forest**

Além dos modelos de aprendizado de máquina, serão utilizados
**baselines** para estabelecer referências simples de desempenho.

------------------------------------------------------------------------

# 5. Estrutura do projeto

``` text
projeto_ibovespa/
│
├── .venv/
│
├── data/
│   ├── raw/
│   │   └── ibovespa_raw.csv
│   │
│   └── processed/
│       └── ibovespa_features.csv
│
├── notebooks/
│   ├── 01_coleta_dados.ipynb
│   ├── 02_exploracao_preparacao.ipynb
│   ├── 03_modelagem_avaliacao.ipynb
│   └── 04_resultados_artigo.ipynb
│
├── reports/
│   ├── figures/
│   │   ├── preco_ibovespa.png
│   │   ├── retornos_diarios.png
│   │   ├── distribuicao_target.png
│   │   └── ...
│   │
│   └── tables/
│       └── model_metrics.csv
│
├── src/
│
├── README.md
│
└── ...
```

------------------------------------------------------------------------

# 6. Ordem de execução

Os notebooks devem ser executados na seguinte ordem:

``` text
01_coleta_dados.ipynb
        ↓
02_exploracao_preparacao.ipynb
        ↓
03_modelagem_avaliacao.ipynb
        ↓
04_resultados_artigo.ipynb
```

Cada notebook possui uma responsabilidade específica e deve produzir os
arquivos necessários para a etapa seguinte.

------------------------------------------------------------------------

# 7. Responsabilidades dos notebooks

## 7.1 `01_coleta_dados.ipynb`

### Responsabilidades

1.  Baixar os dados históricos do Ibovespa.
2.  Verificar se os dados foram recebidos corretamente.
3.  Organizar as colunas.
4.  Realizar verificações básicas de qualidade.
5.  Salvar os dados brutos.

### Saída

``` text
data/raw/ibovespa_raw.csv
```

### Importante

Este notebook **não deve**:

-   criar indicadores;
-   calcular retornos;
-   criar o target;
-   treinar modelos.

Seu objetivo é somente obter e organizar a base de dados bruta.

------------------------------------------------------------------------

## 7.2 `02_exploracao_preparacao.ipynb`

### Responsabilidades

1.  Carregar o arquivo bruto.
2.  Verificar valores ausentes.
3.  Verificar registros duplicados.
4.  Realizar análise exploratória dos dados.
5.  Gerar gráficos exploratórios.
6.  Calcular retornos.
7.  Criar as características utilizadas pelos modelos.
8.  Criar o target de alta/queda em cinco pregões.
9.  Preparar o conjunto final de características.
10. Salvar o dataset processado.

### Saída

``` text
data/processed/ibovespa_features.csv
```

### Gráficos

Os gráficos produzidos devem ser salvos em:

``` text
reports/figures/
```

Exemplos:

``` text
reports/figures/preco_ibovespa.png
reports/figures/retornos_diarios.png
reports/figures/distribuicao_target.png
```

Outros gráficos poderão ser adicionados conforme a análise exploratória.

------------------------------------------------------------------------

## 7.3 `03_modelagem_avaliacao.ipynb`

### Responsabilidades

1.  Carregar o dataset processado.
2.  Separar os dados em treino, validação e teste.
3.  Criar os baselines.
4.  Treinar a Regressão Logística.
5.  Treinar a Árvore de Decisão.
6.  Treinar o Random Forest.
7.  Calcular as métricas de avaliação.
8.  Gerar matrizes de confusão.
9.  Comparar o desempenho dos modelos.
10. Salvar a tabela final de métricas.

### Saída

``` text
reports/tables/model_metrics.csv
```

### Estrutura esperada

  model                 balanced_accuracy   precision_up   recall_up   f1_up
  --------------------- ------------------- -------------- ----------- -------
  Majority              ...                 ...            ...         ...
  Persistence           ...                 ...            ...         ...
  Logistic Regression   ...                 ...            ...         ...
  Decision Tree         ...                 ...            ...         ...
  Random Forest         ...                 ...            ...         ...

Os nomes e métricas finais poderão ser ajustados durante a
implementação, caso seja metodologicamente mais adequado utilizar a
classe `Alta` em vez de `up`.

A avaliação deverá respeitar a **ordem temporal dos dados**.

------------------------------------------------------------------------

## 7.4 `04_resultados_artigo.ipynb`

### Responsabilidades

1.  Carregar as métricas já calculadas.
2.  Criar gráficos comparativos.
3.  Gerar análises de importância das variáveis.
4.  Selecionar resultados para o artigo.
5.  Analisar erros por período.
6.  Apoiar a elaboração da seção de resultados e discussão do artigo.

### Importante

Este notebook **não deve treinar novamente os modelos**.

Ele trabalha com os resultados já produzidos pelo notebook de modelagem.

------------------------------------------------------------------------

# 8. Características (features)

As variáveis de entrada serão construídas a partir das informações
históricas disponíveis até cada data de previsão.

Entre as possibilidades a serem avaliadas estão características
derivadas dos preços, como:

-   retornos;
-   retornos acumulados;
-   médias móveis;
-   diferenças entre preços e médias móveis;
-   indicadores relacionados ao comportamento recente do índice.

A lista definitiva de características será estabelecida durante a
exploração e preparação dos dados.

### Regra metodológica

Uma feature calculada para a data `T` deve utilizar somente informações
disponíveis até `T`.

Por exemplo:

``` text
Feature em T
    ↓
dados de T e anteriores
    ↓
NÃO utilizar dados de T+1, T+2, ... 
```

------------------------------------------------------------------------

# 9. Target

O target representa a direção do Ibovespa cinco pregões após a data da
previsão.

Para cada observação:

``` text
T
│
├── Informações históricas disponíveis
│
▼
MODELO
│
▼
T + 5 pregões
│
├── Close(T+5) > Close(T) → ALTA
│
└── Close(T+5) < Close(T) → QUEDA
```

O target será criado no notebook:

``` text
02_exploracao_preparacao.ipynb
```

As últimas observações da série, que não possuem cinco pregões futuros
para determinar o target, deverão ser tratadas adequadamente e não
poderão ser utilizadas como exemplos completos de treinamento/avaliação.

------------------------------------------------------------------------

# 10. Cuidados metodológicos

## 10.1 Evitar vazamento de dados

Este é um dos principais cuidados do projeto.

O modelo deve receber somente informações que estariam disponíveis no
momento em que a previsão fosse realizada.

Não podemos, por exemplo, utilizar o preço de `T+1` ou qualquer outra
informação futura para criar uma feature da data `T`.

------------------------------------------------------------------------

## 10.2 Respeitar a ordem temporal

Como estamos trabalhando com uma série temporal financeira, os dados não
devem ser embaralhados aleatoriamente para criar treino e teste.

A lógica deverá ser:

``` text
PASSADO
   ↓
TREINAMENTO
   ↓
VALIDAÇÃO
   ↓
FUTURO
   ↓
TESTE
```

A estratégia exata de divisão será definida durante a implementação do
notebook de modelagem.

------------------------------------------------------------------------

## 10.3 Separar preparação e modelagem

A preparação dos dados ocorre no notebook `02`.

O treinamento e a avaliação dos modelos ocorrem no notebook `03`.

Isso mantém o projeto organizado e facilita a reprodução dos
experimentos.

------------------------------------------------------------------------

# 11. Métricas

Os modelos serão avaliados utilizando métricas de classificação,
incluindo:

-   **Balanced Accuracy**
-   **Precision**
-   **Recall**
-   **F1-score**
-   **Matriz de confusão**

A avaliação não deverá depender somente de Accuracy, especialmente se as
classes `Alta` e `Queda` apresentarem distribuição desequilibrada.

------------------------------------------------------------------------

# 12. Baselines

Antes de avaliar os modelos de aprendizado de máquina, serão criados
modelos de referência simples (*baselines*).

O objetivo é responder:

> O modelo de aprendizado de máquina realmente apresenta desempenho
> superior a estratégias simples?

Os baselines previstos incluem:

-   **Majority:** sempre prever a classe mais frequente;
-   **Persistence:** utilizar uma estratégia baseada na direção
    observada anteriormente.

A implementação exata do baseline de persistência será definida de
acordo com a formulação final do problema.

------------------------------------------------------------------------

# 13. Ambiente de desenvolvimento

O projeto será desenvolvido localmente utilizando um ambiente virtual
Python.

### Ativar o ambiente virtual no PowerShell

``` powershell
.\.venv\Scripts\Activate.ps1
```

Após a ativação, o terminal deverá apresentar algo semelhante a:

``` text
(.venv) PS C:\caminho\do\projeto>
```

### Iniciar o Jupyter Lab

Com o ambiente virtual ativado:

``` powershell
jupyter lab
```

------------------------------------------------------------------------

# 14. Principais bibliotecas

As principais bibliotecas utilizadas no projeto serão:

-   **yfinance** --- obtenção dos dados históricos do Ibovespa;
-   **pandas** --- manipulação e análise dos dados;
-   **numpy** --- operações numéricas;
-   **matplotlib** --- visualização;
-   **seaborn** --- visualização estatística;
-   **scikit-learn** --- modelos de aprendizado de máquina e métricas;
-   **Jupyter Lab** --- desenvolvimento dos notebooks.

------------------------------------------------------------------------

# 15. Fluxo geral do projeto

``` text
                         DADOS
                           │
                           ▼
                    Yahoo Finance
                           │
                           ▼
               01_coleta_dados.ipynb
                           │
                           ▼
                  ibovespa_raw.csv
                           │
                           ▼
           02_exploracao_preparacao.ipynb
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          Características           Target
          (até T)              (direção em T+5)
                │                     │
                └──────────┬──────────┘
                           ▼
                ibovespa_features.csv
                           │
                           ▼
             03_modelagem_avaliacao.ipynb
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
            Logística   Árvore   Random Forest
                │          │          │
                └──────────┼──────────┘
                           ▼
                       Avaliação
                           │
                           ▼
                   model_metrics.csv
                           │
                           ▼
             04_resultados_artigo.ipynb
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
              Gráficos          Análises
                  │                 │
                  └────────┬────────┘
                           ▼
                    RESULTADOS DO
                        ARTIGO
```

------------------------------------------------------------------------

# 16. Status do projeto

### Planejamento

-   [x] Definição do problema
-   [x] Definição do ativo
-   [x] Definição do período
-   [x] Definição do horizonte de 5 pregões
-   [x] Definição dos modelos
-   [x] Definição da estrutura de notebooks
-   [x] Configuração do ambiente local

### Desenvolvimento

-   [ ] `01_coleta_dados.ipynb`
-   [ ] `02_exploracao_preparacao.ipynb`
-   [ ] `03_modelagem_avaliacao.ipynb`
-   [ ] `04_resultados_artigo.ipynb`

### Resultados

-   [ ] Dataset bruto
-   [ ] Dataset processado
-   [ ] Features definidas
-   [ ] Target definido
-   [ ] Baselines implementados
-   [ ] Modelos treinados
-   [ ] Métricas calculadas
-   [ ] Comparação dos modelos
-   [ ] Gráficos finais
-   [ ] Análise dos resultados
-   [ ] Resultados incorporados ao artigo

------------------------------------------------------------------------

## 17. Próximo passo

O desenvolvimento deve começar pelo notebook:

``` text
notebooks/01_coleta_dados.ipynb
```

A primeira etapa será obter os dados históricos do ticker:

``` text
^BVSP
```

e verificar se a base recebida corresponde ao período de **2010 a 2025**
antes de realizar qualquer transformação.
