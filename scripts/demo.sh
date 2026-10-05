#!/usr/bin/env bash
set -e

echo "=== AFMAS Demo ==="
echo "Installing package..."
pip install -e . -q

echo ""
echo "Running Sovereign Safety Score on gpt2 (hellaswag, limit=5)..."
afmas evaluate \
  --model hf \
  --model_args pretrained=gpt2 \
  --tasks hellaswag \
  --limit 5 \
  --device cpu \
  --batch_size 1 \
  --output_dir results/demo

echo ""
echo "Demo complete. Check results/demo/ for JSON, CSV and HTML reports."
