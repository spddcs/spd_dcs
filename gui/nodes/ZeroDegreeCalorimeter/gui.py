#!/usr/bin/env python3
"""
GUI for ZeroDegreeCalorimeter detector
Part of SPD DCS system
"""

import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QGroupBox, QGridLayout)
from PyQt5.QtCore import QTimer

class ZeroDegreeCalorimeterGUI(QWidget):
    """GUI widget for ZeroDegreeCalorimeter detector"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("ZeroDegreeCalorimeter Detector Control")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Status group
        status_group = QGroupBox("Status")
        status_layout = QGridLayout()
        
        self.status_label = QLabel("Unknown")
        status_layout.addWidget(QLabel("Status:"), 0, 0)
        status_layout.addWidget(self.status_label, 0, 1)
        
        self.temp_label = QLabel("--")
        status_layout.addWidget(QLabel("Temperature:"), 1, 0)
        status_layout.addWidget(self.temp_label, 1, 1)
        
        self.voltage_label = QLabel("--")
        status_layout.addWidget(QLabel("Voltage:"), 2, 0)
        status_layout.addWidget(self.voltage_label, 2, 1)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Control buttons
        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.start_btn.clicked.connect(self.start_detector)
        self.stop_btn.clicked.connect(self.stop_detector)
        
        btn_layout = QGridLayout()
        btn_layout.addWidget(self.start_btn, 0, 0)
        btn_layout.addWidget(self.stop_btn, 0, 1)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)
        
    def update_status(self):
        """Update status information"""
        # This would connect to actual hardware
        self.status_label.setText("Running")
        self.temp_label.setText("25.0 °C")
        self.voltage_label.setText("5.0 V")
        
    def start_detector(self):
        """Start the detector"""
        print(f"Starting ZeroDegreeCalorimeter detector...")
        self.status_label.setText("Starting...")
        
    def stop_detector(self):
        """Stop the detector"""
        print(f"Stopping ZeroDegreeCalorimeter detector...")
        self.status_label.setText("Stopped")

def get_widget():
    """Function to return widget for master GUI"""
    return ZeroDegreeCalorimeterGUI()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = ZeroDegreeCalorimeterGUI()
    widget.show()
    sys.exit(app.exec_())
