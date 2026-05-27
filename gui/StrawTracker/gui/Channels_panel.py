#!/usr/bin/env python3
"""All Channels Overview - Real data from TANGO device server"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel

from PyQt5.QtWidgets import (QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QPushButton, QHBoxLayout, QApplication, QLabel)
from PyQt5.QtCore import Qt, QTimer

try:
    import tango
    from tango import DeviceProxy
    TANGO_AVAILABLE = True
except ImportError:
    TANGO_AVAILABLE = False

class ChannelsPanel(BaseNodePanel):
    def __init__(self, device=None, parent=None):
        self.tango_device = None
        self.device_name = "SPD/CaenSMARTHV/StrawTrackerCaenHV_0"
        super().__init__("All Channels Overview", device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        # Connection status
        self.conn_label = QLabel("● Connecting to device server...")
        self.conn_label.setStyleSheet("background-color: #34495e; color: white; padding: 5px;")
        self.content_layout.addWidget(self.conn_label)
        
        # Create table for all channels
        self.channel_table = QTableWidget()
        self.channel_table.setColumnCount(6)
        headers = ["Channel", "VMon (V)", "IMon (A)", "VSet (V)", "ISet (A)", "Status"]
        self.channel_table.setHorizontalHeaderLabels(headers)
        self.channel_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.channel_table.setAlternatingRowColors(True)
        
        self.content_layout.addWidget(self.channel_table)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh Now")
        self.refresh_btn.setStyleSheet("background-color: #3498db; padding: 8px;")
        self.refresh_btn.clicked.connect(self.update_values)
        
        self.on_all_btn = QPushButton("ON ALL")
        self.on_all_btn.setStyleSheet("background-color: #27ae60; padding: 8px;")
        self.on_all_btn.clicked.connect(self.global_on)
        
        self.off_all_btn = QPushButton("OFF ALL")
        self.off_all_btn.setStyleSheet("background-color: #e74c3c; padding: 8px;")
        self.off_all_btn.clicked.connect(self.global_off)
        
        control_layout.addWidget(self.refresh_btn)
        control_layout.addWidget(self.on_all_btn)
        control_layout.addWidget(self.off_all_btn)
        self.content_layout.addLayout(control_layout)
        
        self.content_layout.addStretch()
        
        self.connect_to_device()
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_values)
        self.update_timer.start(2000)
    
    def connect_to_device(self):
        """Connect to TANGO device"""
        if not TANGO_AVAILABLE:
            self.conn_label.setText("✗ TANGO module not available")
            return
            
        try:
            self.tango_device = DeviceProxy(self.device_name)
            self.conn_label.setText(f"✓ Connected to {self.device_name}")
            self.conn_label.setStyleSheet("background-color: #27ae60; color: white; padding: 5px;")
            self.update_values()
        except Exception as e:
            self.conn_label.setText(f"✗ Failed to connect: {e}")
            self.conn_label.setStyleSheet("background-color: #e74c3c; color: white; padding: 5px;")
    
    def update_values(self):
        """Update table with all channel data from device"""
        if not self.tango_device:
            return
        
        try:
            self.channel_table.setRowCount(8)
            
            # Get data from device
            vmon = self.tango_device.VMon if hasattr(self.tango_device, 'VMon') else [0]*8
            imon = self.tango_device.IMon if hasattr(self.tango_device, 'IMon') else [0]*8
            vset = self.tango_device.VSet if hasattr(self.tango_device, 'VSet') else [0]*8
            iset = self.tango_device.ISet if hasattr(self.tango_device, 'ISet') else [0]*8
            
            for ch in range(8):
                # Channel number
                self.channel_table.setItem(ch, 0, QTableWidgetItem(f"CH{ch}"))
                
                # VMon
                vmon_val = vmon[ch] if ch < len(vmon) else 0
                vmon_item = QTableWidgetItem(f"{vmon_val:.2f}")
                self.channel_table.setItem(ch, 1, vmon_item)
                
                # IMon
                imon_val = imon[ch] if ch < len(imon) else 0
                imon_item = QTableWidgetItem(f"{imon_val:.4f}")
                self.channel_table.setItem(ch, 2, imon_item)
                
                # VSet
                vset_val = vset[ch] if ch < len(vset) else 0
                vset_item = QTableWidgetItem(f"{vset_val:.2f}")
                self.channel_table.setItem(ch, 3, vset_item)
                
                # ISet
                iset_val = iset[ch] if ch < len(iset) else 0
                iset_item = QTableWidgetItem(f"{iset_val:.4f}")
                self.channel_table.setItem(ch, 4, iset_item)
                
                # Status (simplified - on if VMon > 0)
                status = "ON" if vmon_val > 0 else "OFF"
                status_item = QTableWidgetItem(status)
                if status == "ON":
                    status_item.setBackground(Qt.green)
                else:
                    status_item.setBackground(Qt.red)
                self.channel_table.setItem(ch, 5, status_item)
            
            self.status_label.setText(f"Updated at {QTimer.remainingTime()}")
            
        except Exception as e:
            self.status_label.setText(f"Update error: {e}")
    
    def global_on(self):
        if self.tango_device and hasattr(self.tango_device, 'On'):
            self.tango_device.On()
            self.status_label.setText("Global ON command sent")
    
    def global_off(self):
        if self.tango_device and hasattr(self.tango_device, 'Off'):
            self.tango_device.Off()
            self.status_label.setText("Global OFF command sent")

def get_panel(device=None):
    return ChannelsPanel(device)

def main():
    app = QApplication(sys.argv)
    panel = ChannelsPanel()
    panel.setWindowTitle("All Channels - Real Data")
    panel.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
