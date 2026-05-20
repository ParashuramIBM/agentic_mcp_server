#!/bin/bash

echo "Setting up Simple MCP CI/CD Server..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Please edit .env file and add your GITHUB_TOKEN"
fi

echo "Setup complete! Run 'python -m src.server' to start"