#!/usr/bin/env python3
"""
SPD DCS Master GUI - Merges all node panels
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTreeWidget, QTreeWidgetItem, 
                             QStackedWidget, QLabel, QFrame)
from PyQt5.QtCore import Qt

class MasterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPD DCS Control System")
        self.setGeometry(100, 100, 1200, 800)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # Left panel - Navigation
        left_panel = QFrame()
        left_panel.setFixedWidth(250)
        left_panel.setStyleSheet("background-color: #2c3e50;")
        left_layout = QVBoxLayout(left_panel)
        
        title = QLabel("SPD DCS Navigation")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Detectors")
        self.tree.setStyleSheet("color: white; background-color: #34495e;")
        
        # Create navigation tree
        spd = QTreeWidgetItem(["SPD"])
        self.tree.addTopLevelItem(spd)
        
        devices = ["MicroMegas", "StrawTracker", "Magnet", "RangeSystem", 
                   "StrawTrackerEndCap", "BBC", "RangeSystemEndCap", 
                   "BBC_MCP", "ZeroDegreeCalorimeter"]
        for dev in devices:
            item = QTreeWidgetItem([dev])
            spd.addChild(item)
        
        self.tree.expandAll()
        left_layout.addWidget(self.tree)
        layout.addWidget(left_panel)
        
        # Right panel - Content
        self.content_stack = QStackedWidget()
        welcome = QLabel("Select a detector from the navigation tree")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        self.content_stack.addWidget(welcome)
        layout.addWidget(self.content_stack)
        
        self.tree.itemClicked.connect(self.on_item_clicked)
    
    def on_item_clicked(self, item, col):
        title = f"SPD DCS - {item.text(col)}"
        self.setWindowTitle(title)

def main():
    app = QApplication(sys.argv)
    window = MasterGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
