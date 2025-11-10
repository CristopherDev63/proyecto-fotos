#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the database initialization command
# We set the FLASK_APP environment variable for this command
export FLASK_APP=app.py
flask init-db

echo "Build script finished successfully."
