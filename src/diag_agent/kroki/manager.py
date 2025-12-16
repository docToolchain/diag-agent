"""Kroki Docker container lifecycle management.

Manages local Kroki deployment using Docker containers for privacy-focused,
local-first diagram rendering (ADR-003: Local-First with Docker).
"""

import subprocess
import httpx


class KrokiManagerError(Exception):
    """Exception raised when Kroki Docker management fails.
    
    This wraps Docker command errors and provides context about
    the operation that failed.
    """
    pass


class KrokiManager:
    """Manager for Kroki Docker container lifecycle.
    
    Provides methods to start, stop, and monitor a local Kroki
    server running in a Docker container. Uses the yuzutech/kroki
    image which includes all diagram libraries.
    """

    CONTAINER_NAME = "kroki"
    DOCKER_IMAGE = "yuzutech/kroki"
    DEFAULT_PORT = 8000
    HEALTH_CHECK_TIMEOUT = 5.0  # seconds

    def __init__(self, port: int = DEFAULT_PORT) -> None:
        """Initialize Kroki manager.
        
        Args:
            port: Port to expose Kroki service on (default: 8000)
        """
        self.port = port
        self.kroki_url = f"http://localhost:{port}"

    def start(self) -> None:
        """Start Kroki Docker container.
        
        Launches a detached Docker container with the Kroki service.
        The container is named 'kroki' and exposes the service on
        the configured port.
        
        Raises:
            KrokiManagerError: If Docker is not available or start fails
        """
        try:
            # Run docker container in detached mode
            subprocess.run(
                [
                    "docker", "run",
                    "-d",  # Detached mode
                    "--name", self.CONTAINER_NAME,
                    f"-p{self.port}:{self.DEFAULT_PORT}",  # Port mapping
                    self.DOCKER_IMAGE
                ],
                capture_output=True,
                text=True,
                check=True
            )
            
        except FileNotFoundError:
            raise KrokiManagerError(
                "Docker is not installed or not available in PATH. "
                "Please install Docker to use local Kroki deployment."
            )
        except subprocess.CalledProcessError as e:
            raise KrokiManagerError(
                f"Failed to start Kroki container: {e.stderr}"
            ) from e

    def stop(self) -> None:
        """Stop and remove Kroki Docker container.
        
        Stops the running container and removes it to free resources.
        Gracefully handles the case where the container doesn't exist.
        
        Raises:
            KrokiManagerError: If Docker is not installed
        """
        try:
            # Stop the container
            subprocess.run(
                ["docker", "stop", self.CONTAINER_NAME],
                capture_output=True,
                text=True,
                check=False  # Don't fail if already stopped
            )
            
            # Remove the container
            subprocess.run(
                ["docker", "rm", self.CONTAINER_NAME],
                capture_output=True,
                text=True,
                check=False  # Don't fail if already removed
            )
            
        except FileNotFoundError:
            raise KrokiManagerError(
                "Docker is not installed or not available in PATH."
            )

    def is_running(self) -> bool:
        """Check if Kroki container is currently running.
        
        Returns:
            True if container is running, False otherwise
        """
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={self.CONTAINER_NAME}", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Check if container name appears in output
            return self.CONTAINER_NAME in result.stdout
            
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def health_check(self) -> bool:
        """Check if Kroki service is responding to HTTP requests.
        
        Returns:
            True if Kroki responds successfully, False otherwise
        """
        try:
            response = httpx.get(
                self.kroki_url,
                timeout=self.HEALTH_CHECK_TIMEOUT
            )
            return response.status_code == 200
            
        except Exception:
            # Any connection error, timeout, etc. = not healthy
            return False
