#!/usr/bin/env python3
"""MicroMegas Detector Panel - Simple panel without status"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class MicroMegasPanel(BaseNodePanel):
    def __init__(self, device=None, parent=None):
        super().__init__("MicroMegas Detector", device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        # Clear the existing content layout from base class
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create a centered layout for the content
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        
        # Information frame
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_frame.setStyleSheet("QFrame { background-color: #f8f8f8; border: 2px solid #3498db; border-radius: 10px; }")
        info_layout = QVBoxLayout(info_frame)
        
        info_label = QLabel("MicroMegas Detector\n\nControl panel will be available soon.")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #2c3e50; padding: 50px; font-size: 14px;")
        info_layout.addWidget(info_label)
        
        center_layout.addWidget(info_frame)
        
        # Add stretch to center vertically
        self.content_layout.addStretch()
        self.content_layout.addLayout(center_layout)
        self.content_layout.addStretch()

def get_panel(device=None):
    return MicroMegasPanel(device)

def main():
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    # Fix Qt platform
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    os.environ['XDG_SESSION_TYPE'] = 'x11'
    
    panel = MicroMegasPanel()
    panel.setWindowTitle("MicroMegas Detector")
    panel.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
