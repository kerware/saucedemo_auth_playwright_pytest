#!/usr/bin/env bash
set -euo pipefail
pytest --browser chromium --browser firefox --browser webkit
