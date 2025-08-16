#!/usr/bin/env python3
"""
Basic usage example for the Penpoint Python client library.

This example demonstrates how to:
1. Initialize the client
2. Upload a file
3. Search for references
4. Download the marked-up file
5. Update file metadata
6. List files
"""

import os
from penpoint import PenpointClient


def main():
    """Main example function."""
    
    # Initialize the client with your API key
    # You can get your API key from https://api.penpoint.ai
    api_key = os.getenv("PENPOINT_API_KEY")
    if not api_key:
        print("Please set the PENPOINT_API_KEY environment variable")
        return
    
    client = PenpointClient(api_key=api_key)
    
    print("🚀 Penpoint Python Client Example")
    print("=" * 40)
    
    # Example 1: List existing files
    print("\n📁 Listing existing files...")
    try:
        files = client.files.list(limit=5)
        print(f"Found {len(files.data)} files:")
        for file_obj in files.data:
            print(f"  - {file_obj.name} (ID: {file_obj.id})")
            if file_obj.summary:
                print(f"    Summary: {file_obj.summary}")
    except Exception as e:
        print(f"Error listing files: {e}")
    
    # Example 2: Upload a file (if you have one)
    # Uncomment and modify the path to test file upload
    """
    print("\n📤 Uploading a file...")
    try:
        file_path = "path/to/your/document.pdf"
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_obj = client.files.upload(
                    file=f,
                    filename=os.path.basename(file_path),
                    summary="Example document for testing"
                )
            print(f"✅ File uploaded successfully! ID: {file_obj.id}")
            print(f"   Name: {file_obj.name}")
            print(f"   Pages: {file_obj.pages}")
            print(f"   Created: {file_obj.created_at}")
        else:
            print("⚠️  File not found, skipping upload example")
    except Exception as e:
        print(f"Error uploading file: {e}")
    """
    
    # Example 3: Search for references (requires an existing file ID)
    # Uncomment and modify the file_id to test reference search
    """
    print("\n🔍 Searching for references...")
    try:
        file_id = 123  # Replace with an actual file ID from your account
        
        # Basic search
        print("  Performing basic search...")
        basic_results = client.discrete_references.basic(
            file_id=file_id,
            prompt="CMake integration",
            markup_file=False
        )
        
        if basic_results.refs and "parts" in basic_results.refs:
            parts = basic_results.refs["parts"]
            print(f"    Found {len(parts)} references:")
            for part in parts[:3]:  # Show first 3 results
                print(f"      - {part.segment[:100]}...")
                print(f"        Score: {part.hybrid_score:.3f}")
        else:
            print("    No references found")
        
        # Advanced search
        print("  Performing advanced search...")
        advanced_results = client.discrete_references.advanced(
            file_id=file_id,
            prompt="performance profiling",
            markup_file=True,
            markup_color="#FF0000"
        )
        
        if advanced_results.refs and "parts" in advanced_results.refs:
            parts = advanced_results.refs["parts"]
            print(f"    Found {len(parts)} references:")
            for part in parts[:3]:  # Show first 3 results
                print(f"      - {part.segment[:100]}...")
                print(f"        Score: {part.hybrid_score:.3f}")
        else:
            print("    No references found")
            
    except Exception as e:
        print(f"Error searching references: {e}")
    """
    
    # Example 4: Update file metadata (requires an existing file ID)
    # Uncomment and modify the file_id to test metadata update
    """
    print("\n✏️  Updating file metadata...")
    try:
        file_id = 123  # Replace with an actual file ID from your account
        
        updated_file = client.files.update(
            file_id=file_id,
            summary="Updated description with new information",
            expiration_date="2025-12-31"
        )
        
        print(f"✅ File updated successfully!")
        print(f"   New summary: {updated_file.summary}")
        print(f"   Expires: {updated_file.expires_at}")
        
    except Exception as e:
        print(f"Error updating file: {e}")
    """
    
    print("\n✨ Example completed!")
    print("\nTo run the full examples:")
    print("1. Set your PENPOINT_API_KEY environment variable")
    print("2. Uncomment the example sections above")
    print("3. Modify file paths and IDs as needed")


if __name__ == "__main__":
    main()
