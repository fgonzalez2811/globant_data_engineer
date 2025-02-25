from fastapi import FastAPI
from contextlib import asynccontextmanager
from models import Department, Job, HiredEmployee
from database import Base, SessionLocal, engine
from datetime import datetime


# SQLAlchemy imports
from sqlalchemy.exc import SQLAlchemyError

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Create data tables from models if they don't exist:
    try:
        Base.metadata.create_all(engine) 
    except SQLAlchemyError as e:
        print(f'Error creating tables: {e}')
    
    yield 
    
app = FastAPI(lifespan=lifespan)

@app.get('/')
def index():
    # create session
    session = SessionLocal()
    
    # Create test instances in database:
    new_department = Department(name="Logistics")
    session.add(new_department)
    session.commit()
    
    new_job = Job(name="Manager")
    session.add(new_job)
    session.commit()
    
    new_employee = HiredEmployee(name="Jhon", datetime=datetime.now(), department_id=1, job_id=1)
    session.add(new_employee)
    session.commit()

    session.close()
    
    # Query database for employee: 'jhon'
    employees = session.query(HiredEmployee).all()

    return {'data':'Hello Globant', 'employees': employees}


 
   
    