# Globant Data Engineer Interview Assignment
Developer: Felipe González Vásquez

## Introduction
This project was developed as part of a Data Engineering interview assignment from Globant.

**The assignment consists of two sections:**

1. Building a local REST API that must:

     - Receive historical data from CSV files.
     - Upload these files to a new database.
     - Support batch inserts of 1 to 1,000 rows in a single request.
      
2. Exploring the inserted data and creating endpoints that provide the required insights for stakeholders.

The frameworks, libraries, databases or cloud services used are entirely up to me. In the following section, I will explain my tool stack choices.

## Tech Stack and Architecture

There are multiple valid approaches to building the requested solution. In this project, I propose two possible implementations:

1. **Lightweight Local Solution (implemented here):** a simple, efficient, and resource-friendly approach designed to handle the provided dataset (2,000 rows) with reasonable speed and minimal overhead.

2. **Scalable Cloud-Based Solution:** a more robust, cloud based, distributed architecture designed for significantly larger datasets (over 1 million rows). The architecture for this solution is outlined at the end of this document.

### Tech Stack:
- **FastAPI**: A high-performance API framework with asynchronous support, automatic documentation, and built-in data validation, making it ideal for scalable and efficient API development.
  
- **PostgreSQL**: A powerful, ACID-compliant relational database known for reliability, scalability, and strong support for complex queries, making it well-suited for structured data storage.
  
- **Pandas**: A versatile data manipulation library that efficiently processes CSV files; its in-memory operations are sufficient for this use case since the dataset size is not highly memory-intensive.
  
- **SQLAlchemy**: A flexible ORM that simplifies database interactions, offering both raw SQL capabilities and an abstraction layer for cleaner, maintainable code.
  
- **Pydantic**: Ensures strict data validation and serialization in FastAPI, reducing errors and improving API robustness.
  
- **Docker**: Provides a consistent, isolated environment for the application, making deployment across different systems seamless and predictable.
  
- **Docker Compose**: Manages multi-container setups efficiently, automating the deployment of FastAPI, PostgreSQL, and other dependencies in a single configuration.

## Installation and setup


1. Make sure you have docker installed, if not, install it:
     ```
     sudo apt update
     sudo apt install docker.io
     ```
2. Clone the repository
     ```
     git clone https://github.com/fgonzalez2811/globant_data_engineer.git
     ```
3. Create `.env` file and add credentials for database creation:
     ```
     POSTGRES_PASSWORD = <password>
     POSTGRES_USER = <username>
     POSTGRES_DB = <database_name>
     ```
4. Run docker compose to build the images and start the containers. Use this command:
     ```
     docker compose up --build
     ```
5. Access the documentation at http://127.0.0.1:8000/docs

## API Endpoints

### Upload CSV files

- **POST** `/upload-csv/`
  
     Uploads 3 csv files containing the 3 tables that will be added to the database. The 3 files must be sent in the same requests, this avoids inconsistencies with table relations. 

     **Request example:**
     ```
     curl -X POST "localhost:8000/upload-csv" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "departments_file=@files/departments.csv;type=text/csv" \
     -F "jobs_file=@files/Jobs.csv;type=text/csv" \
     -F "hired_employees_file=@files/hired_employees.csv;type=text/csv"
     ```
     **Response example:**
     ```JSON
     {"message":"Files uploaded and data inserted in batches successfully - 2124 total rows inserted and 70 rows ignored","Ignored rows":{"Departments":{"no_name_rows":[],"incomplete_rows":[]},"Jobs":{"no_name_rows":[],"incomplete_rows":[]},"Hired Employees":{"no_name_rows":[{"id":162,"name":null,"datetime":"2021-04-22T14:31:39Z","department_id":4.0,"job_id":91.0},{"id":340,"name":null,"datetime":"2022-01-13T21:09:49Z","department_id":4.0,"job_id":45.0},{"id":350,"name":null,"datetime":"2021-07-13T23:34:40Z","department_id":10.0,"job_id":86.0},{"id":571,"name":null,"datetime":"2021-11-28T02:28:40Z","department_id":7.0,"job_id":69.0},{"id":623,"name":null,"datetime":"2022-01-04T17:42:48Z","department_id":7.0,"job_id":48.0},
     """
     ...

     """
     ```

### Get list of jobs and departments with count of hires by quarter of 2021

- **GET** `/quarterly-hires-2021`
  
     **Request example:**
     ```
     curl -X 'GET' \
     'localhost:8000/quarterly-hires-2021' \
     -H 'accept: application/json'
     ```

     **Response example:**     
     ```JSON
     {
  "message": "Data extracted succesfully",
  "data": [
    {
      "Department": "Accounting",
      "Job": "Account Representative IV",
      "Q1": 1,
      "Q2": 0,
      "Q3": 0,
      "Q4": 0
    },
    {
      "Department": "Accounting",
      "Job": "Actuary",
      "Q1": 0,
      "Q2": 1,
      "Q3": 0,
      "Q4": 0
    },
    {
      "Department": "Accounting",
      "Job": "Analyst Programmer",
      "Q1": 0,
      "Q2": 0,
      "Q3": 1,
      "Q4": 0
    },
    {
      "Department": "Accounting",
      "Job": "Budget/Accounting Analyst III",
      "Q1": 0,
      "Q2": 1,
      "Q3": 0,
      "Q4": 0
    },
    {
      "Department": "Accounting",
      "Job": "Cost Accountant",
      "Q1": 0,
      "Q2": 1,
      "Q3": 0,
      "Q4": 0
    },
    """
    ...

    """
     ```


### Get list of departments and count of hires that were above average in 2021

- **GET** `/hires-above-average-2021`
     
     **Request example:**
     ```
     curl -X 'GET' \
     'localhost:8000/hires-above-average-2021' \
     -H 'accept: application/json'
     ```

     **Response example:** 
     ```JSON
     {
     "message": "Data extracted succesfully",
     "data": [
               {
                    "id": 8,
                    "department": "Support",
                    "hired": 216
               },
               {
                    "id": 5,
                    "department": "Engineering",
                    "hired": 205
               },
               {
                    "id": 6,
                    "department": "Human Resources",
                    "hired": 201
               },
               {
                    "id": 7,
                    "department": "Services",
                    "hired": 200
               },
               {
                    "id": 4,
                    "department": "Business Development",
                    "hired": 185
               },
               {
                    "id": 3,
                    "department": "Research and Development",
                    "hired": 148
               },
               {
                    "id": 9,
                    "department": "Marketing",
                    "hired": 142
               }
          ]
     }
     ```

## Database structure

### Database Schema

#### departments
  
     | Column  | Type  | Description |
     |---------|-------|-------------|
     | id      | INT   | Primary Key |
     | name    | TEXT  | Name of the department |

#### jobs
  
     | Column  | Type  | Description |
     |---------|-------|-------------|
     | id      | INT   | Primary Key |
     | name    | TEXT  | Name of the job position |

#### hired_employees
  
     | Column          | Type      | Description |
     |----------------|----------|-------------|
     | id            | INT      | Primary Key |
     | name          | TEXT     | Employee's full name |
     | datetime      | TIMESTAMP | Date and time of hiring |
     | department_id | INT      | Foreign Key → `departments(id)` |
     | job_id        | INT      | Foreign Key → `jobs(id)` |

## Files overview

1.  **`main.py`:** Contains the FastAPI REST API .
   
2.  **`helpers.py`:** Contains helper functions that are used in main.py
   
    - `get_db()`: Returns a database session for handling requests and closes it when the transactions finish.
    - `get_invalid_rows(df)`: Recevies a dataframe and returns a dictinary containing the rows of the dataframe that have invalid or incomplete data.
    - `clean_data(df)`: Receives a dataframe and performs transfromations and cleans the data before returning it.

3. **`models.py`**: Contains the PostgreSQL database models.
   
4. **`database.py`**: Sets up database connection and configures SQLAlchemy to be used as ORM for the project.