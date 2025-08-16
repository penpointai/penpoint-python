#!/usr/bin/env python3
"""
Asynchronous usage example for the Penpoint Python client library.

This example demonstrates how to:
1. Initialize the async client
2. Perform async operations
3. Handle multiple concurrent requests
4. Use async context managers
"""

import asyncio
import os
from penpoint import AsyncPenpointClient


async def list_files_async(client: AsyncPenpointClient):
    """List files asynchronously."""
    print("📁 Listing files asynchronously...")
    try:
        files = await client.files.list(limit=10)
        print(f"Found {len(files.data)} files:")
        for file_obj in files.data[:3]:  # Show first 3
            print(f"  - {file_obj.name} (ID: {file_obj.id})")
        return files
    except Exception as e:
        print(f"Error listing files: {e}")
        return None


async def search_references_async(client: AsyncPenpointClient, file_id: int):
    """Search for references asynchronously."""
    print(f"🔍 Searching references for file {file_id}...")
    try:
        # Perform multiple search types concurrently
        tasks = [
            client.discrete_references.basic(
                file_id=file_id,
                prompt="CMake integration",
                markup_file=False
            ),
            client.discrete_references.standard(
                file_id=file_id,
                prompt="CMake integration",
                markup_file=False
            ),
            client.discrete_references.advanced(
                file_id=file_id,
                prompt="CMake integration",
                markup_file=False
            )
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"    {['Basic', 'Standard', 'Advanced'][i]} search failed: {result}")
            else:
                parts_count = len(result.refs.get("parts", [])) if result.refs else 0
                print(f"    {['Basic', 'Standard', 'Advanced'][i]} search: {parts_count} references")
        
        return results
    except Exception as e:
        print(f"Error searching references: {e}")
        return None


async def concurrent_operations(client: AsyncPenpointClient, file_ids: list):
    """Perform multiple operations concurrently."""
    print(f"⚡ Performing concurrent operations on {len(file_ids)} files...")
    
    # Create tasks for multiple operations
    tasks = []
    for file_id in file_ids:
        # Get file info and search references concurrently for each file
        file_task = client.files.get(file_id)
        search_task = client.discrete_references.basic(
            file_id=file_id,
            prompt="integration",
            markup_file=False
        )
        tasks.extend([file_task, search_task])
    
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i in range(0, len(results), 2):
            file_id = file_ids[i // 2]
            file_result = results[i]
            search_result = results[i + 1]
            
            print(f"  File {file_id}:")
            if isinstance(file_result, Exception):
                print(f"    File info: Error - {file_result}")
            else:
                print(f"    File info: {file_result.name}")
            
            if isinstance(search_result, Exception):
                print(f"    Search: Error - {search_result}")
            else:
                parts_count = len(search_result.refs.get("parts", [])) if search_result.refs else 0
                print(f"    Search: {parts_count} references")
        
    except Exception as e:
        print(f"Error in concurrent operations: {e}")


async def main():
    """Main async example function."""
    
    # Initialize the async client with your API key
    api_key = os.getenv("PENPOINT_API_KEY")
    if not api_key:
        print("Please set the PENPOINT_API_KEY environment variable")
        return
    
    client = AsyncPenpointClient(api_key=api_key)
    
    print("🚀 Penpoint Async Python Client Example")
    print("=" * 45)
    
    try:
        # Example 1: Basic async operations
        print("\n1️⃣ Basic async operations...")
        files = await list_files_async(client)
        
        if files and files.data:
            # Example 2: Search references for first file
            print("\n2️⃣ Searching references...")
            first_file_id = files.data[0].id
            await search_references_async(client, first_file_id)
            
            # Example 3: Concurrent operations
            print("\n3️⃣ Concurrent operations...")
            file_ids = [file_obj.id for file_obj in files.data[:3]]  # Use first 3 files
            await concurrent_operations(client, file_ids)
        
        # Example 4: Error handling and timeouts
        print("\n4️⃣ Error handling example...")
        try:
            # This will likely fail with a non-existent file ID
            await asyncio.wait_for(
                client.files.get(99999),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            print("  ⏰ Request timed out (expected)")
        except Exception as e:
            print(f"  ❌ Expected error: {type(e).__name__}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        print("\n✨ Async example completed!")
        print("\nKey benefits of async usage:")
        print("- Concurrent operations for better performance")
        print("- Non-blocking I/O operations")
        print("- Better resource utilization")
        print("- Suitable for web applications and high-throughput scenarios")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
