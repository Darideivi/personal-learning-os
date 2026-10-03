#!/usr/bin/env bash
# setup-tools.sh - install the dev tools for LearnHouse inside WSL Ubuntu on DavidLab.
# Run once, BEFORE PHASE0_PLAN goal 1:   bash scripts/davidlab/setup-tools.sh
# Safe to re-run: anything already installed is skipped. Needs no sudo.

set -euo pipefail

BUN_VERSION="1.4.2"   # same as upstream .bun-version
NODE_MAJOR="24"

step() { printf '\n==> %s\n' "$1"; }
fail() { printf 'ERROR: %s\n' "$1" >&2; exit 1; }

# ---- 1. Checks -------------------------------------------------------------
step "Checking environment"

grep -qi microsoft /proc/version 2>/dev/null \
  || fail "This does not look like WSL. Run this inside Ubuntu on DavidLab."
echo "WSL: ok"

missing=""
for pkg in git curl build-essential; do
  dpkg -s "$pkg" >/dev/null 2>&1 || missing="$missing $pkg"
done
if [ -n "$missing" ]; then
  echo "Missing packages:$missing" >&2
  echo "Run this yourself (it needs your sudo password), then re-run this script:" >&2
  echo "  sudo apt update && sudo apt install -y git curl build-essential" >&2
  exit 1
fi
echo "git, curl, build-essential: ok"

DOCKER_OK=1
if ! docker info >/dev/null 2>&1; then
  DOCKER_OK=0
  echo "WARNING: Docker is not reachable from WSL (not needed for these tools, but needed to run LearnHouse)." >&2
  echo "Fix: start Docker Desktop, then Settings > Resources > WSL integration," >&2
  echo "enable 'Ubuntu', click 'Apply & restart'." >&2
else
  echo "docker: ok"
fi

# ---- 2. Node via nvm -------------------------------------------------------
step "Node $NODE_MAJOR via nvm"
export NVM_DIR="$HOME/.nvm"
if [ ! -s "$NVM_DIR/nvm.sh" ]; then
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
fi
# nvm.sh is not written for 'set -u', so relax it while loading and using nvm.
set +u
. "$NVM_DIR/nvm.sh"
if node -v 2>/dev/null | grep -q "^v$NODE_MAJOR\."; then
  echo "Node $(node -v) already installed, skipping"
else
  nvm install "$NODE_MAJOR"
fi
nvm alias default "$NODE_MAJOR" >/dev/null
set -u

# ---- 3. bun (pinned) -------------------------------------------------------
step "bun $BUN_VERSION"
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
if [ "$(bun --version 2>/dev/null || true)" = "$BUN_VERSION" ]; then
  echo "bun $BUN_VERSION already installed, skipping"
else
  # bun's installer needs unzip; fail early with a clear message.
  command -v unzip >/dev/null || fail "unzip is missing: sudo apt install -y unzip"
  curl -fsSL https://bun.sh/install | bash -s "bun-v$BUN_VERSION"
fi

# ---- 4. uv -----------------------------------------------------------------
step "uv"
export PATH="$HOME/.local/bin:$PATH"
if command -v uv >/dev/null; then
  echo "uv $(uv --version) already installed, skipping"
else
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# ---- 5. graphify -----------------------------------------------------------
step "graphify (package: graphifyy)"
if uv tool list 2>/dev/null | grep -q '^graphifyy'; then
  echo "graphifyy already installed, skipping"
else
  uv tool install graphifyy
fi

# ---- 6. Summary ------------------------------------------------------------
step "Installed versions"
echo "node:    $(node -v 2>/dev/null || echo missing)"
echo "npm:     $(npm -v 2>/dev/null || echo missing)"
echo "bun:     $(bun --version 2>/dev/null || echo missing)"
echo "uv:      $(uv --version 2>/dev/null || echo missing)"
if command -v graphify >/dev/null; then
  echo "graphify: $(graphify --version 2>/dev/null || echo installed)"
else
  echo "graphify: not on PATH (open a new shell, or check 'uv tool list')"
fi
if [ "$DOCKER_OK" = 1 ]; then
  echo "docker:  $(docker --version)"
  echo "compose: $(docker compose version)"
else
  echo "docker:  NOT reachable from WSL (enable WSL integration)"
fi

echo
echo "Done. New shells pick up nvm/bun/uv automatically; in THIS shell run:"
echo "  source ~/.bashrc"
