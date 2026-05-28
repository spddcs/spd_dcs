# SPD DCS - SPD Detector Control System

[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/)
[![TANGO](https://img.shields.io/badge/TANGO-Controls-orange.svg)](https://tango-controls.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-GUI-brightgreen.svg)](https://riverbankcomputing.com/software/pyqt/)

## Overview
SPD DCS is a detector complete control system, integrating:
- CAEN SMARTHV high voltage power supplies via OPC UA
- TANGO controls framework for distributed control
- PyQt5-based GUI for monitoring and control
- Complete database persistence for configurations

## Features

### Device Server
- **13 channel parameters** per channel (IMRange, IMon, ISet, Name, PDwn, Pw, RDwn, RUp, Status, Trip, VMon, VSet, Index)
- **8 channels** support with array attributes
- **OPC UA integration** with automatic updates
- **TANGO device server** with read/write capabilities

### GUI
- **Multi-detector support**: SPD, BBC, BBC_MCP, Magnet, MicroMegas, RangeSystem, RangeSystemEndCaap, StrawTracker, StrawTrackerEndCap, ZeroDegreeCalorimeter
- **Complete StrawTracker control** with all 13 parameters per channel
- **Navigation tree** for easy access
- **Real-time monitoring** with auto-refresh
- **Color-coded status** for voltage, current, and alarms

### Database
- **TANGO database schema** with history tables
- **Migration scripts** for easy updates
- **Backup and restore** utilities

## Repository Structure
spd_dcs/
├── database/ # Database schemas and migrations
│ ├── schema.sql # Complete database schema
│ └── migrate.sh # Migration script
├── device_server/ # TANGO device server
│ └── CaenSMARTHV.py # Main device server with OPC UA
├── gui/ # PyQt5 GUI application
│ ├── master_merge_gui.py # Main GUI launcher
│ ├── base_panel.py # Base panel class
│ ├── StrawTracker/ # StrawTracker panels
│ ├── SPD/ # SPD detector panels
│ ├── BBC/ # BBC detector panels
│ └── ... # Other detectors
├── scripts/ # Installation and setup scripts
│ ├── install.sh # Main installer
│ ├── install_dependencies.sh # System dependencies
│ ├── setup_device_server.sh # Device server setup
│ ├── install_gui.sh # GUI installation
│ └── verify_gui.sh # Verification script
└── docs/ # Documentation

## Quick Installation

### From GitHub
```bash
git clone https://github.com/spddcs/spd_dcs.git
cd spd_dcs
sudo ./scripts/install.sh
System Requirements
Hardware

    CPU: 2+ cores

    RAM: 4+ GB

    Disk: 10+ GB

Software

    Rocky Linux 9 / RHEL 9

    Python 3.9+

    MariaDB 10.5+

    TANGO Controls 9.5+
Usage
Start Device Server
bash

systemctl start tango-caen-device
systemctl status tango-caen-device

Launch GUI
bash

su - spddcs
./start_spd_gui.sh


Monitor Channels

Navigate through: SPD → StrawTracker → S0 → HV → Channels → Channel X
Configuration
TANGO Database

    Host: na62dcs99.cern.ch:10000

    User: tango

    Password: tango

OPC UA Server

    URL: opc.tcp://na62dcs99.cern.ch:4801

    Nodes: STT-HV0.Board00.ChanXXX.*
Development
Adding New Parameters

    Update device server attribute definitions

    Add OPC UA node mapping

    Update GUI panels

Testing
bash

python -m pytest tests/
./scripts/verify_gui.sh
Troubleshooting
Device Server Won't Start
bash

journalctl -u tango-caen-device -f
./scripts/verify_gui.sh

GUI Won't Launch
bash

# Check PyQt5
python -c "from PyQt5.QtWidgets import QApplication"

# Check TANGO connection
python -c "import tango; tango.DeviceProxy('spd/caensmarthv/strawtrackercaenhv_0')"
Documentation

    Installation Guide

    User Manual

    Developer Guide

    API Reference

License

Proprietary - SPD Collaboration
Contact

    SPD DCS Team - JINR

    Email: Sergey.Shkarovskiy@jinr.ru

    Issue Tracker: https://github.com/spddcs/spd_dcs/issues
Acknowledgments

    JINR LHEP SPD DCS group for TANGO framework

    CAEN for SMARTHV power supplies

    PyQt5 team for GUI framework

*Last Updated: 2025-05-27*
