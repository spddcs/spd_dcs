#!/usr/bin/env python3
from tango.server import Device, command, run
from tango import DevState

class SimpleDB(Device):
    def init_device(self):
        super().init_device()
        self.devices = []
        self.set_state(DevState.ON)
        print("Simple TANGO Database Started")
    
    @command(dtype_out=str)
    def get_device_list(self):
        return str(self.devices)
    
    @command(dtype_in=str, dtype_out=str)
    def add_device(self, name):
        if name not in self.devices:
            self.devices.append(name)
            return f"Added {name}"
        return f"{name} exists"
    
    @command(dtype_in=str, dtype_out=str)
    def device_class(self, name):
        return "CaenSMARTHV"

if __name__ == "__main__":
    run([SimpleDB], args=["SimpleDB", "-ORBendPoint", "giop:tcp::10000"])
