#!/bin/bash

# Start Jupyter notebook with the virtual environment
echo "Starting Jupyter notebook with KCG LLM environment..."

# Activate virtual environment
source venv/bin/activate

# Change to retail_data directory
cd retail_data

# Start Jupyter notebook
echo "Jupyter will be available at: http://localhost:8888"
echo "Make sure to select 'KCG LLM Environment' as the kernel"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

jupyter notebook --no-browser --port=8888 