#!/bin/bash

# AI Trip Planner - Quick Start Script
# This script sets up and runs the Django backend

set -e

echo "================================"
echo "AI Trip Planner - Quick Start"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 is installed"

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r ../requirements.txt
echo "✓ Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "✓ .env file created"
fi

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate
echo "✓ Migrations complete"

# Ask if user wants to create superuser
echo ""
read -p "Do you want to create a superuser for admin access? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Run tests
echo ""
echo "Running tests..."
python manage.py test --verbosity=1
echo "✓ All tests passed"

# Start the server
echo ""
echo "================================"
echo "Starting development server..."
echo "================================"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Admin interface at: http://localhost:8000/admin"
echo ""
echo "Example API call:"
echo "  curl -X POST http://localhost:8000/api/trips/plan/ \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"message\": \"I want to visit Paris next month for 5 days\"}'"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
