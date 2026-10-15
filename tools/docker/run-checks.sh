#!/usr/bin/env bash
# Run the linters and the whole test suite (with the e2e tests of the real Tk
# window) on the virtual desktop.
#
# Purpose:  the quality gate without a desktop of the host (ADR-0005).
# Usage:    run-checks.sh        (from the repository root, via in-container.sh)
# Env:      see start-desktop.sh
# Needs:    ruff, mypy, import-linter, pytest (the dev extra), the desktop
# Exit:     0 only when every check passes
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."
# shellcheck source=tools/docker/start-desktop.sh
. tools/docker/start-desktop.sh

python -m ruff check src tests tools
python -m ruff format --check src tests tools
python -m mypy
lint-imports
python -m pytest -ra -q
echo "checks passed on desktop: ${DESKTOP_KIND}"
