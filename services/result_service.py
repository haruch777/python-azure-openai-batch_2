from datetime import datetime
from typing import Dict, Optional
from utils.logger import setup_logger
from utils.file_utils import save_json

logger = setup_logger(__name__)

class ResultService:
    @staticmethod
    def save_results(results: Dict, output_file: str = None) -> Tuple[Optional[str], Optional[str]]:
        """Save batch processing results to a JSON file."""
        try:
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f'batch_results_{timestamp}.json'

            save_json(results, output_file)
            return output_file, None
            
        except Exception as e:
            error_msg = f"Error saving results: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    @staticmethod
    def print_batch_status(status: Dict):
        """Print batch processing status."""
        logger.info("\nBatch Processing Status:")
        logger.info("-" * 50)
        logger.info(f"Status: {status.get('status', 'Unknown')}")
        logger.info(f"Created at: {status.get('created_at', 'Unknown')}")
        
        if status.get('error'):
            logger.error(f"Error: {status['error']}")
        
        if status.get('metrics'):
            metrics = status['metrics']
            logger.info("\nMetrics:")
            logger.info(f"Total files: {metrics.get('total_files', 0)}")
            logger.info(f"Completed files: {metrics.get('completed_files', 0)}")
            logger.info(f"Failed files: {metrics.get('failed_files', 0)}")
            
        logger.info("-" * 50)