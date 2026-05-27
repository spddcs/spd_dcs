#!/usr/bin/env python3
import sys
from tango.server import Device, command, run
from tango import DevState

class WorkingDB(Device):
    def init_device(self):
        super().init_device()
        self.devices = []
        self.set_state(DevState.ON)
        print("\n" + "="*60)
        print("WORKING TANGO DATABASE SERVER")
        print("Database is ready to accept devices")
        print("="*60 + "\n")
    
    @command(dtype_in=str, dtype_out=str)
    def add_device(self, device_name):
        if device_name not in self.devices:
            self.devices.append(device_name)
            print(f"✓ Device added: {device_name}")
            return f"Device {device_name} added"
        return f"Device {device_name} already exists"
    
    @command(dtype_out=str)
    def get_device_list(self):
        return str(self.devices)
    
    @command(dtype_out=str)
    def get_info(self):
        return f"WorkingDB with {len(self.devices)} devices"

if __name__ == "__main__":
    # The instance name is passed automatically when running
    # Just run the server without extra arguments
    run([WorkingDB])
