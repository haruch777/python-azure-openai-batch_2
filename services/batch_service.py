import time
from typing import Dict, Optional, Tuple
from openai import AzureOpenAI
from config import AzureConfig
from utils.logger import setup_logger
from utils.validation import validate_batch_response

logger = setup_logger(__name__)

class BatchService:
    def __init__(self, config: AzureConfig):
        self.client = config.get_client()
        self.deployment_name = config.deployment_name

    def submit_batch(self, input_file: str) -> Tuple[Optional[str], Optional[str]]:
        """Submit a batch processing job."""
        try:
            # Upload the JSONL file
            with open(input_file, 'rb') as f:
                file_upload = self.client.files.create(
                    file=f,
                    purpose='batch'
                )

            # Submit batch job
            batch_response = self.client.batches.create(
                input_file_id=file_upload.id,
                endpoint="/chat/completions",
                completion_window="24h",
            )
            
            # Validate response
            is_valid, error_msg = validate_batch_response(batch_response.model_dump())
            if not is_valid:
                return None, error_msg
            
            return batch_response.id, None
            
        except Exception as e:
            error_msg = f"Error submitting batch job: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    def get_batch_status(self, batch_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Get the status of a batch job."""
        try:
            status = self.client.batches.retrieve(batch_id).model_dump()
            return status, None
        except Exception as e:
            error_msg = f"Error retrieving batch status: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    def wait_for_completion(self, batch_id: str, check_interval: int = 60) -> Tuple[Optional[Dict], Optional[str]]:
        """Wait for batch job completion and return final status."""
        while True:
            status, error = self.get_batch_status(batch_id)
            if error:
                return None, error
            
            if status.get("status") in ["succeeded", "failed", "cancelled"]:
                return status, None
            
            logger.info(f"Batch job status: {status.get('status')} - Waiting {check_interval} seconds...")
            time.sleep(check_interval)