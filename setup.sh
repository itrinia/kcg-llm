#!/bin/bash

# Setup script for KCG LLM Chatbot Project
echo "Setting up virtual environment for KCG LLM Chatbot..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Register the kernel for Jupyter
echo "Registering Jupyter kernel..."
python -m ipykernel install --user --name=kcg-llm --display-name="KCG LLM Chatbot"

echo "Setup complete! To activate the environment, run:"
echo "source venv/bin/activate"
echo ""
echo "To start Jupyter notebook:"
echo "jupyter notebook"
echo ""
echo "To test Ollama connection:"
echo "python -c \"import ollama; print('Ollama available:', ollama.list())\"" 