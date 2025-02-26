from fastapi import FastAPI, Depends, UploadFile, File
from typing import List
from contextlib import asynccontextmanager
from models import Department, Job, HiredEmployee
from database import Base, engine
from helpers import get_db, clean_data, get_invalid_rows
from io import StringIO
import pandas as pd

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


@app.get('/')
def index(db: Session = Depends(get_db)):
    
    # Query database for employees
    employees = db.query(HiredEmployee).all()

    return {'data':'Hello Globant', 'employees': employees}


@app.post('/upload-csv/')
async def ingest_csv(departments_file: UploadFile = File(...), jobs_file: UploadFile = File(...), hired_employees_file: UploadFile = File(...), db: Session = Depends(get_db)):

    try:
        # Read CSV files to dataframes
        departments_df = pd.read_csv(StringIO((await departments_file.read()).decode('utf-8')), names=['id', 'name'], header=None)
        jobs_df = pd.read_csv(StringIO((await jobs_file.read()).decode('utf-8')), names=['id', 'name'], header=None)
        hired_employees_df = pd.read_csv(StringIO((await hired_employees_file.read()).decode('utf-8')), names=['id', 'name', 'datetime', 'department_id', 'job_id'], header=None)

        print('Dataframes:')
        print(departments_df)
        print(jobs_df)
        print(hired_employees_df)
        

        # Clean and Convert data frames to dicts to enable batch inserts
        departments_dict = clean_data(departments_df).to_dict(orient="records")
        jobs_dict = clean_data(jobs_df).to_dict(orient="records")
        hired_employees_dict = clean_data(hired_employees_df).to_dict(orient="records")

        # Insert data in batches up to 1000 rows
        BATCH_SIZE = 1000

        for i in range(0, len(departments_dict), BATCH_SIZE):
            db.bulk_insert_mappings(Department, departments_dict[i:i+BATCH_SIZE])
        
        for i in range(0, len(jobs_dict), BATCH_SIZE):
            db.bulk_insert_mappings(Department, jobs_dict[i:i+BATCH_SIZE])

        for i in range(0, len(hired_employees_dict), BATCH_SIZE):
            db.bulk_insert_mappings(Department, hired_employees_dict[i:i+BATCH_SIZE])

        # save to database
        db.commit()

        return {"message": "Files uploaded and data inserted in batches successfully"}
   
    except Exception as e:
        # Rollback in case of error:
        db.rollback()
        return {'error':f'Data ingestion failed with error: {e}'}