#!/usr/bin/env bash
# command to run this file: bash bin/setup.sh 
# just make sure you are in the bank_demo directory when you run it
#it must be run from a GIT BASH terminal on Windows, or a Linux/Mac terminal. It will not work in a Windows command prompt.

set -e

echo "== BANK DEMO SETUP SCRIPT =="

cd backend

#create our .venv file if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

source .venv/Scripts/activate
pip install -r requirements.txt

#create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "Fill in real values in the backend/.env file before running the application."
    cp .env.example .env
fi

#Front end setup
cd ../frontend
echo "Setting up frontend..."
npm install

echo "Setup complete. You can now run the backend and frontend applications."