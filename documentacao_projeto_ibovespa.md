# Documentação do Projeto — Previsão da Direção do Ibovespa

> **Status:** Notebook 3 em desenvolvimento  
> **Objetivo atual:** utilizar aprendizado de máquina para prever se o Ibovespa fechará em **alta (1)** ou **queda (0)** daqui a **5 pregões**.

---

## 1. Visão geral

O projeto utiliza dados históricos diários do Ibovespa (`^BVSP`), referentes ao período de 2010 a 2025, para investigar se informações disponíveis até determinada data conseguem ajudar a prever a direção do índice cinco pregões à frente.

O problema é tratado como uma **classificação binária**:

- `1` = ALTA
- `0` = QUEDA

### Modelos planejados

1. Majority Baseline
2. Persistence Baseline
3. Regressão Logística
4. Árvore de Decisão
5. Random Forest

A métrica principal para comparação é a **Balanced Accuracy**. Precision, Recall, F1 e matrizes de confusão serão usadas para interpretar o comportamento dos modelos.

---

# 2. Notebook 1 — `01_coleta_dados.ipynb`

**Status:** concluído e funcional.

Responsabilidades:

- baixar os dados;
- verificar se foram recebidos corretamente;
- organizar as colunas;
- salvar `data/raw/ibovespa_raw.csv`.

### Validação da base bruta

- **Linhas:** 3965
- **Data inicial:** 2010-01-04
- **Data final:** 2025-12-30
- **Valores ausentes:** nenhum
- **Duplicatas:** nenhuma

A coluna `Price` observada inicialmente não fazia parte das variáveis utilizadas; era o nome associado ao índice das colunas na apresentação da tabela.

---

# 3. Notebook 2 — `02_exploracao_preparacao.ipynb`

**Status:** concluído e funcional.

Responsabilidades:

- carregar os dados brutos;
- verificar ausências e duplicatas;
- realizar exploração;
- calcular retornos;
- calcular indicadores derivados;
- construir o target;
- salvar a base processada.

Arquivo:

`data/processed/ibovespa_features.csv`

### Base processada

Dimensões:

`3955 × 9`

Colunas:

- `Date`
- `Retorno_Diario`
- `Retorno_5d`
- `Retorno_10d`
- `Media_Retorno_5d`
- `Volatilidade_5d`
- `Variacao_Intradiaria`
- `Amplitude_Diaria`
- `Direcao_Futura`

### Target

`Direcao_Futura`:

- `1` = ALTA
- `0` = QUEDA

Distribuição final:

| Classe | Quantidade | Percentual |
|---|---:|---:|
| ALTA | 2082 | 52,71% |
| QUEDA | 1868 | 47,29% |

Não foram encontrados fechamentos empatados na construção final do target.

Também não foram encontrados valores ausentes ou infinitos nas features.

---

# 4. Separação temporal

Os dados foram separados cronologicamente, sem embaralhamento, para evitar vazamento temporal.

## Treinamento

- Dimensão: `2765 × 7`
- Período: 2010-01-18 → 2021-03-25
- ALTA: 53,78%
- QUEDA: 46,22%

## Validação

- Dimensão: `592 × 7`
- Período: 2021-03-26 → 2023-08-08
- QUEDA: 51,86%
- ALTA: 48,14%

## Teste

- Dimensão: `593 × 7`
- Período: 2023-08-09 → 2025-12-19
- ALTA: 52,28%
- QUEDA: 47,72%

### Observação

As três divisões mantiveram proporções próximas de 50/50 entre ALTA e QUEDA. Portanto, não há forte desbalanceamento de classes.

---

# 5. Notebook 3 — `03_modelagem_avaliacao.ipynb`

**Status:** em desenvolvimento.

Implementado até o momento:

- separação temporal;
- Majority Baseline;
- Persistence Baseline;
- Regressão Logística.

Pendente:

- Árvore de Decisão;
- Random Forest;
- comparação final;
- consolidação das métricas.

---

# 6. Métrica principal — Balanced Accuracy

A Balanced Accuracy foi escolhida como principal métrica porque queremos avaliar o desempenho para identificar tanto ALTA quanto QUEDA.

As demais métricas são utilizadas como apoio:

- Precision;
- Recall;
- F1-score;
- matriz de confusão.

Um modelo que favoreça uma classe não deve ser considerado excelente apenas porque acerta muitos exemplos dessa classe.

---

# 7. Majority Baseline

## Conceito

O Majority Baseline identifica a classe mais frequente no conjunto de treinamento e utiliza essa classe para todas as previsões.

No treinamento:

- ALTA: 53,78%
- QUEDA: 46,22%

Portanto, o baseline prevê ALTA para todas as observações.

## Resultado

```text
Balanced Accuracy: 50,00%
Precision (ALTA): 52,28%
Recall (ALTA): 100,00%
F1 (ALTA): 68,66%
```

### Interpretação

O Recall de ALTA é 100% porque o modelo prevê ALTA para todos os casos.

Porém, ele não consegue identificar QUEDA.

Por isso a Balanced Accuracy permanece em 50%.

### Aprendizado

O Majority Baseline estabelece uma referência mínima. Um modelo de aprendizado de máquina precisa superar esse comportamento trivial para demonstrar que está extraindo informação útil.

---

# 8. Persistence Baseline

## Conceito

O Persistence Baseline foi adaptado ao horizonte de cinco pregões do projeto. Ele utiliza uma referência baseada na direção observada cinco pregões antes.

A finalidade é criar uma segunda referência simples, sem aprendizado de máquina.

## Resultado

Matriz:

```text
[[143 140]
 [144 166]]
```

Avaliação:

```text
Balanced Accuracy: 52,04%
Precision (ALTA): 54,25%
Recall (ALTA): 53,55%
F1 (ALTA): 53,90%
```

Considerando `0 = QUEDA` e `1 = ALTA`:

- TN = 143
- FP = 140
- FN = 144
- TP = 166

### Interpretação

O comportamento é relativamente equilibrado entre as classes.

A Persistence apresentou 52,04% de Balanced Accuracy, superando o Majority Baseline e, até este momento, também a Regressão Logística.

---

# 9. Regressão Logística

## Objetivo

A Regressão Logística foi o primeiro modelo supervisionado.

Features utilizadas:

- `Retorno_Diario`
- `Retorno_5d`
- `Retorno_10d`
- `Media_Retorno_5d`
- `Volatilidade_5d`
- `Variacao_Intradiaria`
- `Amplitude_Diaria`

Antes do treinamento foi utilizado `StandardScaler`, ajustado **somente com `X_train`** e depois aplicado a treino, validação e teste.

## Resultado

```text
Balanced Accuracy: 50,89%
Precision (ALTA): 52,74%
Recall (ALTA): 96,13%
F1 (ALTA): 68,11%
```

### Matriz de confusão

```text
[[ 16 267]
 [ 12 298]]
```

Portanto:

- TN = 16
- FP = 267
- FN = 12
- TP = 298

### Interpretação

O modelo acertou 298 das 310 ocorrências de ALTA, mas identificou corretamente apenas 16 das 283 ocorrências de QUEDA.

Isso explica o Recall de ALTA de 96,13%, mas também revela uma forte tendência a prever ALTA.

A Balanced Accuracy de 50,89% mostra que o bom desempenho em ALTA não representa boa capacidade de distinguir as duas classes.

### Principal aprendizado

Um Recall alto para uma única classe pode ser enganoso. A matriz de confusão e a Balanced Accuracy revelam que a Regressão Logística praticamente não conseguiu reconhecer QUEDA.

---

# 10. Coeficientes da Regressão Logística

| Feature | Coeficiente |
|---|---:|
| `Retorno_Diario` | -0,007421 |
| `Retorno_5d` | -0,049401 |
| `Retorno_10d` | **0,172398** |
| `Media_Retorno_5d` | -0,046046 |
| `Volatilidade_5d` | -0,005799 |
| `Variacao_Intradiaria` | -0,006800 |
| `Amplitude_Diaria` | **0,067735** |

Intercepto:

```text
0,15217805
```

### Interpretação

`Retorno_10d` apresentou o maior coeficiente em magnitude. Dentro desta configuração, valores maiores dessa variável tendem a aumentar a probabilidade estimada de ALTA, mantendo as demais variáveis constantes.

`Amplitude_Diaria` apresentou o segundo maior coeficiente positivo.

`Retorno_5d` e `Media_Retorno_5d` apresentaram influência negativa.

`Volatilidade_5d`, `Variacao_Intradiaria` e `Retorno_Diario` receberam coeficientes próximos de zero.

Os coeficientes não devem ser interpretados como causalidade econômica; são pesos aprendidos pelo modelo para os dados e configuração utilizados.

---

# 11. Probabilidades da Regressão Logística

Primeiras probabilidades:

```text
[0.4901815  0.5098185]
[0.47262576 0.52737424]
[0.47663115 0.52336885]
[0.49163179 0.50836821]
[0.48908642 0.51091358]
[0.48960782 0.51039218]
[0.48918612 0.51081388]
[0.48970266 0.51029734]
[0.49432344 0.50567656]
[0.4938678  0.5061322]
```

A primeira coluna é a probabilidade de QUEDA e a segunda a probabilidade de ALTA.

### Observação

As probabilidades estão muito próximas de 50%.

Por exemplo:

```text
QUEDA 49,02% / ALTA 50,98%
QUEDA 47,26% / ALTA 52,74%
QUEDA 47,66% / ALTA 52,34%
```

O modelo frequentemente encontra uma pequena vantagem para ALTA e, usando o threshold padrão de 50%, transforma essa pequena diferença em ALTA.

Isso ajuda a explicar a forte concentração de previsões na classe ALTA.

---

# Atualização dos resultados dos modelos

## 1. Regressão Logística — Threshold de 55%

Após a avaliação da Regressão Logística utilizando o threshold padrão de 50%, foi realizado um experimento alterando o threshold de decisão para **55%**.

O objetivo desse teste não foi buscar uma configuração definitiva, mas observar como o comportamento do modelo seria alterado ao exigir uma probabilidade maior para classificar uma observação como **ALTA**.

### Matriz de confusão

```text
[[249  34]
 [260  50]]
```

Interpretação:

- **TN = 249** — previu QUEDA e era QUEDA;
- **FP = 34** — previu ALTA, mas era QUEDA;
- **FN = 260** — previu QUEDA, mas era ALTA;
- **TP = 50** — previu ALTA e era ALTA.

### Métricas

| Métrica | Resultado |
|---|---:|
| Balanced Accuracy | 52,06% |
| Precision (ALTA) | 59,52% |
| Recall (ALTA) | 16,13% |
| F1 (ALTA) | 25,38% |

### Interpretação

O aumento do threshold tornou o modelo **muito mais conservador ao classificar ALTA**.

Isso pode ser observado pela redução expressiva dos falsos positivos:

- FP: **267 → 34**

Ao mesmo tempo, houve um grande aumento dos falsos negativos:

- FN: **12 → 260**

Consequentemente, a precisão das previsões de ALTA aumentou, passando de aproximadamente 52,74% no threshold padrão para **59,52%**. Entretanto, o recall caiu drasticamente para **16,13%**, pois o modelo passou a deixar de identificar grande parte das situações que realmente terminaram em ALTA.

A Balanced Accuracy foi de **50,89%** no threshold padrão para **52,06%** com threshold de 55%.

O experimento demonstrou, portanto, que alterar o threshold modifica significativamente o comportamento do modelo e estabelece um trade-off entre **precision e recall**. O threshold de 55% não foi adotado como configuração definitiva, sendo utilizado apenas como experimento para compreender o comportamento da classificação.

---

# 2. Árvore de Decisão — Configuração padrão

O segundo modelo desenvolvido foi uma **Árvore de Decisão**, inicialmente sem restrição explícita de profundidade.

```python
DecisionTreeClassifier(
    random_state=42
)
```

### Estrutura aprendida

A árvore apresentou:

- **Profundidade:** 26
- **Folhas:** 719
- **Nós:** 1.437

A estrutura revelou um modelo bastante complexo, composto por diversas regras de decisão.

A primeira divisão da árvore utilizou `Retorno_10d`, indicando que essa variável foi considerada inicialmente relevante para separar as classes.

### Importância das variáveis

| Feature | Importância |
|---|---:|
| Amplitude_Diaria | 0,196853 |
| Retorno_10d | 0,188106 |
| Volatilidade_5d | 0,186984 |
| Media_Retorno_5d | 0,112692 |
| Retorno_5d | 0,110377 |
| Retorno_Diario | 0,102975 |
| Variacao_Intradiaria | 0,102014 |

As três variáveis com maior importância foram:

1. `Amplitude_Diaria`;
2. `Retorno_10d`;
3. `Volatilidade_5d`.

É importante destacar que essas importâncias não representam pesos equivalentes aos coeficientes da Regressão Logística. Na árvore, elas representam a contribuição das variáveis para as divisões realizadas ao longo da estrutura.

### Probabilidades

A árvore apresentou probabilidades frequentemente extremas, como:

```text
[0.0, 1.0]
```

Isso ocorre porque as probabilidades da Árvore de Decisão são calculadas a partir da distribuição das classes nas folhas. Em folhas nas quais todas as observações de treinamento pertencem à mesma classe, o modelo retorna uma probabilidade de 100% para aquela classe.

Essas probabilidades não devem ser interpretadas como uma certeza real de que o Ibovespa subirá ou cairá.

### Matriz de confusão

```text
[[136 147]
 [131 179]]
```

- **TN = 136**
- **FP = 147**
- **FN = 131**
- **TP = 179**

### Métricas

| Métrica | Resultado |
|---|---:|
| Balanced Accuracy | **52,90%** |
| Precision (ALTA) | 54,91% |
| Recall (ALTA) | 57,74% |
| F1 (ALTA) | 56,29% |

### Interpretação

A Árvore de Decisão apresentou desempenho superior ao da Regressão Logística com threshold padrão e também ao Majority Baseline, alcançando **52,90% de Balanced Accuracy**.

Seu comportamento foi mais equilibrado entre as classes do que o observado na Regressão Logística, que apresentou forte tendência a classificar as observações como ALTA.

Apesar disso, a árvore apresentou uma estrutura bastante complexa, com 26 níveis de profundidade e 719 folhas. Essa complexidade levantou a hipótese de que uma árvore menos profunda poderia apresentar melhor capacidade de generalização.

Por esse motivo, foi realizado um experimento limitando sua profundidade.

---

# 3. Árvore de Decisão — `max_depth=3`

Foi criada uma segunda versão da Árvore de Decisão limitando sua profundidade máxima a três níveis:

```python
DecisionTreeClassifier(
    max_depth=3,
    random_state=42
)
```

O objetivo foi verificar se uma estrutura mais simples poderia apresentar desempenho igual ou superior ao da árvore original.

### Matriz de confusão

```text
[[200  83]
 [185 125]]
```

- **TN = 200**
- **FP = 83**
- **FN = 185**
- **TP = 125**

### Métricas

| Métrica | Resultado |
|---|---:|
| Balanced Accuracy | **55,50%** |
| Precision (ALTA) | 60,10% |
| Recall (ALTA) | 40,32% |
| F1 (ALTA) | 48,26% |

### Comparação com a árvore original

| Métrica | Árvore padrão | `max_depth=3` |
|---|---:|---:|
| Balanced Accuracy | 52,90% | **55,50%** |
| Precision (ALTA) | 54,91% | **60,10%** |
| Recall (ALTA) | **57,74%** | 40,32% |
| F1 (ALTA) | **56,29%** | 48,26% |

### Interpretação

A limitação da profundidade produziu um resultado interessante.

Mesmo sendo uma árvore muito mais simples, o modelo apresentou uma **Balanced Accuracy superior**, passando de 52,90% para **55,50%**.

Entretanto, essa melhora ocorreu acompanhada de uma mudança significativa no comportamento do modelo.

A capacidade de identificar corretamente situações de QUEDA aumentou consideravelmente:

- TN: **136 → 200**
- FP: **147 → 83**

Por outro lado, a capacidade de identificar ALTA diminuiu:

- TP: **179 → 125**
- FN: **131 → 185**

Consequentemente, o recall da classe ALTA caiu de 57,74% para 40,32%, enquanto a precisão aumentou de 54,91% para 60,10%.

Esse resultado demonstra que a redução da complexidade não tornou o modelo simplesmente "melhor em tudo". Ela alterou sua estratégia de classificação, tornando-o mais conservador na identificação de ALTA.

A melhora da Balanced Accuracy indica, entretanto, que essa troca favoreceu o desempenho balanceado entre as duas classes.

### Observação sobre complexidade e generalização

O resultado também é relevante para a análise de complexidade do modelo. A árvore original possuía 26 níveis de profundidade e apresentou 52,90% de Balanced Accuracy, enquanto uma árvore limitada a apenas 3 níveis alcançou 55,50%.

Isso sugere que uma estrutura extremamente complexa não era necessária para obter o melhor desempenho observado no conjunto de teste. O resultado é compatível com a hipótese de que limitar a complexidade pode favorecer a generalização, embora não seja suficiente, isoladamente, para afirmar a existência de overfitting.

---

# 4. Situação dos modelos até o momento

Considerando a **Balanced Accuracy** como principal métrica de comparação:

| Modelo | Balanced Accuracy |
|---|---:|
| Majority Baseline | 50,00% |
| Logistic Regression — threshold 50% | 50,89% |
| Logistic Regression — threshold 55% | 52,06% |
| Persistence Baseline | 52,04% |
| Decision Tree | 52,90% |
| **Decision Tree — `max_depth=3`** | **55,50%** |

Até o momento, a **Árvore de Decisão com `max_depth=3` apresenta o melhor desempenho balanceado** entre os modelos e configurações avaliados.

Entretanto, esse resultado ainda não permite concluir que ela será o melhor modelo final do projeto. O **Random Forest** ainda precisa ser treinado e avaliado, mantendo exatamente o mesmo conjunto de teste e as mesmas métricas para permitir uma comparação justa.

## Observação metodológica

Os experimentos realizados até aqui tiveram caráter exploratório e serviram para compreender o comportamento dos modelos.

Não foram realizadas buscas extensivas de hiperparâmetros. Alterações como o threshold de 55% na Regressão Logística e o `max_depth=3` na Árvore de Decisão foram utilizadas principalmente para estudar como mudanças na configuração dos modelos afetam suas previsões e métricas.

A seleção final do modelo deverá considerar o conjunto completo de resultados, incluindo o Random Forest e, posteriormente, a análise dos erros e da importância das variáveis.

---

# 12. Comparação atual

| Modelo | Balanced Accuracy |
|---|---:|
| Majority Baseline | **50,00%** |
| Persistence Baseline | **52,04%** |
| Logistic Regression | **50,89%** |
| Decision Tree | **52,90%** |
| Random Forest | — |

### Situação atual

O Persistence Baseline apresenta o melhor resultado entre os métodos avaliados até agora.

A Regressão Logística não superou o Persistence Baseline na configuração inicial.

A conclusão atual deve ser limitada a:

> **Na configuração inicial avaliada, a Regressão Logística apresentou desempenho inferior ao Persistence Baseline no conjunto de teste.**

Isso não significa que a Regressão Logística seja incapaz de melhorar com outras configurações.

---

# 13. Ajustes e otimização — PENDENTE

Ainda não foram realizados ajustes destinados a maximizar o desempenho da Regressão Logística.

Possíveis etapas futuras:

- ajuste de hiperparâmetros;
- regularização;
- avaliação de `class_weight`, caso exista justificativa;
- análise de diferentes thresholds;
- seleção ou transformação de features.

Esses ajustes devem ser orientados pelo conjunto de **validação**, mantendo o conjunto de teste reservado para a avaliação final.

A ideia é primeiro estabelecer o desempenho dos modelos em uma configuração inicial e somente depois investigar otimizações.

---

# 14. Próximas etapas

## Árvore de Decisão

- entender o funcionamento das regras de decisão;
- treinar;
- avaliar;
- gerar matriz de confusão;
- comparar com os resultados anteriores.

## Random Forest

- treinar;
- avaliar;
- gerar matriz de confusão;
- comparar com todos os modelos anteriores;
- posteriormente analisar importância das features.

## Comparação final

Consolidar:

- Balanced Accuracy;
- Precision;
- Recall;
- F1;
- matrizes de confusão;
- comportamento dos modelos.

## Notebook 4 — `04_resultados_artigo.ipynb`

Depois de finalizar o Notebook 3:

- carregar métricas já calculadas;
- gerar gráficos comparativos;
- analisar importância das variáveis;
- analisar erros por período;
- selecionar resultados para o artigo.

O Notebook 4 não deve treinar novamente os modelos.

---

# 15. Aprendizados metodológicos consolidados

### Majority Baseline

Serve como referência mínima e prevê sempre a classe majoritária.

### Matriz de confusão

Para este projeto:

- positivo = ALTA;
- negativo = QUEDA.

Estrutura:

```text
                 PREVISÃO
              QUEDA     ALTA

REAL QUEDA      TN       FP
REAL ALTA      FN       TP
```

### Balanced Accuracy

É a principal métrica do projeto porque avalia o desempenho nas duas classes.

### Data leakage

O `StandardScaler` deve aprender seus parâmetros somente com o treinamento.

### Baseline vs. modelo

Um modelo de ML precisa ser comparado com estratégias simples.

### Probabilidade vs. classe

A Regressão Logística produz probabilidades. A classe final depende do threshold.

Por exemplo, 50,2% e 95% podem resultar na mesma classe ALTA com threshold de 50%, embora tenham níveis de confiança muito diferentes.

---

# 16. Histórico resumido

| Etapa | Balanced Accuracy | Principal observação |
|---|---:|---|
| Majority | 50,00% | Prevê a classe majoritária e não distingue adequadamente as classes |
| Persistence | 52,04% | Melhor resultado até o momento |
| Logistic Regression | 50,89% | Forte tendência a ALTA e dificuldade para identificar QUEDA |
| Decision Tree | — | Pendente |
| Random Forest | — | Pendente |

---

> **Última atualização:** Notebook 3 em desenvolvimento, após a análise inicial da Regressão Logística.
