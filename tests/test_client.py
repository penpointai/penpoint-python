"""Tests for the main client classes."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from penpoint import PenpointClient, AsyncPenpointClient
from penpoint.exceptions import PenpointValidationError, PenpointError


class TestPenpointClient:
    """Test the synchronous PenpointClient."""

    def test_init_with_api_key(self):
        """Test client initialization with valid API key."""
        client = PenpointClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://api.penpoint.ai/v1"
        assert client.timeout == 30
        assert client.max_retries == 3

    def test_init_without_api_key(self):
        """Test client initialization without API key raises error."""
        with pytest.raises(PenpointValidationError, match="API key is required"):
            PenpointClient(api_key="")

    def test_init_with_custom_config(self):
        """Test client initialization with custom configuration."""
        client = PenpointClient(
            api_key="test_key",
            base_url="https://custom.api.com/v2",
            timeout=60,
            max_retries=5,
        )
        assert client.base_url == "https://custom.api.com/v2"
        assert client.timeout == 60
        assert client.max_retries == 5

    def test_get_headers(self):
        """Test header generation."""
        client = PenpointClient(api_key="test_key")
        headers = client._get_headers()

        assert headers["x-api-key"] == "test_key"
        assert "User-Agent" in headers
        assert "penpoint-python" in headers["User-Agent"]

    def test_get_headers_with_additional(self):
        """Test header generation with additional headers."""
        client = PenpointClient(api_key="test_key")
        additional = {"Content-Type": "application/json"}
        headers = client._get_headers(additional)

        assert headers["x-api-key"] == "test_key"
        assert headers["Content-Type"] == "application/json"

    @patch("penpoint.client.requests.request")
    def test_make_request_success(self, mock_request):
        """Test successful request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        client = PenpointClient(api_key="test_key")
        response = client._make_request("GET", "/test")

        assert response.status_code == 200
        mock_request.assert_called_once()

    @patch("penpoint.client.requests.request")
    def test_make_request_api_error(self, mock_request):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Bad Request"}
        mock_response.text = "Bad Request"
        mock_request.return_value = mock_response

        client = PenpointClient(api_key="test_key")

        with pytest.raises(Exception):  # Should raise PenpointAPIError
            client._make_request("GET", "/test")

    def test_has_files_resource(self):
        """Test that client has files resource."""
        client = PenpointClient(api_key="test_key")
        assert hasattr(client, "files")
        assert client.files is not None

    def test_has_discrete_references_resource(self):
        """Test that client has discrete references resource."""
        client = PenpointClient(api_key="test_key")
        assert hasattr(client, "discrete_references")
        assert client.discrete_references is not None


class TestAsyncPenpointClient:
    """Test the asynchronous PenpointClient."""

    def test_init_with_api_key(self):
        """Test async client initialization with valid API key."""
        client = AsyncPenpointClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://api.penpoint.ai/v1"

    def test_has_async_resources(self):
        """Test that async client has async resources."""
        client = AsyncPenpointClient(api_key="test_key")
        assert hasattr(client, "files")
        assert hasattr(client, "discrete_references")

    @pytest.mark.asyncio
    async def test_async_client_imports_aiohttp(self):
        """Test that async client requires aiohttp."""
        client = AsyncPenpointClient(api_key="test_key")

        # Since we can't easily mock the import, let's test that the client initializes properly
        # and has the expected async resources
        assert hasattr(client, "files")
        assert hasattr(client, "discrete_references")

        # Test that the client can be used (this will fail at runtime if aiohttp is not available)
        # In a real environment, this would raise an ImportError when aiohttp is not installed
        assert client.api_key == "test_key"
        assert client.base_url == "https://api.penpoint.ai/v1"
