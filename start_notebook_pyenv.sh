#!/bin/bash

# Start Jupyter notebook with pyenv Python 3.10.13
echo "Starting Jupyter notebook with pyenv Python 3.10.13..."

# Change to retail_data directory
cd retail_data

# Start Jupyter notebook using pyenv Python
echo "Jupyter will be available at: http://localhost:8888"
echo "Make sure to select 'Python 3.10.13 (pyenv)' as the kernel"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

/Users/ileene/.pyenv/versions/3.10.13/bin/jupyter notebook --no-browser --port=8888 