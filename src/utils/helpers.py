"""Utility functions and helpers for the EXIF Viewer application."""

import os
import mimetypes
from pathlib import Path
from typing import List, Optional


def is_image_file(file_path: str) -> bool:
    """Check if a file is an image."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith('image/')


def is_video_file(file_path: str) -> bool:
    """Check if a file is a video."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith('video/')


def is_audio_file(file_path: str) -> bool:
    """Check if a file is an audio file."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith('audio/')


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations."""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"
    
    return filename


def get_file_extension_group(file_path: str) -> str:
    """Get the file type group based on extension."""
    ext = Path(file_path).suffix.lower()
    
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif'}
    video_exts = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
    audio_exts = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
    
    if ext in image_exts:
        return "Image"
    elif ext in video_exts:
        return "Video"
    elif ext in audio_exts:
        return "Audio"
    else:
        return "Other"


def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate GPS coordinates."""
    return -90 <= lat <= 90 and -180 <= lon <= 180


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def create_directory_if_not_exists(directory_path: str) -> bool:
    """Create directory if it doesn't exist."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except OSError:
        return False


def get_supported_extensions() -> List[str]:
    """Get list of all supported file extensions."""
    return [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',  # Images
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm',   # Videos
        '.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'           # Audio
    ]


def filter_supported_files(file_paths: List[str]) -> List[str]:
    """Filter list to only include supported file types."""
    supported_exts = set(get_supported_extensions())
    return [f for f in file_paths if Path(f).suffix.lower() in supported_exts]