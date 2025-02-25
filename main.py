from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from models import Department, Job, HiredEmployee
from database import Base, SessionLocal, engine
from datetime import datetime


# SQLAlchemy imports
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Create data tables from models if they don't exist:
    try:
        Base.metadata.create_all(engine) 
    except SQLAlchemyError as e:
        print(f'Error creating tables: {e}')
    
    yield 
    
app = FastAPI(lifespan=lifespan)

def get_db():
    # Create session:
    db = SessionLocal()
    
    # yield session and wait until transaction ends, then close session:
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index(db: Session = Depends(get_db)):
    
    # Query database for employees
    employees = db.query(HiredEmployee).all()

    return {'data':'Hello Globant', 'employees': employees}


 
   
    