# Globant Data Engineer Interview Assignment
Developer: Felipe González Vásquez

## Introduction
This project provides a REST API built with FastAPI for ingesting data from CSV files and storing it in a PostgreSQL database. The API allows users to upload CSV files, process and store the data, and retrieve it through query endpoints.

## Features
- Upload CSV files via REST API
- Insert batch transactions (1 up to 1000 rows) in a PostgreSQL database
- Query stored data with filter options

## Tech Stack
- FastAPI (API framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM for database interaction)
- Pydantic (Data validation)
- Docker (Containerization)