#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH="$PWD/src" python -c "from doc_vlm_qa.evaluation.runner import run_eval; print(run_eval())"
