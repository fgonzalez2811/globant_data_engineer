from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Department(Base):
    __tablename__= "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=False)

    hired_employees = relationship("HiredEmployee", back_populates= "departments_rel")

class Job(Base):
    __tablename__= "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=False)

    hired_employees = relationship("HiredEmployee", back_populates="job_rel")

class HiredEmployee(Base):
    __tablename__= "hired_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime)
    department_id = Column(Integer, ForeignKey("departments.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    department_rel = relationship("Department", back_populates="hired_employees")
    job_rel = relationship("Job", back_populates="hired_employees")