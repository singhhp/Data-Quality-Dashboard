import requests
import pandas as pd

# JSONPlaceholder API URL for todos
url = 'https://jsonplaceholder.typicode.com/todos'

# Make API request
response = requests.get(url)

# Check the status code of the response
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print("Data fetched successfully.")
    data = response.json()

    # Convert JSON data to pandas DataFrame
    df = pd.DataFrame(data)

    # Show first few rows of data
    print("Sample Data:")
    print(df.head())

    # Perform Data Quality Checks
    
    ## Completeness Check (check for missing values)
    missing_values = df.isnull().sum().sum()
    total_values = df.size
    completeness = ((total_values - missing_values) / total_values) * 100

    ## Uniqueness Check (check for duplicate IDs)
    duplicate_ids = df.duplicated(subset='id').sum()

    ## Validity Check (verify if 'completed' field is boolean)
    valid_completed = df['completed'].apply(lambda x: isinstance(x, bool)).sum()
    validity = (valid_completed / len(df)) * 100

    # Print Data Quality Results
    print("\nData Quality Checks:")
    print(f"Completeness: {completeness:.2f}%")
    print(f"Duplicate IDs: {duplicate_ids}")
    print(f"Validity of 'completed' field (boolean): {validity:.2f}%")

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
