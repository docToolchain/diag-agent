"""Unit tests for Settings configuration management."""

import pytest
from unittest.mock import patch
import os


class TestSettings:
    """Tests for Settings class."""

    def test_load_settings_with_defaults(self):
        """Test loading settings with default values when ENV vars not set.

        Validates that:
        - Settings can be instantiated without ENV vars
        - Default values are used for all config options
        - Defaults match .env.example specifications
        """
        from diag_agent.config.settings import Settings

        # Act - create Settings without any ENV vars set
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()

        # Assert - verify defaults from .env.example
        assert settings.llm_provider == "anthropic"
        assert settings.llm_model == "claude-sonnet-4"
        assert settings.kroki_mode == "local"
        assert settings.kroki_local_url == "http://localhost:8000"
        assert settings.max_iterations == 5
        assert settings.max_time_seconds == 60
        assert settings.log_level == "INFO"

    def test_load_settings_from_env(self):
        """Test loading settings from environment variables.

        Validates that:
        - ENV vars override defaults
        - All config categories can be set via ENV (LLM, Kroki, Agent, Output, Logging)
        - ENV var naming follows DIAG_AGENT_ prefix convention
        """
        from diag_agent.config.settings import Settings

        # Arrange - set ENV vars
        test_env = {
            "DIAG_AGENT_LLM_PROVIDER": "openai",
            "DIAG_AGENT_LLM_MODEL": "gpt-4",
            "DIAG_AGENT_KROKI_MODE": "remote",
            "DIAG_AGENT_MAX_ITERATIONS": "10",
            "DIAG_AGENT_LOG_LEVEL": "DEBUG",
        }

        # Act
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()

        # Assert
        assert settings.llm_provider == "openai"
        assert settings.llm_model == "gpt-4"
        assert settings.kroki_mode == "remote"
        assert settings.max_iterations == 10  # Type conversion: str → int
        assert settings.log_level == "DEBUG"
