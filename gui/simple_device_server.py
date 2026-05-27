#!/usr/bin/env python3
"""
Simple TANGO Device Server - No Database Required
Runs in no-database mode using the correct method
"""

import os
import sys
import time
import threading
import random

# Set TANGO host (will be ignored in no-db mode)
os.environ['TANGO_HOST'] = 'localhost:10000'

import tango
from tango.server import Device, attribute, command, run
from tango import DevState, AttrWriteType

class SimpleHV(Device):
    VMon = attribute(dtype=(float,), max_dim_x=8, label="Voltage Monitor", unit="V")
    IMon = attribute(dtype=(float,), max_dim_x=8, label="Current Monitor", unit="A")
    VSet = attribute(dtype=(float,), max_dim_x=8, label="Voltage Setpoint", unit="V", 
                     access=AttrWriteType.READ_WRITE)
    ISet = attribute(dtype=(float,), max_dim_x=8, label="Current Setpoint", unit="A",
                     access=AttrWriteType.READ_WRITE)
    Temperature = attribute(dtype=float, label="Temperature", unit="°C")
    
    def init_device(self):
        super().init_device()
        self._vmon = [0.0] * 8
        self._imon = [0.0] * 8
        self._vset = [100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0]
        self._iset = [0.05] * 8
        self._temperature = 25.0
        
        print(f"✓ Device {self.get_name()} initialized (No-DB Mode)")
        self.set_state(DevState.ON)
        
        self._running = True
        self._thread = threading.Thread(target=self._simulate, daemon=True)
        self._thread.start()
    
    def _simulate(self):
        while self._running:
            for ch in range(8):
                diff = self._vset[ch] - self._vmon[ch]
                if abs(diff) > 1:
                    self._vmon[ch] += diff * 0.1
                self._vmon[ch] += random.uniform(-0.5, 0.5)
                self._vmon[ch] = max(0, min(self._vmon[ch], 1000))
                self._imon[ch] = (self._vmon[ch] / 1000.0) * self._iset[ch]
                self._imon[ch] += random.uniform(-0.0005, 0.0005)
            self._temperature = 25.0 + random.uniform(-2, 2)
            
            self.push_change_event("VMon", self._vmon)
            self.push_change_event("IMon", self._imon)
            self.push_change_event("Temperature", self._temperature)
            time.sleep(1)
    
    def read_VMon(self): return self._vmon
    def read_IMon(self): return self._imon
    def read_VSet(self): return self._vset
    def read_ISet(self): return self._iset
    def read_Temperature(self): return self._temperature
    
    def write_VSet(self, value):
        for ch in range(8):
            self._vset[ch] = max(0, min(value[ch], 1000))
        self.push_change_event("VSet", self._vset)
    
    def write_ISet(self, value):
        for ch in range(8):
            self._iset[ch] = max(0, min(value[ch], 0.1))
        self.push_change_event("ISet", self._iset)
    
    @command
    def On(self):
        print("ON command - All channels enabled")
        self.set_state(DevState.RUNNING)
    
    @command
    def Off(self):
        print("OFF command - All channels disabled")
        for ch in range(8):
            self._vmon[ch] = 0
        self.push_change_event("VMon", self._vmon)
        self.set_state(DevState.ON)
    
    @command
    def Reset(self):
        print("RESET command")
        for ch in range(8):
            self._vmon[ch] = 0
            self._imon[ch] = 0
        self.push_change_event("VMon", self._vmon)
        self.push_change_event("IMon", self._imon)

if __name__ == "__main__":
    import sys
    instance_name = sys.argv[1] if len(sys.argv) > 1 else "1"
    print("=" * 60)
    print(f"Starting Simple HV Device Server")
    print(f"Instance: {instance_name}")
    print(f"Mode: NO DATABASE (Standalone)")
    print("=" * 60)
    
    # Correct way to run without database - use -nodb command line flag
    # The server will run but won't register with a database
    run([SimpleHV])
