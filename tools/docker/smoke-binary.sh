#!/usr/bin/env bash
# Build the Linux binary with PyInstaller and smoke-test it, and the source
# program, on the virtual desktop. The smoke test starts the program, finds the
# window, presses the known button with the virtual mouse of the desktop and
# checks the progress file.
#
# Purpose:  the "does the packaged program work" check without a desktop of the
#           host (ADR-0005, RC-072).
# Usage:    smoke-binary.sh [repeat-count]      (default 5)
# Env:      see start-desktop.sh
# Needs:    pyinstaller (the build extra), binutils, xdotool, the desktop
# Exit:     0 only when every run of both programs passes; 2 on a bad count
set -euo pipefail

repeat="${1:-5}"
if ! [[ "${repeat}" =~ ^[1-9][0-9]*$ ]]; then
  echo "error: repeat-count must be a positive integer, got '${repeat}'" >&2
  echo "usage: smoke-binary.sh [repeat-count]" >&2
  exit 2
fi

cd "$(dirname "${BASH_SOURCE[0]}")/../.."
# shellcheck source=tools/docker/start-desktop.sh
. tools/docker/start-desktop.sh

python tools/build_executable.py --clean
test -x dist/flash-card
echo "== binary"
python tools/docker/smoke_driver.py --repeat "${repeat}" --command dist/flash-card
echo "== source"
python tools/docker/smoke_driver.py --repeat "${repeat}" --command python -m flash_card
