#!/usr/bin/env bash
set -e
set -o errexit
set -o pipefail
set -o nounset
cd /app/testapp
pytest
