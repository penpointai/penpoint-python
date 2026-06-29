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

# Version is dynamic (setuptools_scm derives it from the git tag at build time
# and writes penpoint/_version.py). Read it from there; fall back when running
# from a source checkout that hasn't been built/tagged.
try:
    from ._version import version as __version__
except ImportError:  # pragma: no cover - source checkout without a build
    __version__ = "0.0.0+unknown"
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
