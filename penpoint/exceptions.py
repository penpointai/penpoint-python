"""Custom exceptions for the Penpoint library."""


class PenpointError(Exception):
    """Base exception for all Penpoint-related errors."""

    pass


class PenpointAPIError(PenpointError):
    """Exception raised when the API returns an error response."""

    def __init__(
        self, message: str, status_code: int = None, response_data: dict = None
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

    def __str__(self):
        if self.status_code:
            return f"API Error {self.status_code}: {self.message}"
        return f"API Error: {self.message}"


class PenpointValidationError(PenpointError):
    """Exception raised when input validation fails."""

    pass


class PenpointConnectionError(PenpointError):
    """Exception raised when there's a connection error."""

    pass


class PenpointTimeoutError(PenpointError):
    """Exception raised when a request times out."""

    pass
