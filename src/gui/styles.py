"""Theme and style definitions for the EXIF Viewer application."""

# Light theme
LIGHT_THEME = {
    "background": "#ffffff",
    "surface": "#f5f5f5",
    "primary": "#1976d2",
    "secondary": "#424242",
    "text_primary": "#212121",
    "text_secondary": "#757575",
    "border": "#e0e0e0",
    "accent": "#2196f3",
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#f44336"
}

# Dark theme
DARK_THEME = {
    "background": "#121212",
    "surface": "#1e1e1e",
    "primary": "#bb86fc",
    "secondary": "#03dac6",
    "text_primary": "#ffffff",
    "text_secondary": "#b3b3b3",
    "border": "#333333",
    "accent": "#03dac6",
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#cf6679"
}


def get_main_window_style(theme: dict) -> str:
    """Get the main window stylesheet."""
    return f"""
    QMainWindow {{
        background-color: {theme['background']};
        color: {theme['text_primary']};
    }}
    
    QWidget {{
        background-color: {theme['background']};
        color: {theme['text_primary']};
    }}
    
    QMenuBar {{
        background-color: {theme['surface']};
        color: {theme['text_primary']};
        border-bottom: 1px solid {theme['border']};
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 8px 12px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {theme['primary']};
        color: white;
    }}
    
    QMenu {{
        background-color: {theme['surface']};
        color: {theme['text_primary']};
        border: 1px solid {theme['border']};
    }}
    
    QMenu::item {{
        padding: 8px 20px;
    }}
    
    QMenu::item:selected {{
        background-color: {theme['primary']};
        color: white;
    }}
    
    QStatusBar {{
        background-color: {theme['surface']};
        color: {theme['text_secondary']};
        border-top: 1px solid {theme['border']};
    }}
    """


def get_widget_style(theme: dict) -> str:
    """Get general widget stylesheet."""
    return f"""
    QPushButton {{
        background-color: {theme['primary']};
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {theme['accent']};
    }}
    
    QPushButton:pressed {{
        background-color: {theme['secondary']};
    }}
    
    QPushButton:disabled {{
        background-color: {theme['border']};
        color: {theme['text_secondary']};
    }}
    
    QLineEdit {{
        background-color: {theme['surface']};
        color: {theme['text_primary']};
        border: 2px solid {theme['border']};
        border-radius: 4px;
        padding: 8px;
    }}
    
    QLineEdit:focus {{
        border-color: {theme['primary']};
    }}
    
    QTextEdit, QPlainTextEdit {{
        background-color: {theme['surface']};
        color: {theme['text_primary']};
        border: 1px solid {theme['border']};
        border-radius: 4px;
    }}
    
    QTableWidget {{
        background-color: {theme['surface']};
        color: {theme['text_primary']};
        border: 1px solid {theme['border']};
        gridline-color: {theme['border']};
        selection-background-color: {theme['primary']};
    }}
    
    QTableWidget::item {{
        padding: 8px;
        border-bottom: 1px solid {theme['border']};
    }}
    
    QHeaderView::section {{
        background-color: {theme['primary']};
        color: white;
        padding: 8px;
        border: none;
        font-weight: bold;
    }}
    
    QTabWidget::pane {{
        border: 1px solid {theme['border']};
        background-color: {theme['surface']};
    }}
    
    QTabBar::tab {{
        background-color: {theme['background']};
        color: {theme['text_secondary']};
        padding: 8px 16px;
        border: 1px solid {theme['border']};
        border-bottom: none;
    }}
    
    QTabBar::tab:selected {{
        background-color: {theme['surface']};
        color: {theme['text_primary']};
        border-bottom: 2px solid {theme['primary']};
    }}
    
    QProgressBar {{
        border: 1px solid {theme['border']};
        border-radius: 4px;
        background-color: {theme['surface']};
        text-align: center;
    }}
    
    QProgressBar::chunk {{
        background-color: {theme['primary']};
        border-radius: 3px;
    }}
    
    QLabel {{
        color: {theme['text_primary']};
    }}
    
    QGroupBox {{
        font-weight: bold;
        border: 2px solid {theme['border']};
        border-radius: 8px;
        margin-top: 10px;
        padding-top: 10px;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }}
    
    QComboBox {{
        background-color: {theme['surface']};
        color: {theme['text_primary']};
        border: 2px solid {theme['border']};
        border-radius: 4px;
        padding: 6px;
        min-width: 100px;
    }}
    
    QComboBox:focus {{
        border-color: {theme['primary']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid {theme['text_primary']};
    }}
    
    QScrollBar:vertical {{
        background-color: {theme['surface']};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {theme['border']};
        border-radius: 6px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {theme['text_secondary']};
    }}
    
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
    }}
    """


def get_drop_zone_style(theme: dict) -> str:
    """Get drag and drop zone stylesheet."""
    return f"""
    QFrame {{
        border: 3px dashed {theme['border']};
        border-radius: 12px;
        background-color: {theme['surface']};
        color: {theme['text_secondary']};
    }}
    
    QFrame[drag_active="true"] {{
        border-color: {theme['primary']};
        background-color: {theme['primary']}20;
    }}
    """


class ThemeManager:
    """Manages application themes."""
    
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": LIGHT_THEME,
            "dark": DARK_THEME
        }
    
    def get_theme(self, theme_name: str = None) -> dict:
        """Get theme colors."""
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, LIGHT_THEME)
    
    def set_theme(self, theme_name: str):
        """Set current theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
    
    def get_complete_stylesheet(self, theme_name: str = None) -> str:
        """Get complete application stylesheet."""
        theme = self.get_theme(theme_name)
        return (get_main_window_style(theme) + 
                get_widget_style(theme) + 
                get_drop_zone_style(theme))