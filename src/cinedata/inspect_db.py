import sqlite3


DB_PATH = "cinerocket.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        """
    )

    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        print(f"\n=== {table} ===")

        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()

        for column in columns:
            cid, name, column_type, not_null, default_value, pk = column

            print(
                f"{name} | "
                f"type={column_type} | "
                f"not_null={not_null} | "
                f"pk={pk}"
            )

    cursor.execute(f"PRAGMA foreign_key_list({table})")
    foreign_keys = cursor.fetchall()

    if foreign_keys:
        print("Foreign keys:")

        for fk in foreign_keys:
            print(fk)

    cursor.execute(f"SELECT * FROM {table} LIMIT 3")
    rows = cursor.fetchall()

    print("Exemplos:")

    for row in rows:
        print(row)

    queries = [
        "SELECT DISTINCT tipo_pessoa FROM dim_people;",
        "SELECT DISTINCT nome_genero FROM dim_genres ORDER BY nome_genero;",
        "SELECT DISTINCT idioma_original FROM dim_movies ORDER BY idioma_original;",
        "SELECT DISTINCT status_filme FROM dim_movies ORDER BY status_filme;",
    ]

    for query in queries:
        cursor.execute(query)

        print(f"\n{query}")
        for row in cursor.fetchall():
            print(row)

    conn.close()


if __name__ == "__main__":
    main()