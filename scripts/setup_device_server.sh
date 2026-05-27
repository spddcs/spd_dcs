#!/bin/bash
# Setup device server as systemd service

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Copy device server
cp ${REPO_DIR}/device_server/CaenSMARTHV.py /opt/spddcs/SPD_DCS/device_server/

# Create service file
cat > /etc/systemd/system/tango-caen-device.service << 'SERVICE'
[Unit]
Description=TANGO CAEN SMARTHV Device Server
After=tango-db.service network.target

[Service]
Type=simple
User=spddcs
Environment="TANGO_HOST=na62dcs99.cern.ch:10000"
WorkingDirectory=/opt/spddcs/SPD_DCS/device_server
ExecStart=/home/spddcs/miniforge3/envs/tango_env/bin/python CaenSMARTHV.py StrawTrackerCaenHV_0
Restart=on-failure

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable tango-caen-device
systemctl start tango-caen-device
