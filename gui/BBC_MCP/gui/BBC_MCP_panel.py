#!/usr/bin/env python3
"""BBC MCP Detector Panel with Picture Only"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class BBC_MCPPanel(BaseNodePanel):
    def __init__(self, device=None, parent=None):
        super().__init__("BBC MCP Detector", device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        # Clear the existing content layout from base class
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create a centered layout for the picture
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Picture frame
        picture_frame = QFrame()
        picture_frame.setFrameStyle(QFrame.Box)
        picture_frame.setStyleSheet("QFrame { background-color: white; border: 2px solid #bdc3c7; border-radius: 10px; }")
        picture_layout = QVBoxLayout(picture_frame)
        
        # Load and display picture
        picture_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pictures", "bbcmcp.png")
        
        if os.path.exists(picture_path):
            pixmap = QPixmap(picture_path)
            # Scale the picture to fit while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            picture_label = QLabel()
            picture_label.setPixmap(scaled_pixmap)
            picture_label.setAlignment(Qt.AlignCenter)
            picture_layout.addWidget(picture_label)
        else:
            # Placeholder if picture not found
            placeholder_label = QLabel("BBC MCP Detector Image\n\n(bbcmcp.png not found)\n\nPlace image in:\n/home/shkar/SPD_DCS/pictures/bbcmcp.png")
            placeholder_label.setAlignment(Qt.AlignCenter)
            placeholder_label.setStyleSheet("color: #7f8c8d; padding: 40px; font-size: 12px;")
            picture_layout.addWidget(placeholder_label)
        
        picture_frame.setLayout(picture_layout)
        center_layout.addWidget(picture_frame)
        
        # Add stretch to center vertically
        self.content_layout.addStretch()
        self.content_layout.addLayout(center_layout)
        self.content_layout.addStretch()

def get_panel(device=None):
    return BBC_MCPPanel(device)

def main():
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    # Fix Qt platform
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    os.environ['XDG_SESSION_TYPE'] = 'x11'
    
    panel = BBC_MCPPanel()
    panel.setWindowTitle("BBC MCP Detector")
    panel.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
