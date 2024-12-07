#!/bin/bash
if [ ! -e /usr/local/bin/template-builder ]; then
    echo "Installing template-builder..."
    sudo cp "$0" /usr/local/bin/template-builder
    sudo chmod +x /usr/local/bin/template-builder
    mkdir -p ~/.template-builder
    echo "Copying template files..."
    cp -r ./* ~/.template-builder/
    echo "template-builder installed successfully"
    exit 0
fi

if [ ! -e ~/.template-builder/ ]; then
    echo "Error: template-builder directory not found"
    exit 1
fi

if [ -f "/usr/local/bin/template-builder" ]; then
    cp -r ~/.template-builder/* .
    for arg in "$@"; do
    if [ "$arg" == "--start" ]; then
        docker-compose build --no-cache && docker-compose up -d
        exit 0
    fi
    done
else
    echo "Error: No se encontró el archivo template-builder en /usr/local/bin/template-builder"
    exit 1
fi