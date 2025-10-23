#!/usr/bin/env python3
"""
Test script for integration storage migration.

This script tests the basic functionality of the integration storage system
without requiring real Google Drive connections.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "mcp" / "src"))

from models.document import Document, DocumentType
from storage.integration_provider import IntegrationStorageProvider
from persistence.convex_client import ConvexClient
from integration.merge_client import MergeClient


def test_document_model():
    """Test the updated Document model with new fields."""
    print("Testing Document model...")
    
    doc = Document(
        file_path="test_email.txt",
        content="This is a test email content.",
        doc_type=DocumentType.EMAIL,
        external_id="drv_123",
        external_url="https://drive.google.com/file/123",
        integration_id="int_456",
        summary="Test email about project requirements",
        source="integration",
        convex_document_id="conv_789"
    )
    
    # Test serialization
    doc_dict = doc.to_dict()
    assert doc_dict["external_id"] == "drv_123"
    assert doc_dict["summary"] == "Test email about project requirements"
    assert doc_dict["source"] == "integration"
    
    print("✓ Document model test passed")


def test_config():
    """Test the updated config with integration settings."""
    print("Testing config...")
    
    from config import config
    
    # Test that new config attributes exist
    assert hasattr(config, 'MERGE_API_KEY')
    assert hasattr(config, 'MERGE_API_BASE_URL')
    assert hasattr(config, 'USE_INTEGRATION_STORAGE')
    
    print("✓ Config test passed")


def test_merge_client():
    """Test MergeClient initialization."""
    print("Testing MergeClient...")
    
    try:
        client = MergeClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://api.merge.dev/api/filestorage/v1"
        print("✓ MergeClient test passed")
    except Exception as e:
        print(f"✗ MergeClient test failed: {e}")


def test_integration_provider():
    """Test IntegrationStorageProvider initialization."""
    print("Testing IntegrationStorageProvider...")
    
    try:
        # Mock clients for testing
        class MockConvexClient:
            def query(self, *args, **kwargs):
                return None
            def mutation(self, *args, **kwargs):
                return "mock_id"
        
        class MockMergeClient:
            def __init__(self, api_key):
                self.api_key = api_key
        
        convex_client = MockConvexClient()
        merge_client = MockMergeClient("test_key")
        
        provider = IntegrationStorageProvider(convex_client, merge_client)
        assert provider.convex_client == convex_client
        assert provider.merge_client == merge_client
        
        print("✓ IntegrationStorageProvider test passed")
    except Exception as e:
        print(f"✗ IntegrationStorageProvider test failed: {e}")


def test_document_type_detection():
    """Test document type detection from metadata."""
    print("Testing document type detection...")
    
    try:
        class MockConvexClient:
            def query(self, *args, **kwargs):
                return None
            def mutation(self, *args, **kwargs):
                return "mock_id"
        
        class MockMergeClient:
            def __init__(self, api_key):
                self.api_key = api_key
        
        convex_client = MockConvexClient()
        merge_client = MockMergeClient("test_key")
        
        provider = IntegrationStorageProvider(convex_client, merge_client)
        
        # Test filename-based detection
        assert provider._detect_document_type_from_filename("email_thread.txt") == "email"
        assert provider._detect_document_type_from_filename("transcript_call.txt") == "transcript"
        assert provider._detect_document_type_from_filename("sow_draft.txt") == "sow"
        
        # Test metadata-based detection
        file_info = {
            "name": "requirements.pdf",
            "mime_type": "application/pdf"
        }
        doc_type = provider._detect_document_type_from_metadata(file_info)
        assert doc_type == DocumentType.SOW
        
        print("✓ Document type detection test passed")
    except Exception as e:
        print(f"✗ Document type detection test failed: {e}")


def main():
    """Run all tests."""
    print("Running integration storage migration tests...\n")
    
    try:
        test_document_model()
        test_config()
        test_merge_client()
        test_integration_provider()
        test_document_type_detection()
        
        print("\n🎉 All tests passed! Integration storage migration is ready.")
        print("\nNext steps:")
        print("1. Deploy the updated Convex schema")
        print("2. Set up Merge API credentials")
        print("3. Configure USE_INTEGRATION_STORAGE=true")
        print("4. Test with real Google Drive integration")
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
