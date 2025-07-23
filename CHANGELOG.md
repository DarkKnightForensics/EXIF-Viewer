# Changelog

All notable changes to the EXIF Viewer project will be documented in this file.

## [1.0.0] - 2025-01-23

### Added
- Initial release of EXIF Viewer application
- Comprehensive EXIF metadata extraction for images, videos, and audio files
- Modern PyQt6-based graphical user interface
- Drag-and-drop file support
- Bulk file processing with progress tracking
- Interactive map visualization for geotagged media using Folium
- Advanced metadata filtering and search capabilities
- Export functionality in JSON, CSV, and TXT formats
- Dark and light theme support
- Privacy-focused metadata removal tools
- Multi-threaded file processing for performance
- Comprehensive test suite
- PyInstaller configuration for Windows executable generation
- Cross-platform support (Windows, macOS, Linux)

### Core Features
- **File Support**: 16+ media formats including JPEG, PNG, TIFF, MP4, AVI, MOV, MP3, WAV, FLAC
- **Metadata Categories**: File info, camera details, image properties, GPS data, technical EXIF data
- **Map Integration**: Interactive maps with color-coded markers and detailed popups
- **Export Options**: Multiple formats suitable for forensic reporting and analysis
- **User Interface**: Professional design suitable for digital forensics workflows
- **Performance**: Efficient bulk processing with progress feedback
- **Privacy**: Secure metadata removal functionality

### Technical Specifications
- Built with Python 3.8+ and PyQt6
- Uses PIL/Pillow, exifread, and piexif for metadata extraction
- Folium integration for interactive mapping
- Thread-safe file processing
- Comprehensive error handling and validation
- Memory-efficient design for large file collections

### Documentation
- Comprehensive README with installation and usage instructions
- Quick start guide for immediate productivity
- Complete API documentation in code comments
- Test coverage for all major functionality

### Known Limitations
- GUI requires display server (no headless operation)
- Map functionality requires internet connection for tile loading
- Some proprietary RAW formats may have limited support
- Video metadata extraction may require additional codecs on some systems

## Future Roadmap
- Additional RAW image format support
- Plugin system for custom metadata extractors
- Advanced GPS coordinate analysis tools
- Integration with forensic case management systems
- Command-line interface for automated processing
- Database storage for large evidence collections