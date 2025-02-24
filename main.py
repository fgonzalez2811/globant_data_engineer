from fastapi import FastAPI
from contextlib import asynccontextmanager
from models import Department, Job, HiredEmployee
from database import Base, SessionLocal, engine
import datetime


# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

@app.get('/')
def index():
    # create session
    session = SessionLocal()

    # Create test instances in database:
    new_department = Department(id=1, department="Logistics")
    new_job = Job(id=1, job="Manager")
    new_employee = HiredEmployee(name="Jhon", datetime=datetime.now(), department_id=1, job_id=1)

    session.add(new_department, new_job, new_employee)
    session.commit()

    # Query database for employee: 'jhon'
    employees = session.query(HiredEmployee).all()

    return {'data':'Hello Globant', 'employees': employees[0].name}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastAPI app...")

    # Create database from models if doesn't exist:
    Base.metadata.create_all(engine) 
    
    yield 
    
    print("Shutting down FastAPI app...")
    
    