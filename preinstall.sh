#!/bin/bash

if [[ ! -z "$famhawiteinfosysReal_ACCESS_TOKEN" ]]; then
    echo "Downloading famhawiteinfosysReal_kit..."
    poetry run pip install git+https://${famhawiteinfosysReal_ACCESS_TOKEN}@github.com/famhawiteinfosysReal/famhawiteinfosysReal_kit@v0.1.3
fi
