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
            mock_response.headers = {"Content-Type": "image/png"}
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

    def test_render_diagram_http_error(self):
        """Test diagram rendering fails gracefully on HTTP errors.

        Validates that:
        - Kroki HTTP errors (500, 404, etc.) are caught
        - Custom KrokiRenderError is raised with clear message
        - Error message includes status code and diagram type
        """
        from diag_agent.kroki.client import KrokiClient, KrokiRenderError

        # Arrange
        kroki_url = "http://localhost:8000"
        diagram_source = "@startuml\nAlice -> Bob\n@enduml"
        diagram_type = "plantuml"
        output_format = "png"

        # Mock HTTP error response (500 Internal Server Error)
        with patch("httpx.post") as mock_post:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "500 Server Error",
                request=Mock(),
                response=mock_response
            )
            mock_post.return_value = mock_response

            # Act & Assert
            client = KrokiClient(kroki_url)
            with pytest.raises(KrokiRenderError) as exc_info:
                client.render_diagram(
                    diagram_source=diagram_source,
                    diagram_type=diagram_type,
                    output_format=output_format
                )

            # Verify error message contains useful context
            error_msg = str(exc_info.value)
            assert "500" in error_msg  # Status code
            assert diagram_type in error_msg  # Diagram type for debugging

    def test_render_diagram_text_plain_error(self):
        """Test diagram rendering detects text/plain errors (HTTP 200 with error text).

        Validates that:
        - Kroki returns HTTP 200 with Content-Type: text/plain on syntax errors
        - KrokiRenderError is raised despite 200 status code
        - Error message includes the Kroki error text from response body
        - This catches syntax errors that Kroki reports via text/plain
        """
        from diag_agent.kroki.client import KrokiClient, KrokiRenderError

        # Arrange
        kroki_url = "http://localhost:8000"
        diagram_source = "@startuml\nInvalid syntax here\n@enduml"
        diagram_type = "plantuml"
        output_format = "png"
        
        # Kroki error message in response body
        kroki_error_text = "Syntax error in diagram source at line 2"

        # Mock HTTP response: 200 OK but Content-Type: text/plain (error case)
        with patch("httpx.post") as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {"Content-Type": "text/plain; charset=utf-8"}
            mock_response.text = kroki_error_text
            mock_response.content = kroki_error_text.encode('utf-8')
            # raise_for_status() would NOT raise on 200
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response

            # Act & Assert
            client = KrokiClient(kroki_url)
            with pytest.raises(KrokiRenderError) as exc_info:
                client.render_diagram(
                    diagram_source=diagram_source,
                    diagram_type=diagram_type,
                    output_format=output_format
                )

            # Verify error message contains Kroki error details
            error_msg = str(exc_info.value)
            assert kroki_error_text in error_msg  # Kroki error message
            assert diagram_type in error_msg  # Diagram type for debugging
