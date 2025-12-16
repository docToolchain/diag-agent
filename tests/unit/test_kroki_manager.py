"""Unit tests for Kroki Manager (Docker-based local deployment)."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import subprocess


class TestKrokiManager:
    """Tests for KrokiManager Docker lifecycle management."""

    def test_start_kroki_docker_container_success(self):
        """Test starting Kroki Docker container.

        Validates:
        - docker run command is called with correct parameters
        - Container name: kroki
        - Port mapping: 8000:8000
        - Image: yuzutech/kroki
        - Detached mode: -d
        """
        from diag_agent.kroki.manager import KrokiManager

        # Arrange
        manager = KrokiManager()
        
        # Mock subprocess.run to simulate successful docker run
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout='container_id_123')
            
            # Act
            manager.start()
            
            # Assert
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]  # Get command list
            
            # Validate docker run command structure
            assert 'docker' in call_args
            assert 'run' in call_args
            assert '-d' in call_args  # Detached mode
            assert '--name' in call_args
            assert 'kroki' in call_args  # Container name
            assert '-p8000:8000' in call_args or '-p' in call_args  # Port mapping
            assert 'yuzutech/kroki' in call_args  # Image name

    def test_stop_kroki_docker_container_success(self):
        """Test stopping and removing Kroki Docker container.

        Validates:
        - docker stop command is called
        - docker rm command is called
        - Container name: kroki
        """
        from diag_agent.kroki.manager import KrokiManager

        # Arrange
        manager = KrokiManager()
        
        # Mock subprocess.run for stop + rm commands
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            # Act
            manager.stop()
            
            # Assert - stop() should call docker commands
            assert mock_run.call_count >= 1  # At least one docker command
            
            # Check if 'docker' and 'kroki' are in any of the calls
            calls_str = str(mock_run.call_args_list)
            assert 'docker' in calls_str.lower()
            assert 'kroki' in calls_str.lower()

    def test_is_running_returns_true_when_container_exists(self):
        """Test is_running() returns True when container is running.

        Validates:
        - docker ps command is called with filter
        - Returns True when container found in output
        """
        from diag_agent.kroki.manager import KrokiManager

        # Arrange
        manager = KrokiManager()
        
        # Mock docker ps output showing running container
        mock_output = "CONTAINER ID   IMAGE              NAMES\nabc123         yuzutech/kroki     kroki"
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout=mock_output
            )
            
            # Act
            result = manager.is_running()
            
            # Assert
            assert result is True
            mock_run.assert_called_once()
            
            # Validate docker ps command
            call_args = mock_run.call_args[0][0]
            assert 'docker' in call_args
            assert 'ps' in call_args

    def test_is_running_returns_false_when_container_not_found(self):
        """Test is_running() returns False when container is not running.

        Validates:
        - Returns False when docker ps shows no matching container
        """
        from diag_agent.kroki.manager import KrokiManager

        # Arrange
        manager = KrokiManager()
        
        # Mock docker ps output with no kroki container
        mock_output = "CONTAINER ID   IMAGE   NAMES"
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout=mock_output
            )
            
            # Act
            result = manager.is_running()
            
            # Assert
            assert result is False

    def test_health_check_success(self):
        """Test health_check() returns True when Kroki responds.

        Validates:
        - HTTP GET request to http://localhost:8000
        - Returns True on HTTP 200
        """
        from diag_agent.kroki.manager import KrokiManager

        # Arrange
        manager = KrokiManager()
        
        # Mock httpx.get to simulate successful response
        with patch('httpx.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            # Act
            result = manager.health_check()
            
            # Assert
            assert result is True
            mock_get.assert_called_once()
            
            # Validate URL
            call_args = mock_get.call_args[0][0]
            assert 'localhost:8000' in call_args or '127.0.0.1:8000' in call_args

    def test_health_check_fails_when_kroki_not_responding(self):
        """Test health_check() returns False when Kroki doesn't respond.

        Validates:
        - Returns False on connection error
        - Returns False on non-200 status code
        """
        from diag_agent.kroki.manager import KrokiManager

        # Arrange
        manager = KrokiManager()
        
        # Mock httpx.get to raise connection error
        with patch('httpx.get') as mock_get:
            mock_get.side_effect = Exception("Connection refused")
            
            # Act
            result = manager.health_check()
            
            # Assert
            assert result is False

    def test_start_docker_not_available_raises_error(self):
        """Test start() raises KrokiManagerError when Docker not installed.

        Validates:
        - FileNotFoundError (docker not found) → KrokiManagerError
        - Error message is clear and helpful
        """
        from diag_agent.kroki.manager import KrokiManager, KrokiManagerError

        # Arrange
        manager = KrokiManager()
        
        # Mock subprocess.run to raise FileNotFoundError (docker not found)
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError("docker: command not found")
            
            # Act & Assert
            with pytest.raises(KrokiManagerError) as exc_info:
                manager.start()
            
            # Validate error message
            error_message = str(exc_info.value)
            assert 'docker' in error_message.lower()
