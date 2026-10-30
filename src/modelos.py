from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def criar_logistic_regression(**kwargs):
    """
    Cria um modelo de Regressão Logística.

    Parâmetros adicionais podem ser passados através de kwargs.

    Exemplo:
        modelo = criar_logistic_regression(max_iter=2000)
    """
    parametros = {
        "max_iter": 1000
    }

    parametros.update(kwargs)

    return LogisticRegression(**parametros)


def criar_decision_tree(**kwargs):
    """
    Cria um modelo de Árvore de Decisão.

    Parâmetros adicionais podem ser utilizados para
    controlar o comportamento da árvore.

    Exemplo:
        modelo = criar_decision_tree(max_depth=3)
    """
    parametros = {
        "random_state": 42
    }

    parametros.update(kwargs)

    return DecisionTreeClassifier(**parametros)


def criar_random_forest(**kwargs):
    """
    Cria um modelo Random Forest.

    Parâmetros adicionais podem ser utilizados para
    controlar o comportamento da floresta.

    Exemplo:
        modelo = criar_random_forest(
            n_estimators=100,
            max_depth=3
        )
    """
    parametros = {
        "n_estimators": 100,
        "random_state": 42
    }

    parametros.update(kwargs)

    return RandomForestClassifier(**parametros)