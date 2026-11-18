from functools import partial
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline

from src.preprocessamento import preprocessar_texto


CONFIGURACOES = {
    "A": {"remover_stopwords": False, "vetorizador": "BoW"},
    "B": {"remover_stopwords": False, "vetorizador": "TF-IDF"},
    "C": {"remover_stopwords": True, "vetorizador": "BoW"},
    "D": {"remover_stopwords": True, "vetorizador": "TF-IDF"},
}


def criar_pipeline(configuracao: str) -> Pipeline:
    parametros = CONFIGURACOES[configuracao]
    vetorizadores = {"BoW": CountVectorizer, "TF-IDF": TfidfVectorizer}
    preprocessador = partial(
        preprocessar_texto,
        remover_stopwords=parametros["remover_stopwords"],
    )
    vetorizador = vetorizadores[parametros["vetorizador"]](
        preprocessor=preprocessador,
        tokenizer=str.split,
        token_pattern=None,
        lowercase=False,
    )
    return Pipeline(
        [
            ("vetorizador", vetorizador),
            ("classificador", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )


def comparar_configuracoes(
    textos_treino: pd.Series,
    rotulos_treino: pd.Series,
    destino: Path,
) -> pd.DataFrame:
    validacao = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    metricas = {
        "acuracia": "accuracy",
        "f1": make_scorer(f1_score, pos_label="positivo", zero_division=0),
    }
    resultados = []

    for identificador, parametros in CONFIGURACOES.items():
        modelo = criar_pipeline(identificador)
        pontuacoes = cross_validate(
            modelo,
            textos_treino,
            rotulos_treino,
            cv=validacao,
            scoring=metricas,
            n_jobs=1,
            error_score="raise",
        )
        vetorizador = modelo.named_steps["vetorizador"]
        vetorizador.fit(textos_treino)

        resultados.append(
            {
                "config": identificador,
                "stopwords": "removidas" if parametros["remover_stopwords"] else "mantidas",
                "vetorizador": parametros["vetorizador"],
                "vocabulario": len(vetorizador.vocabulary_),
                "acc_cv_media": pontuacoes["test_acuracia"].mean(),
                "acc_cv_desvio": pontuacoes["test_acuracia"].std(),
                "f1_cv_media": pontuacoes["test_f1"].mean(),
                "f1_cv_desvio": pontuacoes["test_f1"].std(),
            }
        )

    comparacao = pd.DataFrame(resultados)
    comparacao.to_csv(destino, index=False, encoding="utf-8", float_format="%.6f")
    return comparacao


def selecionar_configuracao(comparacao: pd.DataFrame) -> str:
    ordenada = comparacao.sort_values(
        ["f1_cv_media", "acc_cv_media", "config"],
        ascending=[False, False, True],
    )
    return str(ordenada.iloc[0]["config"])
