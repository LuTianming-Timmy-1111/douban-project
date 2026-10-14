#!/bin/bash
set -e
cd "$(dirname "$0")"
set -a; source .env; set +a
python3 split_tables.py
