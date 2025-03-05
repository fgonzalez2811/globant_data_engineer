import pandas as pd
from app.helpers import clean_data, get_invalid_rows

def test_get_invalid_rows():
    data = {
        'name': ['Alice', None, 'Charlie', 'David'],
        'datetime': ['2024-01-01', '2024-02-02', None, '2024-04-04'],
        'job_id': [1, 2, 3, None],
        'department_id': [None, 2, 3, 4]
    }
    df = pd.DataFrame(data)

    result = get_invalid_rows(df)

    assert len(result['no_name_rows']) == 1 
    assert len(result['incomplete_rows']) == 3  

def test_clean_data():
    data = {
        'name': [' Alice ', 'Bob', None, 'David', 'Alice'],
        'datetime': ['2024-01-01', None, '2024-03-03', '2024-04-04', '2024-01-01'],
        'job_id': [1, 2, 3, None, 1],
        'department_id': [1, None, 3, 4, 1]
    }
    df = pd.DataFrame(data)

    cleaned_df = clean_data(df)

    assert cleaned_df.shape[0] == 2  
    assert pd.api.types.is_numeric_dtype(cleaned_df['job_id'])
    assert pd.api.types.is_numeric_dtype(cleaned_df['department_id'])

