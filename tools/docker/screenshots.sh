#!/usr/bin/env bash
# Take the screenshots (level screen, card front, card back, window with the
# menu bar) on the virtual desktop.
#
# Purpose:  screenshots without a desktop of the host (ADR-0005).
# Usage:    screenshots.sh [output-folder]      (default /out)
# Env:      see start-desktop.sh
# Needs:    Pillow (the tools extra), the desktop
# Exit:     0 when the four files were written; else the tool's exit code
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."
# shellcheck source=tools/docker/start-desktop.sh
. tools/docker/start-desktop.sh

out="${1:-/out}"
mkdir -p "${out}"
python tools/capture_screenshots.py --output-dir "${out}"
ls -l "${out}"
