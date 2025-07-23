"""Metadata viewer component for displaying EXIF data."""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QLineEdit, QPushButton, QComboBox,
                            QTabWidget, QTextEdit, QGroupBox, QLabel, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Dict, Any, List


class MetadataViewer(QWidget):
    """Widget for displaying and filtering EXIF metadata."""
    
    export_requested = pyqtSignal(str)  # Emits format type when export is requested
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_data = {}
        self.filtered_data = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Filter and controls section
        filter_group = QGroupBox("Filter and Search")
        filter_layout = QVBoxLayout(filter_group)
        
        # Search and filter controls
        controls_layout = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search metadata fields...")
        self.search_edit.textChanged.connect(self.filter_metadata)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems([
            "All Categories", "File Info", "Camera Info", 
            "Image Info", "GPS Data", "EXIF Data"
        ])
        self.category_filter.currentTextChanged.connect(self.filter_metadata)
        
        self.clear_filter_btn = QPushButton("Clear Filters")
        self.clear_filter_btn.clicked.connect(self.clear_filters)
        
        controls_layout.addWidget(QLabel("Search:"))
        controls_layout.addWidget(self.search_edit)
        controls_layout.addWidget(QLabel("Category:"))
        controls_layout.addWidget(self.category_filter)
        controls_layout.addWidget(self.clear_filter_btn)
        controls_layout.addStretch()
        
        filter_layout.addLayout(controls_layout)
        layout.addWidget(filter_group)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Metadata table
        self.metadata_table = QTableWidget()
        self.metadata_table.setColumnCount(3)
        self.metadata_table.setHorizontalHeaderLabels(["Category", "Field", "Value"])
        self.metadata_table.horizontalHeader().setStretchLastSection(True)
        self.metadata_table.setAlternatingRowColors(True)
        self.metadata_table.setSortingEnabled(True)
        
        # Raw data view
        raw_group = QGroupBox("Raw EXIF Data")
        raw_layout = QVBoxLayout(raw_group)
        
        self.raw_text = QTextEdit()
        self.raw_text.setReadOnly(True)
        self.raw_text.setFont(QFont("Courier", 9))
        raw_layout.addWidget(self.raw_text)
        
        splitter.addWidget(self.metadata_table)
        splitter.addWidget(raw_group)
        splitter.setSizes([600, 400])
        
        layout.addWidget(splitter)
        
        # Export controls
        export_group = QGroupBox("Export Options")
        export_layout = QHBoxLayout(export_group)
        
        self.export_format = QComboBox()
        self.export_format.addItems(["JSON", "CSV", "TXT"])
        
        self.export_btn = QPushButton("Export Metadata")
        self.export_btn.clicked.connect(self.request_export)
        self.export_btn.setEnabled(False)
        
        export_layout.addWidget(QLabel("Export Format:"))
        export_layout.addWidget(self.export_format)
        export_layout.addStretch()
        export_layout.addWidget(self.export_btn)
        
        layout.addWidget(export_group)
    
    def load_metadata(self, data: Dict[str, Any]):
        """Load metadata for display."""
        self.current_data = data
        self.filtered_data = data.copy()
        self.update_display()
        self.export_btn.setEnabled(bool(data))
    
    def update_display(self):
        """Update the metadata display."""
        self.update_metadata_table()
        self.update_raw_display()
    
    def update_metadata_table(self):
        """Update the metadata table with filtered data."""
        self.metadata_table.setRowCount(0)
        
        if not self.filtered_data:
            return
        
        row = 0
        for file_path, metadata in self.filtered_data.items():
            if isinstance(metadata, dict) and "error" not in metadata:
                # Add file info
                if "file_info" in metadata:
                    for key, value in metadata["file_info"].items():
                        self.add_table_row(row, "File Info", key, str(value))
                        row += 1
                
                # Add camera info
                if "camera_info" in metadata and metadata["camera_info"]:
                    for key, value in metadata["camera_info"].items():
                        self.add_table_row(row, "Camera Info", key, str(value))
                        row += 1
                
                # Add image info
                if "image_info" in metadata and metadata["image_info"]:
                    for key, value in metadata["image_info"].items():
                        self.add_table_row(row, "Image Info", key, str(value))
                        row += 1
                
                # Add GPS data
                if "gps_data" in metadata and metadata["gps_data"]:
                    for key, value in metadata["gps_data"].items():
                        self.add_table_row(row, "GPS Data", key, str(value))
                        row += 1
                
                # Add EXIF data
                if "exif_data" in metadata and metadata["exif_data"]:
                    for key, value in metadata["exif_data"].items():
                        self.add_table_row(row, "EXIF Data", key, str(value))
                        row += 1
                
                # Add separator for multiple files
                if len(self.filtered_data) > 1:
                    import os
                    self.add_table_row(row, "---", f"File: {os.path.basename(file_path)}", "---")
                    row += 1
    
    def add_table_row(self, row: int, category: str, field: str, value: str):
        """Add a row to the metadata table."""
        self.metadata_table.insertRow(row)
        
        category_item = QTableWidgetItem(category)
        field_item = QTableWidgetItem(field)
        value_item = QTableWidgetItem(value)
        
        # Make items read-only
        category_item.setFlags(category_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        field_item.setFlags(field_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        self.metadata_table.setItem(row, 0, category_item)
        self.metadata_table.setItem(row, 1, field_item)
        self.metadata_table.setItem(row, 2, value_item)
        
        # Resize columns to content
        self.metadata_table.resizeColumnsToContents()
    
    def update_raw_display(self):
        """Update the raw metadata display."""
        if not self.filtered_data:
            self.raw_text.clear()
            return
        
        raw_content = []
        for file_path, metadata in self.filtered_data.items():
            raw_content.append(f"=== {file_path} ===\n")
            
            if isinstance(metadata, dict):
                if "error" in metadata:
                    raw_content.append(f"Error: {metadata['error']}\n")
                else:
                    import json
                    try:
                        json_str = json.dumps(metadata, indent=2, default=str)
                        raw_content.append(json_str)
                    except:
                        raw_content.append(str(metadata))
            else:
                raw_content.append(str(metadata))
            
            raw_content.append("\n\n")
        
        self.raw_text.setPlainText("".join(raw_content))
    
    def filter_metadata(self):
        """Filter metadata based on search terms and category."""
        search_term = self.search_edit.text().lower()
        category_filter = self.category_filter.currentText()
        
        if not search_term and category_filter == "All Categories":
            self.filtered_data = self.current_data.copy()
        else:
            self.filtered_data = {}
            
            for file_path, metadata in self.current_data.items():
                if isinstance(metadata, dict) and "error" not in metadata:
                    filtered_metadata = {}
                    
                    # Filter by category
                    categories_to_check = []
                    if category_filter == "All Categories":
                        categories_to_check = ["file_info", "camera_info", "image_info", "gps_data", "exif_data"]
                    else:
                        category_map = {
                            "File Info": "file_info",
                            "Camera Info": "camera_info", 
                            "Image Info": "image_info",
                            "GPS Data": "gps_data",
                            "EXIF Data": "exif_data"
                        }
                        categories_to_check = [category_map.get(category_filter, "")]
                    
                    # Check each category
                    for category in categories_to_check:
                        if category in metadata and metadata[category]:
                            category_data = metadata[category]
                            
                            if search_term:
                                # Filter by search term
                                filtered_category = {}
                                for key, value in category_data.items():
                                    if (search_term in key.lower() or 
                                        search_term in str(value).lower()):
                                        filtered_category[key] = value
                                
                                if filtered_category:
                                    filtered_metadata[category] = filtered_category
                            else:
                                filtered_metadata[category] = category_data
                    
                    if filtered_metadata:
                        # Include file_info for context if not already included
                        if "file_info" not in filtered_metadata and "file_info" in metadata:
                            filtered_metadata["file_info"] = metadata["file_info"]
                        
                        self.filtered_data[file_path] = filtered_metadata
        
        self.update_display()
    
    def clear_filters(self):
        """Clear all filters and show all metadata."""
        self.search_edit.clear()
        self.category_filter.setCurrentText("All Categories")
        self.filtered_data = self.current_data.copy()
        self.update_display()
    
    def request_export(self):
        """Request export of current metadata."""
        format_type = self.export_format.currentText().lower()
        self.export_requested.emit(format_type)
    
    def get_current_data_for_export(self) -> Dict[str, Any]:
        """Get the currently filtered data for export."""
        return self.filtered_data if self.filtered_data else self.current_data