"""Tests for the data models."""

import pytest
from penpoint.models import (
    File,
    FileList,
    ReferenceMetadata,
    ReferencePart,
    DiscreteReferenceResponse,
    FileUploadRequest,
    FileUpdateRequest,
    DiscreteReferenceRequest,
    PaginationParams,
)


class TestReferenceMetadata:
    """Test the ReferenceMetadata model."""

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        metadata = ReferenceMetadata(
            page=1, x=0.1, y=0.2, w=0.3, h=0.4, labels=["label1", "label2"]
        )

        assert metadata.page == 1
        assert metadata.x == 0.1
        assert metadata.y == 0.2
        assert metadata.w == 0.3
        assert metadata.h == 0.4
        assert metadata.labels == ["label1", "label2"]

    def test_init_with_minimal_fields(self):
        """Test initialization with minimal fields."""
        metadata = ReferenceMetadata()

        assert metadata.page is None
        assert metadata.x is None
        assert metadata.y is None
        assert metadata.w is None
        assert metadata.h is None
        assert metadata.labels == []

    def test_labels_default_empty_list(self):
        """Test that labels defaults to empty list."""
        metadata = ReferenceMetadata()
        assert metadata.labels == []


class TestReferencePart:
    """Test the ReferencePart model."""

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        metadata = ReferenceMetadata(page=1, x=0.1, y=0.2, w=0.3, h=0.4)

        part = ReferencePart(
            id=123,
            name="test.pdf",
            segment="Test segment text",
            metadata=metadata,
            document_id=456,
            page_number=1,
            chunk_number=5,
            vector_distance=0.1,
            text_distance=0.2,
            hybrid_score=0.15,
        )

        assert part.id == 123
        assert part.name == "test.pdf"
        assert part.segment == "Test segment text"
        assert part.metadata == metadata
        assert part.document_id == 456
        assert part.page_number == 1
        assert part.chunk_number == 5
        assert part.vector_distance == 0.1
        assert part.text_distance == 0.2
        assert part.hybrid_score == 0.15


class TestDiscreteReferenceResponse:
    """Test the DiscreteReferenceResponse model."""

    def test_init_with_parts(self):
        """Test initialization with reference parts."""
        metadata = ReferenceMetadata(page=1)
        part = ReferencePart(
            id=123,
            name="test.pdf",
            segment="Test segment",
            metadata=metadata,
            document_id=456,
            page_number=1,
            chunk_number=1,
            vector_distance=0.1,
            text_distance=0.2,
            hybrid_score=0.15,
        )

        response = DiscreteReferenceResponse(refs={"parts": [part]})

        assert "parts" in response.refs
        assert len(response.refs["parts"]) == 1
        assert response.refs["parts"][0] == part


class TestFile:
    """Test the File model."""

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        file_obj = File(
            id=123,
            name="test.pdf",
            pages=10,
            summary="Test file",
            metadata='{"key": "value"}',
            expires_at="2025-12-31",
            created_at="2024-01-01T00:00:00Z",
            storage_location="s3://bucket/file.pdf",
            company_id=789,
        )

        assert file_obj.id == 123
        assert file_obj.name == "test.pdf"
        assert file_obj.pages == 10
        assert file_obj.summary == "Test file"
        assert file_obj.metadata == '{"key": "value"}'
        assert file_obj.expires_at == "2025-12-31"
        assert file_obj.created_at == "2024-01-01T00:00:00Z"
        assert file_obj.storage_location == "s3://bucket/file.pdf"
        assert file_obj.company_id == 789

    def test_init_with_minimal_fields(self):
        """Test initialization with minimal required fields."""
        file_obj = File(id=123, name="test.pdf", created_at="2024-01-01T00:00:00Z")

        assert file_obj.id == 123
        assert file_obj.name == "test.pdf"
        assert file_obj.created_at == "2024-01-01T00:00:00Z"
        assert file_obj.pages is None
        assert file_obj.summary is None
        assert file_obj.metadata is None
        assert file_obj.expires_at is None
        assert file_obj.storage_location is None
        assert file_obj.company_id is None


class TestFileList:
    """Test the FileList model."""

    def test_init_with_files(self):
        """Test initialization with files."""
        file1 = File(id=1, name="file1.pdf", created_at="2024-01-01T00:00:00Z")
        file2 = File(id=2, name="file2.pdf", created_at="2024-01-02T00:00:00Z")

        file_list = FileList(object="list", has_more=False, data=[file1, file2])

        assert file_list.object == "list"
        assert file_list.has_more is False
        assert len(file_list.data) == 2
        assert file_list.data[0] == file1
        assert file_list.data[1] == file2


class TestFileUploadRequest:
    """Test the FileUploadRequest model."""

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        request = FileUploadRequest(
            file="path/to/file.pdf",
            filename="file.pdf",
            summary="Test file description",
        )

        assert request.file == "path/to/file.pdf"
        assert request.filename == "file.pdf"
        assert request.summary == "Test file description"

    def test_init_without_summary(self):
        """Test initialization without summary."""
        request = FileUploadRequest(file="path/to/file.pdf", filename="file.pdf")

        assert request.file == "path/to/file.pdf"
        assert request.filename == "file.pdf"
        assert request.summary is None


class TestFileUpdateRequest:
    """Test the FileUpdateRequest model."""

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        request = FileUpdateRequest(
            summary="Updated description", expiration_date="2025-12-31"
        )

        assert request.summary == "Updated description"
        assert request.expiration_date == "2025-12-31"

    def test_init_without_expiration_date(self):
        """Test initialization without expiration date."""
        request = FileUpdateRequest(summary="Updated description")

        assert request.summary == "Updated description"
        assert request.expiration_date is None


class TestDiscreteReferenceRequest:
    """Test the DiscreteReferenceRequest model."""

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        request = DiscreteReferenceRequest(
            file_id=123, prompt="search term", markup_file=True, markup_color="#FF0000"
        )

        assert request.file_id == 123
        assert request.prompt == "search term"
        assert request.markup_file is True
        assert request.markup_color == "#FF0000"

    def test_init_without_markup_color(self):
        """Test initialization without markup color."""
        request = DiscreteReferenceRequest(
            file_id=123, prompt="search term", markup_file=False
        )

        assert request.file_id == 123
        assert request.prompt == "search term"
        assert request.markup_file is False
        assert request.markup_color is None


class TestPaginationParams:
    """Test the PaginationParams model."""

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        params = PaginationParams(limit=20, offset=40)

        assert params.limit == 20
        assert params.offset == 40

    def test_init_without_fields(self):
        """Test initialization without fields."""
        params = PaginationParams()

        assert params.limit is None
        assert params.offset is None
