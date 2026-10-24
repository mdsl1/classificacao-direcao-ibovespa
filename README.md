# Classificação da Direção Futura do Ibovespa

Projeto acadêmico de aprendizado de máquina para classificar se o **Ibovespa estará em alta ou em queda daqui a cinco pregões**, utilizando somente informações conhecidas até a data da previsão.

> **Status:** Em desenvolvimento — etapas de coleta e preparação concluídas  
> **Período dos dados:** 2010–2025  
> **Ativo:** Ibovespa (`^BVSP`)  
> **Frequência:** diária  
> **Horizonte de previsão:** 5 pregões

---

# 1. Objetivo

O objetivo do projeto é desenvolver e avaliar modelos de **Aprendizado de Máquina** capazes de classificar a direção futura do Ibovespa em um horizonte de cinco pregões.

O problema será tratado como uma **classificação binária**:

- **Alta**
- **Queda**

A classificação é realizada comparando o fechamento do Ibovespa na data da previsão com o fechamento cinco pregões depois.

De forma simplificada:

```text
Informações disponíveis até T
            ↓
         MODELO
            ↓
       Fechamento T+5
            ↓
      ┌─────┴─────┐
      ↓           ↓
    ALTA        QUEDA
```

Exemplo:

```text
Fechamento em T     = 150.000 pontos
Fechamento em T+5   = 152.000 pontos
Resultado           = ALTA
```

ou:

```text
Fechamento em T     = 150.000 pontos
Fechamento em T+5   = 148.000 pontos
Resultado           = QUEDA
```

O projeto **não tem como objetivo prever exatamente o preço futuro do Ibovespa**, mas sim classificar sua direção.

---

# 2. Dados

## Ativo

- **Nome:** Ibovespa
- **Ticker:** `^BVSP`
- **Mercado:** B3
- **Frequência:** diária

## Período

- **Início:** 2010-01-04
- **Fim:** 2025-12-30

Os dados são obtidos por meio do Yahoo Finance utilizando a biblioteca `yfinance`.

## Dataset bruto

O dataset coletado possui:

- **3.965 pregões**
- **7 colunas**
- Nenhum valor ausente
- Nenhuma data duplicada

Colunas:

```text
Date
Open
High
Low
Close
Adj Close
Volume
```

O dataset bruto é armazenado em:

```text
data/raw/ibovespa_raw.csv
```

---

# 3. Problema de classificação

Para cada data `T`, o modelo recebe somente informações disponíveis até aquele momento.

O alvo é determinado pelo comportamento do índice cinco pregões depois:

```text
Close(T+5) > Close(T) → ALTA
Close(T+5) < Close(T) → QUEDA
```

Os cinco últimos registros da série não possuem cinco pregões futuros disponíveis e, portanto, não podem ser utilizados como exemplos completos para treinamento ou avaliação.

Até o momento, não foram encontrados casos em que:

```text
Close(T+5) == Close(T)
```

Portanto, não foi necessário criar uma terceira classe para empates.

### Regra fundamental

Nenhuma informação posterior à data `T` pode ser utilizada como variável de entrada para realizar a previsão.

Isso é essencial para evitar **vazamento de dados (data leakage)**.

---

# 4. Modelos

Serão implementados e comparados três modelos de classificação:

1. **Regressão Logística**
2. **Árvore de Decisão**
3. **Random Forest**

Além dos modelos de aprendizado de máquina, serão utilizados **baselines** para estabelecer referências simples de desempenho.

Os baselines previstos são:

- **Majority:** sempre prever a classe mais frequente;
- **Persistence:** utilizar uma estratégia baseada na direção observada anteriormente.

A implementação dos baselines será realizada durante a etapa de modelagem.

---

# 5. Estrutura do projeto

```text
classificacao-volatibilidade-ibovespa/
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
│   │   ├── evolucao_ibovespa.png
│   │   ├── distribuicao_retornos_diarios.png
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

---

# 6. Ordem de execução

Os notebooks devem ser executados na seguinte ordem:

```text
01_coleta_dados.ipynb
        ↓
02_exploracao_preparacao.ipynb
        ↓
03_modelagem_avaliacao.ipynb
        ↓
04_resultados_artigo.ipynb
```

Cada notebook possui uma responsabilidade específica e deve produzir os arquivos necessários para a etapa seguinte.

---

# 7. Responsabilidades dos notebooks

## 7.1 `01_coleta_dados.ipynb`

### Status: CONCLUÍDO

### Responsabilidades

1. Baixar os dados históricos do Ibovespa.
2. Verificar se os dados foram recebidos corretamente.
3. Organizar as colunas.
4. Realizar verificações básicas de qualidade.
5. Salvar os dados brutos.

### Validações realizadas

```text
Quantidade de registros: 3965
Data inicial: 2010-01-04
Data final: 2025-12-30
Valores ausentes: 0
Duplicatas: 0
```

### Saída

```text
data/raw/ibovespa_raw.csv
```

### Importante

Este notebook não cria indicadores, não cria o target e não treina modelos.

Seu objetivo é somente obter e organizar a base de dados bruta.

---

# 7.2 `02_exploracao_preparacao.ipynb`

### Status: CONCLUÍDO

### Responsabilidades

1. Carregar o arquivo bruto.
2. Verificar valores ausentes.
3. Verificar registros duplicados.
4. Realizar análise exploratória dos dados.
5. Gerar gráficos exploratórios.
6. Calcular retornos.
7. Criar as características utilizadas pelos modelos.
8. Criar o target de alta/queda em cinco pregões.
9. Preparar o conjunto final de características.
10. Salvar o dataset processado.

### Features atuais

A base preparada possui as seguintes variáveis explicativas:

```text
Retorno_Diario
Retorno_5d
Retorno_10d
Media_Retorno_5d
Volatilidade_5d
Variacao_Intradiaria
Amplitude_Diaria
```

Todas as features são calculadas utilizando somente informações disponíveis até a data `T`.

### Target

```text
Direcao_Futura
```

Definição:

```text
0 → QUEDA
1 → ALTA
```

### Resultado da preparação

Dataset final:

```text
3.950 observações
8 colunas de dados + Date
7 features
1 target
```

Distribuição das classes:

```text
ALTA   → 2.082 observações (52,71%)
QUEDA  → 1.868 observações (47,29%)
```

A distribuição é relativamente equilibrada, não sendo necessário aplicar técnicas específicas de balanceamento neste momento.

### Validações realizadas

```text
Valores ausentes: 0
Valores infinitos: 0
```

### Saída

```text
data/processed/ibovespa_features.csv
```

### Gráficos

Os gráficos produzidos são armazenados em:

```text
reports/figures/
```

Entre os gráficos produzidos estão:

```text
evolucao_ibovespa.png
distribuicao_retornos_diarios.png
distribuicao_target.png
```

---

# 7.3 `03_modelagem_avaliacao.ipynb`

### Status: PRÓXIMA ETAPA

### Responsabilidades

1. Carregar o dataset processado.
2. Separar os dados em treino, validação e teste.
3. Criar os baselines.
4. Treinar a Regressão Logística.
5. Treinar a Árvore de Decisão.
6. Treinar o Random Forest.
7. Calcular as métricas de avaliação.
8. Gerar matrizes de confusão.
9. Comparar o desempenho dos modelos.
10. Salvar a tabela final de métricas.

### Cuidados importantes

Como o projeto utiliza uma série temporal financeira, a divisão dos dados deverá respeitar a ordem cronológica.

A lógica será:

```text
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

Os dados não deverão ser embaralhados aleatoriamente entre treino e teste.

### Métricas previstas

- **Balanced Accuracy**
- **Precision**
- **Recall**
- **F1-score**
- **Matriz de confusão**

### Saída esperada

```text
reports/tables/model_metrics.csv
```

Estrutura prevista:

| Model | Balanced Accuracy | Precision High | Recall High | F1 High |
|---|---:|---:|---:|---:|
| Majority | ... | ... | ... | ... |
| Persistence | ... | ... | ... | ... |
| Logistic Regression | ... | ... | ... | ... |
| Decision Tree | ... | ... | ... | ... |
| Random Forest | ... | ... | ... | ... |

---

# 7.4 `04_resultados_artigo.ipynb`

### Status: PENDENTE

### Responsabilidades

1. Carregar as métricas já calculadas.
2. Criar gráficos comparativos.
3. Gerar análises de importância das variáveis.
4. Selecionar resultados para o artigo.
5. Analisar erros por período.
6. Apoiar a elaboração da seção de resultados e discussão do artigo.

### Importante

Este notebook **não deve treinar novamente os modelos**.

Ele trabalha com os resultados já produzidos pelo notebook de modelagem.

---

# 8. Características (features)

As variáveis de entrada foram construídas a partir das informações históricas disponíveis até cada data de previsão.

## Features atuais

### `Retorno_Diario`

Variação percentual do fechamento em relação ao pregão anterior.

### `Retorno_5d`

Variação percentual do fechamento em relação ao fechamento de cinco pregões anteriores.

### `Retorno_10d`

Variação percentual do fechamento em relação ao fechamento de dez pregões anteriores.

### `Media_Retorno_5d`

Média dos retornos diários dos cinco pregões anteriores.

### `Volatilidade_5d`

Desvio padrão dos retornos diários dos cinco pregões anteriores.

### `Variacao_Intradiaria`

Variação percentual entre a abertura e o fechamento do próprio pregão.

### `Amplitude_Diaria`

Variação percentual entre a mínima e a máxima do próprio pregão.

### Regra metodológica

Uma feature calculada para a data `T` deve utilizar somente informações disponíveis até `T`.

```text
Feature em T
    ↓
Dados de T e anteriores
    ↓
NÃO utilizar dados de T+1, T+2, ...
```

---

# 9. Target

O target representa a direção do Ibovespa cinco pregões após a data da previsão.

Para cada observação:

```text
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

O target é criado no notebook:

```text
02_exploracao_preparacao.ipynb
```

As últimas cinco observações da série não possuem cinco pregões futuros para determinar o target e, portanto, são excluídas da base final.

---

# 10. Cuidados metodológicos

## 10.1 Evitar vazamento de dados

Este é um dos principais cuidados do projeto.

O modelo deve receber somente informações que estariam disponíveis no momento em que a previsão fosse realizada.

Não podemos, por exemplo, utilizar o preço de `T+1` ou qualquer outra informação futura para criar uma feature da data `T`.

---

## 10.2 Respeitar a ordem temporal

Como estamos trabalhando com uma série temporal financeira, os dados não devem ser embaralhados aleatoriamente para criar treino e teste.

A lógica deverá ser:

```text
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

A estratégia exata de divisão será definida durante a implementação do notebook de modelagem.

---

## 10.3 Separar preparação e modelagem

A preparação dos dados ocorre no notebook `02`.

O treinamento e a avaliação dos modelos ocorrerão no notebook `03`.

Isso mantém o projeto organizado e facilita a reprodução dos experimentos.

---

# 11. Métricas

Os modelos serão avaliados utilizando métricas de classificação, incluindo:

- **Balanced Accuracy**
- **Precision**
- **Recall**
- **F1-score**
- **Matriz de confusão**

A avaliação não deverá depender somente de Accuracy.

A distribuição atual das classes é:

```text
ALTA   → 52,71%
QUEDA  → 47,29%
```

O desempenho dos modelos deverá ser comparado também com os baselines.

---

# 12. Baselines

Antes de avaliar os modelos de aprendizado de máquina, serão criados modelos de referência simples (*baselines*).

O objetivo é responder:

> O modelo de aprendizado de máquina realmente apresenta desempenho superior a estratégias simples?

Os baselines previstos incluem:

- **Majority:** sempre prever a classe mais frequente;
- **Persistence:** utilizar uma estratégia baseada na direção observada anteriormente.

A implementação exata do baseline de persistência será definida durante a etapa de modelagem.

---

# 13. Ambiente de desenvolvimento

O projeto é desenvolvido localmente utilizando um ambiente virtual Python.

### Ativar o ambiente virtual no PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Após a ativação, o terminal deverá apresentar algo semelhante a:

```text
(.venv) PS C:\caminho\do\projeto>
```

### Iniciar o Jupyter Lab

Com o ambiente virtual ativado:

```powershell
python -m jupyter lab
```

O uso de `python -m jupyter lab` garante que o Jupyter seja executado pelo Python do ambiente virtual ativo.

---

# 14. Principais bibliotecas

As principais bibliotecas utilizadas no projeto são:

- **yfinance** — obtenção dos dados históricos do Ibovespa;
- **pandas** — manipulação e análise dos dados;
- **numpy** — operações numéricas;
- **matplotlib** — visualização;
- **scikit-learn** — modelos de aprendizado de máquina e métricas;
- **Jupyter Lab** — desenvolvimento dos notebooks.

---

# 15. Fluxo geral do projeto

```text
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
                  ┌────────┴────────┐
                  │                 │
                  ▼                 ▼
             Features            Target
              (até T)        (direção em T+5)
                  │                 │
                  └────────┬────────┘
                           ▼
                 ibovespa_features.csv
                           │
                           ▼
              03_modelagem_avaliacao.ipynb
                           │
                  ┌────────┼────────┐
                  ▼        ▼        ▼
              Logística  Árvore  Random Forest
                  │        │        │
                  └────────┼────────┘
                           ▼
                       Avaliação
                           │
                           ▼
                    model_metrics.csv
                           │
                           ▼
              04_resultados_artigo.ipynb
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                Gráficos      Análises
                    │             │
                    └──────┬──────┘
                           ▼
                    RESULTADOS DO
                        ARTIGO
```

---

# 16. Status do projeto

## Planejamento

- [x] Definição do problema
- [x] Definição do ativo
- [x] Definição do período
- [x] Definição do horizonte de 5 pregões
- [x] Definição dos modelos
- [x] Definição da estrutura de notebooks
- [x] Configuração do ambiente local

## Desenvolvimento

- [x] `01_coleta_dados.ipynb`
- [x] `02_exploracao_preparacao.ipynb`
- [ ] `03_modelagem_avaliacao.ipynb`
- [ ] `04_resultados_artigo.ipynb`

## Dados

- [x] Dataset bruto coletado
- [x] Dataset bruto validado
- [x] Dataset processado
- [x] Features definidas
- [x] Target definido
- [x] Verificação de valores ausentes
- [x] Verificação de valores infinitos
- [x] Verificação da distribuição das classes

## Modelagem

- [ ] Definição da divisão treino/validação/teste
- [ ] Baseline Majority
- [ ] Baseline Persistence
- [ ] Regressão Logística
- [ ] Árvore de Decisão
- [ ] Random Forest
- [ ] Métricas calculadas
- [ ] Matrizes de confusão
- [ ] Comparação dos modelos
- [ ] Tabela final de métricas

## Resultados

- [ ] Gráficos comparativos
- [ ] Importância das variáveis
- [ ] Análise de erros por período
- [ ] Seleção dos resultados para o artigo
- [ ] Resultados incorporados ao artigo

---

# 17. Próxima etapa

As etapas de **coleta, validação, exploração e preparação dos dados estão concluídas**.

O próximo passo é implementar:

```text
notebooks/03_modelagem_avaliacao.ipynb
```

A primeira etapa será definir a **separação cronológica entre treinamento, validação e teste**, evitando que informações do futuro sejam utilizadas durante o treinamento.

Em seguida serão implementados:

```text
Dataset processado
        ↓
Divisão temporal
        ↓
Baselines
        ↓
Regressão Logística
        ↓
Árvore de Decisão
        ↓
Random Forest
        ↓
Avaliação
        ↓
Comparação dos resultados
```

O objetivo desta etapa será descobrir se os modelos de aprendizado de máquina conseguem superar estratégias simples na classificação da direção do Ibovespa cinco pregões à frente.