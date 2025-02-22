import os
from fastapi import FastAPI

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get('/')
def index():
    return {'data':'Hello Globant'}