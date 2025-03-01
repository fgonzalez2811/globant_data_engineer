from fastapi.testclient import TestClient
from app.main import app, get_db

client = TestClient(app)

def test_upload_csv():
    url = "/upload-csv"
    files = {
    "departments_file": ("departments.csv", open("data/departments.csv", "rb"), "text/csv"),
    "jobs_file": ("jobs.csv", open("data/jobs.csv", "rb"), "text/csv"),
    "hired_employees_file": ("hired_employees.csv", open("data/hired_employees.csv", "rb"), "text/csv"),
    }
    response = client.post(url, files=files)
    assert response.status_code == 200  
    assert "message" in response.json()


def test_get_above_avg_hires():
    response = client.get('/hires-above-average-2021')
    data = response.json()
    assert response.status_code == 200
    assert 'message' in data
    assert 'data' in data
    
def test_get_quarterly_hires():
    response = client.get('/quarterly-hires-2021')
    data = response.json()
    assert response.status_code == 200
    assert 'message' in data
    assert 'data' in data