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
    
    # Query database tables
    employees = db.query(HiredEmployee).all()
    departments = db.query(Department).all()
    jobs = db.query(Job).all()

    return {'data':'Hello Globant', 'employees': employees, 'departments':departments, 'jobs':jobs}


@app.post('/upload-csv/')
async def ingest_csv(departments_file: UploadFile = File(...), jobs_file: UploadFile = File(...), hired_employees_file: UploadFile = File(...), db: Session = Depends(get_db)):

    try:
        # Read CSV files to dataframes
        departments_df = pd.read_csv(StringIO((await departments_file.read()).decode('utf-8')), names=['id', 'name'], header=None)
        jobs_df = pd.read_csv(StringIO((await jobs_file.read()).decode('utf-8')), names=['id', 'name'], header=None)
        hired_employees_df = pd.read_csv(StringIO((await hired_employees_file.read()).decode('utf-8')), names=['id', 'name', 'datetime', 'department_id', 'job_id'], header=None)
        
        # Clean dataframes 
        cleaned_departments_df = clean_data(departments_df)
        cleaned_jobs_df = clean_data(jobs_df)
        cleaned_hired_employees_df = clean_data(hired_employees_df)

        # Convert data frames to dicts to enable batch inserts
        departments_dict = cleaned_departments_df.to_dict(orient="records")
        jobs_dict = cleaned_jobs_df.to_dict(orient="records")
        hired_employees_dict = cleaned_hired_employees_df.to_dict(orient="records")

        # Filter out data with existing ids before inserting
        departments_existing_ids = {d.id for d in db.query(Department.id).all()}
        filtered_departments = [
            d for d in departments_dict if d["id"] not in departments_existing_ids
        ]
        jobs_existing_ids = {j.id for j in db.query(Job.id).all()}
        filtered_jobs = [
            j for j in jobs_dict if j["id"] not in jobs_existing_ids
        ]
        employees_existing_ids = {e.id for e in db.query(HiredEmployee.id).all()}
        filtered_hired_employees = [
            e for e in hired_employees_dict if e["id"] not in employees_existing_ids
        ]

        # Insert data in batches up to 1000 rows
        try:
            BATCH_SIZE = 1000

            for i in range(0, len(filtered_departments), BATCH_SIZE):
                db.bulk_insert_mappings(Department, filtered_departments[i:i+BATCH_SIZE])

            for i in range(0, len(filtered_jobs), BATCH_SIZE):
                db.bulk_insert_mappings(Job, filtered_jobs[i:i+BATCH_SIZE])

            for i in range(0, len(filtered_hired_employees), BATCH_SIZE):
                db.bulk_insert_mappings(HiredEmployee, filtered_hired_employees[i:i+BATCH_SIZE])

            # save to database
            db.commit()

            return {"message": "Files uploaded and data inserted in batches successfully"}
        
        except Exception as e:
            # Rollback in case of error:
            db.rollback()
            return {'error':f'Database insertion failed with error: {e}'}


    except Exception as e:
        # Rollback in case of error:
        db.rollback()
        return {'error':f'Data ingestion failed with error: {e}'}