# RELATORIO — Análise de Sentimento com PLN

**Nome:Victor Schanth da Silva** 
**Repositório:https://github.com/victorschnath/sentimento-pln-ap2** 
**Data:17/11/2026** 

> Responda cada pergunta com **4 a 12 linhas**, com suas palavras e usando números dos arquivos de `resultados/`. Apague as instruções em itálico ao entregar.

## Tabela-resumo (preencha com os seus resultados)

| Config | Stopwords | Vetorizador | Vocabulário | Acurácia CV (média ± desvio) | F1 CV (média ± desvio) |
| A | mantidas | BoW | 425 | 0,8410 ± 0,0714 | 0,8401 ± 0,0755 |
| B | mantidas | TF-IDF | 425 |	0,8205 ± 0,0917 | 0,8189 ± 0,0900 |
| C | removidas | BoW | 404 | 0,8462 ± 0,0827 | 0,8459 ± 0,0865 |
| D | removidas | TF-IDF | 404 | 0,8410 ± 0,0817 | 0,8422 ± 0,0843 |

**Configuração escolhida:** C **Acurácia no teste:** 84,62% **F1 no teste:** 0,8529

---

## 1. Pré-processamento
*Quais decisões você tomou (minúsculas, pontuação, números, stopwords)? Qual o tamanho do vocabulário com e sem remoção de stopwords? O que você fez com a palavra "não" e por quê?*

Coloquei todos os textos em letras minúsculas, retirei a pontuação e os números e mantive os acentos. Depois separei cada texto em palavras para que elas pudessem ser representadas por números e usadas pelo modelo. Também defini uma lista com 30 stopwords e deixei a remoção delas opcional para comparar os resultados com e sem essas palavras. Mantendo as stopwords o vocabulário do treino ficou com 425 palavras diferentes, removendo elas ficou com 404. Decidi manter a palavra “não” porque ela faz diferença no sentido da frase por exemplo se ela fosse retirada de “não gostei”, sobraria apenas “gostei”, mudando uma opinião negativa para positiva.

## 2. BoW vs. TF-IDF
*Compare as quatro configurações levando em conta o desvio padrão. As diferenças são relevantes? Qual você escolheu e com base em quê? Explique a diferença conceitual entre as duas representações.*

O Bag of Words conta quantas vezes cada palavra aparece no texto já o TF-IDF leva em conta também em quantos textos ela aparece dando menos peso as palavras muito comuns no conjunto. Mantendo as stopwords a configuração A teve F1 médio de 0,8401 ± 0,0755, enquanto B ficou com 0,8189 ± 0,0900. Sem as stopwords C chegou a 0,8459 ± 0,0865 e D a 0,8422 ± 0,0843. Escolhi a configuração C que usa BoW com remoção de stopwords, porque ela apresentou o maior F1 médio na validação cruzada. Sua acurácia média também foi a maior com 0,8462 ± 0,0827. Mesmo assim os resultados ficaram próximos e os desvios mostram uma variação considerável entre as divisões. Por isso C foi a melhor opção, mas não da para afirmar que será melhor em qualquer situação.

## 3. Avaliação no teste
*Mostre a matriz de confusão e interprete precisão, recall e F1 de cada classe. Para uma loja, qual erro é mais grave: classificar uma reclamação como elogio ou o contrário? Por que a acurácia é menos enganosa aqui do que no exemplo de fraude da Aula 8?*

| Previsto | Negativo | Positivo |
| Negativo | 26 | 7 |
| Positivo | 3 | 29 |

O modelo acertou 55 das 65 avaliações com acurácia de 84,62%. A matriz mostrou 26 negativas e 29 positivas corretas além de sete negativas classificadas como positivas e três positivas como negativas. Nos negativos, precisão foi 0,8966 recall foi 0,7879 e F1 foi 0,8387, nos positivos precisão foi 0,8056 recall foi 0,9062 e F1 foi 0,8529. Isso mostra maior recall para avaliações positivas e maior precisão nas previsões negativas. Para a loja considero pior classificar reclamações como elogios pois problemas dos clientes podem passar despercebidos. A acurácia é menos enganosa aqui porque tem 130 avaliações de cada classe. Em um cenário com poucas fraudes um modelo poderia ter acurácia alta apenas prevendo a classe mais comum, sem detectar as fraudes.

## 4. Validação cruzada vs. divisão única
*Por que a validação cruzada é mais confiável do que um único conjunto de teste para comparar configurações? Por que a escolha não pode ser feita olhando o teste? O que seria vazamento de dados neste trabalho e como você o evitou?*

Separei os dados em 195 avaliações para treino e 65 para teste mantendo a proporção entre as classes e usando random_state=42. No treino usei validação cruzada com cinco partes, em cada rodada, quatro foram usadas para treinar e uma para validar permitindo comparar as médias e os desvios dos resultados, isso deixa a comparação menos dependente de uma única divisão dos dados. Escolhi a configuração com base nessa validação e deixei o teste para a avaliação final, porque usar ele na escolha poderia favorecer um modelo que funciona melhor especificamente naquele conjunto. Para evitar vazamento de dados usei uma Pipeline, que faz o vetorizador aprender o vocabulário somente com o treino de cada rodada. Ajustar com todos os dados antes dessa divisão faria informações da validação ou do teste influenciarem o treinamento.

## 5. Análise de erros e palavras influentes
*Escolha 3 textos de `erros.csv` e explique por que o modelo pode ter errado. Observe as 10 palavras mais influentes de cada classe: há alguma que não carrega sentimento por si só (ex.: palavra funcional ou de domínio)? O que isso diz sobre o que o modelo realmente aprendeu?*

O modelo errou dez avaliações no teste, a  frase “Panela de péssima qualidade, a comida gruda e queima” foi classificada como positiva. Nesse caso “gruda” e “queima” não estavam no vocabulário enquanto palavras como “panela” e “qualidade” contribuíram para a previsão positiva. Já “Aula dinâmica e interessante, aprendi muito em pouco tempo” foi classificada como negativa. As palavras “dinâmica” e “interessante” ficaram fora do vocabulário, e “pouco” e “tempo” tiveram pesos negativos. Em “Cheguei animado, mas me arrependi, tudo estava sujo”, a previsão foi positiva: “arrependi” não estava no vocabulário, enquanto “tudo” teve bastante peso positivo. Olhando as palavras mais influentes vi que termos como “bastante”, “tudo”, “mais” e “dinheiro” não indicam um sentimento por si só. Isso mostra que o modelo aprendeu associações entre palavras e sentimentos nos dados de treino mas não entende completamente o sentido das frases.

## 6. Casos difíceis e limitações
*Com base em `casos_dificeis_predicoes.csv`, como o modelo se saiu em negação, ironia e frases mistas? Explique por que BoW/TF-IDF têm essa limitação, proponha duas melhorias (cite técnicas vistas na Aula 11) e discuta duas limitações do dataset e um risco de usar este modelo em produção.*

Nos casos difíceis o modelo acertou duas das quatro frases de negação e duas das três frases de ironia. Por exemplo “Que ótimo, o produto chegou quebrado” foi classificada como positiva, mesmo sendo uma reclamação. Os dois casos mistos foram classificados como positivos e o neutro como negativo porque o modelo só consegue escolher entre essas duas classes. Considerando os dez casos com resposta esperada positiva ou negativa foram sete acertos. Como o modelo trabalha com palavras isoladas, ele tem dificuldade para entender a ordem das palavras e o contexto da frase. Para melhorar eu testaria bigramas que representam pares de palavras e um tratamento específico para negação. Outra limitação é o conjunto ter apenas 260 avaliações com parte delas gerada por padrões, o que pode deixar os resultados melhores do que seriam com dados reais. Em uma loja isso poderia fazer reclamações serem classificadas como elogios e ficarem sem atendimento.

---

## Declaração de uso de IA

Marque uma opção e complete:

- [ ] Não usei IA generativa em nenhuma parte deste trabalho.
- [X] Usei IA generativa **somente** para: Ajuda com o Readme.me, tirar dúvidas e com o Github (não é permitido gerar código ou relatório).
