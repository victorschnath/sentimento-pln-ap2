from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from src.exploracao import salvar_exploracao
from src.modelos import comparar_configuracoes, selecionar_configuracao


def main() -> None:
    pasta_projeto = Path(__file__).resolve().parent
    caminho_dados = pasta_projeto / "data" / "avaliacoes.csv"
    pasta_resultados = pasta_projeto / "resultados"

    avaliacoes = pd.read_csv(caminho_dados, encoding="utf-8")
    salvar_exploracao(avaliacoes, pasta_resultados / "exploracao.txt")

    treino, teste = train_test_split(
        avaliacoes,
        test_size=0.25,
        stratify=avaliacoes["sentimento"],
        random_state=42,
    )
    comparacao = comparar_configuracoes(
        treino["texto"],
        treino["sentimento"],
        pasta_resultados / "comparacao.csv",
    )
    escolhida = selecionar_configuracao(comparacao)

    print(f"Avaliacoes para treino: {len(treino)}; para teste: {len(teste)}.")
    print(f"Configuracao escolhida pela validacao cruzada: {escolhida}.")


if __name__ == "__main__":
    main()
