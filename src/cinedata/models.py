from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    answer: str = Field(
        description="Resposta final para o usuário em linguagem natural."
    )

    sql: str = Field(
        description="Consulta SQL final utilizada para obter a resposta."
    )