from typing import Optional, Tuple
from config import AzureConfig
from services.csv_service import CSVService
from services.batch_service import BatchService
from services.result_service import ResultService
from utils.logger import setup_logger

logger = setup_logger(__name__)

def process_minutes() -> Tuple[bool, Optional[str]]:
    """Process meeting minutes using Azure OpenAI batch API."""
    try:
        # Initialize configuration
        config = AzureConfig()
        
        # Initialize services
        csv_service = CSVService()
        batch_service = BatchService(config)
        result_service = ResultService()
        
        # Read meeting minutes from CSV
        logger.info("Reading meeting minutes from CSV...")
        minutes_data, error = csv_service.read_meeting_minutes('meeting_minutes.csv')
        if error:
            return False, error

        # Prepare JSONL file for batch processing
        logger.info("Preparing batch input file...")
        input_file = "batch_input.jsonl"
        success, error = csv_service.prepare_batch_jsonl(minutes_data, input_file)
        if not success:
            return False, error

        # Submit batch job
        logger.info("Submitting batch job...")
        batch_id, error = batch_service.submit_batch(input_file)
        if error:
            return False, error

        logger.info(f"Batch job submitted successfully. Batch ID: {batch_id}")
        
        # Wait for completion and get final status
        logger.info("Waiting for batch job completion...")
        final_status, error = batch_service.wait_for_completion(batch_id)
        if error:
            return False, error
        
        # Handle results
        result_service.print_batch_status(final_status)
        output_file, error = result_service.save_results(final_status)
        if error:
            return False, error
            
        logger.info(f"\nResults have been saved to '{output_file}'")
        return True, None
        
    except Exception as e:
        error_msg = f"Unexpected error in main process: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def main():
    """Main entry point of the application."""
    success, error = process_minutes()
    if not success:
        logger.error(f"Process failed: {error}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())