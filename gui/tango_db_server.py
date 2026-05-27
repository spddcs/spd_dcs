#!/usr/bin/env python3
"""
TANGO Database Server - Python Implementation
"""

import os
import sys
import sqlite3
import time

os.environ['TANGO_HOST'] = 'na62dcs99.cern.ch:10000'

import tango
from tango.server import Device, run
from tango import DevState

DB_PATH = "/home/shkar/SPD_DCS/tango_database.db"

class TangoDB(Device):
    def init_device(self):
        super().init_device()
        
        # Initialize SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device (
                name TEXT PRIMARY KEY,
                class TEXT,
                server TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_property (
                device_name TEXT,
                property_name TEXT,
                property_value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self.set_state(DevState.ON)
        print("=" * 60)
        print("TANGO Database Server Running")
        print(f"TANGO_HOST: {os.environ.get('TANGO_HOST')}")
        print(f"Database: {DB_PATH}")
        print("=" * 60)

if __name__ == "__main__":
    import sys
    instance_name = sys.argv[1] if len(sys.argv) > 1 else "1"
    print("Starting TANGO Database Server...")
    print(f"Instance: {instance_name}")
    run([TangoDB])
