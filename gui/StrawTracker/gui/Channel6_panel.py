#!/usr/bin/env python3
"""Channel 0 Panel - Complete CAEN SMARTHV parameters"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel

from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QLabel, QGroupBox, 
                             QPushButton, QApplication, QLineEdit, 
                             QHBoxLayout, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QTimer

try:
    import tango
    from tango import DeviceProxy
    TANGO_AVAILABLE = True
except ImportError:
    TANGO_AVAILABLE = False

class Channel6Panel(BaseNodePanel):
    def __init__(self, device=None, parent=None):
        self.tango_device = None
        self.device_name = "spd/caensmarthv/strawtrackercaenhv_0"
        self.channel = 6
        super().__init__("Channel 6 Control", device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        # Connection status
        self.conn_label = QLabel("● Connecting to device server...")
        self.conn_label.setStyleSheet("background-color: #34495e; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
        self.content_layout.addWidget(self.conn_label)
        
        # Main widget
        main_widget = QFrame()
        main_layout = QVBoxLayout(main_widget)
        
        # Parameters group - Removed the "All 13 Parameters" title
        param_group = QGroupBox()
        param_group.setStyleSheet("QGroupBox { border: none; margin-top: 0px; }")
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # Dictionary for value displays
        self.values = {}
        
        # Define all parameters
        params = [
            ("VMon (Voltage Monitor)", "vmon", "V"),
            ("IMon (Current Monitor)", "imon", "A"),
            ("VSet (Voltage Setpoint)", "vset", "V"),
            ("ISet (Current Setpoint)", "iset", "A"),
            ("Channel Name", "name", ""),
            ("Channel Index", "index", ""),
            ("Power (Pw)", "pw", "W"),
            ("Power Down (PDwn)", "pdwn", "W"),
            ("Ramp Up Rate (RUp)", "rup", "V/s"),
            ("Ramp Down Rate (RDwn)", "rdwn", "V/s"),
            ("Current Range (IMRange)", "imrange", "A"),
            ("Channel Status", "ch_status", ""),
            ("Trip Status", "trip", "")
        ]
        
        row = 0
        for label_text, key, unit in params:
            # Label
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold;")
            layout.addWidget(label, row, 0)
            
            # Value display
            self.values[key] = QLabel("--")
            self.values[key].setStyleSheet("background-color: #ecf0f1; padding: 8px; border-radius: 5px; font-family: monospace; font-size: 12px;")
            self.values[key].setMinimumWidth(200)
            layout.addWidget(self.values[key], row, 1)
            
            # Unit
            if unit:
                unit_label = QLabel(unit)
                unit_label.setStyleSheet("color: #7f8c8d;")
                layout.addWidget(unit_label, row, 2)
            row += 1
        
        # Separator
        separator = QLabel("─" * 50)
        separator.setAlignment(Qt.AlignCenter)
        layout.addWidget(separator, row, 0, 1, 3)
        row += 1
        
        # VSet edit
        layout.addWidget(QLabel("Set VSet (V):"), row, 0)
        self.vset_edit = QLineEdit()
        self.vset_edit.setStyleSheet("padding: 5px;")
        layout.addWidget(self.vset_edit, row, 1)
        row += 1
        
        # ISet edit
        layout.addWidget(QLabel("Set ISet (A):"), row, 0)
        self.iset_edit = QLineEdit()
        self.iset_edit.setStyleSheet("padding: 5px;")
        layout.addWidget(self.iset_edit, row, 1)
        row += 1
        
        param_group.setLayout(layout)
        main_layout.addWidget(param_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px; font-weight: bold; border-radius: 5px;")
        refresh_btn.clicked.connect(self.update_values)
        btn_layout.addWidget(refresh_btn)
        
        apply_btn = QPushButton("Apply Settings")
        apply_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 8px; font-weight: bold; border-radius: 5px;")
        apply_btn.clicked.connect(self.apply_settings)
        btn_layout.addWidget(apply_btn)
        
        on_btn = QPushButton("Turn ON")
        on_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px; font-weight: bold; border-radius: 5px;")
        on_btn.clicked.connect(self.turn_on)
        btn_layout.addWidget(on_btn)
        
        off_btn = QPushButton("Turn OFF")
        off_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; font-weight: bold; border-radius: 5px;")
        off_btn.clicked.connect(self.turn_off)
        btn_layout.addWidget(off_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 8px; font-weight: bold; border-radius: 5px;")
        reset_btn.clicked.connect(self.reset_device)
        btn_layout.addWidget(reset_btn)
        
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()
        
        self.content_layout.addWidget(main_widget)
        
        # Connect to device
        self.connect_to_device()
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(2000)
    
    def connect_to_device(self):
        if not TANGO_AVAILABLE:
            self.conn_label.setText("✗ TANGO module not available")
            return
        
        try:
            self.tango_device = DeviceProxy(self.device_name)
            self.conn_label.setText(f"✓ Connected to {self.device_name}")
            self.conn_label.setStyleSheet("background-color: #27ae60; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
            self.update_values()
        except Exception as e:
            self.conn_label.setText(f"✗ Connection failed: {e}")
            self.conn_label.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
    
    def update_values(self):
        if not self.tango_device:
            return
        
        try:
            # Read all attributes
            vmon = self._get_attr('VMon')
            imon = self._get_attr('IMon')
            vset = self._get_attr('VSet')
            iset = self._get_attr('ISet')
            name = self._get_attr('ChannelName')
            idx = self._get_attr('ChannelIndex')
            pw = self._get_attr('Pw')
            pdwn = self._get_attr('PDwn')
            rup = self._get_attr('RUp')
            rdwn = self._get_attr('RDwn')
            imrange = self._get_attr('IMRange')
            ch_status = self._get_attr('ChannelStatus')
            trip = self._get_attr('Trip')
            
            # Update VMon
            if vmon is not None and len(vmon) > self.channel:
                val = vmon[self.channel]
                self.values['vmon'].setText(f"{val:.2f} V")
            else:
                self.values['vmon'].setText("N/A")
            
            # Update IMon
            if imon is not None and len(imon) > self.channel:
                val = imon[self.channel]
                self.values['imon'].setText(f"{val:.6f} A")
            else:
                self.values['imon'].setText("N/A")
            
            # Update VSet
            if vset is not None and len(vset) > self.channel:
                val = vset[self.channel]
                self.values['vset'].setText(f"{val:.2f} V")
                self.vset_edit.setText(f"{val:.1f}")
            else:
                self.values['vset'].setText("N/A")
            
            # Update ISet
            if iset is not None and len(iset) > self.channel:
                val = iset[self.channel]
                self.values['iset'].setText(f"{val:.6f} A")
                self.iset_edit.setText(f"{val:.6f}")
            else:
                self.values['iset'].setText("N/A")
            
            # Update Channel Name (string, not array)
            if name is not None:
                self.values['name'].setText(str(name))
            else:
                self.values['name'].setText("N/A")
            
            # Update Channel Index
            if idx is not None and len(idx) > self.channel:
                self.values['index'].setText(str(idx[self.channel]))
            else:
                self.values['index'].setText("N/A")
            
            # Update Power
            if pw is not None and len(pw) > self.channel:
                self.values['pw'].setText(f"{pw[self.channel]:.4f} W")
            else:
                self.values['pw'].setText("N/A")
            
            # Update Power Down
            if pdwn is not None and len(pdwn) > self.channel:
                self.values['pdwn'].setText(f"{pdwn[self.channel]:.4f} W")
            else:
                self.values['pdwn'].setText("N/A")
            
            # Update Ramp Up
            if rup is not None and len(rup) > self.channel:
                self.values['rup'].setText(f"{rup[self.channel]:.2f} V/s")
            else:
                self.values['rup'].setText("N/A")
            
            # Update Ramp Down
            if rdwn is not None and len(rdwn) > self.channel:
                self.values['rdwn'].setText(f"{rdwn[self.channel]:.2f} V/s")
            else:
                self.values['rdwn'].setText("N/A")
            
            # Update Current Range
            if imrange is not None and len(imrange) > self.channel:
                self.values['imrange'].setText(f"{imrange[self.channel]:.6f} A")
            else:
                self.values['imrange'].setText("N/A")
            
            # Update Channel Status with color
            if ch_status is not None and len(ch_status) > self.channel:
                status_val = ch_status[self.channel]
                status_map = {0: "OFF", 1: "ON", 2: "RAMPING", 3: "TRIP", 4: "FAULT"}
                status_text = status_map.get(status_val, f"UNKNOWN({status_val})")
                self.values['ch_status'].setText(status_text)
                
                if status_val == 1:
                    self.values['ch_status'].setStyleSheet("background-color: #27ae60; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
                elif status_val == 2:
                    self.values['ch_status'].setStyleSheet("background-color: #f39c12; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
                elif status_val in [3, 4]:
                    self.values['ch_status'].setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
                else:
                    self.values['ch_status'].setStyleSheet("background-color: #95a5a6; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
            else:
                self.values['ch_status'].setText("N/A")
            
            # Update Trip Status
            if trip is not None and len(trip) > self.channel:
                trip_val = trip[self.channel]
                self.values['trip'].setText("TRIPPED" if trip_val else "OK")
                if trip_val:
                    self.values['trip'].setStyleSheet("background-color: #e74c3c; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
                else:
                    self.values['trip'].setStyleSheet("background-color: #27ae60; color: white; padding: 8px; border-radius: 5px; font-weight: bold;")
            else:
                self.values['trip'].setText("N/A")
            
            self.status_label.setText("✓ Updated")
            
        except Exception as e:
            self.status_label.setText(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    def _get_attr(self, attr_name):
        """Safely get attribute value"""
        try:
            if hasattr(self.tango_device, attr_name):
                return getattr(self.tango_device, attr_name)
        except Exception as e:
            print(f"Error reading {attr_name}: {e}")
        return None
    
    def apply_settings(self):
        if not self.tango_device:
            QMessageBox.warning(self, "Error", "Device not connected")
            return
        
        try:
            # Read current arrays
            vset_arr = self._get_attr('VSet')
            iset_arr = self._get_attr('ISet')
            
            if vset_arr is not None and iset_arr is not None:
                # Convert to list if numpy array
                if hasattr(vset_arr, 'tolist'):
                    vset_list = vset_arr.tolist()
                    iset_list = iset_arr.tolist()
                else:
                    vset_list = list(vset_arr)
                    iset_list = list(iset_arr)
                
                # Update this channel
                vset_list[self.channel] = float(self.vset_edit.text())
                iset_list[self.channel] = float(self.iset_edit.text())
                
                # Write back
                self.tango_device.VSet = vset_list
                self.tango_device.ISet = iset_list
                
                QMessageBox.information(self, "Success", f"Channel {self.channel} updated")
                self.update_values()
            else:
                QMessageBox.warning(self, "Error", "Could not read current settings")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply settings: {e}")
    
    def turn_on(self):
        if self.tango_device and hasattr(self.tango_device, 'On'):
            try:
                self.tango_device.On()
                QMessageBox.information(self, "Success", "ON command sent")
                self.update_values()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def turn_off(self):
        if self.tango_device and hasattr(self.tango_device, 'Off'):
            try:
                self.tango_device.Off()
                QMessageBox.information(self, "Success", "OFF command sent")
                self.update_values()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def reset_device(self):
        if self.tango_device and hasattr(self.tango_device, 'Reset'):
            try:
                self.tango_device.Reset()
                QMessageBox.information(self, "Success", "Reset command sent")
                self.update_values()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

def get_panel(device=None):
    return Channel6Panel(device)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    panel = Channel6Panel()
    panel.show()
    sys.exit(app.exec_())
