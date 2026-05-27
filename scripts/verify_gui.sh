#!/bin/bash
# Verify GUI installation

echo "Verifying SPD DCS GUI installation..."
echo "=========================================="

# Check if all detector directories exist
cd /opt/spddcs/SPD_DCS

detectors=("SPD" "BBC" "BBC_MCP" "Magnet" "MicroMegas" "RangeSystem" "RangeSystemEndCap" "StrawTracker" "StrawTrackerEndCap" "ZeroDegreeCalorimeter")

missing=0
for detector in "${detectors[@]}"; do
    if [ -d "$detector" ]; then
        echo "✓ $detector"
    else
        echo "✗ $detector - MISSING"
        missing=$((missing+1))
    fi
done

# Check main files
main_files=("master_merge_gui.py" "base_panel.py" "master_node_manager.py")
for file in "${main_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file - MISSING"
        missing=$((missing+1))
    fi
done

echo ""
if [ $missing -eq 0 ]; then
    echo "✅ GUI verification passed!"
else
    echo "⚠️ GUI verification failed: $missing components missing"
fi
