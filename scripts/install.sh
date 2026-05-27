#!/bin/bash
# Main installation script for SPD DCS

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Installing SPD DCS from repository..."

# Install system dependencies
bash ${REPO_DIR}/scripts/install_dependencies.sh

# Setup database
bash ${REPO_DIR}/database/migrate.sh

# Setup device server
bash ${REPO_DIR}/scripts/setup_device_server.sh

# Setup GUI
bash ${REPO_DIR}/scripts/setup_gui.sh

echo "Installation complete!"
