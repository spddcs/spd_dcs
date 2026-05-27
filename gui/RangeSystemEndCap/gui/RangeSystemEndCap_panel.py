#!/usr/bin/env python3
"""Range System End Cap Panel"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from base_panel import BaseNodePanel

class RangeSystemEndCapPanel(BaseNodePanel):
    def __init__(self, device=None, parent=None):
        super().__init__("Range System End Cap", device, parent)

def get_panel(device=None):
    panel = RangeSystemEndCapPanel(device)
    return panel

def main():
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    panel = RangeSystemEndCapPanel()
    panel.setWindowTitle("Range System End Cap")
    panel.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
