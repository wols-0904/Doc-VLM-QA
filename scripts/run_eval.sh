#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -c "from src.doc_vlm_qa.evaluation.runner import run_eval; print(run_eval())"
