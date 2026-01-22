#!/bin/bash

# PVB WhatsApp Chatbot - Local Setup Script
# Run this after configuring your .env file

echo "=========================================="
echo "PVB WhatsApp Chatbot - Local Setup"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "ERROR: .env file not found!"
    echo ""
    echo "Please create .env file first:"
    echo "  cp .env.example .env"
    echo "  Then edit .env with your Meta credentials"
    echo ""
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create SQLite database
echo ""
echo "Database will be created automatically on first run"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the chatbot server:"
echo "   source venv/bin/activate"
echo "   python app/main.py"
echo ""
echo "2. In a NEW terminal, start ngrok:"
echo "   ngrok http 5000"
echo ""
echo "3. Copy the ngrok HTTPS URL (e.g., https://abc123.ngrok.io)"
echo ""
echo "4. Go to Meta Developer Console:"
echo "   WhatsApp > Configuration > Webhook"
echo "   - Callback URL: YOUR_NGROK_URL/webhook"
echo "   - Verify Token: (same as META_VERIFY_TOKEN in .env)"
echo ""
echo "5. Subscribe to webhook fields: messages"
echo ""
echo "6. Test by sending a WhatsApp message to your test number!"
echo ""
