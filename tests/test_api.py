"""Live API integration tests for the Penpoint client.

These tests hit the real Penpoint API and require PENPOINT_API_KEY to be set.
They are skipped entirely when the key is absent.
"""

import io
import logging
import os
import time
from datetime import datetime, timedelta

import pytest

from penpoint import PenpointClient
from penpoint.models import DiscreteReferenceResponse, File

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("penpoint").setLevel(logging.DEBUG)

pytestmark = pytest.mark.skipif(
    not os.environ.get("PENPOINT_API_KEY"),
    reason="PENPOINT_API_KEY not set",
)

SEARCH_PROMPT = "document reference search"

REFERENCE_PART_KEYS = {
    "id",
    "segment",
    "metadata",
    "page_number",
}

TEST_MARKDOWN = """\
# Penpoint Integration Test Document

## Overview

This document is used for automated integration testing of the Penpoint API client library.
It contains several sections with varied content to ensure that discrete reference search
can locate relevant passages across different effort levels.

## Document Reference Search

Penpoint provides a powerful document reference search API that allows developers to upload
files, index their contents, and perform semantic searches to find relevant passages. The
API supports three effort levels: basic, standard, and advanced.

## Features and Capabilities

- **File Upload**: Supports uploading documents in various formats including PDF, Markdown,
  and plain text. Each uploaded file is processed and indexed for search.
- **Metadata Management**: Files can be annotated with summaries and expiration dates to
  help organize and manage document lifecycles.
- **Discrete References**: The core search functionality returns discrete references,
  which are specific segments of the document that are relevant to the search query.

## Technical Details

The reference search engine uses a hybrid approach combining vector similarity and text
matching. Each reference part includes a vector distance score, a text distance score,
and a combined hybrid score. Results are returned as a dictionary keyed by reference
identifiers, with each value being a list of matching segments.

## Conclusion

This test document provides enough structured content for the integration test suite to
verify that upload, update, search, and delete operations work correctly end-to-end.
"""

SUMMARY = "Automated integration test document for the Penpoint Python client library."


def assert_reference_shape(response):
    """Validate the structure of a DiscreteReferenceResponse."""
    assert isinstance(response, DiscreteReferenceResponse)
    assert isinstance(response.refs, dict)
    assert "parts" in response.refs, f"Expected 'parts' key, got {list(response.refs.keys())}"
    parts = response.refs["parts"]
    assert isinstance(parts, list), f"Expected list for 'parts', got {type(parts)}"
    assert len(parts) > 0, "Expected at least one reference part"
    for part in parts:
        assert isinstance(part, dict), f"Expected dict, got {type(part)}"
        assert REFERENCE_PART_KEYS.issubset(part.keys()), (
            f"Missing keys: {REFERENCE_PART_KEYS - part.keys()}"
        )


@pytest.fixture(scope="module")
def client():
    return PenpointClient(
        api_key=os.environ["PENPOINT_API_KEY"],
        base_url=os.environ.get("PENPOINT_API_BASE_URL", "https://api.penpoint.ai/v1"),
        timeout=120,
    )


@pytest.fixture(scope="module")
def uploaded_file(client):
    """Upload a temporary markdown file and delete it after all tests complete."""
    result = client.files.upload(
        file=io.BytesIO(TEST_MARKDOWN.encode()),
        filename="penpoint_integration_test.md",
    )
    yield result
    try:
        client.files.delete(result.id)
    except Exception:
        pass


@pytest.fixture(scope="module")
def updated_file(client, uploaded_file):
    """Update the file with a summary and expiration, polling until indexed."""
    if not (uploaded_file.pages and uploaded_file.pages > 0):
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            resp = client.get(f"/files/{uploaded_file.id}")
            if resp.headers.get("content-type", "").startswith("application/json"):
                data = resp.json()
                if data.get("pages") and data["pages"] > 0:
                    break
            time.sleep(2)

    expiration = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
    return client.files.update(
        file_id=uploaded_file.id,
        summary=SUMMARY,
        expiration_date=expiration,
    )


class TestPenpointAPI:
    def test_upload_returns_file(self, uploaded_file):
        assert isinstance(uploaded_file, File)
        assert isinstance(uploaded_file.id, int)
        assert isinstance(uploaded_file.name, str)
        assert "penpoint_integration_test" in uploaded_file.name

    def test_update_sets_summary_and_expiration(self, updated_file):
        assert isinstance(updated_file, File)
        assert updated_file.summary == SUMMARY

    def test_discrete_references_basic(self, client, updated_file, uploaded_file):
        response = client.discrete_references.basic(
            file_id=uploaded_file.id,
            prompt=SEARCH_PROMPT,
            markup_file=False,
        )
        assert_reference_shape(response)

    def test_discrete_references_standard(self, client, updated_file, uploaded_file):
        response = client.discrete_references.standard(
            file_id=uploaded_file.id,
            prompt=SEARCH_PROMPT,
            markup_file=False,
        )
        assert_reference_shape(response)

    def test_discrete_references_advanced(self, client, updated_file, uploaded_file):
        response = client.discrete_references.advanced(
            file_id=uploaded_file.id,
            prompt=SEARCH_PROMPT,
            markup_file=False,
        )
        assert_reference_shape(response)
        assert "content" in response.refs, "Advanced response should include 'content'"
        assert isinstance(response.refs["content"], str)

    def test_delete_file(self, client, uploaded_file):
        assert client.files.delete(uploaded_file.id) is True
