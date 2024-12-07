import json
from typing import Any, Dict
from pathlib import Path

def ensure_directory(directory: str) -> None:
    """Ensure the specified directory exists."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def save_json(data: Any, filepath: str, ensure_dir: bool = True) -> None:
    """Save data to a JSON file."""
    if ensure_dir:
        ensure_directory(str(Path(filepath).parent))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filepath: str) -> Dict:
    """Load data from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)