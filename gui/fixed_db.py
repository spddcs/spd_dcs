#!/usr/bin/env python3
import sys
from tango.server import Device, command, run
from tango import DevState

class FixedDB(Device):
    def init_device(self):
        super().init_device()
        self.devices = []
        self.set_state(DevState.ON)
        print("="*50, flush=True)
        print("TANGO DATABASE SERVER READY", flush=True)
        print("="*50, flush=True)
    
    @command(dtype_in=str, dtype_out=str)
    def add_device(self, device_name):
        if device_name not in self.devices:
            self.devices.append(device_name)
            print(f"Device added: {device_name}", flush=True)
            return f"Added {device_name}"
        return f"{device_name} exists"
    
    @command(dtype_out=str)
    def get_device_list(self):
        return str(self.devices)

if __name__ == "__main__":
    # Instance name is required as first argument
    print("Starting TANGO Database...", flush=True)
    run([FixedDB], args=["FixedDB", "-ORBendPoint", "giop:tcp::10000", "-v2"])
