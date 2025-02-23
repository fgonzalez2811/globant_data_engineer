import os
from fastapi import FastAPI
import psycopg2

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
    print(conn)
    cur = conn.cursor()
    cur.execute("SELECT 'Postgre Responding'")
    message = cur.fetchall()
    cur.close()
    conn.close()
    return {'data':'Hello Globant', 'message':message}

    