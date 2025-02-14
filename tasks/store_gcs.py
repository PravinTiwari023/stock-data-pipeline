from prefect import task
import pandas as pd
from google.cloud import storage
import tempfile
# import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\pc\Desktop\Automation Tutorial\Python GCP APACHE Airflow\Data Pipeline\stock-data-pipeline\Keys\python-stock-data-pipeline-bdf682d3a54e.json"

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