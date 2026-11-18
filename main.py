from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from src.avaliacao import avaliar_casos_dificeis, avaliar_no_teste, salvar_palavras_influentes
from src.exploracao import salvar_exploracao
from src.modelos import comparar_configuracoes, criar_pipeline, selecionar_configuracao


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
    modelo_final = criar_pipeline(escolhida)
    modelo_final.fit(treino["texto"], treino["sentimento"])

    metricas = avaliar_no_teste(modelo_final, teste, pasta_resultados)
    salvar_palavras_influentes(modelo_final, pasta_resultados / "palavras_influentes.csv")

    casos_dificeis = pd.read_csv(pasta_projeto / "data" / "casos_dificeis.csv", encoding="utf-8")
    avaliar_casos_dificeis(
        modelo_final,
        casos_dificeis,
        pasta_resultados / "casos_dificeis_predicoes.csv",
    )

    print(f"Avaliacoes para treino: {len(treino)}; para teste: {len(teste)}.")
    print(f"Configuracao escolhida pela validacao cruzada: {escolhida}.")
    print(f"Acuracia no teste: {metricas['acuracia']:.4f}.")
    print(f"F1 da classe positiva no teste: {metricas['f1']:.4f}.")
    print("Arquivos gerados em resultados/.")


if __name__ == "__main__":
    main()
