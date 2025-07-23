"""Interactive map viewer for geotagged media."""

import os
import tempfile
from typing import Dict, Any, List, Tuple
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal
import folium
from folium import plugins


class MapViewer(QWidget):
    """Interactive map widget for displaying geotagged media locations."""
    
    location_selected = pyqtSignal(str)  # Emits file path when marker is clicked
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.temp_file = None
        self.geotagged_data = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        self.info_label = QLabel("No geotagged files loaded")
        self.refresh_btn = QPushButton("Refresh Map")
        self.clear_btn = QPushButton("Clear Map")
        
        self.refresh_btn.clicked.connect(self.refresh_map)
        self.clear_btn.clicked.connect(self.clear_map)
        
        control_layout.addWidget(self.info_label)
        control_layout.addStretch()
        control_layout.addWidget(self.refresh_btn)
        control_layout.addWidget(self.clear_btn)
        
        layout.addLayout(control_layout)
        
        # Web view for map
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # Initialize with empty map
        self.create_empty_map()
    
    def create_empty_map(self):
        """Create an empty map centered on the world."""
        m = folium.Map(
            location=[20, 0],  # Center of the world
            zoom_start=2,
            tiles='OpenStreetMap'
        )
        
        # Add some basic controls
        folium.plugins.Fullscreen().add_to(m)
        folium.plugins.MeasureControl().add_to(m)
        
        self.display_map(m)
    
    def load_geotagged_data(self, data: Dict[str, Any]):
        """Load geotagged data and update the map."""
        self.geotagged_data = data
        self.update_info_label()
        self.create_map_with_markers()
    
    def update_info_label(self):
        """Update the information label."""
        count = len(self.geotagged_data)
        if count == 0:
            self.info_label.setText("No geotagged files loaded")
        elif count == 1:
            self.info_label.setText("1 geotagged file on map")
        else:
            self.info_label.setText(f"{count} geotagged files on map")
    
    def create_map_with_markers(self):
        """Create a map with markers for all geotagged files."""
        if not self.geotagged_data:
            self.create_empty_map()
            return
        
        # Calculate center point and bounds
        locations = []
        for file_path, metadata in self.geotagged_data.items():
            if ("gps_data" in metadata and 
                "DecimalLatitude" in metadata["gps_data"] and 
                "DecimalLongitude" in metadata["gps_data"]):
                
                try:
                    lat = float(metadata["gps_data"]["DecimalLatitude"])
                    lon = float(metadata["gps_data"]["DecimalLongitude"])
                    locations.append((lat, lon, file_path, metadata))
                except (ValueError, TypeError):
                    continue
        
        if not locations:
            self.create_empty_map()
            return
        
        # Calculate center
        center_lat = sum(loc[0] for loc in locations) / len(locations)
        center_lon = sum(loc[1] for loc in locations) / len(locations)
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10 if len(locations) == 1 else 8,
            tiles='OpenStreetMap'
        )
        
        # Add markers
        for lat, lon, file_path, metadata in locations:
            self.add_marker_to_map(m, lat, lon, file_path, metadata)
        
        # Add plugins
        folium.plugins.Fullscreen().add_to(m)
        folium.plugins.MeasureControl().add_to(m)
        
        # Fit bounds if multiple markers
        if len(locations) > 1:
            bounds = [[loc[0], loc[1]] for loc in locations]
            m.fit_bounds(bounds, padding=(20, 20))
        
        self.display_map(m)
    
    def add_marker_to_map(self, map_obj: folium.Map, lat: float, lon: float, 
                         file_path: str, metadata: Dict[str, Any]):
        """Add a marker to the map for a geotagged file."""
        # Prepare popup content
        popup_content = self.create_popup_content(file_path, metadata)
        
        # Determine marker color based on file type
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            color = 'blue'
            icon = 'camera'
        elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']:
            color = 'red'
            icon = 'video'
        else:
            color = 'green'
            icon = 'file'
        
        # Create marker
        marker = folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=os.path.basename(file_path),
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        )
        
        marker.add_to(map_obj)
    
    def create_popup_content(self, file_path: str, metadata: Dict[str, Any]) -> str:
        """Create HTML content for marker popup."""
        file_name = os.path.basename(file_path)
        
        content = f"""
        <div style="width: 280px;">
            <h4 style="margin: 0 0 10px 0; color: #333;">{file_name}</h4>
        """
        
        # Add file info
        if "file_info" in metadata:
            file_info = metadata["file_info"]
            if "File Size" in file_info:
                content += f"<p><strong>Size:</strong> {file_info['File Size']}</p>"
        
        # Add camera info
        if "camera_info" in metadata and metadata["camera_info"]:
            camera_info = metadata["camera_info"]
            if "Make" in camera_info and "Model" in camera_info:
                content += f"<p><strong>Camera:</strong> {camera_info['Make']} {camera_info['Model']}</p>"
        
        # Add GPS coordinates
        if "gps_data" in metadata:
            gps_data = metadata["gps_data"]
            if "DecimalLatitude" in gps_data and "DecimalLongitude" in gps_data:
                lat = gps_data["DecimalLatitude"]
                lon = gps_data["DecimalLongitude"]
                content += f"<p><strong>Coordinates:</strong><br/>{lat:.6f}, {lon:.6f}</p>"
        
        # Add timestamp if available
        if "exif_data" in metadata:
            exif_data = metadata["exif_data"]
            for key in ["DateTime", "DateTimeOriginal", "CreateDate"]:
                if key in exif_data:
                    content += f"<p><strong>Date:</strong> {exif_data[key]}</p>"
                    break
        
        content += f"""
            <div style="margin-top: 10px;">
                <button onclick="selectLocation('{file_path}')" 
                        style="background: #007bff; color: white; border: none; 
                               padding: 5px 10px; border-radius: 3px; cursor: pointer;">
                    Select File
                </button>
            </div>
        </div>
        """
        
        return content
    
    def display_map(self, map_obj: folium.Map):
        """Display the folium map in the web view."""
        # Save map to temporary file
        if self.temp_file:
            try:
                os.unlink(self.temp_file)
            except:
                pass
        
        fd, self.temp_file = tempfile.mkstemp(suffix='.html')
        
        # Add JavaScript for marker interaction
        map_html = map_obj._repr_html_()
        interactive_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>EXIF Viewer Map</title>
        </head>
        <body>
            {map_html}
            <script>
                function selectLocation(filePath) {{
                    console.log('Selected file:', filePath);
                    // This would need to be connected to Qt signals
                    // For now, just log to console
                }}
            </script>
        </body>
        </html>
        """
        
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(interactive_html)
        
        # Load in web view
        self.web_view.load(QUrl.fromLocalFile(self.temp_file))
    
    def refresh_map(self):
        """Refresh the map with current data."""
        self.create_map_with_markers()
    
    def clear_map(self):
        """Clear all markers from the map."""
        self.geotagged_data = {}
        self.update_info_label()
        self.create_empty_map()
    
    def closeEvent(self, event):
        """Clean up temporary files when closing."""
        if self.temp_file:
            try:
                os.unlink(self.temp_file)
            except:
                pass
        super().closeEvent(event)