"""Export functionality for EXIF data."""

import json
import csv
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class DataExporter:
    """Handles exporting EXIF data to various formats."""
    
    def __init__(self):
        self.supported_formats = {'json', 'csv', 'txt'}
    
    def export_data(self, data: Dict[str, Any], output_path: str, format_type: str) -> bool:
        """Export data to specified format."""
        format_type = format_type.lower()
        
        if format_type not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format_type}")
        
        try:
            if format_type == 'json':
                return self._export_json(data, output_path)
            elif format_type == 'csv':
                return self._export_csv(data, output_path)
            elif format_type == 'txt':
                return self._export_txt(data, output_path)
        except Exception as e:
            print(f"Export error: {e}")
            return False
        
        return False
    
    def _export_json(self, data: Dict[str, Any], output_path: str) -> bool:
        """Export data as JSON."""
        try:
            # Make data JSON serializable
            clean_data = self._clean_for_json(data)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(clean_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception:
            return False
    
    def _export_csv(self, data: Dict[str, Any], output_path: str) -> bool:
        """Export data as CSV."""
        try:
            # Flatten the data structure for CSV
            flattened_data = []
            
            for file_path, metadata in data.items():
                if isinstance(metadata, dict) and "error" not in metadata:
                    row = {"File Path": file_path}
                    
                    # Add file info
                    if "file_info" in metadata:
                        for key, value in metadata["file_info"].items():
                            row[f"File_{key}"] = str(value)
                    
                    # Add EXIF data
                    if "exif_data" in metadata:
                        for key, value in metadata["exif_data"].items():
                            row[f"EXIF_{key}"] = str(value)
                    
                    # Add GPS data
                    if "gps_data" in metadata:
                        for key, value in metadata["gps_data"].items():
                            row[f"GPS_{key}"] = str(value)
                    
                    # Add camera info
                    if "camera_info" in metadata:
                        for key, value in metadata["camera_info"].items():
                            row[f"Camera_{key}"] = str(value)
                    
                    # Add image info
                    if "image_info" in metadata:
                        for key, value in metadata["image_info"].items():
                            row[f"Image_{key}"] = str(value)
                    
                    flattened_data.append(row)
            
            if not flattened_data:
                return False
            
            # Write CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = set()
                for row in flattened_data:
                    fieldnames.update(row.keys())
                
                writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
                writer.writeheader()
                writer.writerows(flattened_data)
            
            return True
        except Exception:
            return False
    
    def _export_txt(self, data: Dict[str, Any], output_path: str) -> bool:
        """Export data as formatted text."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("EXIF Viewer Export Report\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Files: {len(data)}\n\n")
                
                for file_path, metadata in data.items():
                    f.write(f"File: {file_path}\n")
                    f.write("-" * 50 + "\n")
                    
                    if isinstance(metadata, dict):
                        if "error" in metadata:
                            f.write(f"Error: {metadata['error']}\n\n")
                            continue
                        
                        # File Information
                        if "file_info" in metadata:
                            f.write("File Information:\n")
                            for key, value in metadata["file_info"].items():
                                f.write(f"  {key}: {value}\n")
                            f.write("\n")
                        
                        # Camera Information
                        if "camera_info" in metadata and metadata["camera_info"]:
                            f.write("Camera Information:\n")
                            for key, value in metadata["camera_info"].items():
                                f.write(f"  {key}: {value}\n")
                            f.write("\n")
                        
                        # Image Information
                        if "image_info" in metadata and metadata["image_info"]:
                            f.write("Image Information:\n")
                            for key, value in metadata["image_info"].items():
                                f.write(f"  {key}: {value}\n")
                            f.write("\n")
                        
                        # GPS Information
                        if "gps_data" in metadata and metadata["gps_data"]:
                            f.write("GPS Information:\n")
                            for key, value in metadata["gps_data"].items():
                                f.write(f"  {key}: {value}\n")
                            f.write("\n")
                        
                        # EXIF Data
                        if "exif_data" in metadata and metadata["exif_data"]:
                            f.write("EXIF Data:\n")
                            for key, value in metadata["exif_data"].items():
                                f.write(f"  {key}: {value}\n")
                            f.write("\n")
                    
                    f.write("\n" + "=" * 50 + "\n\n")
            
            return True
        except Exception:
            return False
    
    def _clean_for_json(self, data: Any) -> Any:
        """Clean data to be JSON serializable."""
        if isinstance(data, dict):
            return {key: self._clean_for_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._clean_for_json(item) for item in data]
        elif isinstance(data, (str, int, float, bool)) or data is None:
            return data
        else:
            return str(data)
    
    def get_suggested_filename(self, format_type: str, prefix: str = "exif_export") -> str:
        """Get a suggested filename for export."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{format_type.lower()}"