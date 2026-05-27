#!/usr/bin/env python3
"""
Python TANGO Database Server - No MySQL Required
"""

import sys
import logging
from tango.server import Device, command, attribute, run
from tango import DevState, AttrWriteType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TangoDatabase(Device):
    """In-memory TANGO database server"""
    
    def init_device(self):
        super().init_device()
        self.devices = {}  # device_name -> device_class
        self.exported_devices = []  # List of exported devices
        self.set_state(DevState.ON)
        logger.info("="*50)
        logger.info("TANGO Database Server Started")
        logger.info("Database type: In-memory")
        logger.info("="*50)
    
    @command(dtype_in=str, dtype_out=str)
    def add_device(self, device_name):
        """Add a device to the database"""
        device_class = "CaenSMARTHV"  # Default class
        if device_name not in self.devices:
            self.devices[device_name] = device_class
            if device_name not in self.exported_devices:
                self.exported_devices.append(device_name)
            logger.info(f"Added device: {device_name} (class: {device_class})")
            return f"Device {device_name} added successfully"
        else:
            return f"Device {device_name} already exists"
    
    @command(dtype_out=str)
    def get_device_list(self):
        """Get list of all devices"""
        return str(self.exported_devices)
    
    @command(dtype_in=str, dtype_out=str)
    def get_device_class(self, device_name):
        """Get class of a device"""
        return self.devices.get(device_name, "Unknown")
    
    @command(dtype_in=str, dtype_out=bool)
    def device_exists(self, device_name):
        """Check if device exists"""
        return device_name in self.devices
    
    @command(dtype_out=str)
    def info(self):
        """Get database info"""
        return f"TANGO Database (Python) - {len(self.devices)} devices registered"

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting Python TANGO Database Server")
    print("Port: 10000 | Mode: In-memory")
    print("="*60 + "\n")
    
    # Run the database server
    run([TangoDatabase], args=["TangoDatabase", "-ORBendPoint", "giop:tcp::10000", "-v3"])
