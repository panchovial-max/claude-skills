#!/bin/bash
# Quick Reference Commands for PVB WhatsApp Chatbot

# ============================================================================
# DEVELOPMENT SETUP
# ============================================================================

# First time setup
setup_dev() {
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    echo "✅ Setup complete. Edit .env with your credentials"
}

# Run locally
run_dev() {
    source venv/bin/activate
    python app/main.py
}

# Run with ngrok (expose to internet for testing)
run_with_ngrok() {
    # In terminal 1:
    ngrok http 5000
    
    # Copy the HTTPS URL and use it as webhook URL in Meta Developers
    # Example: https://xyz123.ngrok.io/webhook
}

# ============================================================================
# DATABASE MANAGEMENT
# ============================================================================

# Check database (SQLite)
db_check() {
    sqlite3 chatbot.db "SELECT COUNT(*) FROM leads;"
}

# View all leads
db_leads() {
    sqlite3 chatbot.db "SELECT id, phone_number, name, service_category, lead_quality, status FROM leads;"
}

# View conversations for specific lead
db_conversations() {
    LEAD_ID=$1
    sqlite3 chatbot.db "SELECT sender, message_text, flow_state, created_at FROM conversations WHERE lead_id=$LEAD_ID ORDER BY created_at;"
}

# Backup database
db_backup() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    cp chatbot.db "backups/chatbot_$TIMESTAMP.db"
    echo "✅ Backed up to backups/chatbot_$TIMESTAMP.db"
}

# ============================================================================
# TESTING
# ============================================================================

# Test webhook health
test_health() {
    curl http://localhost:5000/health
}

# Test API - get all leads
test_get_leads() {
    curl http://localhost:5000/api/leads
}

# Test API - get single lead
test_get_lead() {
    LEAD_ID=$1
    curl http://localhost:5000/api/leads/$LEAD_ID
}

# Simulate incoming WhatsApp message
test_message() {
    curl -X POST http://localhost:5000/webhook \
    -H "Content-Type: application/json" \
    -d '{
        "object": "whatsapp_business_account",
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "56912345678",
                        "id": "test123",
                        "timestamp": "'$(date +%s)'",
                        "type": "text",
                        "text": {"body": "1"}
                    }]
                }
            }]
        }]
    }'
}

# ============================================================================
# DEPLOYMENT
# ============================================================================

# Deploy to Heroku
deploy_heroku() {
    git push heroku main
    heroku logs --tail
}

# Deploy to Railway
deploy_railway() {
    git push origin main  # Railway auto-detects and deploys
}

# View logs (Heroku)
logs_heroku() {
    heroku logs --tail
}

# Check deployed app health
test_production() {
    DOMAIN=$1  # Example: pvb-chatbot.herokuapp.com
    curl https://$DOMAIN/health
}

# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

# Print all env vars needed
env_template() {
    echo "
META_BUSINESS_ACCOUNT_ID=
META_PHONE_NUMBER_ID=
META_VERIFY_TOKEN=
META_ACCESS_TOKEN=
META_API_VERSION=v18.0

DATABASE_URL=sqlite:///chatbot.db

ADMIN_PHONE=+56912345678
ADMIN_EMAIL=pancho@pvbestudio.com

N8N_WEBHOOK_URL=https://...
"
}

# Set env vars in Heroku
set_env_heroku() {
    heroku config:set META_BUSINESS_ACCOUNT_ID=$1
    heroku config:set META_PHONE_NUMBER_ID=$2
    heroku config:set META_VERIFY_TOKEN=$3
    heroku config:set META_ACCESS_TOKEN=$4
    heroku config:set ADMIN_PHONE=$5
    heroku config:set ADMIN_EMAIL=$6
}

# ============================================================================
# MONITORING & DEBUGGING
# ============================================================================

# Show last 50 lines of error log
logs() {
    tail -50 /var/log/chatbot.log
}

# Count total leads
count_leads() {
    sqlite3 chatbot.db "SELECT COUNT(*) as total_leads FROM leads;"
}

# Count qualified leads
count_qualified() {
    sqlite3 chatbot.db "SELECT COUNT(*) FROM leads WHERE status='qualified';"
}

# Find hot leads
find_hot_leads() {
    sqlite3 chatbot.db "SELECT phone_number, name, service_category FROM leads WHERE lead_quality='hot' ORDER BY created_at DESC;"
}

# Get conversion rate
conversion_rate() {
    TOTAL=$(sqlite3 chatbot.db "SELECT COUNT(*) FROM leads;")
    QUALIFIED=$(sqlite3 chatbot.db "SELECT COUNT(*) FROM leads WHERE status='qualified';")
    echo "Total: $TOTAL, Qualified: $QUALIFIED, Rate: $(echo "scale=2; $QUALIFIED*100/$TOTAL" | bc)%"
}

# ============================================================================
# CLEANUP & MAINTENANCE
# ============================================================================

# Remove old leads (older than 30 days)
cleanup_old_leads() {
    sqlite3 chatbot.db "DELETE FROM conversations WHERE lead_id IN (SELECT id FROM leads WHERE created_at < date('now', '-30 days'));"
    sqlite3 chatbot.db "DELETE FROM leads WHERE created_at < date('now', '-30 days');"
    echo "✅ Deleted leads older than 30 days"
}

# Reset database (WARNING: deletes everything)
reset_db() {
    read -p "Are you sure? This deletes everything! (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f chatbot.db
        python app/main.py  # Will recreate empty DB
        echo "✅ Database reset"
    fi
}

# ============================================================================
# USAGE
# ============================================================================

# Show help
help() {
    echo "PVB WhatsApp Chatbot - Quick Commands"
    echo ""
    echo "DEVELOPMENT:"
    echo "  setup_dev          - First time setup"
    echo "  run_dev            - Run app locally"
    echo ""
    echo "TESTING:"
    echo "  test_health        - Test if app is running"
    echo "  test_get_leads     - Get all leads"
    echo "  test_message       - Simulate WhatsApp message"
    echo ""
    echo "DATABASE:"
    echo "  count_leads        - Total leads count"
    echo "  find_hot_leads     - Show HOT leads only"
    echo "  conversion_rate    - Show conversion %"
    echo ""
    echo "DEPLOYMENT:"
    echo "  deploy_heroku      - Deploy to Heroku"
    echo "  logs_heroku        - View Heroku logs"
    echo ""
    echo "Run 'source dev-commands.sh' to load these functions into your shell"
}

# Load commands
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    help
else
    echo "✅ Loaded PVB chatbot commands. Type 'help' for list."
fi
