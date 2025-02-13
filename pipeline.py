from prefect import flow
from tasks.fetch_data import fetch_data
# from tasks.validate_data import validate_data
from tasks.clean_data import clean_data
from tasks.store_gcs import store_gcs

@flow(name="Stock Pipeline")
def stock_pipeline():
    # 1. Fetch data
    raw_data = fetch_data()
    
    # 2. Validate data
    # validation = validate_data(raw_data)
    
    # if not validation.success:
    #     raise ValueError("Data validation failed!")
    
    # 3. Clean data
    # cleaned_data = clean_data(raw_data)
    
    # 4. Store in GCS
    store_gcs(raw_data)

if __name__ == "__main__":
    stock_pipeline()