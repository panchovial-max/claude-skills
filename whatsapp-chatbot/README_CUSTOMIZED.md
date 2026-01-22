# PVB Estudio Creativo - WhatsApp Chatbot (Customized)

## Overview

This is a fully customized WhatsApp chatbot for **PVB Estudio Creativo** that:

- ✅ Qualifies leads from Instagram and WhatsApp
- ✅ Routes customers to the right service (Photography, Audiovisual, Marketing)
- ✅ Collects project details and budget information
- ✅ Automatically notifies Pancho via n8n
- ✅ Scores leads as HOT/WARM/COLD based on engagement and budget
- ✅ Recommends appropriate service tier ($600 AI Ads, $1-3k Strategic, $3-7k Premium)

## Services Offered

### 1. Fotografía Fine Art
- **Fotografía Ecuestre**: Piezas de nivel galería con experiencia en exhibiciones internacionales
- **Fotografía Automotriz**: Enfoque cinematográfico, combinando arte y precisión técnica
- **Producción Audiovisual**: Experiencia en producciones internacionales de nivel Super Bowl
- **Portfolio**: panchovial.com
- **Budget**: From $1,000 - $10,000+ custom quotes

### 2. Marketing Digital con IA
- **AI Ad Generation**: $600 - Test the approach with optimized ads
- **Strategic Package**: $1,000 - $3,000 - Monthly strategy & automation
- **Premium Package**: $3,000 - $7,000 - Full management + direct access

## System Architecture

```
┌─────────────────┐
│   Instagram     │
│  Lead Ads/      │
│  Bio Link       │ ──────┐
└─────────────────┘       │
                          │
                          ▼
┌─────────────────────────────────┐
│   WhatsApp Chatbot              │
│  (Flask + Meta Cloud API)       │
│                                 │
│ • Greeting & Service Selection  │
│ • Photography Flow              │
│ • Marketing Flow                │
│ • About/FAQ                     │
│ • Handoff to Pancho             │
└────────────┬────────────────────┘
             │
             ▼
     ┌───────────────┐
     │  SQLAlchemy   │
     │  SQLite/      │
     │  PostgreSQL   │
     │               │
     │  • Leads      │
     │  • Convs      │
     │  • Metrics    │
     └───────────────┘
             │
             ▼
     ┌───────────────┐
     │  n8n Webhook  │
     │               │
     │  • Email      │
     │  • WhatsApp   │
     │  • Follow-ups │
     │  • Calendar   │
     └───────────────┘
```

## Conversation Flows

### Photography Flow
1. **Project Type** - Ecuestre, Automotriz, Video, Otro
2. **Context** - Gallery, Brand, Personal, Event
3. **Location** - Where will the shoot take place?
4. **Date** - Timeline for the project
5. **Budget** - Investment range (<1k, 1-3k, 3-10k, >10k)
6. **Contact Capture** - Name, company, email, WhatsApp

### Marketing Flow
1. **Problem** - What's the main challenge? (More sales, Ads not working, Launch, etc)
2. **Current Campaigns** - Are you running ads? (Meta/Google/Both/None)
3. **Current Spend** - How much do you invest monthly? (<$500, $500-2k, $2-5k, >$5k)
4. **Service Budget** - Recommendation based on spend ($600/$1-3k/$3-7k)
5. **Contact Capture** - Name, company, website, email, WhatsApp, business description

### About/Info Flow
- Service descriptions
- Pricing information
- Portfolio link (panchovial.com)
- FAQ responses
- Direct handoff to Pancho

## Configuration

### Environment Variables

```bash
# Meta WhatsApp Cloud API
META_API_TOKEN=your_access_token_here
META_PHONE_NUMBER_ID=your_phone_number_id
META_BUSINESS_ACCOUNT_ID=your_business_account_id
WEBHOOK_VERIFY_TOKEN=your_verify_token

# Database
DATABASE_URL=sqlite:///chatbot.db  # or postgresql://...

# n8n Webhook
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/new-lead

# Pancho's Contact
PANCHO_WHATSAPP=+56-9-xxxx-xxxx
PANCHO_EMAIL=pancho@pvbstudio.com

# Optional
FLASK_ENV=production
FLASK_DEBUG=False
```

### Services Configuration

All messages, templates, and scoring logic are centralized in:
```
app/config/pvb_services.py
```

This includes:
- ✅ Welcome messages (Spanish/English)
- ✅ All conversation flows
- ✅ Contact capture templates
- ✅ FAQ responses
- ✅ Lead scoring weights
- ✅ Service recommendations

## Lead Quality Scoring

### Photography Leads
- Budget >$10k: 3 points
- Budget $3-10k: 2 points
- Budget $1-3k: 1 point
- Gallery context: +2 points
- Brand context: +1 point
- Has location: +1 point
- Has date: +1 point

**Thresholds:**
- HOT: 5+ points
- WARM: 3-4 points
- COLD: <3 points

### Marketing Leads
- Spend >$5k: 3 points
- Spend $2-5k: 2 points
- Spend $500-2k: 1 point
- Has campaigns: +2 points
- Problem is "ads not working": +2 points
- Problem is "launch": +1 point
- Budget $3-7k (Premium): +3 points
- Budget $1-3k (Strategic): +2 points
- Budget $600 (AI Ads): +1 point

**Thresholds:**
- HOT: 5+ points
- WARM: 3-4 points
- COLD: <3 points

## Files Overview

```
whatsapp-chatbot/
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── pvb_services.py        ← ALL messages & config
│   ├── flows/
│   │   └── conversation_engine.py ← Conversation flows
│   ├── models/
│   │   └── database.py            ← Database models
│   ├── utils/
│   │   ├── meta_api.py            ← Meta API wrapper
│   │   └── lead_router.py         ← Lead scoring (PVB-specific)
│   └── main.py                    ← Flask app & webhooks
├── requirements.txt
├── .env.example
├── dev-commands.sh
└── docs/
    ├── START_HERE.md
    ├── SETUP.md
    ├── ARCHITECTURE.md
    └── ...
```

## Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your actual values
```

### 3. Initialize Database
```bash
python -c "from app.models.database import Base, engine; Base.metadata.create_all(engine)"
```

### 4. Run Flask App
```bash
python -m flask run --host 0.0.0.0 --port 5000
```

### 5. Deploy
See [SETUP.md](docs/SETUP.md) for deployment instructions (Heroku, Railway, AWS, etc)

## Testing Conversations

### Test Photography Flow
```
User: 1
Bot: [Photography type question]
User: Ecuestre
Bot: [Context question]
...
```

### Test Marketing Flow
```
User: 2
Bot: [Problem question]
User: Más ventas
Bot: [Campaigns question]
...
```

## Pancho's Notifications

When a qualified lead is captured, n8n receives:

```json
{
  "notification_type": "new_lead",
  "lead_quality": "hot",
  "lead": {
    "name": "Juan García",
    "phone_number": "+56912345678",
    "email": "juan@empresa.cl",
    "company": "Brand X",
    "service_category": "marketing",
    "problem": "Ads not working",
    "spend": "$2-5k",
    "recommendation": "strategic"
  },
  "recommended_service": {
    "service": "Strategic Marketing",
    "price_range": "$1,000 - $3,000",
    "includes": [...]
  }
}
```

This triggers automated workflows:
1. Send email to Pancho
2. Send WhatsApp notification
3. Create calendar event
4. Log to CRM
5. Queue auto-follow-ups

## Next Steps

1. **Set up Meta API** - Complete webhook setup with Meta
2. **Configure n8n** - Create workflows for notifications
3. **Add Instagram Integration** - Enable lead ads
4. **Deploy** - Choose hosting (Heroku/Railway/AWS)
5. **Test** - Run through complete conversations
6. **Go Live** - Activate WhatsApp link in Instagram bio

## Support

For questions about the chatbot setup, see:
- [START_HERE.md](docs/START_HERE.md) - Quick overview
- [SETUP.md](docs/SETUP.md) - Detailed setup guide
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Technical details
- [CONVERSATION_EXAMPLES.md](docs/CONVERSATION_EXAMPLES.md) - Real examples
