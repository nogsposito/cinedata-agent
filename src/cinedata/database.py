import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "cinerocket.db"

MAX_ROWS = 100


def get_connection():
    if not DB_PATH.is_file():
        raise FileNotFoundError(
            "Coloque cinerocket.db na raiz do projeto."
        )

    conn = sqlite3.connect(
        DB_PATH.as_uri() + "?mode=ro",
        uri=True,
    )

    conn.execute("PRAGMA query_only = ON")

    # Interrompe consultas excessivamente caras.
    # Não representa um limite exato de tempo.
    budget = [0]

    def progress():
        budget[0] += 1
        return int(budget[0] > 10000)

    conn.set_progress_handler(progress, 1000)

    return conn


def quote_identifier(value):
    return '"' + value.replace('"', '""') + '"'


def validate_table(conn, table_name):
    result = conn.execute(
        """
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    ).fetchone()

    if result is None:
        raise ValueError(
            f"Tabela '{table_name}' não encontrada."
        )

    return result[0]


def get_table_info(table_name: str) -> str:
    conn = None

    try:
        conn = get_connection()

        schema = validate_table(conn, table_name)

        rows = conn.execute(
            f"SELECT * FROM {quote_identifier(table_name)} LIMIT 3"
        ).fetchall()

        return (
            f"Schema:\n{schema}\n\n"
            f"Exemplos:\n{rows}"
        )

    except (sqlite3.Error, ValueError, OSError) as error:
        return f"Erro ao consultar tabela: {error}"

    finally:
        if conn is not None:
            conn.close()


def get_distinct_values(
    table_name: str,
    column_name: str,
    limit: int = 50,
) -> list:
    conn = None

    try:
        conn = get_connection()

        validate_table(conn, table_name)

        columns = {
            row[1]
            for row in conn.execute(
                f"PRAGMA table_info({quote_identifier(table_name)})"
            )
        }

        if column_name not in columns:
            return [
                f"Erro: coluna '{column_name}' não encontrada."
            ]

        limit = max(1, min(int(limit), MAX_ROWS))

        column = quote_identifier(column_name)
        table = quote_identifier(table_name)

        rows = conn.execute(
            f"""
            SELECT DISTINCT {column}
            FROM {table}
            WHERE {column} IS NOT NULL
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [row[0] for row in rows]

    except (
        sqlite3.Error,
        ValueError,
        TypeError,
        OSError,
    ) as error:
        return [f"Erro ao consultar valores: {error}"]

    finally:
        if conn is not None:
            conn.close()


def clean_query(query: str) -> str:
    query = query.strip()

    if query.startswith("```"):
        lines = query.splitlines()[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        query = "\n".join(lines).strip()

    return query


def execute_query(query: str) -> dict:
    query = clean_query(query)

    first_word = (
        query.split(None, 1)[0].upper()
        if query
        else ""
    )

    if first_word not in {"SELECT", "WITH"}:
        return {
            "success": False,
            "error": "Apenas consultas SELECT ou WITH são permitidas.",
        }

    conn = None

    try:
        conn = get_connection()

        allowed = {
            sqlite3.SQLITE_SELECT,
            sqlite3.SQLITE_READ,
            sqlite3.SQLITE_FUNCTION,
        }

        if hasattr(sqlite3, "SQLITE_RECURSIVE"):
            allowed.add(sqlite3.SQLITE_RECURSIVE)

        def authorize(
            action,
            arg1,
            arg2,
            database,
            source,
        ):
            if (
                action == sqlite3.SQLITE_FUNCTION
                and (arg2 or "").lower() == "load_extension"
            ):
                return sqlite3.SQLITE_DENY

            if action in allowed:
                return sqlite3.SQLITE_OK

            return sqlite3.SQLITE_DENY

        conn.set_authorizer(authorize)

        cursor = conn.execute(query)

        if cursor.description is None:
            return {
                "success": False,
                "error": "A consulta não retornou dados.",
            }

        rows = cursor.fetchmany(MAX_ROWS + 1)

        return {
            "success": True,
            "columns": [
                item[0]
                for item in cursor.description
            ],
            "rows": rows[:MAX_ROWS],
            "truncated": len(rows) > MAX_ROWS,
        }

    except (sqlite3.Error, ValueError, OSError) as error:
        return {
            "success": False,
            "error": str(error),
        }

    finally:
        if conn is not None:
            conn.close()