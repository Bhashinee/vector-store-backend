import psycopg
from pgvector.psycopg import register_vector


def add_to_pgvector(embeddings, host, port, password, user, dbname, table_name):
    # Connect to an existing database
    connection_string = f"host={host} port={port} user={user} password={password} dbname={dbname}"

    with psycopg.connect(connection_string) as conn:

        # Open a cursor to perform database operations
        with conn.cursor() as cur:

            conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
            register_vector(conn)

            conn.execute('CREATE TABLE IF NOT EXISTS %s (id bigserial PRIMARY KEY, text_segment VARCHAR(2048),  embedding vector(1536))', (table_name))

            for embedding in embeddings:
                conn.execute('INSERT INTO items (embedding, text_segment) VALUES (%s, %s)', (embedding["values"], embedding["text_segment"]))

            # Make the changes to the database persistent
            conn.commit()

    return True
