#!/usr/bin/env bash
# Run one of the check scripts on a COPY of the repository, so that the
# mounted repository stays untouched (no build/, dist/ or caches in it).
#
# Purpose:  isolate the checks from the host (ADR-0005).
# Usage:    in-container.sh <script> [args...]
#             in-container.sh run-checks.sh
#             in-container.sh screenshots.sh /out
#             in-container.sh smoke-binary.sh 5
# Env:      REPO_DIR (default /repo, mounted read-only), WORK_DIR (default
#           $HOME/work; it is deleted and recreated, so it must be a folder of
#           the container, never the mounted repository)
# Needs:    bash 5, tar
# Exit:     2 on bad arguments or a missing script; else the exit code of the
#           script that was run
set -euo pipefail

repo="${REPO_DIR:-/repo}"
work="${WORK_DIR:-${HOME}/work}"

usage() {
  echo "usage: in-container.sh <script> [args...]" >&2
  echo "scripts: run-checks.sh screenshots.sh smoke-binary.sh" >&2
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi
script="$1"
shift
if [[ ! -f "${repo}/tools/docker/${script}" ]]; then
  echo "error: no such script: tools/docker/${script}" >&2
  usage
  exit 2
fi
if [[ "${work}" == "${repo}" || "${work}" == "/" ]]; then
  echo "error: WORK_DIR must not be the repository or /" >&2
  exit 2
fi

rm -rf "${work}"
mkdir -p "${work}"
tar -C "${repo}" \
  --exclude=.git --exclude=.venv --exclude=build --exclude=dist \
  --exclude=docs/doxygen --exclude=.codex --exclude='__pycache__' \
  -cf - . | tar -C "${work}" -xf -
cd "${work}"
export PYTHONPATH="${work}/src"
exec bash "tools/docker/${script}" "$@"
