from prefect import flow
from tasks.fetch_data import fetch_data
from tasks.validate_data import validate_data
from tasks.preprocess_data import preprocess_data
from tasks.clean_data import clean_data
from tasks.store_gcs import store_gcs

@flow(name="Stock Pipeline")
def stock_pipeline():
    # 1. Fetch data
    processed_dfs = fetch_data()  # Rename from raw_data to processed_dfs
    
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
    
    # 4. Store in GCS
    store_gcs(cleaned_data)

if __name__ == "__main__":
    stock_pipeline()