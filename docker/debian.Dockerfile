# Debian based image for the flash card checks (ADR-0005).
#
# Build (from the repository root):
#   docker build -f docker/debian.Dockerfile -t flash-card-debian .
# Run the linters and the tests on a virtual desktop:
#   docker run --rm -v "$PWD:/app" flash-card-debian
#
# The base image is the official Python image (Debian bookworm), because the
# program needs Python 3.13. The desktop is a virtual X screen (Xvfb) with
# GNOME Shell when it can start in a container, else GNOME's window manager.
FROM python:3.13-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DISPLAY=:99

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      xvfb xauth x11-utils x11-xserver-utils xdotool dbus dbus-x11 \
      procps ca-certificates \
      libgl1-mesa-dri libegl1 libgles2 \
      mutter gnome-session gnome-shell gnome-settings-daemon \
      adwaita-icon-theme gsettings-desktop-schemas \
      tk fonts-liberation fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

# PyInstaller on Linux needs objdump (binutils).
RUN apt-get update \
 && apt-get install -y --no-install-recommends binutils \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash flash
WORKDIR /app

# Dependencies first, so a change of the sources does not rebuild this layer.
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --upgrade pip \
 && python -m pip install -e ".[dev,speech,tools,build]" \
 && chown -R flash:flash /app

USER flash
ENV PATH="/app/tools/docker:${PATH}"
CMD ["bash", "tools/docker/run-checks.sh"]
