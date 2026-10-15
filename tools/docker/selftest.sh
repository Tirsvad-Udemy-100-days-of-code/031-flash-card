#!/usr/bin/env bash
# Tests of the check scripts themselves: argument errors and refusals. The
# success paths are the runs of run-checks.sh, screenshots.sh and
# smoke-binary.sh.
#
# Purpose:  QC-SH-001 criterion 11 (success, failure and bypass paths).
# Usage:    selftest.sh          (from the repository root)
# Needs:    bash 5
# Exit:     0 when every case behaves as stated; 1 when one differs
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."
fail=0

expect_exit() {
  local expected="$1" label="$2"
  shift 2
  local code=0
  "$@" >/dev/null 2>&1 || code=$?
  if [[ "${code}" -ne "${expected}" ]]; then
    echo "FAIL: ${label}: exit ${code}, expected ${expected}" >&2
    fail=1
  else
    echo "ok: ${label}"
  fi
}

expect_exit 2 "in-container without arguments" bash tools/docker/in-container.sh
expect_exit 2 "in-container with an unknown script" bash tools/docker/in-container.sh nope.sh
expect_exit 2 "in-container refuses the repository as work folder" \
  env REPO_DIR="$(pwd)" WORK_DIR="$(pwd)" bash tools/docker/in-container.sh run-checks.sh
expect_exit 2 "smoke-binary with a text count" bash tools/docker/smoke-binary.sh many
expect_exit 2 "smoke-binary with zero" bash tools/docker/smoke-binary.sh 0
for script in start-desktop run-checks screenshots smoke-binary in-container selftest; do
  expect_exit 0 "bash -n ${script}.sh" bash -n "tools/docker/${script}.sh"
done
exit "${fail}"
