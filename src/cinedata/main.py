from .agent import agent


def main():
    question = input("Pergunta: ").strip()

    if not question:
        print("Digite uma pergunta.")
        return

    try:
        result = agent.run_sync(question)

        print("\nResposta:")
        print(result.output.answer)

        print("\nSQL utilizado:")
        print(result.output.sql)

    except Exception as error:
        print(f"Erro ao processar consulta: {error}")


if __name__ == "__main__":
    main()