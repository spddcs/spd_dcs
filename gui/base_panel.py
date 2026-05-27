#!/usr/bin/env python3
"""Base class for all SPD DCS node panels"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QGroupBox, QGridLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

def create_font(family="Sans Serif", size=8, bold=False, italic=False):
    font = QFont(family, size)
    font.setBold(bold)
    font.setItalic(italic)
    return font

SANS_FONT = create_font("Sans Serif", 8)
VALUE_FONT = create_font("Sans Serif", 9)
TITLE_FONT = create_font("Sans Serif", 14, bold=True)
SECTION_FONT = create_font("Sans Serif", 10, bold=True)

class BaseNodePanel(QWidget):
    """Base class for all node panels"""
    
    def __init__(self, node_name, device=None, parent=None):
        super().__init__(parent)
        self.node_name = node_name
        self.device = device
        self.setup_ui()
        
        # Timer for periodic updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(2000)
    
    def setup_ui(self):
        """Setup basic UI structure"""
        self.setFixedSize(950, 850)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel(self.node_name)
        title.setFont(TITLE_FONT)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        main_layout.addWidget(title)
        
        # Content area (to be overridden by child classes)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        main_layout.addWidget(self.content_widget)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("background-color: #34495e; color: white; padding: 5px;")
        main_layout.addWidget(self.status_label)
    
    def update_values(self):
        """Override in child classes"""
        pass

class InfoPanel(BaseNodePanel):
    """Information panel for nodes without specific GUI"""
    
    def __init__(self, node_name, device=None, parent=None):
        super().__init__(node_name, device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_frame.setStyleSheet("QFrame { background-color: #f8f8f8; border: 2px solid #3498db; border-radius: 10px; }")
        info_layout = QVBoxLayout(info_frame)
        
        info_label = QLabel(f"{self.node_name} Detector\n\nControl panel will be available soon.")
        info_label.setFont(create_font("Sans Serif", 12))
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        self.content_layout.addWidget(info_frame)
        self.content_layout.addStretch()

class PlaceholderPanel(BaseNodePanel):
    """Placeholder panel for nodes that don't exist yet"""
    
    def __init__(self, node_name, device=None, parent=None):
        super().__init__(node_name, device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        placeholder_label = QLabel(f"⚠️ {self.node_name} panel not yet implemented")
        placeholder_label.setFont(create_font("Sans Serif", 12))
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_label.setStyleSheet("color: #e74c3c; padding: 50px;")
        self.content_layout.addWidget(placeholder_label)
        self.content_layout.addStretch()
