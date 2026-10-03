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


def execute_query(query: str) -> dict:
    normalized_query = query.strip().upper()

    for command in FORBIDDEN_COMMANDS:
        if command in normalized_query:
            raise ValueError(
                f"Comando SQL não permitido: {command}"
            )

    if not (
        normalized_query.startswith("SELECT")
        or normalized_query.startswith("WITH")
    ):
        raise ValueError(
            "Apenas consultas SELECT ou WITH são permitidas."
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        description[0]
        for description in cursor.description
    ]

    conn.close()

    return {
        "columns": columns,
        "rows": rows,
    }