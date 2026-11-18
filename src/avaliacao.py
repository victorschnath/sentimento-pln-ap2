from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.pipeline import Pipeline


def avaliar_no_teste(
    modelo: Pipeline,
    teste: pd.DataFrame,
    pasta_resultados: Path,
) -> dict[str, float]:
    reais = teste["sentimento"]
    previstos = modelo.predict(teste["texto"])
    probabilidades = modelo.predict_proba(teste["texto"])

    classes = ["negativo", "positivo"]
    matriz = confusion_matrix(reais, previstos, labels=classes)
    tabela_matriz = pd.DataFrame(matriz, index=classes, columns=classes)
    tabela_matriz.index.name = "real"
    tabela_matriz.to_csv(pasta_resultados / "matriz_confusao.csv", encoding="utf-8")

    predicoes = teste[["texto", "sentimento"]].rename(columns={"sentimento": "real"})
    predicoes["previsto"] = previstos
    predicoes["probabilidade"] = probabilidades.max(axis=1)
    erros = predicoes.loc[predicoes["real"] != predicoes["previsto"]]
    erros.to_csv(
        pasta_resultados / "erros.csv",
        index=False,
        encoding="utf-8",
        float_format="%.6f",
    )

    acuracia = accuracy_score(reais, previstos)
    f1 = f1_score(reais, previstos, pos_label="positivo", zero_division=0)
    classificacao = classification_report(
        reais,
        previstos,
        labels=classes,
        digits=4,
        zero_division=0,
    )
    (pasta_resultados / "relatorio_classificacao.txt").write_text(classificacao, encoding="utf-8")
    return {"acuracia": acuracia, "f1": f1}


def salvar_palavras_influentes(modelo: Pipeline, destino: Path) -> None:
    vetorizador = modelo.named_steps["vetorizador"]
    classificador = modelo.named_steps["classificador"]
    palavras = vetorizador.get_feature_names_out()
    coeficientes = classificador.coef_[0]

    if classificador.classes_[1] != "positivo":
        coeficientes = -coeficientes

    indices_positivos = np.argsort(-coeficientes, kind="stable")[:10]
    indices_negativos = np.argsort(coeficientes, kind="stable")[:10]
    positivas = pd.DataFrame(
        {
            "palavra": palavras[indices_positivos],
            "coeficiente": coeficientes[indices_positivos],
        }
    )
    negativas = pd.DataFrame(
        {
            "palavra": palavras[indices_negativos],
            "coeficiente": coeficientes[indices_negativos],
        }
    )
    pd.concat([positivas, negativas], ignore_index=True).to_csv(
        destino,
        index=False,
        encoding="utf-8",
        float_format="%.6f",
    )


def avaliar_casos_dificeis(modelo: Pipeline, casos: pd.DataFrame, destino: Path) -> None:
    indice_positivo = modelo.classes_.tolist().index("positivo")
    probabilidades = modelo.predict_proba(casos["texto"])
    resultados = casos[["texto", "tipo", "sentimento_esperado"]].rename(
        columns={"sentimento_esperado": "esperado"}
    )
    resultados["previsto"] = modelo.predict(casos["texto"])
    resultados["probabilidade_positivo"] = probabilidades[:, indice_positivo]
    resultados.to_csv(destino, index=False, encoding="utf-8", float_format="%.6f")
