from pathlib import Path

import pandas as pd


def salvar_exploracao(avaliacoes: pd.DataFrame, destino: Path) -> None:
    total = len(avaliacoes)
    linhas = ["Exploração das avaliações", f"Total de avaliações: {total}"]

    for sentimento, grupo in avaliacoes.groupby("sentimento", sort=True):
        quantidade = len(grupo)
        tamanhos = grupo["texto"].fillna("").str.split().str.len()

        linhas.extend(
            [
                "",
                f"Classe: {sentimento}",
                f"Quantidade: {quantidade}",
                f"Percentual: {quantidade / total:.1%}",
                f"Tamanho médio dos textos: {tamanhos.mean():.2f} palavras",
                "Três primeiros exemplos da classe:",
            ]
        )

        for avaliacao in grupo.head(3).itertuples(index=False):
            linhas.append(f"- {avaliacao.texto}")

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
