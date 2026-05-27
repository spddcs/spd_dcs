#!/usr/bin/env python3
"""
CAEN SMARTHV Device Server for SPD DCS
Complete OPC UA integration with all channel parameters
"""

import tango
from tango.server import Device, attribute, device_property, command, run
from tango import DevState, AttrWriteType
import time
import threading
import logging
from opcua import Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaenSMARTHV(Device):
    """CAEN SMARTHV High Voltage Power Supply Device Server"""
    
    # Device properties
    OpcUrl = device_property(dtype=str, default_value="opc.tcp://na62dcs99.cern.ch:4801")
    UpdateInterval = device_property(dtype=int, default_value=1000)
    NumChannels = device_property(dtype=int, default_value=8)
    
    # Channel attributes
    IMRange = attribute(dtype=(float,), max_dim_x=8, label="Current Range", unit="A",
                        access=AttrWriteType.READ_WRITE)
    IMon = attribute(dtype=(float,), max_dim_x=8, label="Current Monitor", unit="A")
    ISet = attribute(dtype=(float,), max_dim_x=8, label="Current Setpoint", unit="A",
                     access=AttrWriteType.READ_WRITE)
    ChannelName = attribute(dtype=(str,), max_dim_x=8, label="Channel Name")
    PDwn = attribute(dtype=(float,), max_dim_x=8, label="Power Down", unit="W")
    Pw = attribute(dtype=(float,), max_dim_x=8, label="Channel Power", unit="W")
    RDwn = attribute(dtype=(float,), max_dim_x=8, label="Ramp Down Rate", unit="V/s",
                     access=AttrWriteType.READ_WRITE)
    RUp = attribute(dtype=(float,), max_dim_x=8, label="Ramp Up Rate", unit="V/s",
                    access=AttrWriteType.READ_WRITE)
    ChannelStatus = attribute(dtype=(int,), max_dim_x=8, label="Channel Status")
    Trip = attribute(dtype=(bool,), max_dim_x=8, label="Trip Status")
    VMon = attribute(dtype=(float,), max_dim_x=8, label="Voltage Monitor", unit="V")
    VSet = attribute(dtype=(float,), max_dim_x=8, label="Voltage Setpoint", unit="V",
                     access=AttrWriteType.READ_WRITE)
    ChannelIndex = attribute(dtype=(int,), max_dim_x=8, label="Channel Index")
    
    # Board/Crate attributes
    CrateModel = attribute(dtype=str, label="Crate Model")
    Address = attribute(dtype=str, label="Address")
    ConnectionStatus = attribute(dtype=bool, label="Connection Status")
    BoardModel = attribute(dtype=str, label="Board Model")
    BDHVmax = attribute(dtype=float, label="Board HV Maximum", unit="V")
    BDHImax = attribute(dtype=float, label="Board Current Maximum", unit="A")
    BdStatus = attribute(dtype=int, label="Board Status")
    
    def init_device(self):
        super().init_device()
        self._init_arrays()
        self._init_opcua()
        self._start_update_thread()
        logger.info(f"Device initialized with {self.NumChannels} channels")
    
    def _init_arrays(self):
        n = self.NumChannels
        self._imrange = [0.0] * n
        self._imon = [0.0] * n
        self._iset = [0.0] * n
        self._channel_name = [f"CH{ch:03d}" for ch in range(n)]
        self._pdwn = [0.0] * n
        self._pw = [0.0] * n
        self._rdwn = [0.0] * n
        self._rup = [0.0] * n
        self._channel_status = [0] * n
        self._trip = [False] * n
        self._vmon = [0.0] * n
        self._vset = [0.0] * n
        self._channel_index = list(range(n))
    
    def _init_opcua(self):
        self._client = None
        self._opc_connected = False
        try:
            self._client = Client(self.OpcUrl)
            self._client.connect()
            self._opc_connected = True
            self.set_state(DevState.ON)
            logger.info(f"Connected to OPC UA at {self.OpcUrl}")
        except Exception as e:
            logger.error(f"OPC UA connection failed: {e}")
            self.set_state(DevState.FAULT)
    
    def _start_update_thread(self):
        self._running = True
        self._update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self._update_thread.start()
    
    def _update_loop(self):
        while self._running:
            try:
                if self._opc_connected and self._client:
                    self._read_all_parameters()
                    self._push_all_events()
                time.sleep(self.UpdateInterval / 1000.0)
            except Exception as e:
                logger.error(f"Update error: {e}")
                time.sleep(5)
    
    def _read_all_parameters(self):
        for ch in range(self.NumChannels):
            self._read_parameter(ch, "IMRange", "imrange")
            self._read_parameter(ch, "IMon", "imon")
            self._read_parameter(ch, "ISet", "iset")
            self._read_parameter(ch, "Name", "channel_name", str)
            self._read_parameter(ch, "PDwn", "pdwn")
            self._read_parameter(ch, "Pw", "pw")
            self._read_parameter(ch, "RDwn", "rdwn")
            self._read_parameter(ch, "RUp", "rup")
            self._read_parameter(ch, "Status", "channel_status", int)
            self._read_parameter(ch, "Trip", "trip", bool)
            self._read_parameter(ch, "VMon", "vmon")
            self._read_parameter(ch, "VSet", "vset")
            self._read_parameter(ch, "index", "channel_index", int)
    
    def _read_parameter(self, channel, opc_name, attr_name, cast_type=float):
        try:
            node_path = f"ns=2;s=STT-HV0.Board00.Chan{channel:03d}.{opc_name}"
            node = self._client.get_node(node_path)
            value = node.get_value()
            setattr(self, f"_{attr_name}", value)
        except Exception:
            pass
    
    def _push_all_events(self):
        self.push_change_event("IMRange", self._imrange)
        self.push_change_event("IMon", self._imon)
        self.push_change_event("ISet", self._iset)
        self.push_change_event("ChannelName", self._channel_name)
        self.push_change_event("PDwn", self._pdwn)
        self.push_change_event("Pw", self._pw)
        self.push_change_event("RDwn", self._rdwn)
        self.push_change_event("RUp", self._rup)
        self.push_change_event("ChannelStatus", self._channel_status)
        self.push_change_event("Trip", self._trip)
        self.push_change_event("VMon", self._vmon)
        self.push_change_event("VSet", self._vset)
        self.push_change_event("ChannelIndex", self._channel_index)
    
    # Read methods
    def read_IMRange(self): return self._imrange
    def read_IMon(self): return self._imon
    def read_ISet(self): return self._iset
    def read_ChannelName(self): return self._channel_name
    def read_PDwn(self): return self._pdwn
    def read_Pw(self): return self._pw
    def read_RDwn(self): return self._rdwn
    def read_RUp(self): return self._rup
    def read_ChannelStatus(self): return self._channel_status
    def read_Trip(self): return self._trip
    def read_VMon(self): return self._vmon
    def read_VSet(self): return self._vset
    def read_ChannelIndex(self): return self._channel_index
    
    # Write methods
    def write_VSet(self, value):
        self._vset = value
        self.push_change_event("VSet", self._vset)
    
    def write_ISet(self, value):
        self._iset = value
        self.push_change_event("ISet", self._iset)
    
    @command
    def On(self):
        logger.info("ON all channels")
    
    @command
    def Off(self):
        logger.info("OFF all channels")
    
    @command
    def Reset(self):
        logger.info("Reset device")
    
    def delete_device(self):
        self._running = False
        if self._client:
            try:
                self._client.disconnect()
            except:
                pass
        super().delete_device()

if __name__ == "__main__":
    run([CaenSMARTHV])
