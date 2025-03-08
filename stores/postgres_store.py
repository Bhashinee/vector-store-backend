import psycopg
from psycopg import sql
from pgvector.psycopg import register_vector


def add_to_pgvector(embeddings, host, password, user, dbname, table_name):
    # Connect to an existing database
    connection_string = f"host={host} user={user} password={password} dbname={dbname}"

    print(connection_string)

    embedding_size = len(embeddings[0]["embedding"])

    with psycopg.connect(connection_string) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
            register_vector(conn)

            add_to_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} (id bigserial PRIMARY KEY, text_segment VARCHAR(2048), embedding vector({embedding_size}))").format(table=sql.Identifier(table_name), embedding_size=sql.Identifier(str(embedding_size)))

            conn.execute(add_to_table_query)

            for chunk in embeddings:
                add_to_table_query = sql.SQL(
                    'INSERT INTO {table} (embedding, text_segment) VALUES (%s, %s)').format(
                        table=sql.Identifier(table_name),
                        )

                conn.execute(add_to_table_query, (chunk["embedding"], chunk["text_segment"]))

            # Make the changes to the database persistent
            conn.commit()

    return True
