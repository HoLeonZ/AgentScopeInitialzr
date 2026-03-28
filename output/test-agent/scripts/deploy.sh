#!/bin/bash
# Deploy script for AgentScope project

echo "🚀 Deploying AgentScope project..."

# Run tests
echo "Running tests..."
pytest tests/ -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed. Aborting deployment."
    exit 1
fi

echo "✅ Deployment ready!"
