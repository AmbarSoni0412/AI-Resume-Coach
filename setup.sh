#!/bin/bash
# Setup script for deployment

# Install system dependencies for pdf2image
if command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y poppler-utils
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    sudo yum install -y poppler-utils
elif command -v brew &> /dev/null; then
    # macOS
    brew install poppler
fi

echo "Setup completed!"
