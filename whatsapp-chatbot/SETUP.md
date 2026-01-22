# SETUP COMPLETO: PVB WhatsApp Chatbot

## FASE 1: Meta Cloud API Setup (30 minutos)

### 1.1 Crear Business App en Meta

**URL:** https://developers.facebook.com

Pasos:
1. Click "Mi Aplicaciones" (top derecha)
2. "Crear aplicación"
   - App Name: "PVB Sales Bot"
   - App Purpose: "Business"
3. Click "Crear aplicación"

### 1.2 Agregar WhatsApp Product

1. En dashboard app, click "+ Agregar producto"
2. Busca "WhatsApp"
3. Click "Configurar"
4. Selecciona "WhatsApp Cloud API"

### 1.3 Crear Test Phone Number

1. En WhatsApp > Getting started
2. Bajo "Send test message", click "Create test phone number"
3. Selecciona numero test de WhatsApp (Meta te proporciona)
4. **Copia estos valores para .env:**
   - `META_PHONE_NUMBER_ID` = El ID del número
   - `META_BUSINESS_ACCOUNT_ID` = Tu Business Account ID

### 1.4 Generar Access Token

**IMPORTANTE: Hay 2 tipos de tokens**

#### Opción A: Temporary Token (24 horas - desarrollo)
1. WhatsApp > Getting started
2. "Temporary access token" - copia el token
3. Pega en `.env` como `META_ACCESS_TOKEN`

#### Opción B: Permanent Token (producción - recomendado)
1. Settings > User Tokens
2. Genera nuevo token con permisos:
   - `whatsapp_business_messaging`
   - `whatsapp_business_management`
3. Pega en `.env`

### 1.5 Webhook Setup

**IMPORTANTE: Tu servidor debe estar en HTTPS público**

Si estás en desarrollo local:
```bash
# Opción 1: Usa ngrok para exponer localhost
ngrok http 5000
# Te dará URL como: https://xyz123.ngrok.io

# Opción 2: Deploy a Heroku/Railway primero
```

En Meta Developers:
1. WhatsApp > Configuration
2. **Webhook URL:** `https://tu-dominio.com/webhook`
   (Por ejemplo: `https://pvb-chatbot.herokuapp.com/webhook`)
3. **Verify Token:** Pon un token random (ejemplo: `"abc123xyzrandom"`)
   - Pega MISMO valor en `.env` como `META_VERIFY_TOKEN`
4. **Subscribe to messages:**
   - ✅ messages
   - ✅ message_status

5. Click "Verify and save"
   - Meta enviará GET request a tu webhook para verificar
   - Tu app responde con el challenge token
   - Si funciona, te aparecerá "Active"

---

## FASE 2: Código & Database Setup (20 minutos)

### 2.1 Clone & Install

```bash
cd /Users/franciscovialbrown/.claude-worktrees/GitHub/crazy-mcclintock
git clone <tu-repo> whatsapp-chatbot
cd whatsapp-chatbot

# Virtual env
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt
```

### 2.2 Environment Variables

```bash
cp .env.example .env
nano .env  # O abre con editor
```

Completa los valores:
```bash
# De Meta Developers
META_BUSINESS_ACCOUNT_ID=123456789
META_PHONE_NUMBER_ID=123456789
META_VERIFY_TOKEN=abc123xyzrandom
META_ACCESS_TOKEN=EAAxxxxxx...
META_API_VERSION=v18.0

# Database (elige uno)
# Desarrollo - SQLite (automático)
DATABASE_URL=sqlite:///chatbot.db

# Producción - PostgreSQL
# DATABASE_URL=postgresql://user:password@db.example.com:5432/pvb_chatbot

ENVIRONMENT=development

# Notificaciones
ADMIN_PHONE=+56912345678  # Tu número para recibir notificaciones
ADMIN_EMAIL=pancho@pvbestudio.com

# n8n (después de configurar)
N8N_WEBHOOK_URL=https://tu-n8n-instance.com/webhook/lead-notification
```

### 2.3 Database Setup

**Para SQLite (desarrollo):**
```bash
# Se crea automáticamente al correr la app
python app/main.py
# Presiona Ctrl+C después de ver "Running on http://0.0.0.0:5000"
```

**Para PostgreSQL (producción):**
```bash
# En tu DB
createdb pvb_chatbot
# O en psql:
# CREATE DATABASE pvb_chatbot;

# Luego en .env:
# DATABASE_URL=postgresql://user:password@localhost:5432/pvb_chatbot
```

---

## FASE 3: Ejecutar Localmente (5 minutos)

```bash
source venv/bin/activate
python app/main.py
```

Deberías ver:
```
 * Running on http://0.0.0.0:5000
```

**Test webhook:**
```bash
curl http://localhost:5000/health
# Respuesta: {"status":"ok"}
```

---

## FASE 4: Deployment a Producción

### Opción A: Heroku (Más Fácil)

```bash
# Install Heroku CLI
brew install heroku  # macOS

# Login
heroku login

# Create app
heroku create pvb-chatbot

# Set environment variables
heroku config:set META_BUSINESS_ACCOUNT_ID=123456...
heroku config:set META_PHONE_NUMBER_ID=123456...
heroku config:set META_VERIFY_TOKEN=abc123...
heroku config:set META_ACCESS_TOKEN=EAAxxxx...
heroku config:set DATABASE_URL=postgresql://... # Heroku lo genera

# Deploy
git push heroku main

# Ver logs
heroku logs --tail

# Tu webhook URL será:
# https://pvb-chatbot.herokuapp.com/webhook
```

### Opción B: Railway (Recomendado)

1. Ve a https://railway.app
2. Click "Start a New Project"
3. Conecta tu GitHub repo
4. Railway auto-detecta Python
5. Agrega PostgreSQL plugin
6. En "Variables":
   - Pega todas las variables de `.env`
7. Deploy automático cuando pushs a main

**Webhook URL:** `https://tu-proyecto.railway.app/webhook`

### Opción C: DigitalOcean/AWS

```bash
# En tu servidor (Ubuntu 20.04+)
sudo apt update
sudo apt install python3-pip postgresql postgresql-contrib nginx

# Clone repo
git clone <tu-repo> pvb-chatbot
cd pvb-chatbot

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Setup PostgreSQL
sudo -u postgres createdb pvb_chatbot

# Create systemd service
sudo nano /etc/systemd/system/pvb-chatbot.service
```

Contenido de `pvb-chatbot.service`:
```ini
[Unit]
Description=PVB WhatsApp Chatbot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/pvb-chatbot
Environment="PATH=/home/ubuntu/pvb-chatbot/venv/bin"
EnvironmentFile=/home/ubuntu/pvb-chatbot/.env
ExecStart=/home/ubuntu/pvb-chatbot/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    app.main:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start pvb-chatbot
sudo systemctl enable pvb-chatbot
```

---

## FASE 5: Instagram Integration

### 5.1 Link en Bio

En tu Instagram `@panchovial`:
1. Edit Profile
2. Bio: "Agrega WhatsApp link"
   - Tools > Links > "Add WhatsApp"
   - Selecciona tu Business número
3. Save

Cuando toquen el link → abre WhatsApp chat con tu bot

### 5.2 Stories & Posts (CTAs)

**Story CTA:**
1. Publica story
2. Sticker > "Link"
3. Link a WhatsApp: `https://wa.me/56912345678?text=Hola%20Pancho`

**Post Caption:**
```
Disponible en WhatsApp 💬
Contamos con:
✨ Fotografía Fine Art
🎬 Producción Audiovisual  
🤖 Marketing Digital

Link en bio →
```

---

## FASE 6: n8n Automation Setup (30 minutos)

### 6.1 Instalar n8n

**Docker (Recomendado):**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e DB_TYPE=sqlite \
  n8nio/n8n
```

Accede a: `http://localhost:5678`

**O NPM:**
```bash
npm install -g n8n
n8n start
```

### 6.2 Importar Workflows

1. En n8n UI > Workflows (menu lateral)
2. Click "+" > "Import from file"
3. Selecciona `n8n-workflows/lead-notification.json`
4. Repite con `auto-followup.json`

### 6.3 Configurar Credenciales

Para cada workflow necesitas:

**Email Credentials:**
1. Credentials (menu lateral)
2. "+ Add new credential"
3. Busca "Gmail" o "SMTP"
4. Agrega tu email account

**WhatsApp Credentials (Twilio):**
1. Crea cuenta en https://www.twilio.com
2. Copiar Account SID y Auth Token
3. Crea WhatsApp Twilio numero
4. Agrega a n8n Credentials

**HTTP Credentials (para API calls):**
- Usar Bearer Token con tu META_ACCESS_TOKEN

### 6.4 Activar Workflows

1. Abre cada workflow
2. Click en la esquina arriba-derecha (activar)
3. Status debe cambiar a "Active"

### 6.5 Webhook URL para Chatbot

En n8n, en workflow "Lead Notification":
1. Nodo "Webhook - Lead from Chatbot"
2. Verás "Production URL" como:
   ```
   https://tu-n8n-instance.com/webhook/lead-notification
   ```
3. Copia y pega en tu `.env`:
   ```
   N8N_WEBHOOK_URL=https://...
   ```
4. Redeploy tu chatbot

---

## TESTING COMPLETO

### Test 1: Verificar Webhook
```bash
# En terminal
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
            "text": {"body": "Hola bot"}
          }]
        }
      }]
    }]
  }'
```

Respuesta esperada:
```json
{"status": "ok"}
```

### Test 2: Enviar Mensaje Real

1. Abre WhatsApp en tu teléfono
2. Toca el link de bot (desde Instagram bio)
3. Escribe: `1` (para Fotografía)
4. El bot debería responder con opciones

### Test 3: Verificar Base de Datos

```bash
# SQLite
sqlite3 chatbot.db
sqlite> SELECT * FROM leads;
sqlite> SELECT * FROM conversations;

# PostgreSQL
psql -U postgres -d pvb_chatbot
postgres=# SELECT * FROM leads;
```

### Test 4: Verificar n8n

1. En n8n, abre workflow "Lead Notification"
2. Completa flujo en WhatsApp
3. Deberías ver ejecución en n8n logs
4. Deberías recibir email/WhatsApp de notificación

---

## Checklist Final

- [ ] Meta Developers app creado
- [ ] Phone Number ID y Access Token obtenidos
- [ ] Webhook URL registrada en Meta
- [ ] `.env` completado con todos los valores
- [ ] Database creada y migrada
- [ ] Aplicación corriendo localmente
- [ ] Desplegada a Heroku/Railway/AWS
- [ ] Instagram bio actualizado con link
- [ ] n8n instalado y workflows importados
- [ ] Credenciales de Email configuradas en n8n
- [ ] Primera prueba end-to-end completada ✅

---

## Próximas Mejoras

- [ ] Dashboard para ver leads en tiempo real
- [ ] Integración con Calendly para agendar calls
- [ ] Análisis de conversiones
- [ ] A/B testing de mensajes
- [ ] Soporte multiidioma (EN/ES)

---

**¿Preguntas?** Revisa logs con:
```bash
heroku logs --tail  # Si está en Heroku
tail -f /var/log/app.log  # Si está en servidor
```
