#!/usr/bin/env python3
"""CAEN HV Boards Panel - Real data from TANGO device server"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel, SECTION_FONT

from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QLabel, QGroupBox, 
                             QTabWidget, QWidget, QApplication, QFrame)
from PyQt5.QtCore import Qt, QTimer

try:
    import tango
    from tango import DeviceProxy
    TANGO_AVAILABLE = True
except ImportError:
    TANGO_AVAILABLE = False

class BoardsPanel(BaseNodePanel):
    def __init__(self, device=None, parent=None):
        self.tango_device = None
        self.device_name = "SPD/CaenSMARTHV/StrawTrackerCaenHV_0"
        super().__init__("CAEN HV Boards", device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        # Connection status
        self.conn_label = QLabel("● Connecting to device server...")
        self.conn_label.setStyleSheet("background-color: #34495e; color: white; padding: 5px;")
        self.content_layout.addWidget(self.conn_label)
        
        # Create tab widget for each board (we have 1 board in your device)
        self.board_tabs = QTabWidget()
        
        # Create tab for Board 00
        board_tab = self.create_board_tab(0)
        self.board_tabs.addTab(board_tab, "Board 00")
        
        self.content_layout.addWidget(self.board_tabs)
        
        self.content_layout.addStretch()
        
        self.connect_to_device()
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_values)
        self.update_timer.start(1000)
    
    def create_board_tab(self, board_num):
        """Create tab for a specific board"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Board information
        info_group = QGroupBox(f"Board {board_num:02d} Information")
        info_layout = QGridLayout()
        
        self.board_fields = {}
        info_items = [
            ("Board Model:", "model", "--"),
            ("HV Max:", "hvmax", "-- V"),
            ("I Max:", "imax", "-- A"),
            ("Board Status:", "status", "--"),
            ("Connection:", "connection", "--")
        ]
        
        for i, (label, key, default) in enumerate(info_items):
            info_layout.addWidget(QLabel(label), i, 0)
            self.board_fields[key] = QLabel(default)
            self.board_fields[key].setStyleSheet("font-weight: bold; padding: 5px; background-color: #ecf0f1;")
            info_layout.addWidget(self.board_fields[key], i, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Channels table for this board
        channels_group = QGroupBox("Channels (0-7)")
        channels_layout = QGridLayout()
        
        # Headers
        headers = ["Channel", "VMon (V)", "IMon (A)", "VSet (V)", "ISet (A)"]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold; background-color: #bdc3c7; padding: 5px;")
            channels_layout.addWidget(label, 0, col)
        
        self.channel_fields = {}
        for ch in range(8):
            row = ch + 1
            # Channel name
            ch_label = QLabel(f"CH{ch}")
            ch_label.setStyleSheet("font-weight: bold;")
            channels_layout.addWidget(ch_label, row, 0)
            
            # Create fields for each channel
            self.channel_fields[ch] = {}
            for col, key in enumerate(["vmon", "imon", "vset", "iset"]):
                field = QLabel("--")
                field.setStyleSheet("padding: 3px; background-color: #ecf0f1;")
                channels_layout.addWidget(field, row, col + 1)
                self.channel_fields[ch][key] = field
        
        channels_group.setLayout(channels_layout)
        layout.addWidget(channels_group)
        
        layout.addStretch()
        return tab
    
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
        """Update board and channel information from device"""
        if not self.tango_device:
            return
            
        try:
            # Update board information
            if hasattr(self.tango_device, 'BoardModel'):
                self.board_fields["model"].setText(str(self.tango_device.BoardModel))
            
            if hasattr(self.tango_device, 'BDHVmax'):
                self.board_fields["hvmax"].setText(f"{self.tango_device.BDHVmax:.1f} V")
            
            if hasattr(self.tango_device, 'BDHImax'):
                self.board_fields["imax"].setText(f"{self.tango_device.BDHImax:.4f} A")
            
            if hasattr(self.tango_device, 'BdStatus'):
                status = self.tango_device.BdStatus
                status_text = {0: "OK", 1: "Warning", 2: "Error"}.get(status, f"Unknown({status})")
                self.board_fields["status"].setText(status_text)
                
                color = "#27ae60" if status == 0 else "#f39c12" if status == 1 else "#e74c3c"
                self.board_fields["status"].setStyleSheet(f"color: {color}; font-weight: bold; padding: 5px;")
            
            if hasattr(self.tango_device, 'ConnectionStatus'):
                conn = self.tango_device.ConnectionStatus
                self.board_fields["connection"].setText("Connected" if conn else "Disconnected")
                color = "#27ae60" if conn else "#e74c3c"
                self.board_fields["connection"].setStyleSheet(f"color: {color}; font-weight: bold; padding: 5px;")
            
            # Update channel data
            if hasattr(self.tango_device, 'VMon'):
                vmon = self.tango_device.VMon
                for ch in range(8):
                    if ch < len(vmon):
                        self.channel_fields[ch]["vmon"].setText(f"{vmon[ch]:.2f}")
            
            if hasattr(self.tango_device, 'IMon'):
                imon = self.tango_device.IMon
                for ch in range(8):
                    if ch < len(imon):
                        self.channel_fields[ch]["imon"].setText(f"{imon[ch]:.4f}")
            
            if hasattr(self.tango_device, 'VSet'):
                vset = self.tango_device.VSet
                for ch in range(8):
                    if ch < len(vset):
                        self.channel_fields[ch]["vset"].setText(f"{vset[ch]:.2f}")
            
            if hasattr(self.tango_device, 'ISet'):
                iset = self.tango_device.ISet
                for ch in range(8):
                    if ch < len(iset):
                        self.channel_fields[ch]["iset"].setText(f"{iset[ch]:.4f}")
            
        except Exception as e:
            print(f"Update error: {e}")

def get_panel(device=None):
    return BoardsPanel(device)

def main():
    app = QApplication(sys.argv)
    panel = BoardsPanel()
    panel.setWindowTitle("CAEN HV Boards - Real Data")
    panel.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
