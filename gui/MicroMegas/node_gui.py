#!/usr/bin/env python3
"""
GUI for MicroMegas detector
Part of SPD DCS system
"""

import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QGridLayout, QTextEdit, QLineEdit, QComboBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QFrame, QProgressBar, QCheckBox, QSpinBox,
    QDoubleSpinBox, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon

class MicroMegasGUI(QWidget):
    """GUI widget for MicroMegas detector"""
    
    # Signals
    data_updated = pyqtSignal(dict)
    alarm_triggered = pyqtSignal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.node_name = "MicroMegas"
        self.full_name = "Micromegas Detector"
        self.color = "#2ecc71"
        self.icon = "📡"
        
        # Data storage
        self.parameters = {}
        self.status_data = {}
        self.alarms = []
        
        # Initialize UI
        self.init_ui()
        
        # Setup timers
        self.setup_timers()
        
        # Load configuration
        self.load_config()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header with node information
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create tab widget for different sections
        self.tab_widget = QTabWidget()
        
        # Add different tabs
        self.tab_widget.addTab(self.create_status_tab(), "Status")
        self.tab_widget.addTab(self.create_control_tab(), "Controls")
        self.tab_widget.addTab(self.create_monitoring_tab(), "Monitoring")
        self.tab_widget.addTab(self.create_config_tab(), "Configuration")
        self.tab_widget.addTab(self.create_logs_tab(), "Logs")
        
        main_layout.addWidget(self.tab_widget)
        
        # Footer with status bar
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
        
        # Set stylesheet
        self.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {self.color};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            QPushButton {{
                background-color: {self.color};
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
            QProgressBar {{
                border: 1px solid grey;
                border-radius: 3px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {self.color};
                width: 10px;
            }}
        """)
        
    def create_header(self):
        """Create header section"""
        header = QFrame()
        header.setFrameStyle(QFrame.Box | QFrame.Raised)
        layout = QHBoxLayout()
        
        # Node title
        title = QLabel(f"{self.icon} {self.full_name} ({self.node_name})")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Status indicator
        self.status_indicator = QLabel("● CONNECTED")
        self.status_indicator.setStyleSheet(f"color: {self.color}; font-weight: bold;")
        layout.addWidget(self.status_indicator)
        
        # Time display
        self.time_label = QLabel()
        layout.addWidget(self.time_label)
        
        header.setLayout(layout)
        return header
    
    def create_status_tab(self):
        """Create status monitoring tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Status grid
        status_group = QGroupBox("Current Status")
        status_layout = QGridLayout()
        
        # Create status fields
        self.status_fields = {}
        status_items = [
            ("Status:", "status_value", "Unknown"),
            ("Temperature:", "temp_value", "-- °C"),
            ("Voltage:", "voltage_value", "-- V"),
            ("Current:", "current_value", "-- A"),
            ("Pressure:", "pressure_value", "-- mbar"),
            ("Humidity:", "humidity_value", "-- %"),
            ("HV Status:", "hv_status", "Off"),
            ("LV Status:", "lv_status", "Off"),
            ("Interlock:", "interlock_status", "OK"),
            ("Run Mode:", "run_mode", "Idle")
        ]
        
        row = 0
        col = 0
        for label, key, default in status_items:
            status_layout.addWidget(QLabel(label), row, col*2)
            self.status_fields[key] = QLabel(default)
            self.status_fields[key].setStyleSheet("font-weight: bold;")
            status_layout.addWidget(self.status_fields[key], row, col*2+1)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Parameters group
        params_group = QGroupBox("Parameters")
        params_layout = QGridLayout()
        
        self.param_fields = {}
        parameters = [
            ("Set Voltage:", "set_voltage", "0.0", "V"),
            ("Set Current:", "set_current", "0.0", "A"),
            ("Ramp Rate:", "ramp_rate", "10.0", "V/s"),
            ("Trip Limit:", "trip_limit", "100.0", "µA")
        ]
        
        for i, (label, key, default, unit) in enumerate(parameters):
            params_layout.addWidget(QLabel(label), i, 0)
            self.param_fields[key] = QLabel(f"{default} {unit}")
            self.param_fields[key].setStyleSheet("color: blue; font-weight: bold;")
            params_layout.addWidget(self.param_fields[key], i, 1)
            
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Progress bars
        progress_group = QGroupBox("Performance")
        progress_layout = QVBoxLayout()
        
        self.progress_bars = {}
        for name in ["Efficiency", "Occupancy", "Data Rate"]:
            pb = QProgressBar()
            pb.setRange(0, 100)
            pb.setValue(0)
            progress_layout.addWidget(QLabel(name))
            progress_layout.addWidget(pb)
            self.progress_bars[name] = pb
            
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_control_tab(self):
        """Create control panel tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Power control group
        power_group = QGroupBox("Power Control")
        power_layout = QGridLayout()
        
        self.hv_checkbox = QCheckBox("HV Enable")
        self.lv_checkbox = QCheckBox("LV Enable")
        power_layout.addWidget(self.hv_checkbox, 0, 0)
        power_layout.addWidget(self.lv_checkbox, 0, 1)
        
        # Buttons
        self.start_btn = QPushButton("▶ Start")
        self.stop_btn = QPushButton("■ Stop")
        self.reset_btn = QPushButton("⟳ Reset")
        self.start_btn.clicked.connect(self.start_detector)
        self.stop_btn.clicked.connect(self.stop_detector)
        self.reset_btn.clicked.connect(self.reset_detector)
        
        power_layout.addWidget(self.start_btn, 1, 0)
        power_layout.addWidget(self.stop_btn, 1, 1)
        power_layout.addWidget(self.reset_btn, 1, 2)
        
        power_group.setLayout(power_layout)
        layout.addWidget(power_group)
        
        # Settings group
        settings_group = QGroupBox("Settings")
        settings_layout = QGridLayout()
        
        # Threshold settings
        settings_layout.addWidget(QLabel("Threshold:"), 0, 0)
        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(0, 1000)
        self.threshold_spin.setSuffix(" mV")
        settings_layout.addWidget(self.threshold_spin, 0, 1)
        
        # Gain settings
        settings_layout.addWidget(QLabel("Gain:"), 1, 0)
        self.gain_combo = QComboBox()
        self.gain_combo.addItems(["Low", "Medium", "High"])
        settings_layout.addWidget(self.gain_combo, 1, 1)
        
        # Update rate
        settings_layout.addWidget(QLabel("Update Rate:"), 2, 0)
        self.update_rate = QDoubleSpinBox()
        self.update_rate.setRange(0.1, 10.0)
        self.update_rate.setSingleStep(0.1)
        self.update_rate.setSuffix(" Hz")
        self.update_rate.setValue(1.0)
        settings_layout.addWidget(self.update_rate, 2, 1)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Apply button
        apply_btn = QPushButton("Apply Settings")
        apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_monitoring_tab(self):
        """Create monitoring tab with plots"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Create table for real-time data
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(["Parameter", "Value", "Unit"])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(QLabel("Real-time Data:"))
        layout.addWidget(self.data_table)
        
        # Add sample data
        sample_data = [
            ("Channel 1", "0.0", "V"),
            ("Channel 2", "0.0", "V"),
            ("Temperature Sensor 1", "0.0", "°C"),
            ("Temperature Sensor 2", "0.0", "°C")
        ]
        
        self.data_table.setRowCount(len(sample_data))
        for i, (param, value, unit) in enumerate(sample_data):
            self.data_table.setItem(i, 0, QTableWidgetItem(param))
            self.data_table.setItem(i, 1, QTableWidgetItem(value))
            self.data_table.setItem(i, 2, QTableWidgetItem(unit))
        
        # Export button
        export_btn = QPushButton("Export Data")
        export_btn.clicked.connect(self.export_data)
        layout.addWidget(export_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_config_tab(self):
        """Create configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Configuration editor
        layout.addWidget(QLabel("Node Configuration:"))
        self.config_text = QTextEdit()
        self.config_text.setPlainText(self.get_config_text())
        layout.addWidget(self.config_text)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save Configuration")
        reload_btn = QPushButton("Reload")
        save_btn.clicked.connect(self.save_config)
        reload_btn.clicked.connect(self.load_config)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(reload_btn)
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_logs_tab(self):
        """Create logs tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        # Clear button
        clear_btn = QPushButton("Clear Logs")
        clear_btn.clicked.connect(self.clear_logs)
        layout.addWidget(clear_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_footer(self):
        """Create footer section"""
        footer = QFrame()
        footer.setFrameStyle(QFrame.Box | QFrame.Sunken)
        layout = QHBoxLayout()
        
        self.message_label = QLabel("Ready")
        layout.addWidget(self.message_label)
        
        layout.addStretch()
        
        self.update_time_label = QLabel("Last update: --")
        layout.addWidget(self.update_time_label)
        
        footer.setLayout(layout)
        return footer
    
    def setup_timers(self):
        """Setup update timers"""
        # Timer for status updates
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(2000)  # Update every 2 seconds
        
        # Timer for clock
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        
    def update_status(self):
        """Update status information (simulated)"""
        # This would normally read from hardware/TANGO
        import random
        
        # Simulate changing values
        self.status_fields["temp_value"].setText(f"{random.uniform(20, 30):.1f} °C")
        self.status_fields["voltage_value"].setText(f"{random.uniform(4.8, 5.2):.1f} V")
        self.status_fields["current_value"].setText(f"{random.uniform(0, 2):.2f} A")
        
        # Update progress bars
        for name, pb in self.progress_bars.items():
            pb.setValue(random.randint(60, 100))
        
        # Update table data
        for row in range(self.data_table.rowCount()):
            if row < 2:  # Voltage channels
                value = f"{random.uniform(4.8, 5.2):.2f}"
            else:  # Temperature sensors
                value = f"{random.uniform(20, 30):.1f}"
            self.data_table.setItem(row, 1, QTableWidgetItem(value))
        
        # Update timestamp
        self.update_time_label.setText(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        
        # Emit data updated signal
        self.data_updated.emit(self.status_data)
        
    def update_clock(self):
        """Update clock display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)
    
    def start_detector(self):
        """Start the detector"""
        self.add_log("Starting detector...")
        self.status_fields["run_mode"].setText("Running")
        self.message_label.setText("Detector started")
        QMessageBox.information(self, "Start", f"{self.full_name} detector started")
        
    def stop_detector(self):
        """Stop the detector"""
        self.add_log("Stopping detector...")
        self.status_fields["run_mode"].setText("Stopped")
        self.message_label.setText("Detector stopped")
        
    def reset_detector(self):
        """Reset the detector"""
        self.add_log("Resetting detector...")
        self.message_label.setText("Detector reset")
        
    def apply_settings(self):
        """Apply new settings"""
        self.add_log(f"Applied settings: Threshold={self.threshold_spin.value()}mV, "
                    f"Gain={self.gain_combo.currentText()}, "
                    f"Rate={self.update_rate.value()}Hz")
        self.message_label.setText("Settings applied")
        
    def load_config(self):
        """Load configuration from file"""
        config_file = os.path.join(os.path.dirname(__file__), "node_config.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
                    self.config_text.setPlainText(json.dumps(self.config, indent=2))
                    self.add_log("Configuration loaded")
            except Exception as e:
                self.add_log(f"Error loading config: {e}")
                
    def save_config(self):
        """Save configuration to file"""
        try:
            config_data = json.loads(self.config_text.toPlainText())
            config_file = os.path.join(os.path.dirname(__file__), "node_config.json")
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            self.add_log("Configuration saved")
            QMessageBox.information(self, "Success", "Configuration saved successfully")
        except Exception as e:
            self.add_log(f"Error saving config: {e}")
            QMessageBox.warning(self, "Error", f"Failed to save configuration: {e}")
            
    def get_config_text(self):
        """Get configuration as text"""
        config_file = os.path.join(os.path.dirname(__file__), "node_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return f.read()
        else:
            return json.dumps({
                "name": self.node_name,
                "enabled": True,
                "parameters": {
                    "threshold": 100,
                    "gain": "Medium",
                    "update_rate": 1.0
                }
            }, indent=2)
    
    def export_data(self):
        """Export monitoring data to file"""
        filename, _ = QFileDialog.getSaveFileName(self, "Export Data", 
                                                   f"{self.node_name}_data.csv",
                                                   "CSV Files (*.csv)")
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Parameter,Value,Unit\n")
                    for row in range(self.data_table.rowCount()):
                        param = self.data_table.item(row, 0).text()
                        value = self.data_table.item(row, 1).text()
                        unit = self.data_table.item(row, 2).text()
                        f.write(f"{param},{value},{unit}\n")
                self.add_log(f"Data exported to {filename}")
                QMessageBox.information(self, "Success", "Data exported successfully")
            except Exception as e:
                self.add_log(f"Error exporting data: {e}")
                
    def add_log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.append(log_entry)
        
    def clear_logs(self):
        """Clear log display"""
        self.log_text.clear()
        self.add_log("Logs cleared")
        
    def closeEvent(self, event):
        """Handle close event"""
        self.add_log("GUI closing...")
        event.accept()

def get_widget():
    """Function to return widget for master GUI"""
    return MicroMegasGUI()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget = MicroMegasGUI()
    widget.setWindowTitle("Micromegas Detector Control Panel")
    widget.setGeometry(100, 100, 1200, 800)
    widget.show()
    sys.exit(app.exec_())

