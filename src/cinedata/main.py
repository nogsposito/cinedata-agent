import os

from dotenv import load_dotenv
from httpx2 import query
from pydantic_ai import Agent

from .database import get_distinct_values, execute_query

from .config import OPENROUTER_API_KEY

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

agent = Agent(
    f"openrouter:{MODEL_NAME}"
)

from .database import (
    execute_query,
    get_distinct_values,
    get_table_info,
)


from .agent import agent


def main():
    result = agent.run_sync(
        "Quais são os 5 filmes com maior receita em reais?"
    )

    print(result.output)

if __name__ == "__main__":
    main()