"""Configuration management for diag-agent.

Loads settings from multiple sources with precedence:
1. Environment variables (highest priority)
2. .env file (loaded via python-dotenv)
3. Hardcoded defaults (lowest priority)
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Settings:
    """Application settings loaded from environment variables.
    
    All settings have defaults matching .env.example specifications.
    Environment variables use DIAG_AGENT_ prefix.
    """

    # LLM Configuration
    llm_provider: str
    llm_model: str
    
    # Kroki Configuration
    kroki_mode: str
    kroki_local_url: str
    
    # Agent Configuration
    max_iterations: int
    max_time_seconds: int
    
    # Logging
    log_level: str

    def __init__(self):
        """Initialize settings from environment variables with defaults."""
        # Load .env file if it exists (does not override existing ENV vars)
        load_dotenv()

        # LLM Configuration
        self.llm_provider = os.getenv("DIAG_AGENT_LLM_PROVIDER", "anthropic")
        self.llm_model = os.getenv("DIAG_AGENT_LLM_MODEL", "claude-sonnet-4")
        
        # Kroki Configuration
        self.kroki_mode = os.getenv("DIAG_AGENT_KROKI_MODE", "local")
        self.kroki_local_url = os.getenv(
            "DIAG_AGENT_KROKI_LOCAL_URL", 
            "http://localhost:8000"
        )
        
        # Agent Configuration
        self.max_iterations = self._get_int_env("DIAG_AGENT_MAX_ITERATIONS", 5)
        self.max_time_seconds = self._get_int_env("DIAG_AGENT_MAX_TIME_SECONDS", 60)
        
        # Logging
        self.log_level = os.getenv("DIAG_AGENT_LOG_LEVEL", "INFO")

    @staticmethod
    def _get_int_env(key: str, default: int) -> int:
        """Get integer value from environment variable with fallback to default.
        
        Args:
            key: Environment variable name
            default: Default value if ENV var not set or invalid
            
        Returns:
            Integer value from ENV or default if conversion fails
        """
        value = os.getenv(key)
        if value is None:
            return default
        
        try:
            return int(value)
        except ValueError:
            # Invalid integer value, fall back to default
            return default
