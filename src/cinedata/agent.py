import os

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from .models import AgentResponse

from .database import (
    execute_query,
    get_distinct_values,
    get_table_info,
)

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

agent = Agent(
    f"openrouter:{MODEL_NAME}",
    output_type=AgentResponse,
    instructions="""
Você é um agente especialista em análise de dados da CineData Analytics.

Sua tarefa é responder perguntas sobre filmes usando exclusivamente os dados
disponíveis no banco SQLite.

Regras:
- Não invente dados.
- Use as ferramentas disponíveis para consultar o schema e os dados.
- Antes de responder, execute a consulta SQL necessária.
- Gere apenas consultas de leitura.
- O banco utiliza SQLite.
- Receita, faturamento e bilheteria devem ser tratados como conceitos equivalentes.
- No campo sql da resposta final, retorne a consulta SQL realmente utilizada.
- Nunca forneça uma resposta baseada apenas em conhecimento próprio.
- Toda resposta factual sobre os filmes deve vir de uma consulta executada no banco.
- Se uma consulta SQL retornar erro, analise a mensagem de erro, corrija a consulta e execute novamente.
- Nunca apresente ao usuário uma resposta baseada em uma consulta que falhou.
- Quando o usuário perguntar por receita, faturamento ou bilheteria sem especificar moeda, use receita_usd.
- Quando mencionar reais, R$ ou BRL, use receita_brl.
- Quando mencionar dólares, USD ou US$, use receita_usd.
"""
)

# Retorna o schema e exemplos de uma tabela do banco.
@agent.tool_plain
def tool_get_table_info(table_name: str) -> str:
    return get_table_info(table_name)

# Retorna valores distintos de uma coluna de uma tabela do banco.
@agent.tool_plain
def tool_get_distinct_values(
    table_name: str,
    column_name: str,
    limit: int = 50,
) -> list:
    return get_distinct_values(
        table_name,
        column_name,
        limit,
    )

# Executa uma consulta SQL no banco e retorna os resultados.
@agent.tool_plain
def tool_execute_query(query: str) -> dict:
    return execute_query(query)