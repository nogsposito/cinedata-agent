import os

from dotenv import load_dotenv
from httpx2 import query
from pydantic_ai import Agent

from .database import get_distinct_values, execute_query

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

agent = Agent(
    f"openrouter:{MODEL_NAME}"
)

from .agent import agent


def main():
    question = input("Pergunta: ")

    result = agent.run_sync(question)

    print("\nResposta:")
    print(result.output.answer)

    print("\nSQL utilizado:")
    print(result.output.sql)


if __name__ == "__main__":
    main()