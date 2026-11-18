from pathlib import Path

import pandas as pd

from src.exploracao import salvar_exploracao


def main() -> None:
    pasta_projeto = Path(__file__).resolve().parent
    caminho_dados = pasta_projeto / "data" / "avaliacoes.csv"
    caminho_saida = pasta_projeto / "resultados" / "exploracao.txt"

    avaliacoes = pd.read_csv(caminho_dados, encoding="utf-8")
    salvar_exploracao(avaliacoes, caminho_saida)

    print("Arquivo gerado em resultados/exploracao.txt.")


if __name__ == "__main__":
    main()
