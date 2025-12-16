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
    kroki_remote_url: str
    
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
        self.kroki_remote_url = os.getenv(
            "DIAG_AGENT_KROKI_REMOTE_URL",
            "https://kroki.io"
        )
        
        # Agent Configuration
        self.max_iterations = self._get_int_env("DIAG_AGENT_MAX_ITERATIONS", 5)
        self.max_time_seconds = self._get_int_env("DIAG_AGENT_MAX_TIME_SECONDS", 60)
        
        # Logging
        self.log_level = os.getenv("DIAG_AGENT_LOG_LEVEL", "INFO")

    @property
    def kroki_url(self) -> str:
        """Get Kroki URL based on configured mode.

        Returns local or remote URL depending on kroki_mode setting.
        Falls back to local URL if mode is invalid.

        Returns:
            Kroki service URL (local or remote based on mode)
        """
        if self.kroki_mode == "remote":
            return self.kroki_remote_url
        # Default to local (mode=="local" or invalid mode)
        return self.kroki_local_url

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
