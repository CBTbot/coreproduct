# Configuration settings for CBT Chatbot

from pydantic import BaseModel


class CBTConfig(BaseModel):
    """Configuration for the CBT chatbot."""
    similarity_threshold: float = 0.85
    min_text_length: int = 3
    model_name: str = "en_core_web_md"
    max_retries: int = 3


# Global configuration instance
config: CBTConfig = CBTConfig()
