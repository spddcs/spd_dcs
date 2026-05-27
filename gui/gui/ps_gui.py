#!/usr/bin/env python
import sys
import tango
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QGroupBox, 
                             QPushButton, QLineEdit, QFrame,
                             QTreeWidget, QTreeWidgetItem, QStackedWidget,
                             QScrollArea, QSizePolicy, QCheckBox)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

def create_font(family="Sans Serif", size=8, bold=False, italic=False):
    font = QFont(family, size)
    font.setBold(bold)
    font.setItalic(italic)
    font.setKerning(True)
    return font

SANS_FONT = create_font("Sans Serif", 8, bold=False)
VALUE_FONT = create_font("Sans Serif", 9, bold=False)
TITLE_FONT = create_font("Sans Serif", 14, bold=False)
SECTION_FONT = create_font("Sans Serif", 10, bold=False)
BUTTON_FONT = create_font("Sans Serif", 9, bold=False)

class InfoPanel(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedSize(950, 530)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title_label = QLabel(self.title)
        title_label.setFont(create_font("Sans Serif", 18, bold=False))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.Box)
        info_frame.setStyleSheet("QFrame { background-color: #f8f8f8; border: 2px solid #ccc; border-radius: 10px; }")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(15)
        
        info_label = QLabel(f"This is the {self.title} information panel.\n\nDetailed information about {self.title} will be displayed here.")
        info_label.setFont(create_font("Sans Serif", 12, bold=False))
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        layout.addWidget(info_frame)
        layout.addStretch()

class STTHV0Panel(QWidget):
    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.device = device
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedSize(950, 200)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        title = QLabel("CaenCrate / STT-HV0 Information")
        title.setFont(create_font("Sans Serif", 12, bold=False))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title, 0, 0, 1, 2)
        
        layout.addWidget(QLabel("Crate Model:"), 1, 0)
        self.crate_model_label = QLabel("--")
        self.crate_model_label.setStyleSheet("background-color: #e0f0ff; padding: 5px; font-weight: bold;")
        self.crate_model_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.crate_model_label, 1, 1)
        
        layout.addWidget(QLabel("Address:"), 2, 0)
        self.address_label = QLabel("--")
        self.address_label.setStyleSheet("background-color: #e0f0ff; padding: 5px;")
        self.address_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.address_label, 2, 1)
        
        layout.addWidget(QLabel("Connection Status:"), 3, 0)
        self.conn_status_label = QLabel("--")
        self.conn_status_label.setStyleSheet("background-color: #e0f0ff; padding: 5px;")
        self.conn_status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.conn_status_label, 3, 1)
        
        layout.addWidget(QLabel("Clear Alarm:"), 4, 0)
        self.clear_alarm_check = QCheckBox("Clear Alarm")
        self.clear_alarm_check.setStyleSheet("padding: 5px;")
        self.clear_alarm_check.stateChanged.connect(self.clear_alarm_changed)
        layout.addWidget(self.clear_alarm_check, 4, 1)
    
    def update_values(self):
        if not self.device:
            return
        try:
            if hasattr(self.device, 'CrateModel'):
                self.crate_model_label.setText(str(self.device.CrateModel))
            if hasattr(self.device, 'Address'):
                self.address_label.setText(str(self.device.Address))
            if hasattr(self.device, 'ConnectionStatus'):
                conn_status = self.device.ConnectionStatus
                self.conn_status_label.setText("Connected" if conn_status else "Disconnected")
                self.conn_status_label.setStyleSheet(
                    "background-color: #00cc00; padding: 5px;" if conn_status 
                    else "background-color: #cc0000; padding: 5px; color: white;"
                )
            if hasattr(self.device, 'ClearAlarm'):
                self.clear_alarm_check.setChecked(self.device.ClearAlarm)
        except Exception as e:
            print(f"STT-HV0 update error: {e}")
    
    def clear_alarm_changed(self, state):
        if self.device and hasattr(self.device, 'ClearAlarm'):
            self.device.ClearAlarm = (state == Qt.Checked)

class BoardPanel(QWidget):
    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.device = device
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedSize(950, 300)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
       
        title = QLabel("Board Information")
        title.setFont(create_font("Sans Serif", 12, bold=False))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title, 0, 0, 1, 5)
        
        layout.addWidget(QLabel("Board Model:"), 1, 0)
        self.board_model_label = QLabel("--")
        self.board_model_label.setStyleSheet("background-color: #c0e0ff; padding: 5px; font-weight: bold;")
        self.board_model_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.board_model_label, 1, 1)
        
        layout.addWidget(QLabel("BDHVmax (V):"), 2, 0)
        self.bdhvmax_label = QLabel("--")
        self.bdhvmax_label.setStyleSheet("background-color: #e0f0ff; padding: 5px;")
        self.bdhvmax_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.bdhvmax_label, 2, 1)
        
        layout.addWidget(QLabel("BDHImax (A):"), 2, 2)
        self.bdhimax_label = QLabel("--")
        self.bdhimax_label.setStyleSheet("background-color: #e0ffe0; padding: 5px;")
        self.bdhimax_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.bdhimax_label, 2, 3)
        
        layout.addWidget(QLabel("Board Status:"), 3, 0)
        self.bdstatus_label = QLabel("--")
        self.bdstatus_label.setStyleSheet("background-color: #f0f0f0; padding: 5px;")
        self.bdstatus_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.bdstatus_label, 3, 1)
    
    def update_values(self):
        if not self.device:
            return
        try:
            if hasattr(self.device, 'BoardModel'):
                self.board_model_label.setText(str(self.device.BoardModel))
            if hasattr(self.device, 'BDHVmax'):
                self.bdhvmax_label.setText(f"{self.device.BDHVmax:.1f}")
            if hasattr(self.device, 'BDHImax'):
                self.bdhimax_label.setText(f"{self.device.BDHImax:.1f}")
            if hasattr(self.device, 'BdStatus'):
                self.bdstatus_label.setText(str(self.device.BdStatus))
        except Exception as e:
            print(f"Board update error: {e}")

class AllChannelsPanel(QWidget):
    def __init__(self, device, parent=None):
        super().__init__(parent)
        self.device = device
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedSize(950, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 10, 0)
        layout.setSpacing(5)
        
        title = QLabel("All Channels Overview")
        title.setFont(create_font("Sans Serif", 12, bold=False))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setStyleSheet("QFrame { background-color: #e0e0e0; border: 1px solid #999; }")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        headers = ["Name", "Commands", "VMon (V)", "IMon (A)", "VSet (V)", "Apply", "ISet (A)", "Apply"]
        widths = [40, 90, 80, 80, 80, 50, 80, 50]
        
        for h, w in zip(headers, widths):
            label = QLabel(h)
            label.setFixedWidth(w)
            label.setFixedHeight(30)
            label.setFont(SECTION_FONT)
            label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(label)
        
        layout.addWidget(header_frame)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        
        self.channel_widgets = []
        for ch in range(8):
            channel_frame = QFrame()
            channel_frame.setFrameStyle(QFrame.Box)
            channel_frame.setStyleSheet("QFrame { background-color: #f8f8f8; border: 1px solid #ccc; }")
            channel_layout = QHBoxLayout(channel_frame)
            channel_layout.setSpacing(10)
            channel_layout.setContentsMargins(5, 5, 5, 5)
            
            ch_label = QLabel(f"CH{ch}")
            ch_label.setFixedWidth(40)
            ch_label.setFixedHeight(35)
            ch_label.setAlignment(Qt.AlignCenter)
            channel_layout.addWidget(ch_label)
            
            buttons_widget = QWidget()
            buttons_widget.setFixedWidth(90)
            buttons_widget.setFixedHeight(35)
            buttons_layout = QHBoxLayout(buttons_widget)
            buttons_layout.setSpacing(5)
            buttons_layout.setContentsMargins(0, 0, 0, 0)
            
            on_btn = QPushButton("ON")
            on_btn.setFixedWidth(40)
            on_btn.setFixedHeight(30)
            on_btn.setStyleSheet("background-color: #00cc00; color: white;")
            on_btn.clicked.connect(lambda checked, c=ch: self.channel_on(c))
            buttons_layout.addWidget(on_btn)
            
            off_btn = QPushButton("OFF")
            off_btn.setFixedWidth(40)
            off_btn.setFixedHeight(30)
            off_btn.setStyleSheet("background-color: #cc0000; color: white;")
            off_btn.clicked.connect(lambda checked, c=ch: self.channel_off(c))
            buttons_layout.addWidget(off_btn)
            
            channel_layout.addWidget(buttons_widget)
            
            vmon_label = QLabel("-- V")
            vmon_label.setFixedWidth(80)
            vmon_label.setFixedHeight(35)
            vmon_label.setStyleSheet("background-color: #e0f0ff; border: 1px solid #999;")
            vmon_label.setAlignment(Qt.AlignCenter)
            channel_layout.addWidget(vmon_label)
            
            imon_label = QLabel("-- A")
            imon_label.setFixedWidth(80)
            imon_label.setFixedHeight(35)
            imon_label.setStyleSheet("background-color: #e0ffe0; border: 1px solid #999;")
            imon_label.setAlignment(Qt.AlignCenter)
            channel_layout.addWidget(imon_label)
            
            vset_edit = QLineEdit("0.0")
            vset_edit.setFixedWidth(80)
            vset_edit.setFixedHeight(30)
            vset_edit.setStyleSheet("background-color: #fff8e0; border: 1px solid #999;")
            vset_edit.setAlignment(Qt.AlignCenter)
            channel_layout.addWidget(vset_edit)
            
            vset_btn = QPushButton("Apply")
            vset_btn.setFixedWidth(50)
            vset_btn.setFixedHeight(30)
            vset_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            vset_btn.clicked.connect(lambda checked, c=ch, w=vset_edit: self.apply_vset(c, w))
            channel_layout.addWidget(vset_btn)
            
            iset_edit = QLineEdit("0.0")
            iset_edit.setFixedWidth(80)
            iset_edit.setFixedHeight(30)
            iset_edit.setStyleSheet("background-color: #fff8e0; border: 1px solid #999;")
            iset_edit.setAlignment(Qt.AlignCenter)
            channel_layout.addWidget(iset_edit)
            
            iset_btn = QPushButton("Apply")
            iset_btn.setFixedWidth(50)
            iset_btn.setFixedHeight(30)
            iset_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            iset_btn.clicked.connect(lambda checked, c=ch, w=iset_edit: self.apply_iset(c, w))
            channel_layout.addWidget(iset_btn)
            
            scroll_layout.addWidget(channel_frame)
            
            self.channel_widgets.append({
                'vmon': vmon_label,
                'imon': imon_label,
                'vset': vset_edit,
                'iset': iset_edit,
                'channel': ch
            })
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        cmd_frame = QFrame()
        cmd_frame.setFrameStyle(QFrame.Box)
        cmd_frame.setStyleSheet("QFrame { background-color: #f0f0f0; margin-top: 10px; }")
        cmd_layout = QHBoxLayout(cmd_frame)
        cmd_layout.setSpacing(40)
        
        self.btn_on = QPushButton("ON ALL")
        self.btn_on.setFont(BUTTON_FONT)
        self.btn_on.setStyleSheet("background-color: #00cc00; color: white; font-size: 10pt; padding: 8px;")
        self.btn_on.clicked.connect(self.global_on)
        cmd_layout.addWidget(self.btn_on)
        
        self.btn_off = QPushButton("OFF ALL")
        self.btn_off.setFont(BUTTON_FONT)
        self.btn_off.setStyleSheet("background-color: #cc0000; color: white; font-size: 10pt; padding: 8px;")
        self.btn_off.clicked.connect(self.global_off)
        cmd_layout.addWidget(self.btn_off)
        
        cmd_layout.addStretch()
        
        self.status_label = QLabel("Ready")
        self.status_label.setFont(SANS_FONT)
        self.status_label.setStyleSheet("background-color: #e0e0e0; padding: 5px;")
        cmd_layout.addWidget(self.status_label)
        
        layout.addWidget(cmd_frame)
    
    def update_values(self):
        if not self.device:
            return
        try:
            for ch_widget in self.channel_widgets:
                ch = ch_widget['channel']
                try:
                    vmon = self.device.VMon[ch]
                    imon = self.device.IMon[ch]
                    vset = self.device.VSet[ch]
                    iset = self.device.ISet[ch]
                    ch_widget['vmon'].setText(f"{vmon:.3f}")
                    ch_widget['imon'].setText(f"{imon:.3f}")
                    ch_widget['vset'].setText(f"{vset:.3f}")
                    ch_widget['iset'].setText(f"{iset:.3f}")
                except:
                    ch_widget['vmon'].setText("--")
                    ch_widget['imon'].setText("--")
                    ch_widget['vset'].setText("--")
                    ch_widget['iset'].setText("--")
        except Exception as e:
            pass
    
    def apply_vset(self, channel, widget):
        if not self.device:
            return
        try:
            new_vset = float(widget.text())
            vset_list = list(self.device.VSet)
            vset_list[channel] = new_vset
            self.device.VSet = vset_list
        except:
            pass
    
    def apply_iset(self, channel, widget):
        if not self.device:
            return
        try:
            new_iset = float(widget.text())
            iset_list = list(self.device.ISet)
            iset_list[channel] = new_iset
            self.device.ISet = iset_list
        except:
            pass
    
    def channel_on(self, channel):
        pass
    
    def channel_off(self, channel):
        pass
    
    def global_on(self):
        if self.device:
            try:
                self.device.On()
            except:
                pass
    
    def global_off(self):
        if self.device:
            try:
                self.device.Off()
            except:
                pass

class ChannelPanel(QWidget):
    def __init__(self, channel, device, parent=None):
        super().__init__(parent)
        self.channel = channel
        self.device = device
        self.setup_ui()
    
    def setup_ui(self):
        self.setFixedSize(950, 530)
        
        layout = QGridLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(0, 0, 10, 0)
        
        title = QLabel(f"Channel {self.channel} Control Panel")
        title.setFont(create_font("Sans Serif", 12, bold=False))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title, 0, 0, 1, 2)
        
        vmon_group = QGroupBox("Voltage Monitor")
        vmon_group.setFont(SANS_FONT)
        vmon_layout = QVBoxLayout(vmon_group)
        self.vmon_label = QLabel("-- V")
        self.vmon_label.setFont(create_font("Sans Serif", 16, bold=False))
        self.vmon_label.setStyleSheet("background-color: #e0f0ff; padding: 20px;")
        self.vmon_label.setAlignment(Qt.AlignCenter)
        vmon_layout.addWidget(self.vmon_label)
        layout.addWidget(vmon_group, 1, 0)
        
        imon_group = QGroupBox("Current Monitor")
        imon_group.setFont(SANS_FONT)
        imon_layout = QVBoxLayout(imon_group)
        self.imon_label = QLabel("-- A")
        self.imon_label.setFont(create_font("Sans Serif", 16, bold=False))
        self.imon_label.setStyleSheet("background-color: #e0ffe0; padding: 20px;")
        self.imon_label.setAlignment(Qt.AlignCenter)
        imon_layout.addWidget(self.imon_label)
        layout.addWidget(imon_group, 1, 1)
        
        vset_group = QGroupBox("Voltage Setpoint")
        vset_group.setFont(SANS_FONT)
        vset_layout = QHBoxLayout(vset_group)
        self.vset_edit = QLineEdit("100.0")
        self.vset_edit.setFont(create_font("Sans Serif", 12, bold=False))
        self.vset_edit.setStyleSheet("background-color: #fff8e0; padding: 10px;")
        self.vset_edit.setAlignment(Qt.AlignCenter)
        vset_layout.addWidget(self.vset_edit)
        self.vset_btn = QPushButton("Apply")
        self.vset_btn.setFont(create_font("Sans Serif", 10, bold=False))
        self.vset_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.vset_btn.clicked.connect(self.apply_vset)
        vset_layout.addWidget(self.vset_btn)
        layout.addWidget(vset_group, 2, 0)
        
        iset_group = QGroupBox("Current Setpoint")
        iset_group.setFont(SANS_FONT)
        iset_layout = QHBoxLayout(iset_group)
        self.iset_edit = QLineEdit("50.0")
        self.iset_edit.setFont(create_font("Sans Serif", 12, bold=False))
        self.iset_edit.setStyleSheet("background-color: #fff8e0; padding: 10px;")
        self.iset_edit.setAlignment(Qt.AlignCenter)
        iset_layout.addWidget(self.iset_edit)
        self.iset_btn = QPushButton("Apply")
        self.iset_btn.setFont(create_font("Sans Serif", 10, bold=False))
        self.iset_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.iset_btn.clicked.connect(self.apply_iset)
        iset_layout.addWidget(self.iset_btn)
        layout.addWidget(iset_group, 2, 1)
        
        cmd_group = QGroupBox("Channel Commands")
        cmd_group.setFont(SANS_FONT)
        cmd_layout = QHBoxLayout(cmd_group)
        self.on_btn = QPushButton("ON")
        self.on_btn.setFont(create_font("Sans Serif", 10, bold=False))
        self.on_btn.setStyleSheet("background-color: #00cc00; color: white; padding: 10px;")
        self.on_btn.clicked.connect(self.channel_on)
        cmd_layout.addWidget(self.on_btn)
        
        self.off_btn = QPushButton("OFF")
        self.off_btn.setFont(create_font("Sans Serif", 10, bold=False))
        self.off_btn.setStyleSheet("background-color: #cc0000; color: white; padding: 10px;")
        self.off_btn.clicked.connect(self.channel_off)
        cmd_layout.addWidget(self.off_btn)
        
        self.reset_btn = QPushButton("RESET")
        self.reset_btn.setFont(create_font("Sans Serif", 10, bold=False))
        self.reset_btn.setStyleSheet("background-color: #ffcc00; padding: 10px;")
        self.reset_btn.clicked.connect(self.channel_reset)
        cmd_layout.addWidget(self.reset_btn)
        
        layout.addWidget(cmd_group, 3, 0, 1, 2)
    
    def update_values(self):
        if not self.device:
            return
        try:
            vmon = self.device.VMon[self.channel]
            imon = self.device.IMon[self.channel]
            vset = self.device.VSet[self.channel]
            iset = self.device.ISet[self.channel]
            self.vmon_label.setText(f"{vmon:.3f} V")
            self.imon_label.setText(f"{imon:.3f} A")
            self.vset_edit.setText(f"{vset:.1f}")
            self.iset_edit.setText(f"{iset:.1f}")
        except:
            pass
    
    def apply_vset(self):
        if not self.device:
            return
        try:
            new_vset = float(self.vset_edit.text())
            vset_list = list(self.device.VSet)
            vset_list[self.channel] = new_vset
            self.device.VSet = vset_list
        except:
            pass
    
    def apply_iset(self):
        if not self.device:
            return
        try:
            new_iset = float(self.iset_edit.text())
            iset_list = list(self.device.ISet)
            iset_list[self.channel] = new_iset
            self.device.ISet = iset_list
        except:
            pass
    
    def channel_on(self):
        pass
    
    def channel_off(self):
        pass
    
    def channel_reset(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPD DCS")
        self.setGeometry(100, 100, 1500, 1000)
        
        self.setFont(SANS_FONT)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        fixed_container = QWidget()
        fixed_container.setFixedSize(1280, 950)
        container_layout = QHBoxLayout(fixed_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)
        
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_panel.setFixedHeight(1900)  # Only this changed from 900 to 1900
        left_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.nav_tree = QTreeWidget()
        self.nav_tree.setHeaderLabel("SPD DCS")
        self.nav_tree.setFixedWidth(280)
        self.nav_tree.itemClicked.connect(self.on_tree_item_clicked)
        
        # Build navigation tree
        spd_item = QTreeWidgetItem(["SPD"])
        self.nav_tree.addTopLevelItem(spd_item)
        
        micromegas_item = QTreeWidgetItem(["MicroMegas"])
        spd_item.addChild(micromegas_item)
        
        straw_tracker_item = QTreeWidgetItem(["StrawTracker"])
        spd_item.addChild(straw_tracker_item)
        
        lv_item = QTreeWidgetItem(["LV"])
        straw_tracker_item.addChild(lv_item)
        
        hv_item = QTreeWidgetItem(["HV"])
        straw_tracker_item.addChild(hv_item)
        
        caen_crate_item = QTreeWidgetItem(["CaenCrate"])
        hv_item.addChild(caen_crate_item)
        
        boards_item = QTreeWidgetItem(["Boards"])
        caen_crate_item.addChild(boards_item)
        
        channels_item = QTreeWidgetItem(["Channels"])
        caen_crate_item.addChild(channels_item)
        
        self.channel_items = []
        for ch in range(8):
            channel_item = QTreeWidgetItem([f"Channel {ch}"])
            channels_item.addChild(channel_item)
            self.channel_items.append(channel_item)
        
        magnet_item = QTreeWidgetItem(["Magnet"])
        spd_item.addChild(magnet_item)
        
        range_system_item = QTreeWidgetItem(["RangeSystem"])
        spd_item.addChild(range_system_item)
        
        straw_tracker_ec_item = QTreeWidgetItem(["StrawTrackerEndCap"])
        spd_item.addChild(straw_tracker_ec_item)
        
        bbc_item = QTreeWidgetItem(["BBC"])
        spd_item.addChild(bbc_item)
        
        range_system_ec_item = QTreeWidgetItem(["RangeSystemEndCap"])
        spd_item.addChild(range_system_ec_item)
        
        bbc_mcp_item = QTreeWidgetItem(["BBC_MCP"])
        spd_item.addChild(bbc_mcp_item)
        
        zero_degree_item = QTreeWidgetItem(["ZeroDegreeCalorimeter"])
        spd_item.addChild(zero_degree_item)
        
        self.nav_tree.expandAll()
        left_layout.addWidget(self.nav_tree)
        left_layout.addStretch()
        
        right_panel = QWidget()
        right_panel.setFixedWidth(960)
        right_panel.setFixedHeight(900)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.content_stack = QStackedWidget()
        self.content_stack.setFixedSize(950, 870)
        
        try:
            self.device = tango.DeviceProxy("sys/CaenSMARTHV/StrawTrackerCaenHV_0")
            print("✓ Connected to sys/ps/1")
        except Exception as e:
            self.device = None
            print(f"✗ Failed to connect: {e}")
        
        self.panels = {}
        
        for name in ["SPD", "MicroMegas", "StrawTracker", "LV", "HV", 
                     "Magnet", "RangeSystem", "StrawTrackerEndCap", "BBC", 
                     "RangeSystemEndCap", "BBC_MCP", "ZeroDegreeCalorimeter"]:
            self.panels[name] = InfoPanel(name)
            self.content_stack.addWidget(self.panels[name])
        
        self.stt_panel = STTHV0Panel(self.device)
        self.content_stack.addWidget(self.stt_panel)
        
        self.board_panel = BoardPanel(self.device)
        self.content_stack.addWidget(self.board_panel)
        
        self.all_channels_panel = AllChannelsPanel(self.device)
        self.content_stack.addWidget(self.all_channels_panel)
        
        self.channel_panels = []
        for ch in range(8):
            channel_panel = ChannelPanel(ch, self.device)
            self.content_stack.addWidget(channel_panel)
            self.channel_panels.append(channel_panel)
        
        right_layout.addWidget(self.content_stack)
        
        container_layout.addWidget(left_panel)
        container_layout.addWidget(right_panel)
        
        main_layout.addWidget(fixed_container, 0, Qt.AlignTop | Qt.AlignLeft)
        main_layout.addStretch()
        
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready - Select item from navigation tree")
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(1000)
        
        self.content_stack.setCurrentIndex(0)
        
        self.index_map = {}
        current_index = 0
        for name in ["SPD", "MicroMegas", "StrawTracker", "LV", "HV", 
                     "Magnet", "RangeSystem", "StrawTrackerEndCap", "BBC", 
                     "RangeSystemEndCap", "BBC_MCP", "ZeroDegreeCalorimeter"]:
            self.index_map[name] = current_index
            current_index += 1
        self.index_map["CaenCrate"] = current_index
        self.index_map["Boards"] = current_index + 1
        self.index_map["Channels"] = current_index + 2
    
    def on_tree_item_clicked(self, item, column):
        item_text = item.text(column)
        
        if item_text in self.index_map:
            self.content_stack.setCurrentIndex(self.index_map[item_text])
        elif item_text == "CaenCrate":
            self.content_stack.setCurrentIndex(self.index_map["CaenCrate"])
        elif item_text == "Boards":
            self.content_stack.setCurrentIndex(self.index_map["Boards"])
        elif item_text == "Channels":
            self.content_stack.setCurrentIndex(self.index_map["Channels"])
        elif item_text.startswith("Channel"):
            try:
                channel_num = int(item_text.split()[1])
                self.content_stack.setCurrentIndex(self.index_map["Channels"] + 1 + channel_num)
            except:
                pass
    
    def update_all(self):
        if not self.device:
            return
        
        try:
            self.stt_panel.update_values()
            self.board_panel.update_values()
            self.all_channels_panel.update_values()
            for panel in self.channel_panels:
                panel.update_values()
        except:
            pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
