"""Main window for the EXIF Viewer application."""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QLabel, QPushButton, QFileDialog, 
                            QProgressBar, QStatusBar, QMenuBar, QMenu, QFrame,
                            QSplitter, QGroupBox, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData, QTimer
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent, QPixmap, QFont

from ..core import EXIFExtractor, FileProcessor, DataExporter
from .metadata_viewer import MetadataViewer
from .map_viewer import MapViewer
from .styles import ThemeManager


class ProcessingThread(QThread):
    """Background thread for file processing."""
    
    progress_updated = pyqtSignal(int, int)
    processing_finished = pyqtSignal(dict)
    
    def __init__(self, file_paths: List[str]):
        super().__init__()
        self.file_paths = file_paths
        self.processor = FileProcessor()
    
    def run(self):
        """Run the file processing."""
        results = self.processor.process_files(
            self.file_paths,
            progress_callback=self.progress_updated.emit
        )
        self.processing_finished.emit(results)


class DropZone(QFrame):
    """Drag and drop zone for files."""
    
    files_dropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the drop zone UI."""
        layout = QVBoxLayout(self)
        
        # Drop zone content
        drop_label = QLabel("📁")
        drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_label.setStyleSheet("font-size: 48px;")
        
        text_label = QLabel("Drag and drop media files here\nor click to browse")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)
        
        browse_btn = QPushButton("Browse Files")
        browse_btn.clicked.connect(self.browse_files)
        
        layout.addStretch()
        layout.addWidget(drop_label)
        layout.addWidget(text_label)
        layout.addWidget(browse_btn)
        layout.addStretch()
        
        self.setMinimumHeight(200)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("drag_active", True)
            self.style().unpolish(self)
            self.style().polish(self)
    
    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self.setProperty("drag_active", False)
        self.style().unpolish(self)
        self.style().polish(self)
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        self.setProperty("drag_active", False)
        self.style().unpolish(self)
        self.style().polish(self)
        
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)
            elif os.path.isdir(file_path):
                # Add all supported files from directory
                processor = FileProcessor()
                dir_files = processor.scan_directory(file_path, recursive=True)
                files.extend(dir_files)
        
        if files:
            self.files_dropped.emit(files)
    
    def browse_files(self):
        """Open file browser dialog."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Media Files",
            "",
            "Media Files (*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.mp4 *.avi *.mov *.mkv *.wmv *.mp3 *.wav *.flac *.m4a);;All Files (*)"
        )
        
        if files:
            self.files_dropped.emit(files)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.current_data = {}
        self.processing_thread = None
        
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("EXIF Viewer - Digital Forensics Tool")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Progress bar for status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        self.bulk_process_btn = QPushButton("Bulk Process Directory")
        self.bulk_process_btn.clicked.connect(self.bulk_process_directory)
        
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all_data)
        
        self.remove_exif_btn = QPushButton("Remove EXIF from Files")
        self.remove_exif_btn.clicked.connect(self.remove_exif_data)
        self.remove_exif_btn.setEnabled(False)
        
        toolbar_layout.addWidget(self.bulk_process_btn)
        toolbar_layout.addWidget(self.clear_btn)
        toolbar_layout.addWidget(self.remove_exif_btn)
        toolbar_layout.addStretch()
        
        main_layout.addLayout(toolbar_layout)
        
        # Main content area
        content_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self.process_files)
        content_splitter.addWidget(self.drop_zone)
        
        # Tab widget for metadata and map
        self.tab_widget = QTabWidget()
        
        # Metadata viewer tab
        self.metadata_viewer = MetadataViewer()
        self.metadata_viewer.export_requested.connect(self.export_metadata)
        self.tab_widget.addTab(self.metadata_viewer, "📊 Metadata")
        
        # Map viewer tab
        self.map_viewer = MapViewer()
        self.tab_widget.addTab(self.map_viewer, "🗺️ Map")
        
        content_splitter.addWidget(self.tab_widget)
        content_splitter.setSizes([200, 600])
        
        main_layout.addWidget(content_splitter)
        
        # Status label
        self.status_label = QLabel("Ready. Drop files or click Browse to get started.")
        self.status_bar.addWidget(self.status_label)
        
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open Files...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_files)
        file_menu.addAction(open_action)
        
        open_dir_action = QAction("Open Directory...", self)
        open_dir_action.setShortcut("Ctrl+D")
        open_dir_action.triggered.connect(self.bulk_process_directory)
        file_menu.addAction(open_dir_action)
        
        file_menu.addSeparator()
        
        export_json_action = QAction("Export as JSON...", self)
        export_json_action.triggered.connect(lambda: self.export_metadata("json"))
        file_menu.addAction(export_json_action)
        
        export_csv_action = QAction("Export as CSV...", self)
        export_csv_action.triggered.connect(lambda: self.export_metadata("csv"))
        file_menu.addAction(export_csv_action)
        
        export_txt_action = QAction("Export as TXT...", self)
        export_txt_action.triggered.connect(lambda: self.export_metadata("txt"))
        file_menu.addAction(export_txt_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        self.dark_mode_action = QAction("Dark Mode", self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.dark_mode_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        remove_exif_action = QAction("Remove EXIF Data...", self)
        remove_exif_action.triggered.connect(self.remove_exif_data)
        tools_menu.addAction(remove_exif_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def apply_theme(self, theme_name: str = None):
        """Apply the selected theme."""
        if theme_name:
            self.theme_manager.set_theme(theme_name)
        
        stylesheet = self.theme_manager.get_complete_stylesheet()
        self.setStyleSheet(stylesheet)
        
        # Update dark mode action state
        self.dark_mode_action.setChecked(self.theme_manager.current_theme == "dark")
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        new_theme = "dark" if self.theme_manager.current_theme == "light" else "light"
        self.apply_theme(new_theme)
    
    def open_files(self):
        """Open file dialog to select files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Media Files",
            "",
            "Media Files (*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.mp4 *.avi *.mov *.mkv *.wmv *.mp3 *.wav *.flac *.m4a);;All Files (*)"
        )
        
        if files:
            self.process_files(files)
    
    def bulk_process_directory(self):
        """Process all files in a directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory to Process",
            ""
        )
        
        if directory:
            processor = FileProcessor()
            files = processor.scan_directory(directory, recursive=True)
            
            if files:
                self.process_files(files)
            else:
                QMessageBox.information(
                    self,
                    "No Files Found",
                    "No supported media files found in the selected directory."
                )
    
    def process_files(self, file_paths: List[str]):
        """Process a list of files."""
        if not file_paths:
            return
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(file_paths))
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Processing {len(file_paths)} files...")
        
        # Start processing thread
        self.processing_thread = ProcessingThread(file_paths)
        self.processing_thread.progress_updated.connect(self.update_progress)
        self.processing_thread.processing_finished.connect(self.processing_completed)
        self.processing_thread.start()
    
    def update_progress(self, current: int, total: int):
        """Update the progress bar."""
        self.progress_bar.setValue(current)
        self.status_label.setText(f"Processing files... {current}/{total}")
    
    def processing_completed(self, results: Dict[str, Any]):
        """Handle completion of file processing."""
        self.progress_bar.setVisible(False)
        
        # Update data
        self.current_data.update(results)
        
        # Update UI components
        self.metadata_viewer.load_metadata(self.current_data)
        
        # Filter geotagged data for map
        processor = FileProcessor()
        geotagged_data = processor.filter_geotagged_files(self.current_data)
        self.map_viewer.load_geotagged_data(geotagged_data)
        
        # Update status
        total_files = len(self.current_data)
        error_count = sum(1 for data in self.current_data.values() 
                         if isinstance(data, dict) and "error" in data)
        success_count = total_files - error_count
        geotagged_count = len(geotagged_data)
        
        status_text = f"Loaded {success_count} files"
        if error_count > 0:
            status_text += f" ({error_count} errors)"
        if geotagged_count > 0:
            status_text += f", {geotagged_count} geotagged"
        
        self.status_label.setText(status_text)
        self.remove_exif_btn.setEnabled(success_count > 0)
    
    def export_metadata(self, format_type: str):
        """Export metadata to file."""
        if not self.current_data:
            QMessageBox.information(
                self,
                "No Data",
                "No metadata to export. Please load some files first."
            )
            return
        
        # Get export data
        export_data = self.metadata_viewer.get_current_data_for_export()
        
        # Get save location
        exporter = DataExporter()
        suggested_name = exporter.get_suggested_filename(format_type)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Export Metadata as {format_type.upper()}",
            suggested_name,
            f"{format_type.upper()} Files (*.{format_type});;All Files (*)"
        )
        
        if file_path:
            try:
                success = exporter.export_data(export_data, file_path, format_type)
                if success:
                    QMessageBox.information(
                        self,
                        "Export Successful",
                        f"Metadata exported successfully to:\n{file_path}"
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Export Failed",
                        "Failed to export metadata. Please try again."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"An error occurred while exporting:\n{str(e)}"
                )
    
    def remove_exif_data(self):
        """Remove EXIF data from selected files."""
        if not self.current_data:
            QMessageBox.information(
                self,
                "No Data",
                "No files loaded. Please load some files first."
            )
            return
        
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Remove EXIF Data",
            "This will remove EXIF metadata from the original files.\n"
            "This action cannot be undone.\n\n"
            "Do you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Process files
        extractor = EXIFExtractor()
        success_count = 0
        error_count = 0
        
        for file_path in self.current_data.keys():
            if extractor.is_supported_file(file_path):
                if extractor.remove_exif_data(file_path):
                    success_count += 1
                else:
                    error_count += 1
        
        # Show results
        if success_count > 0:
            message = f"EXIF data removed from {success_count} files."
            if error_count > 0:
                message += f"\n{error_count} files could not be processed."
            QMessageBox.information(self, "EXIF Removal Complete", message)
        else:
            QMessageBox.warning(
                self,
                "EXIF Removal Failed", 
                "No EXIF data could be removed from the files."
            )
    
    def clear_all_data(self):
        """Clear all loaded data."""
        self.current_data = {}
        self.metadata_viewer.load_metadata({})
        self.map_viewer.clear_map()
        self.status_label.setText("Ready. Drop files or click Browse to get started.")
        self.remove_exif_btn.setEnabled(False)
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About EXIF Viewer",
            "EXIF Viewer v1.0\n\n"
            "A comprehensive EXIF metadata viewer for digital forensics.\n\n"
            "Features:\n"
            "• Drag and drop file processing\n"
            "• Comprehensive metadata extraction\n"
            "• Interactive maps for geotagged media\n"
            "• Export capabilities (JSON, CSV, TXT)\n"
            "• Bulk processing support\n"
            "• Dark/Light themes\n"
            "• Privacy-focused metadata removal\n\n"
            "Copyright © 2025 Dark Knight Forensics"
        )
    
    def closeEvent(self, event):
        """Handle application close event."""
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.quit()
            self.processing_thread.wait()
        
        super().closeEvent(event)