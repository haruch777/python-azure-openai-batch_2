import pandas as pd
from typing import List, Dict, Optional, Tuple
from utils.logger import setup_logger
from utils.validation import validate_csv_structure

logger = setup_logger(__name__)

class CSVService:
    @staticmethod
    def read_meeting_minutes(file_path: str) -> Tuple[Optional[List[Dict[str, str]]], Optional[str]]:
        """Read and validate meeting minutes from CSV file."""
        try:
            df = pd.read_csv(file_path)
            
            # Validate CSV structure
            is_valid, error_msg = validate_csv_structure(df)
            if not is_valid:
                return None, error_msg
            
            return df.to_dict('records'), None
            
        except Exception as e:
            error_msg = f"Error reading CSV file: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    @staticmethod
    def prepare_batch_jsonl(minutes_data: List[Dict[str, str]], output_path: str) -> Tuple[bool, Optional[str]]:
        """Prepare JSONL file for batch processing."""
        try:
            system_prompt = """あなたは議事録を分析し、データマネジメントコンサルティングの需要があるかどうかを判断するAIです。以下の基準に基づいて判断してください：

需要ありの指標（'Yes'と回答）：
- データ品質の向上への関心
- データガバナンスのニーズ
- データ統合の要件
- データ可視化のニーズ
- 効率的なデータ活用への意欲
- データ駆動型の意思決定への注力
- データシステムに関する技術的専門知識の必要性
- データシステムの最適化への関心

需要なしの指標（'No'と回答）：
- 現行のデータシステムへの満足
- 社内のデータ管理能力が十分
- 現状維持への注力
- 他の事業分野の優先
- データ関連の緊急課題がない
- 既存のデータ管理体制が充実

'Yes'または'No'のみで回答してください。"""

            with open(output_path, 'w', encoding='utf-8') as f:
                for row in minutes_data:
                    messages = [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": f"この議事録に基づいて、データマネジメントコンサルティングの需要はありますか？議事録: {row['minutes']}"
                        }
                    ]
                    batch_item = {
                        "messages": messages,
                        "temperature": 0,
                        "max_tokens": 3
                    }
                    f.write(f"{pd.io.json.dumps(batch_item)}\n")
            return True, None
            
        except Exception as e:
            error_msg = f"Error preparing JSONL file: {str(e)}"
            logger.error(error_msg)
            return False, error_msg