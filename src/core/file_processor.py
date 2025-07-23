"""File processing module for bulk operations."""

import os
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from .exif_extractor import EXIFExtractor


class FileProcessor:
    """Handles bulk file processing operations."""
    
    def __init__(self):
        self.extractor = EXIFExtractor()
        self.max_workers = 4  # Configurable thread pool size
    
    def process_files(self, file_paths: List[str], 
                     progress_callback: Optional[Callable[[int, int], None]] = None) -> Dict[str, Any]:
        """Process multiple files and extract EXIF data."""
        results = {}
        total_files = len(file_paths)
        
        if total_files == 0:
            return results
        
        # Filter supported files
        supported_files = [f for f in file_paths if self.extractor.is_supported_file(f)]
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(self.extractor.extract_exif_data, file_path): file_path
                for file_path in supported_files
            }
            
            completed = 0
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results[file_path] = result
                except Exception as exc:
                    results[file_path] = {"error": f"Exception occurred: {exc}"}
                
                completed += 1
                if progress_callback:
                    progress_callback(completed, len(supported_files))
        
        return results
    
    def scan_directory(self, directory_path: str, recursive: bool = True) -> List[str]:
        """Scan directory for supported media files."""
        if not os.path.isdir(directory_path):
            return []
        
        files = []
        directory = Path(directory_path)
        
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        for file_path in directory.glob(pattern):
            if file_path.is_file() and self.extractor.is_supported_file(str(file_path)):
                files.append(str(file_path))
        
        return sorted(files)
    
    def get_files_by_extension(self, directory_path: str) -> Dict[str, List[str]]:
        """Group files by their extensions."""
        files = self.scan_directory(directory_path)
        grouped = {}
        
        for file_path in files:
            ext = Path(file_path).suffix.lower()
            if ext not in grouped:
                grouped[ext] = []
            grouped[ext].append(file_path)
        
        return grouped
    
    def filter_geotagged_files(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Filter files that contain GPS data."""
        geotagged = {}
        
        for file_path, metadata in results.items():
            if isinstance(metadata, dict) and "gps_data" in metadata:
                gps_data = metadata["gps_data"]
                if gps_data and "DecimalLatitude" in gps_data and "DecimalLongitude" in gps_data:
                    geotagged[file_path] = metadata
        
        return geotagged