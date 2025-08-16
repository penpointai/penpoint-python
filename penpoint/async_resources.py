"""Asynchronous resource classes for different API endpoints."""

from typing import Optional, Dict, Any, Union, BinaryIO

from .models import (
    File,
    FileList,
    DiscreteReferenceResponse,
    FileUploadRequest,
    FileUpdateRequest,
    DiscreteReferenceRequest,
    PaginationParams,
)
from .exceptions import PenpointValidationError


class AsyncBaseResource:
    """Base class for async API resources."""

    def __init__(self, client):
        self.client = client


class AsyncFilesResource(AsyncBaseResource):
    """Async resource for file-related operations."""

    async def list(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> FileList:
        """
        List files with pagination.

        Args:
            limit: Maximum number of files to return (default: 20)
            offset: Number of files to skip for pagination

        Returns:
            FileList object containing paginated results
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        data = await self.client.get("/files", params=params)

        # Convert to FileList object
        files = [File(**file_data) for file_data in data["data"]]
        return FileList(object=data["object"], has_more=data["has_more"], data=files)

    async def upload(
        self,
        file: Union[str, BinaryIO, bytes],
        filename: str,
        summary: Optional[str] = None,
    ) -> File:
        """
        Upload a file to the API.

        Args:
            file: File path, file-like object, or bytes
            filename: Name of the file
            summary: Optional description of the file

        Returns:
            File object representing the uploaded file
        """
        if not filename:
            raise PenpointValidationError("Filename is required")

        # Prepare form data
        files_data = {"file": (filename, file, "application/octet-stream")}
        data = {}

        if summary:
            data["summary"] = summary

        response_data = await self.client.post("/files", files=files_data, data=data)
        return File(**response_data)

    async def update(
        self, file_id: int, summary: str, expiration_date: Optional[str] = None
    ) -> File:
        """
        Update file metadata.

        Args:
            file_id: ID of the file to update
            summary: New description of the file
            expiration_date: Optional expiration date (YYYY-MM-DD format)

        Returns:
            Updated File object
        """
        if not summary:
            raise PenpointValidationError("Summary is required")

        data = {"summary": summary}
        if expiration_date:
            data["expirationDate"] = expiration_date

        response_data = await self.client.put(f"/files/{file_id}", json_data=data)
        return File(**response_data)

    async def delete(self, file_id: int) -> bool:
        """
        Delete a file.

        Args:
            file_id: ID of the file to delete

        Returns:
            True if deletion was successful
        """
        await self.client.delete(f"/files/{file_id}")
        return True

    async def get(self, file_id: int) -> File:
        """
        Get a specific file by ID.

        Args:
            file_id: ID of the file to retrieve

        Returns:
            File object
        """
        response_data = await self.client.get(f"/files/{file_id}")
        return File(**response_data)


class AsyncDiscreteReferencesResource(AsyncBaseResource):
    """Async resource for discrete reference operations."""

    async def basic(
        self,
        file_id: int,
        prompt: str,
        markup_file: bool,
        markup_color: Optional[str] = None,
    ) -> DiscreteReferenceResponse:
        """
        Perform basic discrete reference search.

        Args:
            file_id: ID of the file to search
            prompt: Search term or description
            markup_file: Whether to generate a marked-up file
            markup_color: Optional hex color for markup

        Returns:
            DiscreteReferenceResponse object
        """
        return await self._search_references(
            "/discrete-references/basic", file_id, prompt, markup_file, markup_color
        )

    async def standard(
        self,
        file_id: int,
        prompt: str,
        markup_file: bool,
        markup_color: Optional[str] = None,
    ) -> DiscreteReferenceResponse:
        """
        Perform standard discrete reference search.

        Args:
            file_id: ID of the file to search
            prompt: Search term or description
            markup_file: Whether to generate a marked-up file
            markup_color: Optional hex color for markup

        Returns:
            DiscreteReferenceResponse object
        """
        return await self._search_references(
            "/discrete-references/standard", file_id, prompt, markup_file, markup_color
        )

    async def advanced(
        self,
        file_id: int,
        prompt: str,
        markup_file: bool,
        markup_color: Optional[str] = None,
    ) -> DiscreteReferenceResponse:
        """
        Perform advanced discrete reference search.

        Args:
            file_id: ID of the file to search
            prompt: Search term or description
            markup_file: Whether to generate a marked-up file
            markup_color: Optional hex color for markup

        Returns:
            DiscreteReferenceResponse object
        """
        return await self._search_references(
            "/discrete-references/advanced", file_id, prompt, markup_file, markup_color
        )

    async def _search_references(
        self,
        endpoint: str,
        file_id: int,
        prompt: str,
        markup_file: bool,
        markup_color: Optional[str] = None,
    ) -> DiscreteReferenceResponse:
        """Internal method for performing reference searches."""
        if not prompt:
            raise PenpointValidationError("Prompt is required")

        data = {"fileId": file_id, "prompt": prompt, "markupFile": markup_file}

        if markup_color:
            data["markupColor"] = markup_color

        response_data = await self.client.post(endpoint, json_data=data)
        return DiscreteReferenceResponse(**response_data)
