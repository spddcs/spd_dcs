#!/bin/bash
# Install complete SPD DCS GUI

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_DIR="/opt/spddcs/SPD_DCS"

echo "Installing SPD DCS GUI..."

# Create installation directory
mkdir -p $INSTALL_DIR

# Copy all GUI files
cp -r $REPO_DIR/gui/* $INSTALL_DIR/

# Set proper permissions
chown -R spddcs:spddcs $INSTALL_DIR
chmod +x $INSTALL_DIR/*.py 2>/dev/null || true
chmod +x $INSTALL_DIR/*/*.py 2>/dev/null || true

# Create launcher script
cat > /home/spddcs/start_spd_gui.sh << 'LAUNCHER'
#!/bin/bash
source /home/spddcs/miniforge3/etc/profile.d/conda.sh
conda activate tango_env
export TANGO_HOST="na62dcs99.cern.ch:10000"
export QT_QPA_PLATFORM=xcb
cd /opt/spddcs/SPD_DCS
python3 master_merge_gui.py
LAUNCHER

chmod +x /home/spddcs/start_spd_gui.sh
chown spddcs:spddcs /home/spddcs/start_spd_gui.sh

echo "GUI installation complete!"
echo "Launch with: su - spddcs -c './start_spd_gui.sh'"
