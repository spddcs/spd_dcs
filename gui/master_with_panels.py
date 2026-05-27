#!/usr/bin/env python3
"""
SPD DCS Master Controller with Right-Side Panels for each node
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QStackedWidget, QLabel, QFrame, QSplitter,
    QPushButton, QStatusBar, QToolBar, QAction
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

# Import all node GUIs dynamically
def import_node_gui(node_name):
    """Import GUI module for a node"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            f"{node_name}_gui",
            f"{node_name}/node_gui.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.get_widget()
    except Exception as e:
        print(f"Error loading {node_name}: {e}")
        return None

class MasterController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.nodes = [
            "SPD", "MicroMegas", "StrawTracker", "Magnet", "RangeSystem",
            "StrawTrackerEndCap", "BBC", "RangeSystemEndCap", "BBC_MCP", 
            "ZeroDegreeCalorimeter"
        ]
        self.node_widgets = {}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("SPD DCS Master Control - All Nodes")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left panel: Node list
        left_panel = self.create_node_list()
        main_layout.addWidget(left_panel)
        
        # Right panel: Stacked widgets for each node
        self.right_panel = QStackedWidget()
        self.load_node_panels()
        main_layout.addWidget(self.right_panel)
        
        # Set proportions (20% left, 80% right)
        main_layout.setStretchFactor(left_panel, 1)
        main_layout.setStretchFactor(self.right_panel, 4)
        
        # Create menu and toolbar
        self.create_menu()
        self.create_toolbar()
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def create_node_list(self):
        """Create list of nodes on the left side"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Box | QFrame.Raised)
        panel.setMaximumWidth(300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Detector Nodes")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Node list
        self.node_list = QListWidget()
        for node in self.nodes:
            self.node_list.addItem(node)
        
        self.node_list.itemClicked.connect(self.on_node_selected)
        layout.addWidget(self.node_list)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh All")
        refresh_btn.clicked.connect(self.refresh_all)
        layout.addWidget(refresh_btn)
        
        panel.setLayout(layout)
        return panel
    
    def load_node_panels(self):
        """Load GUI panels for all nodes"""
        for node in self.nodes:
            print(f"Loading {node}...")
            widget = import_node_gui(node)
            if widget:
                self.node_widgets[node] = widget
                self.right_panel.addWidget(widget)
                # Set the tab text to node name
                index = self.right_panel.indexOf(widget)
                # Store node name for this index
                if not hasattr(self, 'node_index_map'):
                    self.node_index_map = {}
                self.node_index_map[index] = node
                print(f"  ✓ {node} loaded")
            else:
                # Create placeholder
                placeholder = QLabel(f"{node}\nGUI not available")
                placeholder.setAlignment(Qt.AlignCenter)
                self.right_panel.addWidget(placeholder)
                print(f"  ✗ {node} failed to load")
    
    def on_node_selected(self, item):
        """Handle node selection from list"""
        node_name = item.text()
        if node_name in self.node_widgets:
            index = self.right_panel.indexOf(self.node_widgets[node_name])
            self.right_panel.setCurrentIndex(index)
            self.statusBar().showMessage(f"Selected: {node_name}")
    
    def refresh_all(self):
        """Refresh all node panels"""
        self.statusBar().showMessage("Refreshing all nodes...")
        for node, widget in self.node_widgets.items():
            if hasattr(widget, 'update_status'):
                widget.update_status()
        self.statusBar().showMessage("Refresh complete", 2000)
    
    def create_menu(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        for node in self.nodes:
            action = QAction(node, self)
            action.triggered.connect(lambda checked, n=node: self.select_node(n))
            view_menu.addAction(action)
    
    def create_toolbar(self):
        """Create toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Add node buttons
        for node in self.nodes[:5]:  # First 5 nodes
            btn = QPushButton(node[:3])
            btn.clicked.connect(lambda checked, n=node: self.select_node(n))
            toolbar.addWidget(btn)
        
        toolbar.addSeparator()
        
        # Refresh button
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_action)
    
    def select_node(self, node_name):
        """Select and show a specific node"""
        for i in range(self.node_list.count()):
            if self.node_list.item(i).text() == node_name:
                self.node_list.setCurrentRow(i)
                self.on_node_selected(self.node_list.item(i))
                break

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MasterController()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
