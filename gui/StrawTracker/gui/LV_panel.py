#!/usr/bin/env python3
"""Low Voltage Panel for StrawTracker Sections"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QGroupBox)
from PyQt5.QtCore import Qt

class LVPanel(BaseNodePanel):
    def __init__(self, device=None, parent=None):
        super().__init__("Low Voltage", device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        # Clear existing content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Create LV status display
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_frame.setStyleSheet("QFrame { background-color: #f8f8f8; border: 2px solid #3498db; border-radius: 10px; }")
        info_layout = QVBoxLayout(info_frame)
        
        # LV status information
        status_group = QGroupBox("Low Voltage Status")
        status_layout = QGridLayout()
        
        self.status_labels = {}
        lv_items = [
            ("+12V:", "v12", "0.00 V"),
            ("-12V:", "vneg12", "0.00 V"),
            ("+5V:", "v5", "0.00 V"),
            ("+3.3V:", "v33", "0.00 V"),
            ("Status:", "status", "Unknown")
        ]
        
        for i, (label, key, default) in enumerate(lv_items):
            status_layout.addWidget(QLabel(label), i, 0)
            self.status_labels[key] = QLabel(default)
            self.status_labels[key].setStyleSheet("font-weight: bold; padding: 5px; background-color: #ecf0f1;")
            status_layout.addWidget(self.status_labels[key], i, 1)
        
        status_group.setLayout(status_layout)
        info_layout.addWidget(status_group)
        
        info_label = QLabel("\nLow Voltage control panel for StrawTracker section\n\nMonitoring and control of low voltage power supplies")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #7f8c8d; padding: 20px;")
        info_layout.addWidget(info_label)
        
        self.content_layout.addWidget(info_frame)
        self.content_layout.addStretch()

def get_panel(device=None):
    return LVPanel(device)

def main():
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    # Fix Qt platform
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    os.environ['XDG_SESSION_TYPE'] = 'x11'
    
    panel = LVPanel()
    panel.setWindowTitle("Low Voltage Control")
    panel.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
