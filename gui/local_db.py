#!/usr/bin/env python3
"""
Simple TANGO Database Server - SQLite backend
Works without database dependencies
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
        print("=" * 50)
        print("TANGO Database Server Running")
        print(f"Database: {DB_PATH}")
        print(f"TANGO_HOST: {os.environ.get('TANGO_HOST')}")
        print("=" * 50)

if __name__ == "__main__":
    # Remove any existing -nodb flag from sys.argv
    sys.argv = [sys.argv[0]]
    run([TangoDB])
