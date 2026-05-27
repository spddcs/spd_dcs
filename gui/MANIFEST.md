# SPD DCS GUI Manifest

## Directory Structure

### Main GUI Files
- `master_merge_gui.py` - Main merged GUI application
- `master_node_manager.py` - Node management system
- `master_with_panels.py` - Panel management
- `base_panel.py` - Base class for all panels

### Detector GUIs

#### SPD
- Main SPD detector control panel

#### BBC (Beam-Beam Counter)
- BBC detector monitoring and control

#### BBC_MCP
- BBC MCP detector control

#### Magnet
- Magnet power supply control

#### MicroMegas
- MicroMegas detector readout and HV control

#### RangeSystem
- Range system control

#### RangeSystemEndCap
- Endcap range system

#### StrawTracker
- Complete StrawTracker detector control
- HV channels 0-7 with all 13 parameters
- LV monitoring
- CAEN crate control

#### StrawTrackerEndCap
- Endcap StrawTracker control

#### ZeroDegreeCalorimeter
- Zero-degree calorimeter control

### Nodes
- Individual node control panels

### Pictures
- Icons and images for the GUI

## Total Components
- Python files: 141 files
- Detectors: 10 detectors
- Channel parameters: 13 per channel
- Total channels: 8 channels per detector
