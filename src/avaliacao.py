import json
import matplotlib.pyplot as plt

from sklearn.metrics import (
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)


def avaliar_modelo(nome_modelo, y_true, y_pred, mostrar_matriz=True, salvar_figura=False):
    """
    Avalia um modelo de classificação e gera sua matriz de confusão.

    Parâmetros
    ----------
    nome_modelo : str
        Nome que será utilizado para identificar o modelo.

    y_true : array-like
        Valores reais da variável alvo.

    y_pred : array-like
        Valores previstos pelo modelo.

    mostrar_matriz : bool, default=True
        Define se a matriz de confusão será exibida.

    salvar_figura : bool, default=False
        Define se a matriz de confusão será salva como imagem.

    Retorno
    -------
    resultado : dict
        Dicionário contendo as métricas de avaliação.

    matriz : ndarray
        Matriz de confusão.
    """

    # ---------------------------------------------------------
    # 1. Cálculo das métricas
    # ---------------------------------------------------------

    balanced_accuracy = balanced_accuracy_score(
        y_true,
        y_pred
    )

    precision_high = precision_score(
        y_true,
        y_pred,
        pos_label=1,
        zero_division=0
    )

    recall_high = recall_score(
        y_true,
        y_pred,
        pos_label=1,
        zero_division=0
    )

    f1_high = f1_score(
        y_true,
        y_pred,
        pos_label=1,
        zero_division=0
    )

    # ---------------------------------------------------------
    # 2. Organizando os resultados
    # ---------------------------------------------------------

    resultado = {
        "model": nome_modelo,
        "balanced_accuracy": balanced_accuracy,
        "precision_high": precision_high,
        "recall_high": recall_high,
        "f1_high": f1_high
    }

    print(f"Avaliação do(a) {nome_modelo}:")
    print(json.dumps(
        resultado,
        ensure_ascii=False,
        indent=4
    ))

    # ---------------------------------------------------------
    # 3. Matriz de confusão
    # ---------------------------------------------------------

    matriz = confusion_matrix(
        y_true,
        y_pred
    )

    print("\nMatriz de confusão:")
    print(matriz)

    # ---------------------------------------------------------
    # 4. Representação visual da matriz
    # ---------------------------------------------------------

    disp = ConfusionMatrixDisplay(
        confusion_matrix=matriz,
        display_labels=["QUEDA", "ALTA"]
    )

    disp.plot()

    plt.title(f"Matriz de Confusão — {nome_modelo}")
    plt.tight_layout()

    # ---------------------------------------------------------
    # 5. Salvar figura, caso solicitado
    # ---------------------------------------------------------

    if salvar_figura:
        nome_arquivo = (
            nome_modelo
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("=", "")
        )

        caminho = f"resultados/matriz_confusao_{nome_arquivo}.png"

        plt.savefig(
            caminho,
            dpi=300,
            bbox_inches="tight"
        )

        print(f"\nFigura salva em: {caminho}")

    # ---------------------------------------------------------
    # 6. Exibir figura, caso solicitado
    # ---------------------------------------------------------

    if mostrar_matriz:
        plt.show()
    else:
        plt.close()

    return resultado, matriz