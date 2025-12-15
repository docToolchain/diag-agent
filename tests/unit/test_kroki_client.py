"""Unit tests for Kroki HTTP client."""

import pytest
from unittest.mock import Mock, patch
import httpx


class TestKrokiClient:
    """Tests for KrokiClient class."""

    def test_render_diagram_success(self):
        """Test successful diagram rendering with Kroki API.

        Validates that:
        - HTTP POST is sent to correct Kroki endpoint
        - Request contains diagram_type, source, and output_format
        - PNG bytes are returned on success (200 OK)
        """
        from diag_agent.kroki.client import KrokiClient

        # Arrange
        kroki_url = "http://localhost:8000"
        diagram_source = "@startuml\nAlice -> Bob: Hello\n@enduml"
        diagram_type = "plantuml"
        output_format = "png"
        expected_png_bytes = b"\x89PNG\r\n\x1a\n"  # PNG magic bytes

        # Mock HTTP response
        with patch("httpx.post") as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.content = expected_png_bytes
            mock_post.return_value = mock_response

            # Act
            client = KrokiClient(kroki_url)
            result = client.render_diagram(
                diagram_source=diagram_source,
                diagram_type=diagram_type,
                output_format=output_format
            )

            # Assert
            assert result == expected_png_bytes
            mock_post.assert_called_once()

            # Verify request payload structure
            call_args = mock_post.call_args
            assert kroki_url in call_args[0][0]  # URL contains base URL
            assert diagram_type in call_args[0][0]  # URL contains diagram type
            assert output_format in call_args[0][0]  # URL contains output format

            # Verify source was sent in request
            request_data = call_args[1].get("json") or call_args[1].get("data")
            assert request_data is not None
            assert request_data.get("diagram_source") == diagram_source
