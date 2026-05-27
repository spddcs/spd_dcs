#!/usr/bin/env python3
"""
HV Control GUI - HTTP API Version
Connects to device simulator on localhost:8080
"""

import sys
import json
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class HVControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_url = "http://localhost:8080"
        self.init_ui()
        
        # Auto-refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
    
    def init_ui(self):
        self.setWindowTitle("SPD DCS - CAEN HV Control System")
        self.setGeometry(100, 100, 1100, 700)
        
        # Styling
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QLabel { color: white; }
            QGroupBox { color: white; border: 2px solid #3498db; border-radius: 5px; margin-top: 10px; padding-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            QPushButton { background-color: #3498db; color: white; border: none; padding: 8px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #2980b9; }
            QTableWidget { background-color: white; }
            QLineEdit { padding: 5px; border-radius: 3px; }
        """)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Header
        header = QLabel("CAEN Smart HV Control System")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #3498db; padding: 10px;")
        layout.addWidget(header)
        
        # Status bar
        status_frame = QFrame()
        status_frame.setStyleSheet("QFrame { background-color: #34495e; border-radius: 5px; }")
        status_layout = QHBoxLayout(status_frame)
        
        self.conn_label = QLabel("● Device: Connecting...")
        self.conn_label.setStyleSheet("color: #f39c12; font-weight: bold;")
        status_layout.addWidget(self.conn_label)
        
        self.temp_label = QLabel("Temperature: -- °C")
        self.temp_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        status_layout.addWidget(self.temp_label)
        
        status_layout.addStretch()
        layout.addWidget(status_frame)
        
        # Channel table
        group = QGroupBox("Channel Control")
        group_layout = QVBoxLayout(group)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["CH", "VMon (V)", "IMon (A)", "VSet (V)", "ISet (A)", "", ""])
        self.table.setRowCount(8)
        
        self.vset_inputs = []
        self.iset_inputs = []
        self.status_labels = []
        
        for row in range(8):
            # Channel number
            ch_item = QTableWidgetItem(f"{row}")
            ch_item.setFlags(Qt.ItemIsSelectable)
            self.table.setItem(row, 0, ch_item)
            
            # VMon (read-only)
            vmon = QTableWidgetItem("--")
            vmon.setFlags(Qt.ItemIsSelectable)
            self.table.setItem(row, 1, vmon)
            
            # IMon (read-only)
            imon = QTableWidgetItem("--")
            imon.setFlags(Qt.ItemIsSelectable)
            self.table.setItem(row, 2, imon)
            
            # VSet input
            vset = QLineEdit("0")
            vset.setFixedWidth(80)
            self.table.setCellWidget(row, 3, vset)
            self.vset_inputs.append(vset)
            
            # ISet input
            iset = QLineEdit("0")
            iset.setFixedWidth(80)
            self.table.setCellWidget(row, 4, iset)
            self.iset_inputs.append(iset)
            
            # Apply button
            btn_apply = QPushButton("Apply")
            btn_apply.clicked.connect(lambda checked, r=row: self.apply_settings(r))
            self.table.setCellWidget(row, 5, btn_apply)
        
        group_layout.addWidget(self.table)
        layout.addWidget(group)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        
        btn_on = QPushButton("ON ALL")
        btn_on.setStyleSheet("background-color: #27ae60;")
        btn_on.clicked.connect(self.turn_on)
        
        btn_off = QPushButton("OFF ALL")
        btn_off.setStyleSheet("background-color: #e74c3c;")
        btn_off.clicked.connect(self.turn_off)
        
        btn_reset = QPushButton("RESET")
        btn_reset.setStyleSheet("background-color: #f39c12;")
        btn_reset.clicked.connect(self.reset_device)
        
        btn_refresh = QPushButton("REFRESH")
        btn_refresh.clicked.connect(self.update_data)
        
        btn_layout.addWidget(btn_on)
        btn_layout.addWidget(btn_off)
        btn_layout.addWidget(btn_reset)
        btn_layout.addWidget(btn_refresh)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Initial data load
        self.update_data()
    
    def apply_settings(self, channel):
        try:
            vset = float(self.vset_inputs[channel].text())
            iset = float(self.iset_inputs[channel].text())
            
            # Set voltage
            requests.post(f"{self.api_url}/set_voltage", 
                         json={"channel": channel, "voltage": vset}, timeout=1)
            # Set current
            requests.post(f"{self.api_url}/set_current", 
                         json={"channel": channel, "current": iset}, timeout=1)
            
            self.status_bar.showMessage(f"CH{channel}: VSet={vset}V, ISet={iset}A", 2000)
        except Exception as e:
            self.status_bar.showMessage(f"Error applying CH{channel}: {e}", 2000)
    
    def turn_on(self):
        try:
            requests.post(f"{self.api_url}/on", timeout=1)
            self.status_bar.showMessage("All channels turned ON", 2000)
            self.update_data()
        except Exception as e:
            self.status_bar.showMessage(f"Error: {e}", 2000)
    
    def turn_off(self):
        try:
            requests.post(f"{self.api_url}/off", timeout=1)
            self.status_bar.showMessage("All channels turned OFF", 2000)
            self.update_data()
        except Exception as e:
            self.status_bar.showMessage(f"Error: {e}", 2000)
    
    def reset_device(self):
        try:
            requests.post(f"{self.api_url}/reset", timeout=1)
            self.status_bar.showMessage("Device reset", 2000)
            self.update_data()
        except Exception as e:
            self.status_bar.showMessage(f"Error: {e}", 2000)
    
    def update_data(self):
        try:
            response = requests.get(f"{self.api_url}/status", timeout=2)
            if response.status_code == 200:
                data = response.json()
                
                # Update connection status
                self.conn_label.setText(f"● Device: {data['device']} - Status: {data['status']}")
                self.temp_label.setText(f"Temperature: {data['temperature']} °C")
                
                # Update each channel
                for ch in data['channels']:
                    row = ch['channel']
                    self.table.item(row, 1).setText(f"{ch['vmon']:.2f}")
                    self.table.item(row, 2).setText(f"{ch['imon']:.4f}")
                    
                    # Update input fields with current setpoints
                    self.vset_inputs[row].setText(f"{ch['vset']:.1f}")
                    self.iset_inputs[row].setText(f"{ch['iset']:.4f}")
                
                self.status_bar.showMessage(f"Updated at {time.strftime('%H:%M:%S')}", 1000)
            else:
                self.conn_label.setText("● Error: Unable to get status")
        except Exception as e:
            self.conn_label.setText(f"● Connection Error: {e}")
            self.status_bar.showMessage("Cannot connect to device simulator", 2000)

def main():
    app = QApplication(sys.argv)
    window = HVControlGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import time
    main()
