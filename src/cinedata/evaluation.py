from .agent import agent


QUESTIONS = [
    # Bilheteria e finanças
    "Quais são os 10 filmes com maior receita em reais?",
    "Qual é o lucro médio por gênero, considerando apenas filmes com receita informada?",
    "Quais filmes possuem a maior margem de lucro entre os que têm receita e orçamento informados?",

    # Popularidade e engajamento
    "Quais são os 5 filmes mais populares?",
    "Qual filme possui a maior diferença absoluta entre nota TMDB e nota IMDb?",
    "Qual é a nota média IMDb por ano de lançamento?",

    # Elenco e equipe
    "Qual ator teve mais participações em filmes lançados nos últimos 5 anos?",
    "Quais diretores possuem maior nota média IMDb, considerando apenas diretores com pelo menos 5 filmes?",
    "Qual dupla ator-diretor trabalhou junta mais vezes?",

    # Gêneros e produtoras
    "Quantos filmes existem por gênero?",
    "Qual produtora possui o maior lucro total?",
    "Qual gênero possui a maior margem de lucro média?",

    # Avaliações dos usuários
    "Quais são os filmes mais avaliados pelos usuários?",
    "Quais filmes possuem maior divergência entre a nota média dos usuários e a nota IMDb?",
]


EXPECTED_PATTERNS = {
    QUESTIONS[0]: [
        "receita_brl",
        "ORDER BY",
        "LIMIT 10",
    ],
    QUESTIONS[1]: [
        "dim_genres",
        "fact_movies_performance",
        "AVG",
    ],
    QUESTIONS[2]: [
        "receita",
        "orcamento",
        "ORDER BY",
    ],
    QUESTIONS[3]: [
        "popularidade",
        "ORDER BY",
        "LIMIT 5",
    ],
    QUESTIONS[4]: [
        "ABS",
        "nota_tmdb",
        "nota_imdb",
    ],
    QUESTIONS[5]: [
        "nota_imdb",
        "ano_lancamento",
        "AVG",
    ],
    QUESTIONS[6]: [
        "dim_people",
        "bridge_movie_person",
        "Ator",
    ],
    QUESTIONS[7]: [
        "Diretor",
        "AVG",
        "HAVING",
    ],
    QUESTIONS[8]: [
        "Ator",
        "Diretor",
    ],
    QUESTIONS[9]: [
        "dim_genres",
        "COUNT",
    ],
    QUESTIONS[10]: [
        "dim_companies",
        "lucro",
        "SUM",
    ],
    QUESTIONS[11]: [
        "dim_genres",
        "orcamento",
        "lucro",
    ],
    QUESTIONS[12]: [
        "dim_reviews",
        "qtd_avaliacoes_usuarios",
    ],
    QUESTIONS[13]: [
        "nota_media_usuarios",
        "nota_imdb",
        "ABS",
    ],
}


def evaluate_sql(question: str, sql: str) -> list[str]:
    warnings = []

    expected_patterns = EXPECTED_PATTERNS.get(
        question,
        [],
    )

    normalized_sql = sql.upper()

    for pattern in expected_patterns:
        if pattern.upper() not in normalized_sql:
            warnings.append(
                f"Esperado encontrar '{pattern}' no SQL."
            )

    return warnings


def main():
    passed = 0
    failed = 0
    with_warnings = 0

    for index, question in enumerate(QUESTIONS, start=1):
        print()
        print(f"Teste {index}/{len(QUESTIONS)}")
        print(question)

        try:
            result = agent.run_sync(question)

            print("\nResposta:")
            print(result.output.answer)

            print("\nSQL utilizado:")
            print(result.output.sql)

            warnings = evaluate_sql(
                question,
                result.output.sql,
            )

            if warnings:
                with_warnings += 1

                print("\nAvisos:")

                for warning in warnings:
                    print(f"- {warning}")

            else:
                print("\nValidação básica: OK")
                passed += 1

        except Exception as error:
            failed += 1

            print("\nERRO:")
            print(error)

    print("\n" + "=" * 70)
    print("RESUMO DA AVALIAÇÃO")
    print(f"Validações sem avisos: {passed}")
    print(f"Casos com avisos: {with_warnings}")
    print(f"Erros de execução: {failed}")
    print(f"Total de perguntas: {len(QUESTIONS)}")

    print(
        "Esta avaliação verifica padrões SQL; "
        "não comprova a correção dos resultados."
    )


if __name__ == "__main__":
    main()