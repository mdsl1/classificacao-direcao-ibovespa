# Guia de execução dos experimentos de Machine Learning

## 1. Objetivo

O objetivo é executar duas buscas de hiperparâmetros para um projeto de classificação da direção futura do Ibovespa:

- **Decision Tree:** busca exaustiva (`GridSearchCV`), com 201.600 combinações e 5 folds temporais, totalizando 1.008.000 ajustes.
- **Random Forest:** busca aleatória (`RandomizedSearchCV`), com 500 combinações e 5 folds temporais, totalizando 2.500 ajustes.

As buscas utilizam Balanced Accuracy como métrica de seleção.

O projeto foi desenvolvido em Python e utiliza Scikit-learn, Pandas e outras bibliotecas de ciência de dados.

## 2. Requisitos

- Windows 10 ou 11.
- Python 3.11.
- Git (opcional, caso utilize clonagem do repositório).
- Processador com múltiplos núcleos.
- Memória RAM suficiente para executar as buscas.
- Espaço livre em disco para o projeto e os resultados.

**Observação:** não é necessário possuir GPU. As implementações de Decision Tree e Random Forest utilizadas pelo Scikit-learn executam na CPU.

## 3. Preparação do projeto

Primeiro, obtenha uma cópia completa do repositório do projeto.

Pode ser por Git ou por um arquivo ZIP.

Não é necessário copiar a pasta `.venv` da máquina original. Cada computador deve possuir seu próprio ambiente virtual.

A estrutura esperada é semelhante a esta:

```text
classificacao-volatibilidade-ibovespa/
│
├── .venv/
├── data/
│   ├── raw/
│   │   └── ibovespa_raw.csv
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
│   └── experiments/
│
├── src/
│   ├── __init__.py
│   ├── modelos.py
│   ├── avaliacao.py
│   └── depuracao.py
│
└── requirements.txt
```

É importante preservar os arquivos de dados processados, os módulos da pasta `src` e os notebooks.

## 4. Criando o ambiente virtual

Abra o PowerShell dentro da pasta raiz do projeto.

Execute:

```powershell
py -3.11 -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação por política de execução, uma alternativa é utilizar o Prompt de Comando (CMD):

```cmd
.venv\Scripts\activate.bat
```

Atualize o instalador de pacotes:

```powershell
python -m pip install --upgrade pip
```

## 5. Instalando as dependências

Com o ambiente virtual ativado, instale as bibliotecas:

```powershell
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` ainda não estiver disponível, será necessário gerá-lo a partir do ambiente original do projeto, ou instalar as dependências utilizadas nele.

Não é recomendado instalar versões aleatórias das bibliotecas, pois isso pode gerar diferenças de comportamento entre os computadores.

## 6. Verificando o ambiente

Execute:

```powershell
python --version
```

O resultado esperado é:

```text
Python 3.11.x
```

Confira também se o ambiente virtual está sendo utilizado:

```powershell
python -c "import sys; print(sys.executable)"
```

O caminho apresentado deve apontar para a pasta `.venv` do projeto.

Verifique as principais bibliotecas:

```powershell
python -c "import numpy, pandas, sklearn; print('Ambiente OK')"
```

## 7. Executando os experimentos

Abra o Jupyter Notebook a partir da raiz do projeto:

```powershell
jupyter notebook
```

Abra o notebook:

`03_modelagem_avaliacao.ipynb`

Execute as células anteriores às buscas para garantir que:

- Os dados estejam carregados.
- `X_train` e `y_train` estejam definidos.
- `X_val` e `y_val` estejam definidos.
- A validação temporal esteja configurada com `n_splits=5` e `gap=5`.
- As funções e classes necessárias estejam importadas.
- Os diretórios de resultados estejam preparados.

Depois, execute as buscas de hiperparâmetros.

**Importante:** não execute novamente as etapas de coleta e preparação caso os arquivos processados já estejam disponíveis e atualizados.

## 8. Cuidados durante a execução

As buscas podem levar bastante tempo, principalmente a busca exaustiva da Decision Tree.

Recomendações:

- Manter o computador conectado à energia.
- Evitar executar outros programas pesados simultaneamente.
- Não fechar o Jupyter enquanto a busca estiver em andamento.
- Evitar suspender ou hibernar o computador.
- Monitorar temperatura, uso de CPU e memória RAM.

O código utiliza `n_jobs=-1`, permitindo que o Scikit-learn aproveite os núcleos disponíveis do processador.

## 9. Arquivos gerados

Os resultados serão salvos automaticamente em:

```text
reports/experiments/
```

Arquivos esperados:

```text
resultados_decision_tree_grid_search.csv
resultados_random_forest_busca_ampliada.csv
```

Além dos CSVs, é importante registrar:

- Melhores parâmetros encontrados.
- Melhor Balanced Accuracy média da validação cruzada.
- Balanced Accuracy obtida no conjunto de validação.
- Matrizes de confusão dos melhores modelos.

Ao finalizar, envie os dois arquivos CSV e os resultados impressos no notebook.

## 10. Observação final

Não é necessário executar os experimentos utilizando GPU.

O mais importante é possuir um processador com boa capacidade de processamento, memória RAM suficiente e manter o computador estável durante a execução.

Os resultados devem ser preservados integralmente, sem alterar os parâmetros da busca ou os dados utilizados.