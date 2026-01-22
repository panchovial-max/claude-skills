# 🏗️ PROJECT STRUCTURE - Visual Overview

## Complete File Tree

```
whatsapp-chatbot/
│
├── 📄 DOCUMENTACIÓN (LEE EN ESTE ORDEN)
│   ├── INDEX.md                    ← TÚ ESTÁS AQUÍ (overview completo)
│   ├── QUICKSTART.md               ← Empieza aquí (5 min)
│   ├── SETUP.md                    ← Setup detallado (30 min) 
│   ├── INSTAGRAM_STRATEGY.md       ← Plan de marketing (20 min)
│   ├── CONVERSATION_EXAMPLES.md    ← Ejemplos reales
│   └── README.md                   ← Documentación técnica
│
├── 🔧 CÓDIGO PYTHON (Backend)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 ← 🚀 APP PRINCIPAL (Flask)
│   │   │   ├── Webhook verification (Meta)
│   │   │   ├── Message handling
│   │   │   ├── Conversation routing
│   │   │   ├── Lead database management
│   │   │   └── Admin API endpoints
│   │   │
│   │   ├── flows/                  ← Lógica de conversación
│   │   │   ├── __init__.py
│   │   │   └── conversation_engine.py
│   │   │       ├── ConversationFlow (base)
│   │   │       ├── PhotographyFlow (preguntas para foto)
│   │   │       ├── MarketingFlow (preguntas para marketing)
│   │   │       ├── DataCapture (captura de contacto)
│   │   │       └── route_flow() (router)
│   │   │
│   │   ├── models/                 ← Base de datos
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   │       ├── Lead model
│   │   │       ├── Conversation model
│   │   │       └── CampaignMetric model
│   │   │
│   │   └── utils/                  ← Utilidades
│   │       ├── __init__.py
│   │       ├── meta_api.py          ← API de Meta WhatsApp
│   │       │   ├── send_text_message()
│   │       │   ├── send_interactive_message()
│   │       │   ├── verify_webhook()
│   │       │   └── mark_message_as_read()
│   │       │
│   │       └── lead_router.py       ← Lógica de calificación
│   │           ├── determine_lead_quality()
│   │           ├── determine_recommended_service()
│   │           ├── send_admin_notification()
│   │           └── format_lead_brief()
│   │
│   ├── test_conversations.py       ← Test script (ejecutar para debugging)
│   │
│   ├── requirements.txt             ← Dependencias Python
│   └── dev-commands.sh              ← Comandos útiles
│
├── 🤖 AUTOMATIZACIÓN (n8n Workflows)
│   └── n8n-workflows/
│       ├── lead-notification.json   ← Notifica a Pancho cuando hay lead HOT
│       │   └── Flujo:
│       │       1. Recibe webhook de lead
│       │       2. IF HOT → Email + WhatsApp urgente
│       │       3. IF WARM/COLD → Email normal
│       │       4. Update status en DB
│       │
│       └── auto-followup.json       ← Follow-up automático 24h después
│           └── Flujo:
│               1. Corre cada 24h
│               2. Busca leads de ayer
│               3. Envía WhatsApp follow-up
│               4. Envía email con propuesta
│               5. Update en DB
│
├── ⚙️ CONFIGURACIÓN
│   └── .env.example                 ← Template de env variables
│       ├── Meta Cloud API credentials
│       ├── Database URL
│       ├── Admin notifications
│       └── n8n webhook URL
│
└── 📦 DEPENDENCIAS
    └── requirements.txt              ← Python packages
        ├── Flask 3.0.0
        ├── SQLAlchemy 3.1.1
        ├── requests 2.31.0
        ├── python-dotenv 1.0.0
        └── ... (9 total)
```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          INSTAGRAM USER                             │
│                   (follows @panchovial)                             │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           │ Clicks "WhatsApp" link
                           ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    META WHATSAPP CLOUD API                          │
│              (forwards message to our webhook)                      │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           │ POST /webhook
                           ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  FLASK APP (app/main.py)                            │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 1. Webhook verification                                        │ │
│  │ 2. Extract message from Meta                                   │ │
│  │ 3. Get or create Lead in DB                                    │ │
│  │ 4. Route to conversation flow                                  │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    ┌──────┴───────┐
                    │              │
        ┌───────────↓──────┐  ┌────↓─────────────┐
        │  CONVERSATION    │  │ DATABASE        │
        │  ROUTING         │  │ (SQLite/PG)     │
        │                  │  │                 │
        │ If Photography:  │  │ - Leads table   │
        │ ├─ Project type? │  │ - Conversations │
        │ ├─ Use case?     │  │ - Metrics       │
        │ ├─ Timeline?     │  │                 │
        │ └─ Budget?       │  │ Saves:          │
        │                  │  │ - Lead data     │
        │ If Marketing:    │  │ - Messages      │
        │ ├─ Problem?      │  │ - State         │
        │ ├─ Campaigns?    │  │ - Flow history  │
        │ ├─ Spend?        │  │                 │
        │ └─ Service?      │  │                 │
        │                  │  │                 │
        │ ↓ Capture data   │  │                 │
        │ (Name, email,    │  │                 │
        │  company)        │  │                 │
        └────────┬─────────┘  └────┬────────────┘
                 │                 │
                 │ Qualify lead    │
                 │ (HOT/WARM/COLD) │
                 │                 │
    ┌────────────↓──────────────────────┐
    │                                    │
    ↓                                    ↓
IF HOT LEAD                        IF WARM/COLD
    │                                    │
    │ Send notification                  │
    │ to n8n                             │
    ↓                                    ↓
┌──────────────────────────────────────────────┐
│      n8n AUTOMATION WORKFLOWS               │
│  ┌────────────────────────────────────────┐ │
│  │ lead-notification.json                 │ │
│  ├─ Receive webhook                       │ │
│  ├─ IF HOT:                               │ │
│  │   ├─ Send Email to Pancho (urgent)    │ │
│  │   └─ Send WhatsApp to Pancho (urgent) │ │
│  ├─ IF WARM/COLD:                         │ │
│  │   └─ Send Email to Pancho (normal)    │ │
│  └────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
    │
    ├─ Every 24h:
    │  └─ auto-followup.json
    │     ├─ Find qualified leads from yesterday
    │     ├─ Send WhatsApp follow-up
    │     └─ Send Email with proposal
    │
    ↓
PANCHO RECEIVES NOTIFICATION
(Email + WhatsApp if HOT)
    │
    ├─ Opens WhatsApp
    ├─ Responds directly to lead
    ├─ Books call via Calendly
    └─ Closes deal
```

---

## 🗂️ File Purposes at a Glance

| File | Purpose | Editar? |
|------|---------|---------|
| `main.py` | Flask app, webhooks, routing | Solo si quieres agregar features |
| `conversation_engine.py` | Flujos Q&A del bot | Sí - personalizar preguntas |
| `database.py` | Modelos de DB | No (a menos que cambes schema) |
| `meta_api.py` | Integración con WhatsApp | No (funciona out-of-box) |
| `lead_router.py` | Calificación de leads | Sí - ajustar scoring |
| `test_conversations.py` | Test script | Ejecutar para debugging |
| `.env.example` | Variables de entorno | Copiar a `.env` + rellenar |
| `n8n-workflows/*.json` | Automación | Importar a n8n dashboard |
| `SETUP.md` | Guía paso-a-paso | Leer completamente |
| `INSTAGRAM_STRATEGY.md` | Plan de marketing | Leer y ejecutar |

---

## 🚀 Deployment Architecture

```
LOCAL DEVELOPMENT              →    PRODUCTION
═══════════════════════════════════════════════════════════

┌──────────────────┐              ┌──────────────────┐
│  Flask App       │              │  Heroku/Railway  │
│  (localhost:5000)│   Deploy     │  (Public HTTPS)  │
└──────────────────┘    with  ─→  └──────────────────┘
                       git push           ↑
┌──────────────────┐                      │
│  SQLite DB       │                      │ Pulls config
│  (chatbot.db)    │                      │ from Heroku
└──────────────────┘              ┌──────────────────┐
                                  │  PostgreSQL DB   │
                                  │  (Heroku Addon)  │
         ngrok tunnel             └──────────────────┘
         (for testing)                    ↑
         https://xyz.ngrok.io    ┌──────────────────┐
                │                │  n8n Instance    │
                │                │  (Cloud or Self)  │
                └───────→ Meta    └──────────────────┘
                        Servers       │
                           ↓          │
                                      ↓
                              ┌──────────────────┐
                              │  Admin Email     │
                              │  Admin WhatsApp  │
                              │  (Pancho)        │
                              └──────────────────┘
```

---

## 💾 Database Schema (Simplified)

```
LEADS TABLE
├─ id (Primary Key)
├─ phone_number (Unique) ← Main identifier
├─ name
├─ email
├─ company
├─ service_category (photography / marketing / video)
├─ sub_category (ecuestre, automotriz, etc)
├─ budget_range (<5k, 5-15k, 15-50k, >50k)
├─ project_description (free text)
├─ lead_quality (hot / warm / cold) ← Auto-calculated
├─ status (new / qualified / contacted / converted / lost)
├─ created_at (Timestamp)
├─ updated_at (Timestamp)
└─ → Foreign key to Conversations

CONVERSATIONS TABLE
├─ id (Primary Key)
├─ lead_id (Foreign Key) → LEADS.id
├─ message_text
├─ sender (bot / user)
├─ flow_state (greeting / category_selection / photo_budget / etc)
├─ metadata (JSON - stores user responses)
└─ created_at (Timestamp)

CAMPAIGN_METRICS TABLE
├─ id (Primary Key)
├─ lead_id (Foreign Key)
├─ metric_type (impression / click / message / qualification / conversion)
├─ value (string/number)
└─ created_at (Timestamp)
```

---

## 🔌 API Endpoints

```
PUBLIC (Webhook)
├─ GET  /webhook          ← Meta sends verification challenge
└─ POST /webhook          ← Meta sends incoming messages

ADMIN (Protected*)
├─ GET  /api/leads        ← List all leads (filters: status, quality)
├─ GET  /api/leads/<id>   ← Get single lead + full conversation history
└─ PATCH /api/leads/<id>/status ← Update lead status

HEALTH CHECK
└─ GET  /health           ← Server status ("ok")

*Note: Admin endpoints currently unprotected (add API key in SETUP)
```

---

## 🎯 How It All Works Together

```
1. USER sends WhatsApp message
   ↓
2. META forwards to /webhook
   ↓
3. MAIN.PY verifies and processes
   ↓
4. CONVERSATION_ENGINE determines next question
   ↓
5. MAIN.PY sends response via META_API
   ↓
6. DATABASE stores conversation history
   ↓
7. After calification:
   LEAD_ROUTER calculates lead_quality
   ↓
8. IF HOT:
   SEND WEBHOOK to n8n
   ↓
9. n8n WORKFLOW:
   ├─ Sends Email to Pancho
   ├─ Sends WhatsApp to Pancho
   └─ Updates DB status
   ↓
10. PANCHO receives notification
    & responds to lead directly
    ↓
11. 💰 VENTA
```

---

## 📋 Configuration Checklist

```
.env file needs:
□ META_BUSINESS_ACCOUNT_ID  (from Meta Developers)
□ META_PHONE_NUMBER_ID      (from Meta Developers)
□ META_VERIFY_TOKEN         (your random token)
□ META_ACCESS_TOKEN         (from Meta Developers)
□ META_API_VERSION          (v18.0 default)
□ DATABASE_URL              (sqlite:///chatbot.db for dev)
□ ENVIRONMENT               (development / production)
□ ADMIN_PHONE              (your WhatsApp number)
□ ADMIN_EMAIL              (pancho@pvbestudio.com)
□ N8N_WEBHOOK_URL          (will add after n8n setup)
```

---

**Next Step:** Start with [QUICKSTART.md](QUICKSTART.md) (5 min read)

Then: Follow [SETUP.md](SETUP.md) (30 min step-by-step)

You're building something great! 🚀
