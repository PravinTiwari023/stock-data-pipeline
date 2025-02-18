from prefect import task
import pandas as pd
from google.cloud import storage
import tempfile

@task
def store_gcs(cleaned_data):
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        cleaned_data.to_csv(tmp.name, index=False)
        
    # Upload to GCS
    client = storage.Client()
    bucket = client.get_bucket("stock-dat-bucket-1001")
    blob = bucket.blob(f"stock_data_{pd.Timestamp.now()}.csv")
    blob.upload_from_filename(tmp.name)