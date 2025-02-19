from prefect import task
import pandas as pd
from google.cloud import storage
import tempfile

@task
def update_gcs(cleaned_data):
    # Initialize GCS client
    client = storage.Client()
    bucket = client.get_bucket("stock-dat-bucket-1001")
    blob = bucket.blob("stock_data.csv")  # Assuming the name of the existing CSV file

    # Download the existing file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_download:
        blob.download_to_filename(tmp_download.name)
        
        # Read the existing CSV into a DataFrame
        existing_data = pd.read_csv(tmp_download.name)

    # Concatenate the existing data with the new data
    updated_data = pd.concat([existing_data, cleaned_data], ignore_index=True)

    # Save the updated data to another temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_upload:
        updated_data.to_csv(tmp_upload.name, index=False)
        
        # Upload the new file back to GCS, overwriting the existing one
        blob.upload_from_filename(tmp_upload.name)