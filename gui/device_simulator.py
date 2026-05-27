#!/usr/bin/env python3
"""
CAEN HV Device Simulator - HTTP API
No TANGO required - works immediately
"""

import json
import random
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HVDevice:
    def __init__(self):
        self.channels = 8
        self.vmon = [0.0] * self.channels
        self.imon = [0.0] * self.channels
        self.vset = [100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0]
        self.iset = [0.05] * self.channels
        self.temperature = 25.0
        self.status = "ON"
        self.running = True
        
        # Start simulation thread
        self.thread = threading.Thread(target=self._simulate, daemon=True)
        self.thread.start()
    
    def _simulate(self):
        while self.running:
            for ch in range(self.channels):
                diff = self.vset[ch] - self.vmon[ch]
                if abs(diff) > 1:
                    self.vmon[ch] += diff * 0.1
                self.vmon[ch] += random.uniform(-0.5, 0.5)
                self.vmon[ch] = max(0, min(self.vmon[ch], 1000))
                self.imon[ch] = (self.vmon[ch] / 1000.0) * self.iset[ch]
                self.imon[ch] += random.uniform(-0.0005, 0.0005)
                self.imon[ch] = max(0, min(self.imon[ch], 0.1))
            self.temperature = 25.0 + random.uniform(-2, 2)
            time.sleep(1)
    
    def get_status(self):
        return {
            "device": "CAEN Smart HV",
            "status": self.status,
            "temperature": round(self.temperature, 1),
            "channels": [
                {
                    "channel": ch,
                    "vmon": round(self.vmon[ch], 2),
                    "imon": round(self.imon[ch], 4),
                    "vset": round(self.vset[ch], 2),
                    "iset": round(self.iset[ch], 4)
                } for ch in range(self.channels)
            ]
        }
    
    def set_voltage(self, channel, voltage):
        if 0 <= channel < self.channels:
            self.vset[channel] = max(0, min(voltage, 1000))
            return True
        return False
    
    def set_current(self, channel, current):
        if 0 <= channel < self.channels:
            self.iset[channel] = max(0, min(current, 0.1))
            return True
        return False
    
    def turn_on(self):
        self.status = "RUNNING"
        return True
    
    def turn_off(self):
        self.status = "OFF"
        for ch in range(self.channels):
            self.vmon[ch] = 0
        return True
    
    def reset(self):
        for ch in range(self.channels):
            self.vmon[ch] = 0
            self.imon[ch] = 0
        self.status = "ON"
        return True

device = HVDevice()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(device.get_status()).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length else b''
        
        try:
            data = json.loads(post_data) if post_data else {}
        except:
            data = {}
        
        if self.path == '/on':
            device.turn_on()
            self.send_response(200)
            self.end_headers()
        elif self.path == '/off':
            device.turn_off()
            self.send_response(200)
            self.end_headers()
        elif self.path == '/reset':
            device.reset()
            self.send_response(200)
            self.end_headers()
        elif self.path == '/set_voltage':
            channel = data.get('channel', 0)
            voltage = data.get('voltage', 0)
            device.set_voltage(channel, voltage)
            self.send_response(200)
            self.end_headers()
        elif self.path == '/set_current':
            channel = data.get('channel', 0)
            current = data.get('current', 0)
            device.set_current(channel, current)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Silence logging

if __name__ == "__main__":
    port = 8080
    server = HTTPServer(('', port), Handler)
    print("=" * 60)
    print("CAEN HV Device Simulator")
    print("=" * 60)
    print(f"API: http://localhost:{port}")
    print(f"Status: http://localhost:{port}/status")
    print("=" * 60)
    print("Commands:")
    print("  POST /on - Turn on all channels")
    print("  POST /off - Turn off all channels")
    print("  POST /reset - Reset device")
    print("  POST /set_voltage - Set voltage {\"channel\":0,\"voltage\":500}")
    print("  POST /set_current - Set current {\"channel\":0,\"current\":0.05}")
    print("=" * 60)
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
