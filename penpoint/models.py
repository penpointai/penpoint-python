"""Data models for the Penpoint API."""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ReferenceMetadata:
    """Metadata for a reference part."""

    page: Optional[int] = None
    x: Optional[float] = None
    y: Optional[float] = None
    w: Optional[float] = None
    h: Optional[float] = None
    labels: List[str] = field(default_factory=list)


# This might need to change to a union of different reference types (audio, visual, text)
@dataclass
class ReferencePart:
    """A single reference part from a document."""

    id: int
    name: str
    segment: str
    metadata: ReferenceMetadata
    document_id: int
    page_number: int
    chunk_number: int
    vector_distance: float
    text_distance: float
    hybrid_score: float


@dataclass
class DiscreteReferenceResponse:
    """Response from discrete reference endpoints."""

    refs: Dict[str, List[ReferencePart]]


@dataclass
class File:
    """A file object from the API."""

    id: int
    name: str
    pages: Optional[int] = None
    summary: Optional[str] = None
    metadata: Optional[Any] = None
    expires_at: Optional[str] = None
    created_at: str = field(
        default_factory=lambda: datetime.now(datetime.timezone.utc).isoformat()
    )
    storage_location: Optional[str] = None
    company_id: Optional[int] = None
    size: Optional[str] = None
    deleted: Optional[bool] = None
    user_id: Optional[int] = None


@dataclass
class FileList:
    """Paginated list of files."""

    object: str
    has_more: bool
    data: List[File]


@dataclass
class FileUploadRequest:
    """Request for uploading a file."""

    file: Union[str, bytes, Any]  # File-like object or path
    filename: str
    summary: Optional[str] = None


@dataclass
class FileUpdateRequest:
    """Request for updating file metadata."""

    summary: str
    expiration_date: Optional[str] = None


@dataclass
class DiscreteReferenceRequest:
    """Request for discrete reference search."""

    file_id: int
    prompt: str
    markup_file: bool
    markup_color: Optional[str] = None


@dataclass
class PaginationParams:
    """Pagination parameters for list endpoints."""

    limit: Optional[int] = None
    offset: Optional[int] = None
