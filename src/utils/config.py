import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # GitHub configuration
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.github_api_url = os.getenv("GITHUB_API_URL", "https://api.github.com")
        
        # Risk thresholds
        self.risk_auto_fix_threshold = float(os.getenv("RISK_AUTO_FIX_THRESHOLD", "0.3"))
        self.risk_human_review_threshold = float(os.getenv("RISK_HUMAN_REVIEW_THRESHOLD", "0.7"))
        
        # Server configuration
        self.server_host = os.getenv("SERVER_HOST", "0.0.0.0")
        self.server_port = int(os.getenv("SERVER_PORT", "8000"))
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        self._validate()

    def _validate(self):
        """Validate required configuration"""
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN is required")