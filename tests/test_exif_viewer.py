"""Tests for the EXIF Viewer application."""

import unittest
import tempfile
import os
from pathlib import Path
from PIL import Image

# Add src to path
import sys
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from core.exif_extractor import EXIFExtractor
from core.file_processor import FileProcessor
from core.exporter import DataExporter


class TestEXIFExtractor(unittest.TestCase):
    """Test cases for EXIF extraction functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = EXIFExtractor()
        
        # Create a temporary test image
        self.temp_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.temp_dir, "test_image.jpg")
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(self.test_image_path, 'JPEG')
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_supported_file_detection(self):
        """Test supported file format detection."""
        # Test supported image formats
        self.assertTrue(self.extractor.is_supported_file("test.jpg"))
        self.assertTrue(self.extractor.is_supported_file("test.jpeg"))
        self.assertTrue(self.extractor.is_supported_file("test.png"))
        self.assertTrue(self.extractor.is_supported_file("test.gif"))
        
        # Test supported video formats
        self.assertTrue(self.extractor.is_supported_file("test.mp4"))
        self.assertTrue(self.extractor.is_supported_file("test.avi"))
        
        # Test unsupported formats
        self.assertFalse(self.extractor.is_supported_file("test.txt"))
        self.assertFalse(self.extractor.is_supported_file("test.doc"))
    
    def test_extract_image_metadata(self):
        """Test image metadata extraction."""
        metadata = self.extractor.extract_exif_data(self.test_image_path)
        
        # Check that metadata structure is correct
        self.assertIsInstance(metadata, dict)
        self.assertIn("file_info", metadata)
        self.assertIn("image_info", metadata)
        
        # Check file info
        file_info = metadata["file_info"]
        self.assertIn("File Name", file_info)
        self.assertIn("File Size", file_info)
        self.assertEqual(file_info["File Name"], "test_image.jpg")
    
    def test_nonexistent_file(self):
        """Test handling of non-existent files."""
        metadata = self.extractor.extract_exif_data("nonexistent.jpg")
        self.assertIn("error", metadata)
        self.assertEqual(metadata["error"], "File not found")


class TestFileProcessor(unittest.TestCase):
    """Test cases for file processing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = FileProcessor()
        
        # Create temporary test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test images
        for i in range(3):
            img_path = os.path.join(self.temp_dir, f"test_image_{i}.jpg")
            img = Image.new('RGB', (50, 50), color='blue')
            img.save(img_path, 'JPEG')
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_directory_scanning(self):
        """Test directory scanning for supported files."""
        files = self.processor.scan_directory(self.temp_dir)
        
        # Should find all test images
        self.assertEqual(len(files), 3)
        
        # All files should be JPG files
        for file_path in files:
            self.assertTrue(file_path.endswith('.jpg'))
    
    def test_bulk_processing(self):
        """Test bulk file processing."""
        files = self.processor.scan_directory(self.temp_dir)
        results = self.processor.process_files(files)
        
        # Should have results for all files
        self.assertEqual(len(results), 3)
        
        # All results should be valid metadata dictionaries
        for file_path, metadata in results.items():
            self.assertIsInstance(metadata, dict)
            if "error" not in metadata:
                self.assertIn("file_info", metadata)


class TestDataExporter(unittest.TestCase):
    """Test cases for data export functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.exporter = DataExporter()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create sample data
        self.test_data = {
            "test_file.jpg": {
                "file_info": {
                    "File Name": "test_file.jpg",
                    "File Size": "1024 bytes"
                },
                "exif_data": {
                    "Camera": "Test Camera",
                    "ISO": "100"
                }
            }
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_json_export(self):
        """Test JSON export functionality."""
        output_path = os.path.join(self.temp_dir, "test_export.json")
        success = self.exporter.export_data(self.test_data, output_path, "json")
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_path))
        
        # Verify content
        import json
        with open(output_path, 'r', encoding='utf-8') as f:
            exported_data = json.load(f)
        
        self.assertIn("test_file.jpg", exported_data)
    
    def test_csv_export(self):
        """Test CSV export functionality."""
        output_path = os.path.join(self.temp_dir, "test_export.csv")
        success = self.exporter.export_data(self.test_data, output_path, "csv")
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_path))
    
    def test_txt_export(self):
        """Test TXT export functionality."""
        output_path = os.path.join(self.temp_dir, "test_export.txt")
        success = self.exporter.export_data(self.test_data, output_path, "txt")
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_path))
        
        # Verify content structure
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn("EXIF Viewer Export Report", content)
        self.assertIn("test_file.jpg", content)


if __name__ == '__main__':
    unittest.main()