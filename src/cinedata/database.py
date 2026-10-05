import sqlite3


DB_PATH = "cinerocket.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

FORBIDDEN_COMMANDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "REPLACE",
]

MAX_ROWS = 100

# Retorna informações sobre uma tabela do banco, incluindo o schema e exemplos de linhas.
def get_table_info(table_name: str) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    )

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return f"Tabela '{table_name}' não encontrada."

    create_statement = result[0]

    cursor.execute(
        f"SELECT * FROM {table_name} LIMIT 3"
    )
    rows = cursor.fetchall()

    conn.close()

    return (
        f"Schema:\n{create_statement}\n\n"
        f"Exemplos:\n{rows}"
    )

# Retorna valores distintos de uma coluna de uma tabela do banco, limitando a quantidade de resultados.
def get_distinct_values(
    table_name: str,
    column_name: str,
    limit: int = 50,
) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT DISTINCT {column_name}
        FROM {table_name}
        WHERE {column_name} IS NOT NULL
        LIMIT ?
    """

    cursor.execute(query, (limit,))
    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]

# Limpa a consulta SQL removendo blocos de código e espaços em branco desnecessários.
def clean_query(query: str) -> str:
    query = query.strip()

    if query.startswith("```"):
        lines = query.splitlines()

        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        query = "\n".join(lines).strip()

    return query

# Executa uma consulta SQL no banco e retorna os resultados, garantindo que apenas consultas de leitura sejam permitidas.
def execute_query(query: str) -> dict:
    query = clean_query(query)

    normalized_query = query.strip().upper()

    for command in FORBIDDEN_COMMANDS:
        if command in normalized_query:
            return {
                "success": False,
                "error": f"Comando SQL não permitido: {command}",
            }

    if not (
        normalized_query.startswith("SELECT")
        or normalized_query.startswith("WITH")
    ):
        return {
            "success": False,
            "error": "Apenas consultas SELECT ou WITH são permitidas.",
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        columns = [
            description[0]
            for description in cursor.description
        ]

        rows = cursor.fetchmany(MAX_ROWS)

        return {
            "success": True,
            "columns": columns,
            "rows": rows,
        }

    except sqlite3.Error as error:
        return {
            "success": False,
            "error": str(error),
        }

    finally:
        conn.close()