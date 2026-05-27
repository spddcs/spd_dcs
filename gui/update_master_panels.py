#!/usr/bin/env python3
"""Update master_merge_gui.py to include all panels"""

import re

master_file = "/home/shkar/SPD_DCS/master_merge_gui.py"

# Read current file
with open(master_file, 'r') as f:
    content = f.read()

# Update panel_map to include CaenCrate, Boards, Channels, and individual channels
panel_map_update = '''
        # Add CAEN crate panels
        "CaenCrate": f"{base_path}/StrawTracker/gui/CaenCrate_panel.py",
        "Boards": f"{base_path}/StrawTracker/gui/Boards_panel.py",
        "Channels": f"{base_path}/StrawTracker/gui/Channels_panel.py",
        "Channel_0": f"{base_path}/StrawTracker/gui/Channel0_panel.py",
        "Channel_1": f"{base_path}/StrawTracker/gui/Channel1_panel.py",
        "Channel_2": f"{base_path}/StrawTracker/gui/Channel2_panel.py",
        "Channel_3": f"{base_path}/StrawTracker/gui/Channel3_panel.py",
        "Channel_4": f"{base_path}/StrawTracker/gui/Channel4_panel.py",
        "Channel_5": f"{base_path}/StrawTracker/gui/Channel5_panel.py",
        "Channel_6": f"{base_path}/StrawTracker/gui/Channel6_panel.py",
        "Channel_7": f"{base_path}/StrawTracker/gui/Channel7_panel.py",'''

# Update the panel_map section
# This is a simplified approach - manually updating is safer
print("Please manually update master_merge_gui.py to include the new panels")
print("or run this command to add them:")
print("""
# Add these lines to the panel_map dictionary in master_merge_gui.py:

        "CaenCrate": f"{base_path}/StrawTracker/gui/CaenCrate_panel.py",
        "Boards": f"{base_path}/StrawTracker/gui/Boards_panel.py",
        "Channels": f"{base_path}/StrawTracker/gui/Channels_panel.py",
        "Channel_0": f"{base_path}/StrawTracker/gui/Channel0_panel.py",
        "Channel_1": f"{base_path}/StrawTracker/gui/Channel1_panel.py",
        "Channel_2": f"{base_path}/StrawTracker/gui/Channel2_panel.py",
        "Channel_3": f"{base_path}/StrawTracker/gui/Channel3_panel.py",
        "Channel_4": f"{base_path}/StrawTracker/gui/Channel4_panel.py",
        "Channel_5": f"{base_path}/StrawTracker/gui/Channel5_panel.py",
        "Channel_6": f"{base_path}/StrawTracker/gui/Channel6_panel.py",
        "Channel_7": f"{base_path}/StrawTracker/gui/Channel7_panel.py",
""")

print("\nAll panel files have been created!")
print("\nTo use them, update master_merge_gui.py with the panel mapping above.")
