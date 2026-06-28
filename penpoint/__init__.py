"""
Penpoint Python Client Library

Official Python client library for the Penpoint API.
"""

from .client import PenpointClient, AsyncPenpointClient
from .exceptions import PenpointError, PenpointAPIError, PenpointValidationError
from .models import (
    File,
    FileList,
    DiscreteReferenceResponse,
    ReferencePart,
    ReferenceMetadata,
    CanonicalReference,
    ReferenceLocator,
    PENPOINT_REF_SCHEMA_VERSION,
)

__version__ = "0.4.0"
__all__ = [
    "PenpointClient",
    "AsyncPenpointClient",
    "PenpointError",
    "PenpointAPIError",
    "PenpointValidationError",
    "File",
    "FileList",
    "DiscreteReferenceResponse",
    "ReferencePart",
    "ReferenceMetadata",
    "CanonicalReference",
    "ReferenceLocator",
    "PENPOINT_REF_SCHEMA_VERSION",
]
