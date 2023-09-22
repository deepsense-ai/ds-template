#!/bin/bash

if [ ! -d venv ]; then
    python3 -m venv venv
    . venv/bin/activate
    pip install --upgrade pip
    pip install --quiet wheel==0.37.1
    pip install --quiet -r requirements-dev.txt
fi

. venv/bin/activate