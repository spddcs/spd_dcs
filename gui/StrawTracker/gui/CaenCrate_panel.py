#!/usr/bin/env python3
"""CAEN HV Crate Panel - Reads real data from TANGO device server"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel, SECTION_FONT

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                             QGroupBox, QPushButton, QApplication, QFrame)
from PyQt5.QtCore import Qt, QTimer

try:
    import tango
    from tango import DeviceProxy, DevState
    TANGO_AVAILABLE = True
except ImportError:
    TANGO_AVAILABLE = False
    print("Warning: TANGO module not available")

class CaenCratePanel(BaseNodePanel):
    def __init__(self, device=None, parent=None):
        self.tango_device = None
        self.device_name = "SPD/CaenSMARTHV/StrawTrackerCaenHV_0"  # Device server name from your code
        super().__init__("CAEN HV Crate", device, parent)
        
    def setup_ui(self):
        super().setup_ui()
        
        # Connection status at top
        self.conn_frame = QFrame()
        self.conn_frame.setStyleSheet("QFrame { background-color: #34495e; border-radius: 5px; }")
        conn_layout = QHBoxLayout(self.conn_frame)
        self.conn_status_label = QLabel("● Connecting to device server...")
        self.conn_status_label.setStyleSheet("color: white; font-weight: bold; padding: 5px;")
        conn_layout.addWidget(self.conn_status_label)
        self.content_layout.addWidget(self.conn_frame)
        
        # Crate Information Group
        crate_group = QGroupBox("Crate Information")
        crate_group.setFont(SECTION_FONT)
        crate_layout = QGridLayout()
        
        self.crate_fields = {}
        crate_items = [
            ("Crate Model:", "model", "--"),
            ("Address:", "address", "--"),
            ("Connection Status:", "conn_status", "--"),
            ("Clear Alarm:", "clear_alarm", "False")
        ]
        
        for i, (label, key, default) in enumerate(crate_items):
            crate_layout.addWidget(QLabel(label), i, 0)
            self.crate_fields[key] = QLabel(default)
            self.crate_fields[key].setStyleSheet("font-weight: bold; padding: 5px; background-color: #ecf0f1;")
            crate_layout.addWidget(self.crate_fields[key], i, 1)
        
        crate_group.setLayout(crate_layout)
        self.content_layout.addWidget(crate_group)
        
        # Board Information Group
        board_group = QGroupBox("Board Information (Board 00)")
        board_group.setFont(SECTION_FONT)
        board_layout = QGridLayout()
        
        self.board_fields = {}
        board_items = [
            ("Board Model:", "board_model", "--"),
            ("HV Max:", "bdhvmax", "-- V"),
            ("I Max:", "bdhimax", "-- A"),
            ("Board Status:", "bdstatus", "--")
        ]
        
        for i, (label, key, default) in enumerate(board_items):
            board_layout.addWidget(QLabel(label), i, 0)
            self.board_fields[key] = QLabel(default)
            self.board_fields[key].setStyleSheet("font-weight: bold; padding: 5px; background-color: #ecf0f1;")
            board_layout.addWidget(self.board_fields[key], i, 1)
        
        board_group.setLayout(board_layout)
        self.content_layout.addWidget(board_group)
        
        # Channels Summary Group
        channels_group = QGroupBox("Channels Summary (First 4 channels)")
        channels_group.setFont(SECTION_FONT)
        channels_layout = QGridLayout()
        
        # Headers
        headers = ["Channel", "VMon (V)", "IMon (A)", "VSet (V)", "ISet (A)"]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold; background-color: #bdc3c7; padding: 5px;")
            channels_layout.addWidget(label, 0, col)
        
        self.channel_fields = {}
        for ch in range(4):  # Show first 4 channels in summary
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
        self.content_layout.addWidget(channels_group)
        
        # Control buttons
        control_group = QGroupBox("Global Controls")
        control_group.setFont(SECTION_FONT)
        control_layout = QHBoxLayout()
        
        self.on_btn = QPushButton("ON ALL")
        self.on_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold;")
        self.on_btn.clicked.connect(self.global_on)
        
        self.off_btn = QPushButton("OFF ALL")
        self.off_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; font-weight: bold;")
        self.off_btn.clicked.connect(self.global_off)
        
        self.reset_btn = QPushButton("RESET")
        self.reset_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 10px; font-weight: bold;")
        self.reset_btn.clicked.connect(self.global_reset)
        
        control_layout.addWidget(self.on_btn)
        control_layout.addWidget(self.off_btn)
        control_layout.addWidget(self.reset_btn)
        control_group.setLayout(control_layout)
        self.content_layout.addWidget(control_group)
        
        self.content_layout.addStretch()
        
        # Connect to TANGO device
        self.connect_to_device()
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_values)
        self.update_timer.start(1000)  # Update every second
    
    def connect_to_device(self):
        """Connect to TANGO device server"""
        if not TANGO_AVAILABLE:
            self.conn_status_label.setText("✗ TANGO module not available")
            self.conn_status_label.setStyleSheet("color: #e74c3c; font-weight: bold; padding: 5px;")
            return
            
        try:
            # Connect to the Ps device server
            self.tango_device = DeviceProxy(self.device_name)
            
            # Check if device is reachable
            state = self.tango_device.state()
            self.conn_status_label.setText(f"✓ Connected to {self.device_name} (State: {state})")
            self.conn_status_label.setStyleSheet("color: #27ae60; font-weight: bold; padding: 5px;")
            
            # Update crate fields with real data
            self.update_values()
            
        except Exception as e:
            self.conn_status_label.setText(f"✗ Failed to connect: {e}")
            self.conn_status_label.setStyleSheet("color: #e74c3c; font-weight: bold; padding: 5px;")
            print(f"Connection error: {e}")
    
    def update_values(self):
        """Update all values from TANGO device server"""
        if not self.tango_device:
            return
        
        try:
            # Update crate information
            if hasattr(self.tango_device, 'CrateModel'):
                self.crate_fields["model"].setText(str(self.tango_device.CrateModel))
            
            if hasattr(self.tango_device, 'Address'):
                self.crate_fields["address"].setText(str(self.tango_device.Address))
            
            if hasattr(self.tango_device, 'ConnectionStatus'):
                conn_status = self.tango_device.ConnectionStatus
                status_text = "Connected" if conn_status else "Disconnected"
                self.crate_fields["conn_status"].setText(status_text)
                color = "#27ae60" if conn_status else "#e74c3c"
                self.crate_fields["conn_status"].setStyleSheet(f"color: {color}; font-weight: bold; padding: 5px;")
            
            if hasattr(self.tango_device, 'ClearAlarm'):
                self.crate_fields["clear_alarm"].setText(str(self.tango_device.ClearAlarm))
            
            # Update board information
            if hasattr(self.tango_device, 'BoardModel'):
                self.board_fields["board_model"].setText(str(self.tango_device.BoardModel))
            
            if hasattr(self.tango_device, 'BDHVmax'):
                self.board_fields["bdhvmax"].setText(f"{self.tango_device.BDHVmax:.1f} V")
            
            if hasattr(self.tango_device, 'BDHImax'):
                self.board_fields["bdhimax"].setText(f"{self.tango_device.BDHImax:.3f} A")
            
            if hasattr(self.tango_device, 'BdStatus'):
                bdstatus = self.tango_device.BdStatus
                status_map = {0: "OK", 1: "Warning", 2: "Error", 3: "Fault"}
                status_text = status_map.get(bdstatus, f"Unknown ({bdstatus})")
                self.board_fields["bdstatus"].setText(status_text)
                
                # Color code board status
                if bdstatus == 0:
                    self.board_fields["bdstatus"].setStyleSheet("color: #27ae60; font-weight: bold; padding: 5px;")
                elif bdstatus == 1:
                    self.board_fields["bdstatus"].setStyleSheet("color: #f39c12; font-weight: bold; padding: 5px;")
                else:
                    self.board_fields["bdstatus"].setStyleSheet("color: #e74c3c; font-weight: bold; padding: 5px;")
            
            # Update channel data
            if hasattr(self.tango_device, 'VMon'):
                vmon_array = self.tango_device.VMon
                for ch in range(min(4, len(vmon_array))):
                    if ch in self.channel_fields:
                        self.channel_fields[ch]["vmon"].setText(f"{vmon_array[ch]:.2f}")
            
            if hasattr(self.tango_device, 'IMon'):
                imon_array = self.tango_device.IMon
                for ch in range(min(4, len(imon_array))):
                    if ch in self.channel_fields:
                        self.channel_fields[ch]["imon"].setText(f"{imon_array[ch]:.4f}")
            
            if hasattr(self.tango_device, 'VSet'):
                vset_array = self.tango_device.VSet
                for ch in range(min(4, len(vset_array))):
                    if ch in self.channel_fields:
                        self.channel_fields[ch]["vset"].setText(f"{vset_array[ch]:.2f}")
            
            if hasattr(self.tango_device, 'ISet'):
                iset_array = self.tango_device.ISet
                for ch in range(min(4, len(iset_array))):
                    if ch in self.channel_fields:
                        self.channel_fields[ch]["iset"].setText(f"{iset_array[ch]:.4f}")
            
            self.status_label.setText(f"Last update: OK")
            
        except Exception as e:
            self.status_label.setText(f"Update error: {e}")
            print(f"Update error: {e}")
    
    def global_on(self):
        """Turn on all channels"""
        if self.tango_device and hasattr(self.tango_device, 'On'):
            try:
                self.tango_device.On()
                self.status_label.setText("Global ON command sent")
            except Exception as e:
                self.status_label.setText(f"Error: {e}")
    
    def global_off(self):
        """Turn off all channels"""
        if self.tango_device and hasattr(self.tango_device, 'Off'):
            try:
                self.tango_device.Off()
                self.status_label.setText("Global OFF command sent")
            except Exception as e:
                self.status_label.setText(f"Error: {e}")
    
    def global_reset(self):
        """Reset the device"""
        if self.tango_device and hasattr(self.tango_device, 'Reset'):
            try:
                self.tango_device.Reset()
                self.status_label.setText("Reset command sent")
            except Exception as e:
                self.status_label.setText(f"Error: {e}")

def get_panel(device=None):
    return CaenCratePanel(device)

def main():
    app = QApplication(sys.argv)
    panel = CaenCratePanel()
    panel.setWindowTitle("CAEN HV Crate - Real Data")
    panel.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
