# 📋 ÍNDICE COMPLETO - WhatsApp Sales Bot de PVB

## 🎯 ¿QUÉ HEMOS CREADO?

Un **sistema completo de automatización de ventas** que:

1. **Atrae leads** desde Instagram
2. **Califica automáticamente** a través de WhatsApp
3. **Rourea a Pancho** solo los leads prometedores
4. **Automatiza follow-ups** con n8n
5. **Integra todo** en una plataforma centralizada

---

## 📚 DOCUMENTACIÓN (Lee en este orden)

### 1️⃣ COMIENZA AQUÍ
- **[QUICKSTART.md](QUICKSTART.md)** ← LEE PRIMERO (5 min)
  - Overview rápido del sistema
  - 3 pasos para setup básico
  - Ejemplo de flujo de usuario

### 2️⃣ SETUP DETALLADO
- **[SETUP.md](SETUP.md)** ← SIGUE ESTO PASO-A-PASO (30-60 min)
  - Configuración de Meta Cloud API (muy importante!)
  - Setup de Base de Datos
  - Deployment a Heroku/Railway
  - Troubleshooting

### 3️⃣ ESTRATEGIA DE MARKETING
- **[INSTAGRAM_STRATEGY.md](INSTAGRAM_STRATEGY.md)** ← Para Pancho (20 min)
  - Cómo promocionar en Instagram
  - Flujo completo del embudo de ventas
  - Analytics y métricas
  - 30-day action plan

### 4️⃣ EJEMPLOS DE CONVERSACIÓN
- **[CONVERSATION_EXAMPLES.md](CONVERSATION_EXAMPLES.md)** (15 min)
  - 3 ejemplos reales de chats (HOT, WARM, COLD)
  - Cómo el bot califica leads
  - Cómo se ven en el mundo real

### 5️⃣ DOCUMENTACIÓN TÉCNICA
- **[README.md](README.md)** ← Para desarrolladores
  - Arquitectura del sistema
  - API endpoints
  - Estructura del código

---

## 🔧 ESTRUCTURA DEL CÓDIGO

```
app/
├── main.py                    # Flask app principal
│   ├── Webhook verification (Meta)
│   ├── Message handling & routing
│   ├── Admin API endpoints
│   └── Health check
│
├── flows/
│   └── conversation_engine.py # Flujos de conversación
│       ├── PhotographyFlow
│       ├── MarketingFlow
│       ├── DataCapture
│       └── Lead routing logic
│
├── models/
│   └── database.py            # Base de datos
│       ├── Lead model
│       ├── Conversation model
│       └── CampaignMetric model
│
└── utils/
    ├── meta_api.py            # Meta Cloud API wrapper
    │   ├── send_text_message
    │   ├── send_interactive_message
    │   ├── verify_webhook
    │   └── mark_as_read
    │
    └── lead_router.py         # Lead qualification
        ├── determine_lead_quality
        ├── determine_recommended_service
        └── send_admin_notification

n8n-workflows/
├── lead-notification.json     # Notifica a Pancho cuando hay lead
└── auto-followup.json         # Follow-up automático 24h después
```

---

## 🚀 QUICK START (3 pasos)

### PASO 1: Instalar (5 min)
```bash
cd whatsapp-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### PASO 2: Configurar Meta (15 min)
1. Ve a https://developers.facebook.com
2. Crea app "WhatsApp"
3. Obtén credenciales:
   - `META_PHONE_NUMBER_ID`
   - `META_ACCESS_TOKEN`
   - `META_VERIFY_TOKEN` (cualquier token random)
4. Configura webhook en Meta Developers
5. Pasa valores a `.env`

### PASO 3: Deploy (5 min)
```bash
# Opción 1: Heroku
heroku create tu-app-name
heroku config:set META_PHONE_NUMBER_ID=...
git push heroku main

# Opción 2: Railway (recomendado)
# Conecta GitHub + Deploy automático
```

---

## 💬 FLUJO DE USUARIO (Simplificado)

```
User → Instagram @panchovial
       ↓ Toca "WhatsApp"
       ↓
       Bot asks: "¿Qué servicio?"
       ↓
       User selects 1-3 options
       ↓
       Bot asks 3-4 calification questions
       ↓
       Bot captures: Name, Email, Company
       ↓
       System evaluates: HOT/WARM/COLD
       ↓
       IF HOT → Notifica Pancho INMEDIATAMENTE
       ↓
       Pancho responde directamente en WhatsApp
       ↓
       Agendas call / Propuesta
       ↓
       💰 VENTA
```

---

## 📊 FLUJOS DE CLASIFICACIÓN

### Rama 1: Fotografía/Video
```
1. ¿Tipo proyecto? (Ecuestre/Automotriz/Otro/Video)
2. ¿Uso? (Galería/Marca/Personal)
3. ¿Timeline?
4. ¿Presupuesto? (<5k / 5-15k / 15-50k / >50k)
↓
Lead Quality:
  >50k → 🔥 HOT
  15-50k → 🟡 WARM
  <15k → 🔵 COLD
```

### Rama 2: Marketing Digital
```
1. ¿Problema? (Ventas/Leads/Presencia/Optimizar)
2. ¿Campañas activas? (Sí/No)
3. ¿Gasto actual? (<500 / 500-2k / 2-10k / >10k)
4. ¿Servicio? ($600 AI / Premium $2,800-6,500)
↓
Lead Quality:
  Gasto >2k → 🔥 HOT
  Gasto 500-2k → 🟡 WARM
  Gasto <500 → 🔵 COLD
↓
Service Recommendation:
  HOT → Premium ($2,800-6,500)
  WARM → Premium o $600
  COLD → $600 (try it first)
```

---

## 🤖 AUTOMATIZACIÓN CON n8n

### Workflow 1: Lead Notification
**Trigger:** Lead calificado
```
IF Lead Quality = HOT
  → Email a Pancho + WhatsApp urgent notification
  → Copia a admin
  → Log en database

IF Lead Quality = WARM
  → Email a Pancho (normal)
  → Log en database

IF Lead Quality = COLD
  → Wait for auto-follow-up workflow
```

### Workflow 2: Auto Follow-up
**Trigger:** Cada 24 horas
```
1. Busca leads de ayer
2. Para cada lead calificado:
   → Envía WhatsApp follow-up
   → Envía email con propuesta
   → Actualiza timestamp en DB
3. Log de seguimiento
```

---

## 📈 MÉTRICAS ESPERADAS

### Mes 1 (1,000 followers Instagram)
```
Conversión Instagram → WhatsApp: 10%
  → 100 mensajes nuevos

Leads Cualificados: 40%
  → 40 leads calificados

Conversiones: 20%
  → 8 ventas

Revenue esperado: $5,000 - $25,000
(Depende de mix HOT/WARM/COLD)
```

### Breakdown por Lead Quality
```
HOT Leads (10-15% del total)
  └─ Conversion: 80-90%
  └─ Deal size: $2,500-50,000+
  └─ Close time: 2-7 días

WARM Leads (30-40% del total)
  └─ Conversion: 40-60%
  └─ Deal size: $600-6,500
  └─ Close time: 7-21 días

COLD Leads (45-60% del total)
  └─ Conversion: 5-15%
  └─ Deal size: $600-3,000
  └─ Close time: 30-90 días
```

---

## 🛠 COMANDOS ÚTILES

```bash
# Load dev commands
source dev-commands.sh

# Testing
test_health                # ¿Está running?
test_get_leads            # Ver todos los leads
count_leads               # Contar total de leads
find_hot_leads            # Ver solo HOT leads

# Database
db_check                  # Status de DB
db_backup                 # Backup de DB

# Monitoring
conversion_rate           # % de conversión
logs_heroku              # Ver logs en Heroku

# Deployment
deploy_heroku            # Push a Heroku
logs_heroku              # Ver logs
```

---

## 🚨 TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| Webhook no recibe mensajes | Check META_VERIFY_TOKEN en .env y Meta Developers config |
| Mensajes no se envían | Verifica META_ACCESS_TOKEN es valid + PHONE_NUMBER_ID correcto |
| Leads no se guardan | DATABASE_URL correcto + `python app/main.py` crea tablas |
| n8n no notifica | N8N_WEBHOOK_URL en .env + workflow "Active" status |
| ¿No sé dónde empezar? | Lee SETUP.md paso-a-paso |

---

## 📞 NEXT STEPS

### Inmediato (Hoy)
- [ ] Lee QUICKSTART.md (5 min)
- [ ] Lee SETUP.md (30 min)
- [ ] Abre Meta Developers
- [ ] Empieza Meta Cloud API setup

### Hoy + 1 hora
- [ ] Tengas credenciales de Meta
- [ ] .env completado
- [ ] App corriendo localmente (python app/main.py)

### Hoy + 2 horas
- [ ] Desplegada a Heroku o Railway
- [ ] Webhook registrado en Meta
- [ ] Instagram bio actualizado con link

### Día 2
- [ ] n8n instalado y workflows configurados
- [ ] First test lead end-to-end
- [ ] Pancho recibe notificación

### Semana 1
- [ ] 10-20 leads iniciales llegando
- [ ] Ajustes a flujo basado en feedback
- [ ] Primeras conversiones

---

## 📚 RECURSOS

### Documentación oficial
- Meta Cloud API: https://developers.facebook.com/docs/whatsapp
- Flask: https://flask.palletsprojects.com
- SQLAlchemy: https://www.sqlalchemy.org
- n8n: https://docs.n8n.io

### Herramientas recomendadas
- **Hosting:** Railway.app (mejor que Heroku ahora)
- **Database:** PostgreSQL en Railway o Supabase
- **Automation:** n8n (self-hosted o cloud)
- **Calendar:** Calendly para agendar calls

---

## ✅ CHECKLIST FINAL

- [ ] QUICKSTART.md leído
- [ ] SETUP.md leído y pasos seguidos
- [ ] Meta Developers account creado
- [ ] Phone Number ID obtenido
- [ ] Access Token obtenido (permanent)
- [ ] .env completado
- [ ] App running localmente
- [ ] Webhook URL en Meta Developers
- [ ] Desplegada a Heroku/Railway
- [ ] Instagram bio actualizado
- [ ] n8n workflows importados
- [ ] Email credentials configuradas
- [ ] First test lead completado
- [ ] Notificación a Pancho funciona

**Si todo está ✅ → ¡Tu sistema está VIVO y generando leads! 🚀**

---

## 🎉 ¡FELICIDADES!

Ya tienes un sistema de automatización de ventas listo para llevar tu negocio al siguiente nivel.

**Próximas 48 horas:** Espera primeros leads llegando a WhatsApp

**Próximos 30 días:** Deberías tener 30-50 leads calificados

**Próximos 90 días:** $12,500 - $25,000+ en pipeline

Ahora... **¡Empieza a hacer setup! 💪**

---

**¿Preguntas?** Revisa documentos de arriba o corre:
```bash
source dev-commands.sh
help
```
