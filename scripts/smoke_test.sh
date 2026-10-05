#!/usr/bin/env bash
set -e
echo "AFMAS smoke test starting..."
pip install -e . -q
afmas --help > /dev/null
afmas list-tasks > /dev/null
afmas evaluate \
  --model hf \
  --model_args pretrained=gpt2 \
  --tasks hellaswag \
  --limit 2 \
  --device cpu \
  --batch_size 1 \
  --output_dir results/smoke_test
echo "SMOKE TEST PASSED"
