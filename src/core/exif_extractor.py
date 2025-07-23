"""Core EXIF extraction module for the EXIF Viewer application."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exifread
import piexif


class EXIFExtractor:
    """Handles EXIF metadata extraction from various media types."""
    
    def __init__(self):
        self.supported_image_formats = {'.jpg', '.jpeg', '.tiff', '.tif', '.png', '.bmp', '.gif'}
        self.supported_video_formats = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
        self.supported_audio_formats = {'.mp3', '.wav', '.flac', '.m4a'}
    
    def is_supported_file(self, file_path: str) -> bool:
        """Check if the file format is supported."""
        ext = Path(file_path).suffix.lower()
        return ext in (self.supported_image_formats | 
                      self.supported_video_formats | 
                      self.supported_audio_formats)
    
    def extract_exif_data(self, file_path: str) -> Dict[str, Any]:
        """Extract EXIF data from a file."""
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        ext = Path(file_path).suffix.lower()
        
        try:
            if ext in self.supported_image_formats:
                return self._extract_image_exif(file_path)
            elif ext in self.supported_video_formats:
                return self._extract_video_exif(file_path)
            elif ext in self.supported_audio_formats:
                return self._extract_audio_exif(file_path)
            else:
                return {"error": "Unsupported file format"}
        except Exception as e:
            return {"error": f"Failed to extract EXIF data: {str(e)}"}
    
    def _extract_image_exif(self, file_path: str) -> Dict[str, Any]:
        """Extract EXIF data from image files."""
        metadata = {
            "file_info": self._get_file_info(file_path),
            "exif_data": {},
            "gps_data": {},
            "camera_info": {},
            "image_info": {}
        }
        
        try:
            # Try with Pillow first
            with Image.open(file_path) as img:
                exif_dict = img._getexif()
                if exif_dict:
                    for tag_id, value in exif_dict.items():
                        tag = TAGS.get(tag_id, tag_id)
                        
                        if tag == "GPSInfo":
                            metadata["gps_data"] = self._parse_gps_data(value)
                        elif tag in ["Make", "Model", "LensMake", "LensModel"]:
                            metadata["camera_info"][tag] = str(value)
                        elif tag in ["ImageWidth", "ImageLength", "Orientation", "ColorSpace"]:
                            metadata["image_info"][tag] = str(value)
                        else:
                            metadata["exif_data"][tag] = str(value)
                
                # Add image basic info
                metadata["image_info"].update({
                    "Format": img.format,
                    "Mode": img.mode,
                    "Size": f"{img.size[0]}x{img.size[1]}"
                })
            
            # Try with exifread for additional metadata
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f)
                for key, value in tags.items():
                    if key not in metadata["exif_data"]:
                        metadata["exif_data"][key] = str(value)
        
        except Exception as e:
            metadata["error"] = f"Error reading image EXIF: {str(e)}"
        
        return metadata
    
    def _extract_video_exif(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from video files."""
        metadata = {
            "file_info": self._get_file_info(file_path),
            "video_info": {},
            "exif_data": {}
        }
        
        try:
            # Basic file info for videos
            import subprocess
            import json as json_lib
            
            # Try to use ffprobe if available
            try:
                result = subprocess.run([
                    'ffprobe', '-v', 'quiet', '-print_format', 'json',
                    '-show_format', '-show_streams', file_path
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    ffprobe_data = json_lib.loads(result.stdout)
                    metadata["video_info"] = ffprobe_data.get("format", {})
                    metadata["streams"] = ffprobe_data.get("streams", [])
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
            
        except Exception as e:
            metadata["error"] = f"Error reading video metadata: {str(e)}"
        
        return metadata
    
    def _extract_audio_exif(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from audio files."""
        metadata = {
            "file_info": self._get_file_info(file_path),
            "audio_info": {},
            "exif_data": {}
        }
        
        try:
            # Basic implementation - can be extended with mutagen library
            if Path(file_path).suffix.lower() == '.mp3':
                try:
                    import mutagen
                    from mutagen.mp3 import MP3
                    from mutagen.id3 import ID3
                    
                    audio = MP3(file_path)
                    metadata["audio_info"] = {
                        "Length": f"{audio.info.length:.2f} seconds",
                        "Bitrate": f"{audio.info.bitrate} bps",
                        "Sample Rate": f"{audio.info.sample_rate} Hz"
                    }
                    
                    if audio.tags:
                        for key, value in audio.tags.items():
                            metadata["exif_data"][key] = str(value[0]) if isinstance(value, list) else str(value)
                
                except ImportError:
                    metadata["error"] = "Install mutagen library for full audio metadata support"
        
        except Exception as e:
            metadata["error"] = f"Error reading audio metadata: {str(e)}"
        
        return metadata
    
    def _parse_gps_data(self, gps_info: Dict) -> Dict[str, Any]:
        """Parse GPS information from EXIF data."""
        gps_data = {}
        
        if not gps_info:
            return gps_data
        
        # Convert GPS info
        for key, value in gps_info.items():
            decoded = GPSTAGS.get(key, key)
            gps_data[decoded] = str(value)
        
        # Calculate decimal coordinates if available
        try:
            if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                lat = self._convert_to_degrees(gps_info.get(2, []))
                lon = self._convert_to_degrees(gps_info.get(4, []))
                
                if gps_info.get(1) == 'S':
                    lat = -lat
                if gps_info.get(3) == 'W':
                    lon = -lon
                
                gps_data["DecimalLatitude"] = lat
                gps_data["DecimalLongitude"] = lon
        except:
            pass
        
        return gps_data
    
    def _convert_to_degrees(self, value) -> float:
        """Convert GPS coordinates to decimal degrees."""
        if len(value) != 3:
            return 0.0
        
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        
        return d + (m / 60.0) + (s / 3600.0)
    
    def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get basic file information."""
        stat = os.stat(file_path)
        return {
            "File Name": os.path.basename(file_path),
            "File Path": file_path,
            "File Size": f"{stat.st_size:,} bytes",
            "Created": str(stat.st_ctime),
            "Modified": str(stat.st_mtime),
            "Extension": Path(file_path).suffix.lower()
        }
    
    def remove_exif_data(self, file_path: str, output_path: Optional[str] = None) -> bool:
        """Remove EXIF data from an image file."""
        if not output_path:
            output_path = file_path
        
        try:
            ext = Path(file_path).suffix.lower()
            if ext in {'.jpg', '.jpeg'}:
                # Use piexif to remove EXIF data
                piexif.remove(file_path, output_path)
                return True
            elif ext in {'.png', '.bmp', '.gif'}:
                # For other formats, re-save without EXIF
                with Image.open(file_path) as img:
                    data = list(img.getdata())
                    image_without_exif = Image.new(img.mode, img.size)
                    image_without_exif.putdata(data)
                    image_without_exif.save(output_path)
                return True
            else:
                return False
        except Exception:
            return False