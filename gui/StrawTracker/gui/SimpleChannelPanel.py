#!/usr/bin/env python3
"""Simple Channel Panel showing all 13 parameters"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel

from PyQt5.QtWidgets import (QVBoxLayout, QGridLayout, QLabel, QGroupBox, 
                             QPushButton, QApplication, QWidget)
from PyQt5.QtCore import Qt, QTimer

try:
    import tango
    from tango import DeviceProxy
    TANGO_AVAILABLE = True
except ImportError:
    TANGO_AVAILABLE = False

class SimpleChannelPanel(BaseNodePanel):
    def __init__(self, channel=0, device=None, parent=None):
        self.channel = channel
        self.tango_device = None
        self.device_name = "spd/caensmarthv/strawtrackercaenhv_0"
        super().__init__(f"Channel {channel} - All Parameters", device, parent)
    
    def setup_ui(self):
        super().setup_ui()
        
        # Main group
        main_group = QGroupBox(f"Channel {self.channel} - All 13 Parameters")
        main_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        layout = QGridLayout()
        
        # Define all parameters
        self.params = {}
        param_list = [
            ("IMRange (A)", "imrange"),
            ("IMon (A)", "imon"),
            ("ISet (A)", "iset"),
            ("Name", "name"),
            ("PDwn (W)", "pdwn"),
            ("Pw (W)", "pw"),
            ("RDwn (V/s)", "rdwn"),
            ("RUp (V/s)", "rup"),
            ("Status", "status"),
            ("Trip", "trip"),
            ("VMon (V)", "vmon"),
            ("VSet (V)", "vset"),
            ("Index", "index")
        ]
        
        row = 0
        for label, key in param_list:
            layout.addWidget(QLabel(label), row, 0)
            self.params[key] = QLabel("--")
            self.params[key].setStyleSheet("font-weight: bold; padding: 5px; background-color: #ecf0f1;")
            layout.addWidget(self.params[key], row, 1)
            row += 1
        
        main_group.setLayout(layout)
        self.content_layout.addWidget(main_group)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.update_values)
        self.content_layout.addWidget(self.refresh_btn)
        
        self.content_layout.addStretch()
        
        self.connect_to_device()
        
        # Timer for auto-refresh
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(3000)
    
    def connect_to_device(self):
        try:
            self.tango_device = DeviceProxy(self.device_name)
            self.status_label.setText("Connected")
            self.update_values()
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
    
    def update_values(self):
        if not self.tango_device:
            return
        
        try:
            # Read all arrays
            data = {}
            for attr in ['IMRange', 'IMon', 'ISet', 'ChannelName', 'PDwn', 'Pw', 
                        'RDwn', 'RUp', 'Status', 'Trip', 'VMon', 'VSet', 'ChannelIndex']:
                try:
                    value = getattr(self.tango_device, attr)
                    if isinstance(value, (list, tuple)) and len(value) > self.channel:
                        data[attr] = value[self.channel]
                    else:
                        data[attr] = value
                except:
                    data[attr] = "N/A"
            
            # Update display
            self.params['imrange'].setText(str(data.get('IMRange', '--')))
            self.params['imon'].setText(str(data.get('IMon', '--')))
            self.params['iset'].setText(str(data.get('ISet', '--')))
            self.params['name'].setText(str(data.get('ChannelName', '--')))
            self.params['pdwn'].setText(str(data.get('PDwn', '--')))
            self.params['pw'].setText(str(data.get('Pw', '--')))
            self.params['rdwn'].setText(str(data.get('RDwn', '--')))
            self.params['rup'].setText(str(data.get('RUp', '--')))
            self.params['status'].setText(str(data.get('Status', '--')))
            self.params['trip'].setText(str(data.get('Trip', '--')))
            self.params['vmon'].setText(str(data.get('VMon', '--')))
            self.params['vset'].setText(str(data.get('VSet', '--')))
            self.params['index'].setText(str(data.get('ChannelIndex', '--')))
            
            self.status_label.setText("Updated")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

def get_panel(device=None):
    # Extract channel number from the panel name if possible
    return SimpleChannelPanel(0, device)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = SimpleChannelPanel(0)
    panel.show()
    sys.exit(app.exec_())
