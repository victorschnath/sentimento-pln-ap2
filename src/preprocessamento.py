import re


STOPWORDS = frozenset(
    {
        "a", "as", "o", "os", "um", "uma",
        "de", "da", "das", "do", "dos",
        "em", "na", "nas", "no", "nos",
        "para", "por", "com", "e", "que",
        "ao", "aos", "à", "às", "se",
        "eu", "me", "meu", "minha",
    }
)


def preprocessar_texto(texto: str, remover_stopwords: bool = False) -> str:
    palavras = re.findall(r"[a-záàâãéêíóôõúçü]+", texto.lower())
    if remover_stopwords:
        palavras = [palavra for palavra in palavras if palavra not in STOPWORDS]
    return " ".join(palavras)
