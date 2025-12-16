"""Kroki HTTP client for diagram rendering."""

from typing import Literal
import httpx


OutputFormat = Literal["png", "svg", "pdf", "jpeg"]


class KrokiRenderError(Exception):
    """Exception raised when Kroki diagram rendering fails.
    
    This wraps HTTP errors from Kroki service with additional context
    about the diagram type and error details.
    """
    pass


class KrokiClient:
    """HTTP client for interacting with Kroki diagram rendering service.

    Kroki supports multiple diagram types (PlantUML, C4, Mermaid, etc.)
    and output formats (PNG, SVG, PDF).
    """

    DEFAULT_TIMEOUT = 30.0  # seconds

    def __init__(self, kroki_url: str) -> None:
        """Initialize Kroki client.

        Args:
            kroki_url: Base URL of Kroki service (e.g., http://localhost:8000)
        """
        self.kroki_url = kroki_url.rstrip("/")

    def render_diagram(
        self,
        diagram_source: str,
        diagram_type: str,
        output_format: OutputFormat = "png"
    ) -> bytes:
        """Render diagram source code to specified output format.

        Args:
            diagram_source: Source code of the diagram (e.g., PlantUML syntax)
            diagram_type: Type of diagram (plantuml, c4plantuml, mermaid, etc.)
            output_format: Desired output format (png, svg, pdf, jpeg)

        Returns:
            Rendered diagram as bytes

        Raises:
            KrokiRenderError: If Kroki returns an error status or request fails
        """
        # Kroki API endpoint: /{diagram_type}/{output_format}
        endpoint = f"{self.kroki_url}/{diagram_type}/{output_format}"

        try:
            # Make HTTP POST request with diagram source
            response = httpx.post(
                endpoint,
                json={"diagram_source": diagram_source},
                timeout=self.DEFAULT_TIMEOUT
            )

            # Raise exception if request failed
            response.raise_for_status()

            # Check Content-Type for error responses (Kroki returns text/plain on errors)
            content_type = response.headers.get('Content-Type', '')
            if 'text/plain' in content_type:
                error_message = response.text
                raise KrokiRenderError(
                    f"Kroki rendering failed for diagram type '{diagram_type}': {error_message}"
                )

            return response.content

        except httpx.HTTPStatusError as e:
            # Convert HTTP errors to custom exception with context
            raise KrokiRenderError(
                f"Kroki rendering failed for diagram type '{diagram_type}': "
                f"HTTP {e.response.status_code} - {e.response.text}"
            ) from e
