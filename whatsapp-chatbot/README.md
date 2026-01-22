# PVB WhatsApp Chatbot

## Descripción
Bot de ventas automatizado para WhatsApp que califica leads, captura información de proyectos y realiza handoff a Pancho.

**Servicios que vende:**
- 🎨 Fotografía Fine Art (Ecuestre, Automotriz)
- 🎬 Producción Audiovisual
- 🤖 Marketing Digital con IA ($600 o paquetes premium $2,800-$6,500)

## Quick Start

### 1. Instalación

```bash
# Clone repository
cd whatsapp-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Configuración de Variables de Entorno

Edita `.env` con tus credenciales:

```bash
# Meta Cloud API (obtener de https://developers.facebook.com)
META_BUSINESS_ACCOUNT_ID=your_account_id
META_PHONE_NUMBER_ID=your_phone_id
META_VERIFY_TOKEN=your_random_token  # Genera uno random, lo necesitas para Meta
META_ACCESS_TOKEN=your_access_token
META_API_VERSION=v18.0

# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/pvb_chatbot
# O para SQLite (desarrollo): sqlite:///chatbot.db

# Notificaciones
ADMIN_PHONE=+56123456789  # Tu número de WhatsApp
ADMIN_EMAIL=pancho@pvbestudio.com

# n8n Webhook (configurar después)
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/lead-notification
```

### 3. Configurar Meta Cloud API

#### Paso 1: Crear App en Meta Developers
1. Ve a https://developers.facebook.com
2. Crea una nueva app (Business type)
3. Agrega el producto "WhatsApp"

#### Paso 2: Obtener Phone Number ID
1. En WhatsApp > Getting started
2. Click "Create test phone number"
3. Copia el **Phone Number ID**

#### Paso 3: Generar Access Token
1. WhatsApp > Getting started
2. Bajo "Start sending messages", copia el **Temporary Access Token**
3. (Nota: Este token expira - necesitarás crear un permanent token en Settings > Tokens)

#### Paso 4: Webhook Setup en Meta
1. WhatsApp > Configuration
2. **Callback URL:** `https://tu-dominio.com/webhook`
3. **Verify Token:** El valor que pusiste en `.env` (META_VERIFY_TOKEN)
4. Subscribe to webhook fields: `messages`, `message_status`

### 4. Database Setup

```bash
# PostgreSQL (recomendado para producción)
psql -U postgres -c "CREATE DATABASE pvb_chatbot"

# O SQLite para desarrollo (automático)
# La DB se crea al correr la app
```

### 5. Ejecutar Aplicación

```bash
# Desarrollo
python app/main.py

# Producción (con gunicorn)
gunicorn app.main:app --bind 0.0.0.0:5000 --workers 4
```

El servidor estará en `http://localhost:5000`

---

## Flujo de Conversación

### Entrada: Instagram Bio
```
Link en bio → WhatsApp de Business Number
↓
Bot: "¿Qué servicio te interesa?"
  1️⃣ Fotografía/Video
  2️⃣ Producción
  3️⃣ Marketing con IA
```

### Branch 1: Fotografía/Video
```
1. ¿Qué tipo? (Ecuestre, Automotriz, Otro, Video)
2. ¿Uso? (Galería, Marca, Personal)
3. ¿Fecha? (Texto libre)
4. ¿Presupuesto? (<5k, 5-15k, 15-50k, >50k)
↓
→ Captura: Nombre, Email, Empresa
↓
→ Lead Quality = HOT/WARM/COLD (según presupuesto)
↓
→ Handoff a Pancho
```

### Branch 2: Marketing con IA
```
1. ¿Qué problema? (Ventas, Leads, Presencia, Optimizar)
2. ¿Campañas activas? (Sí/No)
3. ¿Gasto actual? (<500, 500-2k, 2-10k, >10k)
4. ¿Presupuesto para servicio? ($600 o Premium)
↓
→ Lead Quality = HOT si gasto >2k
                WARM si gasto 500-2k
                COLD si gasto <500
↓
→ Captura: Nombre, Email, Empresa
↓
→ Recomendación automática de servicio
↓
→ Handoff a Pancho
```

### Calificación de Leads

| Score | Categoría | Acción |
|-------|-----------|--------|
| 4+ puntos | 🔥 HOT | Email + WhatsApp inmediato a Pancho |
| 2-3 puntos | 🟡 WARM | Email a Pancho |
| <2 puntos | 🔵 COLD | Email con follow-up automático |

---

## API Endpoints

### Webhooks
- **GET `/webhook`** - Verificación de Meta
- **POST `/webhook`** - Recibir mensajes

### Admin API
- **GET `/api/leads`** - Todos los leads (filtrable por status/quality)
- **GET `/api/leads/<id>`** - Lead específico con historial completo
- **PATCH `/api/leads/<id>/status`** - Actualizar estado

### Health
- **GET `/health`** - Status de la aplicación

---

## Integración con n8n

### Workflow 1: Lead Notification
Cuando se califica un lead:
1. ✅ Si es HOT → Email + WhatsApp a Pancho
2. ✅ Si es WARM/COLD → Email a Pancho
3. ✅ Guarda timestamp de notificación

**Ubicación:** `n8n-workflows/lead-notification.json`

### Workflow 2: Auto Follow-up
Cada 24 horas:
1. ✅ Busca leads calificados del día anterior
2. ✅ Envía mensaje WhatsApp de follow-up
3. ✅ Envía email con opciones de servicio

**Ubicación:** `n8n-workflows/auto-followup.json`

### Setup n8n
```bash
# Instalar n8n
npm install -g n8n

# O usar Docker
docker run -d --name n8n -p 5678:5678 n8nio/n8n

# En n8n UI:
# 1. Import los workflow JSONs
# 2. Configura credenciales de Email/WhatsApp
# 3. Copia webhook URL a .env (N8N_WEBHOOK_URL)
# 4. Activa los workflows
```

---

## Estructura del Proyecto

```
whatsapp-chatbot/
├── app/
│   ├── main.py                 # Flask app principal
│   ├── flows/
│   │   └── conversation_engine.py  # Flujos de conversación
│   ├── models/
│   │   └── database.py         # SQLAlchemy models
│   └── utils/
│       ├── meta_api.py         # Meta Cloud API wrapper
│       └── lead_router.py      # Lead qualification & routing
├── n8n-workflows/
│   ├── lead-notification.json  # Notificación de leads
│   └── auto-followup.json      # Follow-up automático
├── requirements.txt
├── .env.example
└── README.md
```

---

## Hosting & Deployment

### Opción 1: Heroku (Fácil)
```bash
# Deploy a Heroku
heroku create pvb-chatbot
git push heroku main
heroku config:set META_ACCESS_TOKEN=...

# Webhook URL: https://pvb-chatbot.herokuapp.com/webhook
```

### Opción 2: Railway (Recomendado)
```bash
# Deploy con Railway (railroad.app)
# Conecta tu repo de GitHub
# Variables de entorno en dashboard
# Webhook URL automática
```

### Opción 3: AWS/DigitalOcean (Self-hosted)
```bash
# En tu servidor
sudo apt update && apt install python3-pip postgresql
git clone <repo>
pip install -r requirements.txt
export DATABASE_URL=postgresql://...
gunicorn app.main:app --bind 0.0.0.0:5000
```

---

## Troubleshooting

### Webhook no recibe mensajes
- ✅ Verifica META_VERIFY_TOKEN en .env
- ✅ Webhook URL debe ser HTTPS público
- ✅ Chequea Meta Developers > Logs

### Mensajes no se envían
- ✅ Verifica META_ACCESS_TOKEN es válido
- ✅ Verifica META_PHONE_NUMBER_ID correcto
- ✅ Check API response en logs

### Leads no se guardan en DB
- ✅ DATABASE_URL correcto
- ✅ `python app/main.py` crea tablas automáticamente
- ✅ Si PostgreSQL: `psql -l` para verificar DB existe

---

## Próximos Pasos

### 1. Personalizaciones
- [ ] Agregar más opciones a Photography flow
- [ ] Añadir búsqueda de horarios para agendar calls
- [ ] Integrar con Calendly/Cal.com

### 2. Analytics
- [ ] Dashboard de conversion rate
- [ ] Tracking de cual canal genera más leads
- [ ] ROI por servicio

### 3. Escalabilidad
- [ ] Rate limiting para evitar spam
- [ ] Retry logic para fallidos
- [ ] Webhook de Instagram DM

---

## Soporte
Para preguntas sobre la implementación, contacta a Pancho o revisa los logs con:
```bash
tail -f /var/log/gunicorn.log
```
