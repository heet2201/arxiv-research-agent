"""
Configuration settings for ArXiv Research Agent
"""
import os
from typing import Optional

class Config:
    """Configuration class for ArXiv Research Agent"""
    
    # API Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    SERPER_API_KEY: Optional[str] = os.getenv("SERPER_API_KEY")
    SEMANTIC_SCHOLAR_API_KEY: Optional[str] = os.getenv("SEMANTIC_SCHOLAR_API_KEY", None)
    
    # Model Configuration
    LLM_MODEL: str = "anthropic/claude-sonnet-4"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 5000
    LLM_TIMEOUT: int = 30
    
    # Search Configuration
    MAX_SEARCH_RESULTS: int = 20
    MAX_VISUAL_EXTRACTIONS: int = 3
    MAX_PAPERS_FOR_ANALYSIS: int = 3
    
    # UI Configuration
    GRADIO_SERVER_NAME: str = "0.0.0.0"
    GRADIO_SERVER_PORT: int = 7861
    GRADIO_SHARE: bool = True
    GRADIO_DEBUG: bool = True
    
    # Request Configuration
    REQUEST_TIMEOUT: int = 30
    RATE_LIMIT_DELAY: float = 1.0
    
    # Conversation Configuration
    MAX_CONVERSATION_HISTORY: int = 5
    
    @classmethod
    def get_headers(cls) -> dict:
        """Get request headers for API calls"""
        return {
            "Authorization": f"Bearer {cls.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://arxiv-research-agent.local",
            "X-Title": "ArXiv Research Agent"
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration"""
        if not cls.OPENROUTER_API_KEY or cls.OPENROUTER_API_KEY.startswith("your-"):
            raise ValueError("OPENROUTER_API_KEY is required. Please set it in environment variables or config.py")
        return True 
