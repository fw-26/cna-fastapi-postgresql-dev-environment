import os, psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, 
        autocommit=True, 
        row_factory=dict_row)

def migration():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            -- DROP TABLE IF EXISTS messages;

            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                message VARCHAR
            );

            -- lägg till nya kolumner här
            ALTER TABLE messages 
                ADD COLUMN IF NOT EXISTS author INT;
            ALTER TABLE messages 
                ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT now();
            ALTER TABLE messages 
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT now();

        """)