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

        # Act - create Settings without any ENV vars set (mock load_dotenv to skip .env file)
        with patch.dict(os.environ, {}, clear=True), \
             patch("diag_agent.config.settings.load_dotenv"):
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

    def test_invalid_integer_value_uses_default(self):
        """Test that invalid integer values fall back to defaults gracefully.

        Validates that:
        - Invalid string values for integer settings don't crash
        - Settings class falls back to default value on conversion error
        - Clear error message is logged (optional)
        """
        from diag_agent.config.settings import Settings

        # Arrange - set invalid integer value
        test_env = {
            "DIAG_AGENT_MAX_ITERATIONS": "not_a_number",
        }

        # Act & Assert - should use default (5) instead of crashing
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            assert settings.max_iterations == 5  # Default value

    def test_kroki_url_returns_local_when_mode_local(self):
        """Test kroki_url property returns local URL when mode is 'local'.

        Validates that:
        - kroki_url property exists
        - When kroki_mode='local', returns kroki_local_url
        - Default mode is 'local'
        """
        from diag_agent.config.settings import Settings

        # Arrange - set mode=local explicitly
        test_env = {
            "DIAG_AGENT_KROKI_MODE": "local",
            "DIAG_AGENT_KROKI_LOCAL_URL": "http://localhost:8000",
            "DIAG_AGENT_KROKI_REMOTE_URL": "https://kroki.io",
        }

        # Act
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()

        # Assert
        assert settings.kroki_url == "http://localhost:8000"

    def test_kroki_url_returns_remote_when_mode_remote(self):
        """Test kroki_url property returns remote URL when mode is 'remote'.

        Validates that:
        - When kroki_mode='remote', returns kroki_remote_url
        - Remote URL is loaded from ENV correctly
        """
        from diag_agent.config.settings import Settings

        # Arrange - set mode=remote
        test_env = {
            "DIAG_AGENT_KROKI_MODE": "remote",
            "DIAG_AGENT_KROKI_LOCAL_URL": "http://localhost:8000",
            "DIAG_AGENT_KROKI_REMOTE_URL": "https://kroki.io",
        }

        # Act
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()

        # Assert
        assert settings.kroki_url == "https://kroki.io"

    def test_kroki_url_defaults_to_local_on_invalid_mode(self):
        """Test kroki_url property defaults to local URL on invalid mode.

        Validates that:
        - Invalid mode values (not 'local' or 'remote') fall back to local
        - No crashes on unexpected mode values
        - Graceful degradation
        """
        from diag_agent.config.settings import Settings

        # Arrange - set invalid mode
        test_env = {
            "DIAG_AGENT_KROKI_MODE": "invalid_mode",
            "DIAG_AGENT_KROKI_LOCAL_URL": "http://localhost:8000",
            "DIAG_AGENT_KROKI_REMOTE_URL": "https://kroki.io",
        }

        # Act
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()

        # Assert - should fall back to local
        assert settings.kroki_url == "http://localhost:8000"
