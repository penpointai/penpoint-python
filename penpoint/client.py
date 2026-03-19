"""Main client classes for the Penpoint API."""

import json
import logging
import time
from typing import Optional, Dict, Any, Union, BinaryIO
import requests

logger = logging.getLogger("penpoint")

from .exceptions import (
    PenpointError,
    PenpointAPIError,
    PenpointValidationError,
    PenpointConnectionError,
    PenpointTimeoutError,
)
from .models import (
    File,
    FileList,
    DiscreteReferenceResponse,
    FileUploadRequest,
    FileUpdateRequest,
    DiscreteReferenceRequest,
    PaginationParams,
)
from .resources import FilesResource, DiscreteReferencesResource


class BaseClient:
    """Base client with common functionality."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.penpoint.ai/v1",
        timeout: int = 30,
        max_retries: int = 3,
    ):
        if not api_key:
            raise PenpointValidationError("API key is required")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

        # Initialize resources
        self.files = FilesResource(self)
        self.discrete_references = DiscreteReferencesResource(self)

    def _get_headers(
        self, additional_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """Get default headers with API key."""
        headers = {
            "x-api-key": self.api_key,
            "User-Agent": f"penpoint-python/{self._get_version()}",
        }
        if additional_headers:
            headers.update(additional_headers)
        return headers

    def _get_version(self) -> str:
        """Get the library version."""
        try:
            from . import __version__

            return __version__
        except ImportError:
            return "unknown"

    def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Make an HTTP request with retry logic."""
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(headers)

        logger.debug(
            "%s %s params=%s json=%s data_keys=%s files_keys=%s",
            method,
            url,
            params,
            json_data,
            list(data.keys()) if isinstance(data, dict) else type(data).__name__,
            list(files.keys()) if files else None,
        )

        for attempt in range(self.max_retries + 1):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    params=params,
                    data=data,
                    json=json_data,
                    files=files,
                    timeout=self.timeout,
                )

                logger.debug(
                    "%s %s -> %s %.500s",
                    method,
                    url,
                    response.status_code,
                    response.text,
                )

                if response.status_code >= 400:
                    self._handle_error_response(response, method, url)

                return response

            except requests.exceptions.Timeout:
                if attempt == self.max_retries:
                    raise PenpointTimeoutError(
                        f"Request timed out after {self.timeout} seconds"
                    )
                time.sleep(2**attempt)

            except requests.exceptions.ConnectionError as e:
                if attempt == self.max_retries:
                    raise PenpointConnectionError(f"Connection error: {e}")
                time.sleep(2**attempt)

            except requests.exceptions.RequestException as e:
                raise PenpointError(f"Request failed: {e}")

        raise PenpointError("Max retries exceeded")

    def _handle_error_response(
        self,
        response: requests.Response,
        method: str = "",
        url: str = "",
    ) -> None:
        """Handle error responses from the API."""
        try:
            error_data = response.json()
            message = (
                error_data.get("message")
                or error_data.get("error")
                or json.dumps(error_data)
            )
        except (ValueError, KeyError):
            error_data = {}
            message = response.text or "Unknown error"

        logger.error(
            "%s %s returned %s: %s",
            method,
            url,
            response.status_code,
            message,
        )

        raise PenpointAPIError(
            message=message,
            status_code=response.status_code,
            response_data=error_data,
        )


class PenpointClient(BaseClient):
    """Synchronous client for the Penpoint API."""

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a GET request."""
        return self._make_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a POST request."""
        return self._make_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a PUT request."""
        return self._make_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a DELETE request."""
        return self._make_request("DELETE", endpoint, **kwargs)


class AsyncPenpointClient(BaseClient):
    """Asynchronous client for the Penpoint API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        from .async_resources import AsyncFilesResource, AsyncDiscreteReferencesResource

        self.files = AsyncFilesResource(self)
        self.discrete_references = AsyncDiscreteReferencesResource(self)

    async def _make_async_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ):
        """Make an asynchronous HTTP request."""
        try:
            import aiohttp
        except ImportError:
            raise PenpointError(
                "aiohttp is required for async operations. Install with: pip install aiohttp"
            )

        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(headers)

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=request_headers,
                params=params,
                data=data,
                json=json_data,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as response:
                if response.status >= 400:
                    await self._handle_async_error_response(response)

                return await response.json()

    async def _handle_async_error_response(self, response):
        """Handle error responses from async requests."""
        try:
            error_data = await response.json()
            message = error_data.get("message", "Unknown error")
        except (ValueError, KeyError):
            message = await response.text() or "Unknown error"

        raise PenpointAPIError(
            message=message,
            status_code=response.status,
            response_data=error_data if "error_data" in locals() else {},
        )

    async def get(self, endpoint: str, **kwargs):
        """Make an asynchronous GET request."""
        return await self._make_async_request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs):
        """Make an asynchronous POST request."""
        return await self._make_async_request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs):
        """Make an asynchronous PUT request."""
        return await self._make_async_request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs):
        """Make an asynchronous DELETE request."""
        return await self._make_async_request("DELETE", endpoint, **kwargs)
