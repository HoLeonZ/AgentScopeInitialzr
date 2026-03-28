#!/bin/bash
# Setup script for AgentScope project

echo "🚀 Setting up AgentScope project..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file from example
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys"
fi

echo "✅ Setup complete! Activate your environment with: source venv/bin/activate"
