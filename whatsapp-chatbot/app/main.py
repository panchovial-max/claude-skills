"""
PVB WhatsApp Chatbot - Main Flask Application
Handles webhook from Meta, processes messages, routes conversations
"""

import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

from app.models.database import db, Lead, Conversation
from app.utils.meta_api import MetaWhatsAppAPI
from app.utils.twilio_api import TwilioWhatsAppAPI, get_whatsapp_api
from app.flows.conversation_engine import route_flow, DataCapture, MarketingFlow, PhotographyFlow
from app.utils.lead_router import LeadRouter

load_dotenv()

app = Flask(__name__)

# Database configuration - use /tmp for SQLite on Railway (writable directory)
database_url = os.getenv('DATABASE_URL', 'sqlite:////tmp/chatbot.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize WhatsApp API - auto-selects Twilio if configured, otherwise Meta
whatsapp_api = get_whatsapp_api()
meta_api = whatsapp_api  # Keep backward compatibility

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

with app.app_context():
    try:
        db.create_all()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")

# ============================================================================
# WEBHOOK VERIFICATION (GET request from Meta)
# ============================================================================

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """
    Webhook verification endpoint for Meta WhatsApp Cloud API
    Meta sends a challenge token to verify our webhook is real
    """
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if verify_token == os.getenv('META_VERIFY_TOKEN'):
        return challenge, 200
    else:
        return 'Invalid verification token', 403

# ============================================================================
# TWILIO WEBHOOK (POST request from Twilio)
# ============================================================================

@app.route('/webhook/twilio', methods=['POST'])
def twilio_webhook():
    """
    Webhook handler for incoming Twilio WhatsApp messages
    Twilio sends form-encoded data, not JSON
    """
    try:
        # Verify webhook signature (optional but recommended)
        if isinstance(whatsapp_api, TwilioWhatsAppAPI):
            signature = request.headers.get('X-Twilio-Signature', '')
            url = request.url
            if signature and not whatsapp_api.verify_webhook(url, request.form.to_dict(), signature):
                print("⚠️ Invalid Twilio signature")
                # Continue anyway for sandbox testing

        # Parse incoming message using Twilio format
        message_data = TwilioWhatsAppAPI.parse_incoming_message(request.form.to_dict())

        sender_phone = message_data['from']
        user_input = message_data['body']
        profile_name = message_data['profile_name']

        if not sender_phone or not user_input:
            return '', 200  # Empty response for status callbacks

        print(f"📱 Twilio message from {sender_phone} ({profile_name}): {user_input}")

        # Process the message using the same logic as Meta webhook
        handle_twilio_message(sender_phone, user_input, profile_name)

        return '', 200  # Twilio expects empty 200 response

    except Exception as e:
        print(f"Error processing Twilio webhook: {str(e)}")
        return '', 200  # Always return 200 to prevent retries

def handle_twilio_message(sender_phone: str, user_input: str, profile_name: str = None):
    """
    Process incoming Twilio message - mirrors handle_incoming_message logic
    """
    from datetime import datetime, timezone

    # Get or create lead
    lead = Lead.query.filter_by(phone_number=sender_phone).first()

    if not lead:
        lead = Lead(
            phone_number=sender_phone,
            name=profile_name,  # Twilio provides profile name
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(lead)
        db.session.commit()

        # Send greeting
        send_greeting(lead, sender_phone)
        return

    # Get current conversation state
    last_message = Conversation.query.filter_by(lead_id=lead.id, sender='bot').order_by(Conversation.created_at.desc()).first()
    current_state = last_message.flow_state if last_message else 'greeting'

    # Route based on current state
    process_conversation_step(lead, sender_phone, user_input, current_state)

# ============================================================================
# MESSAGE HANDLING (POST request from Meta)
# ============================================================================

@app.route('/webhook', methods=['POST'])
def webhook_handle():
    """
    Main webhook handler for incoming WhatsApp messages
    Processes incoming messages and routes to appropriate conversation flow
    """
    try:
        data = request.get_json()
        
        # Extract message details
        if data.get('object') == 'whatsapp_business_account':
            entry = data.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            
            messages = value.get('messages', [])
            statuses = value.get('statuses', [])
            
            # Handle incoming messages
            if messages:
                for message in messages:
                    handle_incoming_message(message)
            
            # Handle delivery confirmations (optional)
            if statuses:
                for status in statuses:
                    handle_message_status(status)
        
        return jsonify({'status': 'ok'}), 200
    
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 400

def handle_incoming_message(message: dict):
    """
    Process incoming message and route to conversation flow
    """
    sender_phone = message.get('from')
    message_id = message.get('id')
    timestamp = message.get('timestamp')
    
    # Mark message as read
    meta_api.mark_message_as_read(message_id)
    
    # Extract message text
    message_type = message.get('type', 'text')
    if message_type == 'text':
        user_input = message.get('text', {}).get('body', '')
    elif message_type == 'interactive':
        user_input = message.get('interactive', {}).get('button_reply', {}).get('title', '')
    else:
        return
    
    print(f"📱 Message from {sender_phone}: {user_input}")
    
    # Get or create lead
    lead = Lead.query.filter_by(phone_number=sender_phone).first()
    
    if not lead:
        lead = Lead(
            phone_number=sender_phone,
            created_at=datetime.fromtimestamp(int(timestamp))
        )
        db.session.add(lead)
        db.session.commit()
        
        # Send greeting
        greeting_response = send_greeting(lead, sender_phone)
        return
    
    # Get current conversation state
    last_message = Conversation.query.filter_by(lead_id=lead.id, sender='bot').order_by(Conversation.created_at.desc()).first()
    current_state = last_message.flow_state if last_message else 'greeting'
    
    # Route based on current state
    process_conversation_step(lead, sender_phone, user_input, current_state)

def send_greeting(lead: Lead, phone_number: str):
    """Send initial greeting and category selection"""
    greeting = """¡Hola! 👋 Bienvenido a PVB Estudio Creativo.

¿En qué te podemos ayudar?

1️⃣ Fotografía Fine Art o Video
2️⃣ Producción Audiovisual
3️⃣ Marketing Digital con IA

Responde con el número de tu interés:"""
    
    meta_api.send_text_message(phone_number, greeting)
    
    # Save bot message
    save_conversation(lead, greeting, 'bot', 'category_selection')

def process_conversation_step(lead: Lead, phone_number: str, user_input: str, current_state: str):
    """
    Process conversation based on current state
    Routes to appropriate flow handler
    """
    
    # Category selection
    if current_state == 'category_selection':
        if user_input in ['1', 'Fotografía', 'Photography', 'Fine Art', 'Video']:
            lead.service_category = 'photography'
            flow = PhotographyFlow()
            next_message = flow.MESSAGES['project_type']
            meta_api.send_text_message(phone_number, next_message['message'])
            save_conversation(lead, next_message['message'], 'bot', 'photo_project_type', user_input)
        
        elif user_input in ['3', 'Marketing', 'IA', 'AI']:
            lead.service_category = 'marketing'
            flow = MarketingFlow()
            next_message = flow.MESSAGES['problem']
            meta_api.send_text_message(phone_number, next_message['message'])
            save_conversation(lead, next_message['message'], 'bot', 'marketing_problem', user_input)
        
        else:
            meta_api.send_text_message(phone_number, "Por favor, selecciona una opción válida (1, 2 o 3)")
    
    # Photography flow - project type
    elif current_state == 'photo_project_type':
        lead.sub_category = user_input
        flow = PhotographyFlow()
        next_message = flow.MESSAGES['gallery_or_brand']
        meta_api.send_text_message(phone_number, next_message['message'])
        save_conversation(lead, next_message['message'], 'bot', 'photo_gallery_or_brand', user_input)
    
    # Photography flow - gallery or brand
    elif current_state == 'photo_gallery_or_brand':
        flow = PhotographyFlow()
        next_message = flow.MESSAGES['timeline']
        meta_api.send_text_message(phone_number, next_message['message'])
        save_conversation(lead, next_message['message'], 'bot', 'photo_timeline', user_input)
    
    # Photography flow - timeline
    elif current_state == 'photo_timeline':
        flow = PhotographyFlow()
        next_message = flow.MESSAGES['budget']
        meta_api.send_text_message(phone_number, next_message['message'])
        save_conversation(lead, next_message['message'], 'bot', 'photo_budget', user_input)
    
    # Photography flow - budget (final qualification)
    elif current_state == 'photo_budget':
        lead.budget_range = user_input
        capture_contact_info(lead, phone_number)
    
    # Marketing flow - problem
    elif current_state == 'marketing_problem':
        lead.project_description = user_input
        flow = MarketingFlow()
        next_message = flow.MESSAGES['current_campaigns']
        meta_api.send_text_message(phone_number, next_message['message'])
        save_conversation(lead, next_message['message'], 'bot', 'marketing_campaigns', user_input)
    
    # Marketing flow - current campaigns
    elif current_state == 'marketing_campaigns':
        flow = MarketingFlow()
        next_message = flow.MESSAGES['current_spend']
        meta_api.send_text_message(phone_number, next_message['message'])
        save_conversation(lead, next_message['message'], 'bot', 'marketing_spend', user_input)
    
    # Marketing flow - current spend
    elif current_state == 'marketing_spend':
        flow = MarketingFlow()
        lead.budget_range = user_input
        next_message = flow.MESSAGES['service_budget']
        meta_api.send_text_message(phone_number, next_message['message'])
        save_conversation(lead, next_message['message'], 'bot', 'marketing_service_budget', user_input)
    
    # Marketing flow - service budget (final qualification)
    elif current_state == 'marketing_service_budget':
        if user_input == '600':
            lead.project_description = 'Interested in $600 AI Ad Generation service'
        else:
            lead.project_description = 'Interested in Premium Consulting package ($2,800-$6,500)'
        capture_contact_info(lead, phone_number)
    
    # Contact info capture
    elif current_state == 'capture_name':
        lead.name = user_input
        meta_api.send_text_message(phone_number, DataCapture.MESSAGES['email'])
        save_conversation(lead, DataCapture.MESSAGES['email'], 'bot', 'capture_email', user_input)
    
    elif current_state == 'capture_email':
        lead.email = user_input
        meta_api.send_text_message(phone_number, DataCapture.MESSAGES['company'])
        save_conversation(lead, DataCapture.MESSAGES['company'], 'bot', 'capture_company', user_input)
    
    elif current_state == 'capture_company':
        lead.company = user_input
        send_confirmation_and_handoff(lead, phone_number)
    
    db.session.commit()

def capture_contact_info(lead: Lead, phone_number: str):
    """Start contact information capture"""
    meta_api.send_text_message(phone_number, DataCapture.MESSAGES['name'])
    save_conversation(lead, DataCapture.MESSAGES['name'], 'bot', 'capture_name')

def send_confirmation_and_handoff(lead: Lead, phone_number: str):
    """Send confirmation and hand off to Pancho"""
    # Determine lead quality and recommended service
    lead.lead_quality = LeadRouter.determine_lead_quality(lead.to_dict())
    lead.status = 'qualified'
    db.session.commit()
    
    # Send confirmation to user
    confirmation_msg = DataCapture.MESSAGES['confirmation']['message']
    meta_api.send_text_message(phone_number, confirmation_msg)
    save_conversation(lead, confirmation_msg, 'bot', 'handoff_complete')
    
    # Send notification to Pancho via n8n
    brief = LeadRouter.format_lead_brief(lead.to_dict())
    LeadRouter.send_admin_notification(lead.to_dict(), 'new_lead_qualified')
    
    print(brief)

def save_conversation(lead: Lead, message_text: str, sender: str, flow_state: str, user_response: str = None):
    """Save conversation to database"""
    conversation = Conversation(
        lead_id=lead.id,
        message_text=message_text,
        sender=sender,
        flow_state=flow_state,
        metadata={'user_response': user_response} if user_response else {}
    )
    db.session.add(conversation)
    db.session.commit()

def handle_message_status(status: dict):
    """Handle delivery/read status of sent messages"""
    status_type = status.get('status')
    print(f"Message status: {status_type}")

# ============================================================================
# ADMIN ENDPOINTS
# ============================================================================

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Get all leads (with filtering options)"""
    status_filter = request.args.get('status')
    quality_filter = request.args.get('quality')
    
    query = Lead.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    if quality_filter:
        query = query.filter_by(lead_quality=quality_filter)
    
    leads = query.order_by(Lead.created_at.desc()).all()
    return jsonify([lead.to_dict() for lead in leads])

@app.route('/api/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get single lead with full conversation history"""
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    
    lead_data = lead.to_dict()
    lead_data['conversations'] = [
        {
            'message': c.message_text,
            'sender': c.sender,
            'flow_state': c.flow_state,
            'created_at': c.created_at.isoformat()
        }
        for c in lead.conversations
    ]
    
    return jsonify(lead_data)

@app.route('/api/leads/<int:lead_id>/status', methods=['PATCH'])
def update_lead_status(lead_id):
    """Update lead status"""
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({'error': 'Lead not found'}), 404
    
    data = request.get_json()
    lead.status = data.get('status', lead.status)
    db.session.commit()
    
    return jsonify(lead.to_dict())

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'PVB Chatbot is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
