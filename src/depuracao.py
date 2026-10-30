import numpy as np
import pandas as pd

from sklearn.tree import export_text
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def depurar_modelo(
    modelo,
    X_train,
    X_test,
    nome_modelo,
    detalhado=True
):
    """
    Exibe informações relevantes para compreender
    como o modelo tomou suas decisões.

    O comportamento é adaptado de acordo com
    o tipo de modelo recebido.
    """

    print(f"Depuração: {nome_modelo}")

    # --------------------------------------------------
    # REGRESSÃO LOGÍSTICA
    # --------------------------------------------------

    if isinstance(modelo, LogisticRegression):

        print("\nPesos aprendidos pelo modelo:")
        pesos = pd.DataFrame({
            "Feature": X_train.columns,
            "Coeficiente": modelo.coef_[0]
        })
        pesos["Importancia_Absoluta"] = (
            pesos["Coeficiente"].abs()
        )
        print(
            pesos[
                ["Feature", "Coeficiente"]
            ].to_string(index=False)
        )

        print("\nIntercepto:")
        print(modelo.intercept_)

        print("\nPesos com maior magnitude:")
        pesos_ordenados = (
            pesos
            .sort_values(
                "Importancia_Absoluta",
                ascending=False
            )
        )
        print(
            pesos_ordenados.to_string(
                index=False
            )
        )

        print("\nProbabilidades do modelo:")
        probabilidades = modelo.predict_proba(X_test)
        print(probabilidades[:10])

    # --------------------------------------------------
    # ÁRVORE DE DECISÃO
    # --------------------------------------------------

    elif isinstance(modelo, DecisionTreeClassifier):

        print("\nProfundidade da árvore:")
        print(modelo.get_depth())

        print("\nQuantidade de folhas:")
        print(modelo.get_n_leaves())

        print("\nQuantidade de nós:")
        print(modelo.tree_.node_count)

        print(
            "\nContribuição das variáveis "
            "para a ramificação da árvore:"
        )

        importancias = pd.DataFrame({
            "Feature": X_train.columns,
            "Importancia": modelo.feature_importances_
        })

        importancias = importancias.sort_values(
            "Importancia",
            ascending=False
        )

        print(
            importancias.to_string(index=False)
        )

        print("\nProbabilidades do modelo:")

        probabilidades = modelo.predict_proba(X_test)

        print(probabilidades[:10])
        
        if detalhado == True:
            print("\nRegras da árvore:")

            regras = export_text(
                modelo,
                feature_names=list(X_train.columns)
            )

            print(regras)

    # --------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------

    elif isinstance(modelo, RandomForestClassifier):

        print("\nQuantidade de árvores:")
        print(len(modelo.estimators_))

        profundidades = [
            arvore.get_depth()
            for arvore in modelo.estimators_
        ]

        print("\nProfundidade média:")
        print(np.mean(profundidades))

        print("\nMenor profundidade:")
        print(np.min(profundidades))

        print("\nMaior profundidade:")
        print(np.max(profundidades))

        print(
            "\nImportância das variáveis "
            "para a ramificação das árvores:"
        )

        importancias = pd.DataFrame({
            "Feature": X_train.columns,
            "Importancia": modelo.feature_importances_
        })

        importancias = importancias.sort_values(
            "Importancia",
            ascending=False
        )

        print(
            importancias.to_string(index=False)
        )

        print("\nProbabilidades do modelo:")

        probabilidades = modelo.predict_proba(X_test)

        print(probabilidades[:10])

        print("\nInformações da primeira árvore:")

        primeira_arvore = modelo.estimators_[0]

        print(
            "Profundidade:",
            primeira_arvore.get_depth()
        )

        print(
            "Quantidade de folhas:",
            primeira_arvore.get_n_leaves()
        )

    else:

        print(
            "Tipo de modelo não possui "
            "rotina de depuração implementada."
        )

    print("\n" + "=" * 70)