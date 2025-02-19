from prefect import flow
import pandas as pd
from tasks2.get_data import get_data
from tasks.validate_data import validate_data
from tasks.preprocess_data import preprocess_data
from tasks.clean_data import clean_data
from tasks2.update_gcs import update_gcs

@flow(name="Stock Pipeline Repeat")
def stock_pipeline():
    # 1. Fetch data
    processed_dfs = get_data()  # Rename from raw_data to processed_dfs
    
    # 2. Validate and preprocess data
    max_attempts = 10  # Limit the number of attempts to avoid infinite loops
    attempt = 0
    while attempt < max_attempts:
        validation = validate_data(processed_dfs)
        
        if all(result.success for result in validation):
            print(f"Data validation passed after {attempt + 1} attempts!")
            break
        else:
            print(f"Data validation failed for some or all expectations on attempt {attempt + 1}:")
            for i, result in enumerate(validation):
                if not result.success:
                    print(f"  Expectation {i} failed:")
                    print(f"    {result}")
            processed_dfs = preprocess_data(processed_dfs)  # Use processed_dfs here
            attempt += 1

    if attempt == max_attempts:
        print("Validation could not be resolved after maximum attempts. Data might still have issues.")
    
    # 3. Clean data
    # Note: You might want to adjust this based on what 'clean_data' does vs. 'preprocess_data'
    cleaned_data = clean_data(processed_dfs)

    # Before storing to GCS, format the date:
    cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date']).dt.strftime('%Y-%m-%d')
    
    # 4. Store in GCS
    update_gcs(cleaned_data)

if __name__ == "__main__":
    stock_pipeline()