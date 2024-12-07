from typing import Dict, List, Optional
import pandas as pd

def validate_csv_structure(df: pd.DataFrame) -> tuple[bool, Optional[str]]:
    """Validate the structure of the input CSV file."""
    required_columns = ['minutes']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    if df.empty:
        return False, "CSV file is empty"
    
    return True, None

def validate_batch_response(response: Dict) -> tuple[bool, Optional[str]]:
    """Validate the batch response structure."""
    required_fields = ['id', 'status']
    
    missing_fields = [field for field in required_fields if field not in response]
    if missing_fields:
        return False, f"Missing required fields in batch response: {', '.join(missing_fields)}"
    
    return True, None