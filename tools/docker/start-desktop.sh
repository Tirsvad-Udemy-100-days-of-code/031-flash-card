#!/usr/bin/env bash
# Start a virtual desktop for the checks. Source this file; it must not be run.
#
# Purpose:  give the checks a desktop of their own (a virtual X screen) so that
#           no window opens on the host (ADR-0005).
# Usage:    . tools/docker/start-desktop.sh
# Options:  none
# Env in:   DISPLAY (default :99), SCREEN_SIZE (default 1280x1024x24),
#           SHELL_WAIT_SECONDS (seconds to wait for GNOME Shell, default 25)
# Env out:  DISPLAY, DBUS_SESSION_BUS_ADDRESS, DESKTOP_KIND (gnome-shell or
#           mutter), DESKTOP_LOG_DIR (logs and the file desktop-kind)
# Needs:    bash 5, Xvfb, xdpyinfo, xprop, dbus-launch, gnome-shell, mutter
# Exit:     returns 0 when a desktop runs; 1 when no window manager came up
#
# Steps: Xvfb; a private D-Bus session; GNOME Shell first, and GNOME's window
# manager (mutter) when the shell does not come up in a container (it needs a
# login manager that a container does not have). The kind that runs is printed.

export DISPLAY="${DISPLAY:-:99}"
screen_size="${SCREEN_SIZE:-1280x1024x24}"
shell_wait_seconds="${SHELL_WAIT_SECONDS:-25}"
DESKTOP_LOG_DIR="$(mktemp -d)"
export DESKTOP_LOG_DIR
trap 'rm -rf "${DESKTOP_LOG_DIR}"' EXIT

if ! xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; then
  Xvfb "${DISPLAY}" -screen 0 "${screen_size}" -nolisten tcp >"${DESKTOP_LOG_DIR}/xvfb.log" 2>&1 &
  for _ in $(seq 1 40); do
    xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1 && break
    sleep 0.25
  done
fi

if [[ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]]; then
  eval "$(dbus-launch --sh-syntax)"
  export DBUS_SESSION_BUS_ADDRESS
fi

# Name of the window manager that owns the screen, or nothing.
wm_name() {
  local check
  check="$(xprop -root _NET_SUPPORTING_WM_CHECK 2>/dev/null | awk '{print $NF}')"
  [[ -n "${check}" ]] || return 0
  xprop -id "${check}" _NET_WM_NAME 2>/dev/null | sed -n 's/.*= "\(.*\)"/\1/p'
}

DESKTOP_KIND=""
if command -v gnome-shell >/dev/null 2>&1; then
  gnome-shell --x11 --sm-disable >"${DESKTOP_LOG_DIR}/gnome-shell.log" 2>&1 &
  gnome_pid=$!
  for _ in $(seq 1 $((shell_wait_seconds * 2))); do
    if kill -0 "${gnome_pid}" 2>/dev/null && wm_name | grep -qi "gnome"; then
      DESKTOP_KIND="gnome-shell"
      break
    fi
    sleep 0.5
  done
  if [[ -z "${DESKTOP_KIND}" ]]; then
    kill "${gnome_pid}" 2>/dev/null || true
  fi
fi
if [[ -z "${DESKTOP_KIND}" ]]; then
  mutter --x11 --sm-disable >"${DESKTOP_LOG_DIR}/mutter.log" 2>&1 &
  for _ in $(seq 1 40); do
    if wm_name | grep -qi "mutter"; then
      DESKTOP_KIND="mutter"
      break
    fi
    sleep 0.25
  done
fi
if [[ -z "${DESKTOP_KIND}" ]]; then
  echo "error: no window manager came up on ${DISPLAY}" >&2
  return 1
fi
export DESKTOP_KIND
echo "${DESKTOP_KIND}" >"${DESKTOP_LOG_DIR}/desktop-kind"
echo "desktop: ${DESKTOP_KIND} on ${DISPLAY}"
