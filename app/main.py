import os, psycopg
from fastapi import FastAPI
from psycopg.rows import dict_row
from app.migration import migration

migration()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, 
        autocommit=True, 
        row_factory=dict_row)

@app.get("/")
def read_root():
    return { "msg": "Hello!", "v": "0.1" }

@app.get("/messages")
def get_messages():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM messages
            ORDER BY id desc
        """)
        return cur.fetchall()


@app.get("/messages/{id}")
def read_item(id: int):
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM messages
                WHERE id = %s
            """, (id,))
            return cur.fetchone()
