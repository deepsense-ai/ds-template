#!/bin/bash

if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    apt-get update && apt-get install -y curl
    curl -fsSL https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "Syncing venv..."
uv sync

echo "Activating venv..."
source .venv/bin/activate
