from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import List
from contextlib import asynccontextmanager
from app.models import Department, Job, HiredEmployee
from app.database import Base, engine
from app.helpers import get_db, clean_data, get_invalid_rows
from io import StringIO
import pandas as pd

# SQLAlchemy imports
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):  
    # Create data tables from models if they don't exist:
    try:
        Base.metadata.create_all(engine) 
    except SQLAlchemyError as e:
        print(f'Error creating tables: {e}')
    
    yield 
    
app = FastAPI(lifespan=lifespan)

@app.get('/', include_in_schema=False)
def root():
    # Redirect root endpoint to docs:
    return RedirectResponse(url="/docs")

@app.get('/hires-above-average-2021')
def get_above_avg_hires(db: Session = Depends(get_db)):

    try:
        # Create Query to retrieve departments that hired above average in 2021:
        query = text("""
            WITH 
                     
            total_hires AS
                (SELECT d.id AS id, d.name AS department, COUNT(*) AS hire_count
                FROM departments d
                JOIN hired_employees e ON d.id = e.department_id
                WHERE EXTRACT(YEAR FROM e.datetime) = 2021
                GROUP BY d.id, d.name),
                     
            avg_hires AS 
                (SELECT AVG(hire_count) AS avg_value FROM total_hires)
                     
            SELECT th.id AS id, th.department AS department, th.hire_count AS hired
            FROM total_hires th
            WHERE hire_count > (SELECT avg_value FROM avg_hires)
            ORDER BY th.hire_count DESC;
            """)
        
        results = db.execute(query).fetchall()

        # check is there were results
        if not results:
            return {'message':'No records found'}
        else:
            # Unpack results into a dict
            columns = ["id", "department", "hired"]
            results_dict = [dict(zip(columns, row)) for row in results]

            return {'message': 'Data extracted succesfully', 'data': results_dict}

    except SQLAlchemyError as e:
        return {'message': 'There was an error retrieving the data', 'Error': f'{e}'}

@app.get('/quarterly-hires-2021')
def get_quarterly_hires(db: Session = Depends(get_db)):
    
    try:
        # Create SQL query to get number of employees hired in each quarter of 2021 per job per department:
        query = text(""" 
            SELECT 
            d.name AS Department, 
            j.name AS Job, 
            COUNT(CASE WHEN EXTRACT(MONTH FROM e.datetime) IN (1,2,3) THEN 1 END) AS Q1, 
            COUNT(CASE WHEN EXTRACT(MONTH FROM e.datetime) IN (4,5,6) THEN 1 END) AS Q2, 
            COUNT(CASE WHEN EXTRACT(MONTH FROM e.datetime) IN (7,8,9) THEN 1 END) AS Q3, 
            COUNT(CASE WHEN EXTRACT(MONTH FROM e.datetime) IN (10,11,12) THEN 1 END) AS Q4
            FROM departments d
            JOIN hired_employees e ON d.id = e.department_id
            JOIN jobs j ON e.job_id = j.id
            WHERE EXTRACT(YEAR FROM e.datetime) = 2021
            GROUP BY d.name, j.name
            ORDER BY d.name ASC, j.name ASC;""")
        
        # Excecute query
        results = db.execute(query).fetchall()
        
        # check is there were results
        if not results:
            return {'message':'No records found'}
        else:
            # Unpack results into a dict
            columns = ["Department", "Job", "Q1", "Q2", "Q3", "Q4"]
            results_dict = [dict(zip(columns, row)) for row in results]

            return {'message': 'Data extracted succesfully', 'data': results_dict}
    
    except SQLAlchemyError as e:
        return {'message': 'There was an error retrieving the data', 'Error': f'{e}'}

@app.post('/upload-csv')
async def ingest_csv(departments_file: UploadFile = File(...), 
                     jobs_file: UploadFile = File(...), 
                     hired_employees_file: UploadFile = File(...), 
                     db: Session = Depends(get_db)):

    try:
        # Read CSV files to dataframes
        departments_df = pd.read_csv(StringIO((await departments_file.read()).decode('utf-8')), names=['id', 'name'], header=None)
        jobs_df = pd.read_csv(StringIO((await jobs_file.read()).decode('utf-8')), names=['id', 'name'], header=None)
        hired_employees_df = pd.read_csv(StringIO((await hired_employees_file.read()).decode('utf-8')), names=['id', 'name', 'datetime', 'department_id', 'job_id'], header=None)
        
        # Clean dataframes 
        cleaned_departments_df = clean_data(departments_df)
        cleaned_jobs_df = clean_data(jobs_df)
        cleaned_hired_employees_df = clean_data(hired_employees_df)

        # Get invalid rows from uploaded files to log in the response:
        departments_invalid_rows = get_invalid_rows(departments_df)
        jobs_invalid_rows = get_invalid_rows(departments_df)
        employees_invalid_rows = get_invalid_rows(hired_employees_df)

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

            # count inserted and not inserted rows
            new_rows_count = len(filtered_hired_employees) + len(filtered_departments) + len(filtered_jobs)
            not_inserted_rows_count = sum(len(v) for v in employees_invalid_rows.values()) + sum(len(v) for v in departments_invalid_rows.values()) + sum(len(v) for v in jobs_invalid_rows.values())
            

            return {"message": f"Files uploaded and data inserted in batches successfully - {new_rows_count} total rows inserted and {not_inserted_rows_count} rows ignored",
                     "Ignored rows" : {"Departments": departments_invalid_rows,
                                   "Jobs": jobs_invalid_rows,
                                   "Hired Employees": employees_invalid_rows}}
        
        except Exception as e:
            # Rollback in case of error:
            db.rollback()
            return {'error':f'Database insertion failed with error: {e}'}


    except Exception as e:
        # Rollback in case of error:
        db.rollback()
        return {'error':f'Data ingestion failed with error: {e}'}