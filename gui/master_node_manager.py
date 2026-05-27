#!/usr/bin/env python3
"""
SPD DCS Master Node Manager
Merges GUI components from all detector nodes into a unified interface
"""

import os
import sys
import json
import importlib
import subprocess
from pathlib import Path
from typing import Dict, List, Any

# Qt imports
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                 QHBoxLayout, QTabWidget, QTreeWidget, QTreeWidgetItem,
                                 QPushButton, QLabel, QFrame, QSplitter, QMessageBox,
                                 QStatusBar, QToolBar, QAction, QMenuBar)
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
    from PyQt5.QtGui import QIcon, QFont
    QT_AVAILABLE = True
except ImportError:
    QT_AVAILABLE = False
    print("Warning: PyQt5 not available, running in CLI mode")

class NodeManager:
    """Manages all detector nodes and their GUIs"""
    
    # Define all nodes with their properties
    NODES = {
        'SPD': {
            'name': 'SPD',
            'full_name': 'Silicon Pixel Detector',
            'color': '#3498db',
            'icon': '🎯',
            'order': 1,
            'enabled': True
        },
        'MicroMegas': {
            'name': 'MicroMegas',
            'full_name': 'Micromegas Detector',
            'color': '#2ecc71',
            'icon': '📡',
            'order': 2,
            'enabled': True
        },
        'StrawTracker': {
            'name': 'StrawTracker',
            'full_name': 'Straw Tube Tracker',
            'color': '#e74c3c',
            'icon': '🥤',
            'order': 3,
            'enabled': True
        },
        'Magnet': {
            'name': 'Magnet',
            'full_name': 'Magnet Control',
            'color': '#9b59b6',
            'icon': '🧲',
            'order': 4,
            'enabled': True
        },
        'RangeSystem': {
            'name': 'RangeSystem',
            'full_name': 'Range System',
            'color': '#f39c12',
            'icon': '📏',
            'order': 5,
            'enabled': True
        },
        'StrawTrackerEndCap': {
            'name': 'StrawTrackerEndCap',
            'full_name': 'Straw Tracker End Cap',
            'color': '#1abc9c',
            'icon': '🔚',
            'order': 6,
            'enabled': True
        },
        'BBC': {
            'name': 'BBC',
            'full_name': 'Beam Beam Counter',
            'color': '#e67e22',
            'icon': '🔴',
            'order': 7,
            'enabled': True
        },
        'RangeSystemEndCap': {
            'name': 'RangeSystemEndCap',
            'full_name': 'Range System End Cap',
            'color': '#16a085',
            'icon': '🎯',
            'order': 8,
            'enabled': True
        },
        'BBC_MCP': {
            'name': 'BBC_MCP',
            'full_name': 'BBC MCP Detector',
            'color': '#27ae60',
            'icon': '🔵',
            'order': 9,
            'enabled': True
        },
        'ZeroDegreeCalorimeter': {
            'name': 'ZeroDegreeCalorimeter',
            'full_name': 'Zero Degree Calorimeter',
            'color': '#c0392b',
            'icon': '🌡️',
            'order': 10,
            'enabled': True
        }
    }
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or os.getcwd())
        self.nodes_path = self.base_path / 'nodes'
        self.node_modules = {}
        self.node_status = {}
        
    def discover_nodes(self) -> Dict:
        """Discover and load all available nodes"""
        print(f"Scanning for nodes in: {self.nodes_path}")
        
        for node_name in self.NODES:
            node_dir = self.nodes_path / node_name
            if node_dir.exists():
                print(f"  ✓ Found node: {node_name}")
                self.load_node_module(node_name, node_dir)
            else:
                print(f"  ✗ Missing node: {node_name}")
                self.node_modules[node_name] = None
                self.node_status[node_name] = 'missing'
        
        return self.node_modules
    
    def load_node_module(self, node_name: str, node_dir: Path):
        """Load GUI module from node directory"""
        try:
            # Look for GUI files in node directory
            gui_files = list(node_dir.glob("*gui*.py")) + list(node_dir.glob("*.py"))
            
            if gui_files:
                # Add node directory to Python path
                sys.path.insert(0, str(node_dir))
                
                # Try to import the GUI module
                module_name = f"nodes.{node_name}.gui"
                spec = importlib.util.spec_from_file_location(
                    module_name, 
                    gui_files[0]
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.node_modules[node_name] = module
                    self.node_status[node_name] = 'loaded'
                    print(f"    Loaded GUI from: {gui_files[0].name}")
                else:
                    self.node_modules[node_name] = None
                    self.node_status[node_name] = 'import_error'
            else:
                self.node_modules[node_name] = None
                self.node_status[node_name] = 'no_gui'
                
        except Exception as e:
            print(f"    Error loading {node_name}: {e}")
            self.node_modules[node_name] = None
            self.node_status[node_name] = 'error'
    
    def get_node_info(self) -> Dict:
        """Get aggregated information from all nodes"""
        node_info = {}
        
        for node_name, node_data in self.NODES.items():
            node_info[node_name] = {
                **node_data,
                'status': self.node_status.get(node_name, 'unknown'),
                'has_gui': self.node_modules.get(node_name) is not None,
                'directory': str(self.nodes_path / node_name)
            }
            
            # Try to read node configuration if exists
            config_file = self.nodes_path / node_name / 'node_config.json'
            if config_file.exists():
                try:
                    with open(config_file) as f:
                        config = json.load(f)
                        node_info[node_name]['config'] = config
                except:
                    pass
                    
        return node_info
    
    def merge_gui_tabs(self, parent_widget=None):
        """Merge all node GUIs into tab widget"""
        if not QT_AVAILABLE:
            print("PyQt5 not available, cannot create GUI")
            return None
            
        from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel
        
        tab_widget = QTabWidget()
        
        # Sort nodes by order
        sorted_nodes = sorted(self.NODES.items(), key=lambda x: x[1]['order'])
        
        for node_name, node_info in sorted_nodes:
            if self.node_status.get(node_name) == 'loaded':
                try:
                    # Try to get widget from node module
                    module = self.node_modules[node_name]
                    if hasattr(module, 'get_widget'):
                        widget = module.get_widget()
                    elif hasattr(module, 'create_widget'):
                        widget = module.create_widget()
                    else:
                        # Create placeholder widget
                        widget = QWidget()
                        layout = QVBoxLayout()
                        layout.addWidget(QLabel(f"GUI for {node_info['full_name']}"))
                        layout.addWidget(QLabel(f"Directory: {node_info['directory']}"))
                        widget.setLayout(layout)
                    
                    tab_widget.addTab(widget, f"{node_info['icon']} {node_name}")
                    
                except Exception as e:
                    print(f"Error creating tab for {node_name}: {e}")
                    error_widget = QWidget()
                    layout = QVBoxLayout()
                    layout.addWidget(QLabel(f"Error loading {node_name} GUI"))
                    layout.addWidget(QLabel(str(e)))
                    error_widget.setLayout(layout)
                    tab_widget.addTab(error_widget, f"⚠ {node_name}")
            else:
                # Create disabled/placeholder tab
                placeholder = QWidget()
                layout = QVBoxLayout()
                layout.addWidget(QLabel(f"{node_info['icon']} {node_info['full_name']}"))
                layout.addWidget(QLabel(f"Status: {self.node_status.get(node_name, 'unknown')}"))
                layout.addWidget(QLabel(f"Directory: {node_info['directory']}"))
                placeholder.setLayout(layout)
                tab_widget.addTab(placeholder, f"⭕ {node_name}")
        
        return tab_widget
    
    def start_device_servers(self):
        """Start device servers for all nodes"""
        processes = []
        for node_name in self.NODES:
            node_dir = self.nodes_path / node_name
            server_script = node_dir / 'device_server.py'
            if server_script.exists():
                print(f"Starting device server for {node_name}...")
                proc = subprocess.Popen(
                    [sys.executable, str(server_script)],
                    cwd=str(node_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                processes.append((node_name, proc))
        return processes

class MasterGUI(QMainWindow if QT_AVAILABLE else object):
    """Main GUI window merging all node interfaces"""
    
    def __init__(self, node_manager: NodeManager):
        super().__init__() if QT_AVAILABLE else None
        self.node_manager = node_manager
        self.init_ui()
        
    def init_ui(self):
        """Initialize the unified GUI"""
        if not QT_AVAILABLE:
            return
            
        self.setWindowTitle("SPD DCS Master Control System")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create splitter for navigation and content
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel: Node tree
        left_panel = self.create_node_tree()
        splitter.addWidget(left_panel)
        
        # Right panel: Tab widget with node GUIs
        self.tab_widget = self.node_manager.merge_gui_tabs()
        splitter.addWidget(self.tab_widget)
        
        # Set splitter proportions
        splitter.setSizes([300, 1100])
        
        main_layout.addWidget(splitter)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready")
        
        # Create refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_status)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_all)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        for node_name in self.node_manager.NODES:
            action = QAction(node_name, self)
            action.triggered.connect(lambda checked, n=node_name: self.show_node_tab(n))
            view_menu.addAction(action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        start_all_action = QAction("Start All Device Servers", self)
        start_all_action.triggered.connect(self.start_all_servers)
        tools_menu.addAction(start_all_action)
        
        stop_all_action = QAction("Stop All Device Servers", self)
        stop_all_action.triggered.connect(self.stop_all_servers)
        tools_menu.addAction(stop_all_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Create toolbar with quick actions"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Add refresh button
        refresh_btn = QAction("Refresh", self)
        refresh_btn.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_btn)
        
        toolbar.addSeparator()
        
        # Add node quick buttons
        for node_name, node_info in self.node_manager.NODES.items():
            if node_info.get('enabled', True):
                action = QAction(f"{node_info['icon']} {node_name}", self)
                action.triggered.connect(lambda checked, n=node_name: self.show_node_tab(n))
                toolbar.addAction(action)
                
    def create_node_tree(self):
        """Create tree widget showing all nodes"""
        from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
        
        tree = QTreeWidget()
        tree.setHeaderLabel("Detector Nodes")
        tree.setMaximumWidth(300)
        
        # Add nodes to tree
        for node_name, node_info in sorted(self.node_manager.NODES.items(), 
                                           key=lambda x: x[1]['order']):
            item = QTreeWidgetItem(tree)
            status_icon = "✅" if self.node_manager.node_status.get(node_name) == 'loaded' else "❌"
            item.setText(0, f"{status_icon} {node_info['icon']} {node_name}")
            item.setText(1, node_info['full_name'])
            
            # Add sub-items for node components
            node_dir = self.node_manager.nodes_path / node_name
            if node_dir.exists():
                sub_item = QTreeWidgetItem(item)
                sub_item.setText(0, "  📁 Directory")
                sub_item.setText(1, str(node_dir))
                
                # Check for config files
                config_file = node_dir / 'node_config.json'
                if config_file.exists():
                    config_item = QTreeWidgetItem(item)
                    config_item.setText(0, "  ⚙️ Configuration")
                    config_item.setText(1, "Loaded")
        
        # Connect item selection
        tree.itemClicked.connect(self.on_tree_item_clicked)
        
        # Expand all items
        tree.expandAll()
        
        return tree
    
    def on_tree_item_clicked(self, item, column):
        """Handle tree item click"""
        text = item.text(0)
        for node_name in self.node_manager.NODES:
            if node_name in text:
                self.show_node_tab(node_name)
                break
    
    def show_node_tab(self, node_name: str):
        """Show the tab for a specific node"""
        for i in range(self.tab_widget.count()):
            if node_name in self.tab_widget.tabText(i):
                self.tab_widget.setCurrentIndex(i)
                self.update_status(f"Showing {node_name}")
                break
    
    def refresh_all(self):
        """Refresh all node information"""
        self.update_status("Refreshing...")
        self.node_manager.discover_nodes()
        self.update_status("Refreshed")
    
    def refresh_status(self):
        """Periodic status update"""
        info = self.node_manager.get_node_info()
        loaded_count = sum(1 for n in info.values() if n['has_gui'])
        self.update_status(f"Nodes: {loaded_count}/{len(info)} loaded")
    
    def update_status(self, message: str):
        """Update status bar message"""
        if hasattr(self, 'status_bar'):
            self.status_bar.showMessage(message)
    
    def start_all_servers(self):
        """Start device servers for all nodes"""
        self.update_status("Starting device servers...")
        self.node_manager.start_device_servers()
        self.update_status("Device servers started")
    
    def stop_all_servers(self):
        """Stop all device servers"""
        self.update_status("Stopping device servers...")
        # Implementation would go here
        self.update_status("Device servers stopped")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About SPD DCS Master Control",
            "SPD DCS Master Control System\n\n"
            "Unified interface for all detector nodes:\n"
            "• SPD (Silicon Pixel Detector)\n"
            "• MicroMegas\n"
            "• StrawTracker\n"
            "• Magnet\n"
            "• RangeSystem\n"
            "• StrawTrackerEndCap\n"
            "• BBC\n"
            "• RangeSystemEndCap\n"
            "• BBC_MCP\n"
            "• ZeroDegreeCalorimeter\n\n"
            "Version 1.0"
        )

def main():
    """Main entry point"""
    base_path = os.getcwd()
    
    print("=" * 60)
    print("SPD DCS Master Node Manager")
    print("=" * 60)
    
    # Initialize node manager
    manager = NodeManager(base_path)
    manager.discover_nodes()
    
    # Print node information
    print("\nNode Status:")
    info = manager.get_node_info()
    for node_name, node_data in info.items():
        status = node_data['status']
        status_icon = "✓" if status == 'loaded' else "✗"
        print(f"  {status_icon} {node_name}: {status}")
    
    if QT_AVAILABLE:
        # Start GUI
        app = QApplication(sys.argv)
        window = MasterGUI(manager)
        window.show()
        sys.exit(app.exec_())
    else:
        # CLI mode
        print("\nRunning in CLI mode. Install PyQt5 for GUI mode.")
        print("Node directories structure:")
        for node_name in manager.NODES:
            node_dir = manager.nodes_path / node_name
            print(f"  {node_name}: {node_dir}")

if __name__ == "__main__":
    main()
