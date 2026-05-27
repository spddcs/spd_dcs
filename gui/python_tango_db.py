#!/usr/bin/env python3
"""
Python TANGO Database Server - No external dependencies
"""

import os
import sys
import sqlite3
import threading
import time

os.environ['TANGO_HOST'] = 'localhost:10000'

import tango
from tango.server import Device, run
from tango import DevState

DB_PATH = os.path.expanduser("~/tango_database.db")

class PyTangoDB(Device):
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
        print("=" * 50)
        print("TANGO Database Server (Python/SQLite)")
        print("=" * 50)
        print(f"Database: {DB_PATH}")
        print(f"TANGO_HOST: {os.environ.get('TANGO_HOST')}")
        print("=" * 50)

if __name__ == "__main__":
    run([PyTangoDB], db=False)
