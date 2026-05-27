#!/bin/bash
# Main installation script for SPD DCS

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "=========================================="
echo "SPD DCS Installation"
echo "=========================================="

# Install system dependencies
echo "1. Installing system dependencies..."
bash ${REPO_DIR}/scripts/install_dependencies.sh

# Setup database
echo "2. Setting up database..."
bash ${REPO_DIR}/database/migrate.sh

# Setup device server
echo "3. Setting up device server..."
bash ${REPO_DIR}/scripts/setup_device_server.sh

# Setup GUI
echo "4. Setting up GUI..."
bash ${REPO_DIR}/scripts/install_gui.sh

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start device server: systemctl start tango-caen-device"
echo "  2. Launch GUI: su - spddcs -c './start_spd_gui.sh'"
echo ""
