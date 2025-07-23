# EXIF Viewer - Digital Forensics Tool

A comprehensive EXIF metadata viewer application designed specifically for digital forensics purposes. This Python application provides an intuitive interface for extracting, viewing, and analyzing EXIF data from various media types.

## 🚀 Features

### Core Functionality
- **Drag-and-Drop Interface**: Simply drag and drop media files directly into the application
- **Comprehensive Metadata Extraction**: Extract extensive EXIF data from images, videos, and audio files
- **Multi-Format Support**: Compatible with JPG, PNG, TIFF, MP4, AVI, MOV, MP3, WAV, and more
- **Bulk Processing**: Process multiple files or entire directories simultaneously

### Advanced Features
- **Interactive Geolocation Maps**: Visualize geotagged media locations on interactive maps using Folium
- **Flexible Export Options**: Export metadata in JSON, CSV, or TXT formats
- **Advanced Filtering**: Search and filter metadata fields for focused analysis
- **Theme Support**: Switch between modern dark and light themes
- **Privacy Tools**: Remove EXIF metadata from files for privacy purposes

### Digital Forensics Focused
- **Detailed Metadata Categories**: Organized display of camera, image, GPS, and technical data
- **Batch Analysis**: Process large sets of evidence files efficiently
- **Export for Reporting**: Generate reports in multiple formats for documentation
- **Coordinate Validation**: Verify and analyze GPS coordinates in geotagged media

## 📋 Requirements

- Python 3.8 or higher
- Windows, macOS, or Linux
- Required Python packages (see requirements.txt)

## 🛠️ Installation

### Option 1: From Source

1. Clone the repository:
```bash
git clone https://github.com/DarkKnightForensics/EXIF-Viewer.git
cd EXIF-Viewer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

### Option 2: Using PyInstaller (Windows Executable)

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller build.spec
```

3. Find the executable in the `dist` folder

### Option 3: Development Installation

```bash
pip install -e .
```

## 🖥️ Usage

### Getting Started

1. **Launch the Application**: Run `python src/main.py` or use the built executable
2. **Load Files**: 
   - Drag and drop files directly into the main window
   - Use "Browse Files" to select individual files
   - Use "Bulk Process Directory" to analyze entire folders
3. **View Metadata**: Browse extracted metadata in the organized table view
4. **Explore Maps**: Switch to the Map tab to see geotagged media locations
5. **Export Data**: Use the export options to save metadata for reports

### Key Features Walkthrough

#### Metadata Viewing
- **Organized Categories**: Data is automatically categorized (File Info, Camera Info, GPS Data, etc.)
- **Search & Filter**: Use the search box to find specific metadata fields
- **Raw Data View**: Toggle between formatted table view and raw JSON data

#### Map Visualization
- **Interactive Maps**: Geotagged photos and videos appear as markers on the map
- **Location Details**: Click markers to see file details and exact coordinates
- **Multiple File Support**: View all geotagged files from your analysis on one map

#### Export Options
- **JSON Export**: Complete metadata in JSON format for programmatic analysis
- **CSV Export**: Tabular format suitable for spreadsheet applications
- **TXT Export**: Human-readable report format for documentation

#### Privacy Features
- **EXIF Removal**: Strip metadata from files to protect privacy
- **Batch Processing**: Remove EXIF data from multiple files at once

## 🎨 Interface

### Dark/Light Themes
- Switch between professional dark and light themes
- Accessible via the View menu or toolbar
- Themes persist between application sessions

### Modern UI Elements
- Clean, intuitive interface designed for professional use
- Responsive layout that adapts to different screen sizes
- Professional color schemes suitable for forensic work

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python -m pytest tests/
```

Or run specific tests:

```bash
python tests/test_exif_viewer.py
```

## 📁 Project Structure

```
EXIF-Viewer/
├── src/
│   ├── main.py              # Application entry point
│   ├── gui/                 # User interface components
│   │   ├── main_window.py   # Main application window
│   │   ├── metadata_viewer.py # Metadata display component
│   │   ├── map_viewer.py    # Interactive map component
│   │   └── styles.py        # Theme and styling
│   ├── core/                # Core functionality
│   │   ├── exif_extractor.py # EXIF extraction engine
│   │   ├── file_processor.py # Bulk processing logic
│   │   └── exporter.py      # Export functionality
│   └── utils/               # Utility functions
│       └── helpers.py       # Common helper functions
├── tests/                   # Test suite
├── assets/                  # Application resources
├── requirements.txt         # Python dependencies
├── setup.py                # Package configuration
├── build.spec              # PyInstaller configuration
└── README.md               # This file
```

## 🔧 Supported File Formats

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About Dark Knight Forensics

This tool is developed by Dark Knight Forensics, specializing in digital forensics tools and solutions. For more information or support, please visit our website or contact us through GitHub.

## ⚠️ Disclaimer

This tool is intended for legitimate digital forensics and investigation purposes. Users are responsible for ensuring compliance with applicable laws and regulations when using this software. The developers assume no responsibility for misuse of this tool.

## 🔗 Links

- [GitHub Repository](https://github.com/DarkKnightForensics/EXIF-Viewer)
- [Issue Tracker](https://github.com/DarkKnightForensics/EXIF-Viewer/issues)
- [Latest Releases](https://github.com/DarkKnightForensics/EXIF-Viewer/releases)