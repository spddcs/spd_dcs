#!/usr/bin/env python3
"""
SPD DCS Master GUI - Merges all node panels with exact navigation tree
Includes StrawTracker with S0-S5 sections, each with CaenCrate, HV (with Channels), and LV
"""

import sys
import os
import importlib.util
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QStackedWidget, QLabel, QStatusBar, 
    QPushButton, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

def create_font(family="Sans Serif", size=10, bold=False):
    font = QFont(family, size)
    font.setBold(bold)
    return font

def load_panel(panel_path, panel_name, device=None):
    """Dynamically load a panel from a specific path"""
    try:
        if not os.path.exists(panel_path):
            print(f"Panel not found: {panel_path}")
            return None
        
        # Add parent directory to path for base_panel import
        base_dir = os.path.dirname(os.path.dirname(panel_path))
        if base_dir not in sys.path:
            sys.path.insert(0, base_dir)
        
        # Load module
        spec = importlib.util.spec_from_file_location(panel_name, panel_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get panel instance
        if hasattr(module, 'get_panel'):
            return module.get_panel(device)
        elif hasattr(module, 'main'):
            # Create instance if class exists
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr.__name__.endswith('Panel'):
                    return attr(device)
            return None
        else:
            return None
            
    except Exception as e:
        print(f"Error loading {panel_path}: {e}")
        return None

class MasterMergeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.node_panels = {}
        self.current_panel = None
        self.init_ui()
        self.load_all_panels()
        
    def init_ui(self):
        self.setWindowTitle("SPD DCS - Complete Detector Control System")
        self.setGeometry(100, 100, 1400, 950)
        
        # Main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left panel - Navigation tree
        left_panel = self.create_navigation_panel()
        main_layout.addWidget(left_panel)
        
        # Right panel - Content area
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.Box)
        right_panel.setStyleSheet("QFrame { background-color: #f5f5f5; }")
        right_layout = QVBoxLayout(right_panel)
        
        # Title in right panel
        self.right_title = QLabel("SPD DCS Control System")
        self.right_title.setFont(create_font("Sans Serif", 14, True))
        self.right_title.setAlignment(Qt.AlignCenter)
        self.right_title.setStyleSheet("padding: 20px; background-color: #34495e; color: white;")
        right_layout.addWidget(self.right_title)
        
        # Stacked widget for panels
        self.content_stack = QStackedWidget()
        right_layout.addWidget(self.content_stack)
        
        main_layout.addWidget(right_panel)
        
        # Set proportions (25% left, 75% right)
        main_layout.setStretchFactor(left_panel, 1)
        main_layout.setStretchFactor(right_panel, 3)
        
        # Create status bar
        self.create_status_bar()
        
        # Add placeholder
        placeholder = QLabel("Select an item from the navigation tree\n\nAvailable panels:\n• SPD, BBC, Magnet, MicroMegas\n• StrawTracker (S0-S5 with HV/LV/CaenCrate)\n• Individual Channels 0-7 per section")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet("font-size: 14px; color: #7f8c8d; padding: 50px;")
        self.content_stack.addWidget(placeholder)
    
    def create_status_bar(self):
        """Create status bar with Exit button on the right side"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add permanent widget (right side) - Exit button
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.exit_btn.clicked.connect(self.close)
        self.status_bar.addPermanentWidget(self.exit_btn)
        
        # Add status message on the left
        self.status_bar.showMessage("Ready - Select a detector node")
    
    def create_navigation_panel(self):
        """Create navigation tree with StrawTracker S0-S5 structure"""
        panel = QFrame()
        panel.setFixedWidth(320)
        panel.setStyleSheet("QFrame { background-color: #2c3e50; }")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("SPD DCS Navigation")
        title.setFont(create_font("Sans Serif", 12, True))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; padding: 10px; background-color: #1a252f;")
        layout.addWidget(title)
        
        # Tree widget
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderLabel("Detectors")
        self.nav_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #34495e;
                color: white;
                border: none;
                font-size: 12px;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #3498db;
            }
            QTreeWidget::item:hover {
                background-color: #3d5a73;
            }
        """)
        
        # Build navigation tree structure
        spd_item = QTreeWidgetItem(["SPD"])
        self.nav_tree.addTopLevelItem(spd_item)
        spd_item.setData(0, Qt.UserRole, "SPD")
        
        # MicroMegas under SPD
        micromegas_item = QTreeWidgetItem(["MicroMegas"])
        spd_item.addChild(micromegas_item)
        micromegas_item.setData(0, Qt.UserRole, "MicroMegas")
        
        # StrawTracker under SPD with S0-S5 sections
        straw_tracker_item = QTreeWidgetItem(["StrawTracker"])
        spd_item.addChild(straw_tracker_item)
        straw_tracker_item.setData(0, Qt.UserRole, "StrawTracker")
        
        # Create S0 through S5 sections under StrawTracker
        for section_num in range(6):  # S0 to S5
            section_name = f"S{section_num}"
            section_item = QTreeWidgetItem([section_name])
            straw_tracker_item.addChild(section_item)
            section_item.setData(0, Qt.UserRole, f"StrawTracker_{section_name}")
            
            # CaenCrate under section
            caen_crate_item = QTreeWidgetItem(["CaenCrate"])
            section_item.addChild(caen_crate_item)
            caen_crate_item.setData(0, Qt.UserRole, f"CaenCrate_{section_name}")
            
            # Boards under CaenCrate
            boards_item = QTreeWidgetItem(["Boards"])
            caen_crate_item.addChild(boards_item)
            boards_item.setData(0, Qt.UserRole, f"Boards_{section_name}")
            
            # HV under section
            hv_item = QTreeWidgetItem(["HV"])
            section_item.addChild(hv_item)
            hv_item.setData(0, Qt.UserRole, f"HV_{section_name}")
            
            # Channels under HV
            channels_item = QTreeWidgetItem(["Channels"])
            hv_item.addChild(channels_item)
            channels_item.setData(0, Qt.UserRole, f"Channels_{section_name}")
            
            # Channel 0-7 under Channels
            for ch in range(8):
                channel_item = QTreeWidgetItem([f"Channel {ch}"])
                channels_item.addChild(channel_item)
                channel_item.setData(0, Qt.UserRole, f"Channel_{section_name}_{ch}")
            
            # LV under section
            lv_item = QTreeWidgetItem(["LV"])
            section_item.addChild(lv_item)
            lv_item.setData(0, Qt.UserRole, f"LV_{section_name}")
        
        # Other nodes under SPD
        magnet_item = QTreeWidgetItem(["Magnet"])
        spd_item.addChild(magnet_item)
        magnet_item.setData(0, Qt.UserRole, "Magnet")
        
        range_system_item = QTreeWidgetItem(["RangeSystem"])
        spd_item.addChild(range_system_item)
        range_system_item.setData(0, Qt.UserRole, "RangeSystem")
        
        straw_tracker_ec_item = QTreeWidgetItem(["StrawTrackerEndCap"])
        spd_item.addChild(straw_tracker_ec_item)
        straw_tracker_ec_item.setData(0, Qt.UserRole, "StrawTrackerEndCap")
        
        bbc_item = QTreeWidgetItem(["BBC"])
        spd_item.addChild(bbc_item)
        bbc_item.setData(0, Qt.UserRole, "BBC")
        
        range_system_ec_item = QTreeWidgetItem(["RangeSystemEndCap"])
        spd_item.addChild(range_system_ec_item)
        range_system_ec_item.setData(0, Qt.UserRole, "RangeSystemEndCap")
        
        bbc_mcp_item = QTreeWidgetItem(["BBC_MCP"])
        spd_item.addChild(bbc_mcp_item)
        bbc_mcp_item.setData(0, Qt.UserRole, "BBC_MCP")
        
        zero_degree_item = QTreeWidgetItem(["ZeroDegreeCalorimeter"])
        spd_item.addChild(zero_degree_item)
        zero_degree_item.setData(0, Qt.UserRole, "ZeroDegreeCalorimeter")
        
        # Expand to show structure
        self.nav_tree.expandItem(spd_item)
        self.nav_tree.expandItem(straw_tracker_item)
        for section_num in range(6):
            section_name = f"S{section_num}"
            for i in range(self.nav_tree.topLevelItemCount()):
                item = self.nav_tree.topLevelItem(i)
                if item.text(0) == "SPD":
                    for j in range(item.childCount()):
                        if item.child(j).text(0) == "StrawTracker":
                            for k in range(item.child(j).childCount()):
                                if item.child(j).child(k).text(0) == section_name:
                                    self.nav_tree.expandItem(item.child(j).child(k))
                                    for l in range(item.child(j).child(k).childCount()):
                                        child = item.child(j).child(k).child(l)
                                        if child.text(0) in ["HV", "CaenCrate"]:
                                            self.nav_tree.expandItem(child)
        
        # Connect click event
        self.nav_tree.itemClicked.connect(self.on_navigation_clicked)
        
        layout.addWidget(self.nav_tree)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh All")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px;
                margin-top: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_all)
        layout.addWidget(refresh_btn)
        
        # Info label
        info_label = QLabel("Click on any item\nto view its control panel")
        info_label.setStyleSheet("color: white; padding: 10px; font-size: 10px;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        return panel
    
    def load_all_panels(self):
        """Load panels for all nodes"""
        base_path = "/opt/spddcs/SPD_DCS"
        
        # Map tree items to panel paths
        self.panel_map = {
            "SPD": f"{base_path}/gui/SPD_panel.py",
            "MicroMegas": f"{base_path}/MicroMegas/gui/MicroMegas_panel.py",
            "StrawTracker": f"{base_path}/StrawTracker/gui/StrawTracker_panel.py",
            "Magnet": f"{base_path}/Magnet/gui/Magnet_panel.py",
            "RangeSystem": f"{base_path}/RangeSystem/gui/RangeSystem_panel.py",
            "StrawTrackerEndCap": f"{base_path}/StrawTrackerEndCap/gui/StrawTrackerEndCap_panel.py",
            "BBC": f"{base_path}/BBC/gui/BBC_panel.py",
            "RangeSystemEndCap": f"{base_path}/RangeSystemEndCap/gui/RangeSystemEndCap_panel.py",
            "BBC_MCP": f"{base_path}/BBC_MCP/gui/BBC_MCP_panel.py",
            "ZeroDegreeCalorimeter": f"{base_path}/ZeroDegreeCalorimeter/gui/ZeroDegreeCalorimeter_panel.py",
        }
        
        # Add CAEN panels for each section (S0-S5)
        for section_num in range(6):
            section_name = f"S{section_num}"
            self.panel_map[f"CaenCrate_{section_name}"] = f"{base_path}/StrawTracker/gui/CaenCrate_panel.py"
            self.panel_map[f"Boards_{section_name}"] = f"{base_path}/StrawTracker/gui/Boards_panel.py"
            self.panel_map[f"Channels_{section_name}"] = f"{base_path}/StrawTracker/gui/Channels_panel.py"
            self.panel_map[f"LV_{section_name}"] = f"{base_path}/StrawTracker/gui/LV_panel.py"
            
            # Add individual channel panels for each section
            for ch in range(8):
                self.panel_map[f"Channel_{section_name}_{ch}"] = f"{base_path}/StrawTracker/gui/Channel{ch}_panel.py"
        
        # Load each panel
        print("\n" + "="*60)
        print("Loading Panels")
        print("="*60)
        
        for panel_name, panel_path in self.panel_map.items():
            print(f"Loading {panel_name}...")
            panel = load_panel(panel_path, panel_name)
            if panel:
                self.node_panels[panel_name] = panel
                self.content_stack.addWidget(panel)
                print(f"  ✓ Loaded {panel_name}")
            else:
                # Create placeholder for missing panels
                placeholder = QLabel(f"{panel_name}\nPanel not available\n\nCheck that {os.path.basename(panel_path)} exists")
                placeholder.setAlignment(Qt.AlignCenter)
                placeholder.setStyleSheet("color: #e74c3c; padding: 50px;")
                self.node_panels[panel_name] = placeholder
                self.content_stack.addWidget(placeholder)
                print(f"  ✗ Failed to load {panel_name}")
        
        print(f"\nLoaded {len(self.node_panels)} panels")
    
    def on_navigation_clicked(self, item, column):
        """Handle navigation clicks and show appropriate panel"""
        item_text = item.text(column)
        user_data = item.data(0, Qt.UserRole)
        
        if not user_data:
            user_data = item_text
        
        # Update right panel title
        self.right_title.setText(f"SPD DCS - {item_text}")
        
        # Find panel to display
        if user_data in self.node_panels:
            panel = self.node_panels[user_data]
            index = self.content_stack.indexOf(panel)
            if index >= 0:
                self.content_stack.setCurrentIndex(index)
                self.status_bar.showMessage(f"Showing: {item_text}")
                
                # Trigger update if panel has update method
                if hasattr(panel, 'update_values'):
                    panel.update_values()
        else:
            self.status_bar.showMessage(f"No panel available for: {item_text}")
    
    def refresh_all(self):
        """Refresh all node panels"""
        self.status_bar.showMessage("Refreshing all nodes...")
        for panel_name, panel in self.node_panels.items():
            if hasattr(panel, 'update_values'):
                try:
                    panel.update_values()
                except Exception as e:
                    print(f"Error refreshing {panel_name}: {e}")
        self.status_bar.showMessage("Refresh complete", 2000)

def main():
    app = QApplication(sys.argv)
    
    # Fix Qt platform
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    os.environ['XDG_SESSION_TYPE'] = 'x11'
    
    window = MasterMergeGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
