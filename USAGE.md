# EXIF Viewer - Quick Start Guide

## Installation & Running

### Option 1: Run from Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### Option 2: Build Executable
```bash
# Windows
build.bat

# Linux/macOS
chmod +x build.sh
./build.sh
```

## Using the Application

### 1. Loading Files
- **Drag & Drop**: Simply drag image/video files into the main window
- **Browse**: Click "Browse Files" to select individual files
- **Bulk Process**: Use "Bulk Process Directory" for entire folders

### 2. Viewing Metadata
- Switch between **Metadata** and **Map** tabs
- Use the search box to filter specific fields
- Select categories from the dropdown (File Info, Camera Info, GPS Data, etc.)
- Toggle between table view and raw JSON data

### 3. Interactive Maps
- Geotagged files appear as markers on the map
- Click markers to see file details
- Different colors for different file types:
  - 🔵 Blue: Images
  - 🔴 Red: Videos  
  - 🟢 Green: Other files

### 4. Exporting Data
- Choose export format: JSON, CSV, or TXT
- Click "Export Metadata" to save current filtered data
- Files are saved with timestamp for organization

### 5. Privacy Features
- Use "Remove EXIF from Files" to strip metadata
- Confirmation dialog prevents accidental data loss
- Works on multiple files at once

### 6. Themes
- Switch between Light and Dark themes
- Access via View menu or toggle shortcut
- Settings persist between sessions

## Supported File Types

### Images
- JPEG (.jpg, .jpeg)
- PNG (.png)  
- TIFF (.tiff, .tif)
- BMP (.bmp)
- GIF (.gif)

### Videos
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)

### Audio
- MP3 (.mp3)
- WAV (.wav)
- FLAC (.flac)
- M4A (.m4a)

## Tips for Digital Forensics

1. **Batch Processing**: Use directory scanning for evidence collections
2. **Export Reports**: Generate CSV/TXT files for case documentation
3. **GPS Analysis**: Use the map view to verify location claims
4. **Metadata Validation**: Cross-reference camera information with case details
5. **Privacy Cleaning**: Remove metadata before sharing sensitive images

## Troubleshooting

- **No metadata found**: Some files may not contain EXIF data
- **Map not loading**: Check internet connection for map tiles
- **Large files slow**: Process files in smaller batches
- **Export fails**: Ensure write permissions to destination folder

## Keyboard Shortcuts

- `Ctrl+O`: Open Files
- `Ctrl+D`: Open Directory
- `Ctrl+Q`: Quit Application
- `F11`: Toggle Fullscreen (if supported)

For technical support, see the full README.md file.