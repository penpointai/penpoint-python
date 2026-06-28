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


# --- Canonical cross-modal reference contract (penpoint.ref/1) ---------------
# Mirror of the backend's lib/ai/discreteReferences/canonical.ts and the JS SDK.
# Prefer these over the loose ReferencePart/ReferenceMetadata shape.
PENPOINT_REF_SCHEMA_VERSION = "penpoint.ref/1"


@dataclass
class ReferenceLocator:
    """Unified locator. ``type`` is one of pdf|image|tabular|audio|text; only the
    fields relevant to that type are populated.

    - pdf / image: ``page`` (1-indexed) + ``bbox`` ([x, y, w, h], fractional)
    - tabular:     ``row`` (1-indexed, header = row 1)
    - audio:       ``start_time`` / ``end_time`` (seconds)
    - text:        ``position`` (vertical fraction)
    """

    type: str
    page: Optional[int] = None
    bbox: Optional[List[float]] = None
    row: Optional[int] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    position: Optional[float] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ReferenceLocator":
        return cls(
            type=d.get("type", "text"),
            page=d.get("page"),
            bbox=d.get("bbox"),
            row=d.get("row"),
            start_time=d.get("startTime"),
            end_time=d.get("endTime"),
            position=d.get("position"),
        )


@dataclass
class CanonicalReference:
    """A single citation in the penpoint.ref/1 contract."""

    id: str
    segment: str
    confidence: Optional[float]
    locator: ReferenceLocator

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CanonicalReference":
        return cls(
            id=str(d.get("id", "")),
            segment=d.get("segment", ""),
            confidence=d.get("confidence"),
            locator=ReferenceLocator.from_dict(d.get("locator", {})),
        )


@dataclass
class DiscreteReferenceResponse:
    """Response from discrete reference endpoints."""

    # Legacy reference shape — still emitted for back-compat. Kept as raw dicts so
    # parsing tolerates the differing per-pipeline part fields.
    refs: Dict[str, List[Any]]
    # penpoint.ref/1 — present on current servers; prefer this.
    schema_version: Optional[str] = None
    abstained: Optional[bool] = None
    references: Optional[List[CanonicalReference]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DiscreteReferenceResponse":
        """Tolerant parse: ignores the response's extra fields (document, cached,
        chargedCost, …) and maps the canonical block when present."""
        refs = data.get("refs") or {"parts": []}
        canonical = data.get("references")
        return cls(
            refs=refs,
            schema_version=data.get("schemaVersion"),
            abstained=data.get("abstained"),
            references=(
                [CanonicalReference.from_dict(r) for r in canonical]
                if canonical is not None
                else None
            ),
        )


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
