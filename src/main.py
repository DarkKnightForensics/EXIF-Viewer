"""Main entry point for the EXIF Viewer application."""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from gui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Enable high DPI support
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("EXIF Viewer")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Dark Knight Forensics")
    
    # Set application icon if available
    icon_path = current_dir.parent / "assets" / "icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()