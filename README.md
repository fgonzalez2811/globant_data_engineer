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
