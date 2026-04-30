#!/bin/bash
# Daily update script for YKZZ Quant
# Usage: ./scripts/daily_update.sh

set -e

echo "=== YKZZ Quant Daily Update ==="
echo "Start time: $(date)"

# 1. Data collection
echo ""
echo "Step 1: Data Collection"
python -m app.data.collect

# 2. Factor calculation
echo ""
echo "Step 2: Factor Calculation"
python -m app.factor.calculate

# 3. Strategy execution
echo ""
echo "Step 3: Strategy Execution"
python -m app.strategy.run --strategy double_low --top-n 10
python -m app.strategy.run --strategy low_premium --top-n 10

echo ""
echo "=== Daily Update Complete ==="
echo "End time: $(date)"
