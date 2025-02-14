import logging
from datetime import datetime
import os
from prefect import flow, get_run_logger
from prefect.tasks import exponential_backoff
from typing import Optional
from google.cloud.exceptions import GoogleCloudError
from tasks.fetch_data import fetch_data
from tasks.validate_data import validate_data
from tasks.clean_data import clean_data
from tasks.store_gcs import store_gcs

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("stock_pipeline")

# Environment variables (set in GitHub Secrets/GCP)
REQUIRED_ENV_VARS = {
    "GCP_CREDENTIALS": "GCP service account credentials",
    "GCS_BUCKET_NAME": "Target GCS bucket name",
    # "SLACK_WEBHOOK_URL": "Slack alert webhook (optional)"
}

def validate_environment():
    """Check required environment variables are set"""
    missing = [var for var in REQUIRED_ENV_VARS if var not in os.environ]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

# def send_alert(message: str):
#     """Send incident notification to Slack"""
#     # Implement your alert mechanism (Slack, Email, PagerDuty)
#     pass

@flow(
    name="Stock Pipeline",
    description="End-to-end stock data processing pipeline",
    version=os.getenv("GIT_COMMIT_SHA", "1.0.0"),
    log_prints=True
)
def stock_pipeline():
    """Main pipeline execution flow"""
    try:
        # 0. Initial setup
        validate_environment()
        logger.info("Pipeline started")
        start_time = datetime.now()

        # 1. Fetch data
        raw_data = fetch_data.with_options(
            retries=3,
            retry_delay_seconds=exponential_backoff(backoff_factor=10),
        )(retry_window=3)
        
        if raw_data.empty:
            logger.error("No data fetched from source")
            raise ValueError("Empty dataset received from yfinance")

        # 2. Validate data
        # validation_result = validate_data.with_options(
        #     retries=2,
        #     retry_delay_seconds=30
        # )(raw_data)
        
        # if not validation_result.success:
        #     logger.critical("Data validation failed", extra={
        #         "failed_expectations": validation_result.statistics["unsuccessful_expectations"]
        #     })
        #     send_alert("Data validation failed - check expectations report")
        #     raise ValueError("Data quality check failed")

        # 3. Clean data
        # cleaned_data = clean_data.with_options(
        #     retries=2
        # )(raw_data)
        
        # 4. Store in GCS
        store_gcs.with_options(
            retries=3,
            retry_delay_seconds=[10, 30, 60],
        )(cleaned_data, bucket_name=os.getenv("GCS_BUCKET_NAME"))

        # Pipeline metrics
        duration = datetime.now() - start_time
        logger.info(
            "Pipeline completed successfully",
            extra={
                "duration_seconds": duration.total_seconds(),
                "processed_records": len(cleaned_data)
            }
        )

    except Exception as e:
        logger.exception("Pipeline failed with critical error")
        send_alert(f"Pipeline failed: {str(e)}")
        raise
    finally:
        # Cleanup resources if needed
        pass

if __name__ == "__main__":
    stock_pipeline()