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


def main():
    print(
        get_table_info("dim_movies")
    )

    print(
        get_distinct_values(
            "dim_people",
            "tipo_pessoa",
        )
    )

    print(
        execute_query(
            """
            SELECT titulo, ano_lancamento
            FROM dim_movies
            LIMIT 5
            """
        )
    )


if __name__ == "__main__":
    main()