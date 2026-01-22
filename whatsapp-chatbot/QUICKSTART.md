# QUICKSTART: Tu Chatbot de Ventas ya está listo 🚀

## Lo que acabamos de crear:

```
whatsapp-chatbot/
├── app/main.py                  ← Flask app (webhook + routing)
├── app/flows/conversation_engine.py  ← Flujos de conversación
├── app/models/database.py       ← Database models (leads, conversations)
├── app/utils/meta_api.py        ← Meta Cloud API integration
├── app/utils/lead_router.py     ← Lead qualification & routing
├── n8n-workflows/               ← Automation (notifications, follow-ups)
├── README.md                    ← Documentación general
├── SETUP.md                     ← Guía paso-a-paso de setup
├── INSTAGRAM_STRATEGY.md        ← Estrategia completa de leads
├── test_conversations.py        ← Script para testear flujos
├── dev-commands.sh              ← Comandos útiles
└── requirements.txt             ← Dependencias Python
```

---

## 🎯 SETUP EN 3 PASOS (30 minutos)

### Paso 1: Instalar & Configurar (10 min)

```bash
cd whatsapp-chatbot

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup variables de entorno
cp .env.example .env

# ← EDITA .env CON TUS CREDENCIALES DE META
```

### Paso 2: Conseguir Credenciales de Meta (15 min)

Ve a: https://developers.facebook.com

1. Crea Business App
2. Agrega producto WhatsApp
3. Obtén:
   - `META_BUSINESS_ACCOUNT_ID`
   - `META_PHONE_NUMBER_ID`
   - `META_ACCESS_TOKEN` (permanent token)
   - `META_VERIFY_TOKEN` (token random tuyo)

⚠️ **Para webhook en desarrollo usa ngrok:**
```bash
# Terminal 1:
python app/main.py

# Terminal 2:
ngrok http 5000
# Copias la URL HTTPS y la pones en Meta Developers
```

### Paso 3: Deploy (5 min)

**Opción A: Heroku (gratis tier)**
```bash
heroku create tu-app-name
heroku config:set META_ACCESS_TOKEN=...
git push heroku main
```

**Opción B: Railway.app (recomendado)**
- Conecta GitHub
- Railway auto-deploya al pushear

---

## 🧪 TEST RÁPIDO

```bash
# En terminal, carga los comandos
source dev-commands.sh

# Test que el bot responde
test_health

# Ver leads en DB
count_leads

# Ver hot leads
find_hot_leads

# Simular mensaje WhatsApp
test_message
```

---

## 📱 INSTAGRAM → BOT → VENTAS

### Flujo de Usuario:

```
User ve Instagram @panchovial
  ↓
Toca "WhatsApp" en bio
  ↓
Bot: "¿Qué servicio te interesa?"
  1️⃣ Fotografía/Video
  2️⃣ Producción
  3️⃣ Marketing con IA
  ↓
User selecciona 👉
  ↓
Bot hace preguntas de calificación (3-4 preguntas)
  ↓
Bot pide: Nombre, Email, Empresa
  ↓
🎯 LEAD CALIFICADO
  ↓
Bot: "Pancho se contactará en 24h"
  ↓
n8n envía notificación a Pancho
  ↓
Pancho responde directamente via WhatsApp
  ↓
💰 VENTA
```

---

## 🎨 CONVERSACIÓN REAL - EJEMPLO

### Fotografía (HOT Lead):
```
Bot: "¿Qué tipo de proyecto? 🐴 Ecuestre 🏎️ Automotriz..."
User: "Ecuestre"

Bot: "¿Es para galería, marca o personal?"
User: "Galería"

Bot: "¿Fecha tentativa?"
User: "Febrero 2026"

Bot: "¿Presupuesto?"
User: ">50k USD"

Bot: "¡Perfecto! Nombre completo?"
User: "María García"

Bot: "Email?"
User: "maria@email.com"

Bot: "Empresa?"
User: "Equestrian Gallery"

Bot: "✅ Gracias María! Pancho se contactará en 24h 
     con opciones personalizadas para tu proyecto.
     
📱 Espera mensaje en WhatsApp"

---

[Pancho recibe notificación en n8n + WhatsApp 🔥 HOT LEAD]
[Pancho responde directamente en WhatsApp]
```

---

## 💡 LEAD QUALIFICATION LOGIC

| Criterio | Puntos | Resultado |
|----------|--------|-----------|
| Presupuesto fotografía >50k | +3 | 🔥 HOT |
| Presupuesto fotografía 5-50k | +2 | 🟡 WARM |
| Presupuesto marketing >2k/mes | +3 | 🔥 HOT |
| Ya tiene campañas Meta | +2 | 🟡 WARM |
| Gasto bajo <500 | +0 | 🔵 COLD |

---

## 📊 n8n WORKFLOWS (Automatización)

### Workflow 1: Lead Notification
Cuando se califica un lead:
- ✅ Si HOT → Email + WhatsApp inmediato a Pancho
- ✅ Si WARM → Email a Pancho
- ✅ Si COLD → Nada (wait for auto-follow-up)

**Ubicación:** `n8n-workflows/lead-notification.json`

### Workflow 2: Auto Follow-up (24h después)
- ✅ Busca leads cualificados del día anterior
- ✅ Envía mensaje WhatsApp de follow-up
- ✅ Envía email con opciones de servicio

**Setup n8n:**
```bash
# Docker
docker run -p 5678:5678 n8nio/n8n

# Luego:
# 1. Import JSON workflows
# 2. Configure email credentials
# 3. Copia webhook URL a .env (N8N_WEBHOOK_URL)
```

---

## 📈 MÉTRICAS ESPERADAS (30 días)

Con 1,000 seguidores en Instagram:

```
Día 1-5:     5-10 mensajes nuevos
Día 5-15:   20-30 leads cualificados
Día 15+:    5-10 hot leads listos para vender

Proyección Mes 1:
- Leads: 30-50
- Calificados: 12-20
- Conversiones: 2-4
- Ingresos: $5,000 - $15,000+
```

---

## 🔧 PRÓXIMAS MEJORAS (Roadmap)

**Semana 1:**
- [ ] Deploy en Railway
- [ ] Conectar Instagram con bot
- [ ] Setup n8n workflows
- [ ] First test lead end-to-end

**Semana 2:**
- [ ] Integrar Calendly para agendar calls
- [ ] Dashboard de leads en tiempo real
- [ ] A/B test messages

**Mes 2:**
- [ ] Agregar TikTok funnel
- [ ] Chatbot en website
- [ ] Email sequences

---

## 🆘 SI ALGO FALLA

### Bot no responde a mensajes
1. Check webhook is "Active" en Meta Developers
2. Check `heroku logs` o `railway logs`
3. Check `.env` tiene valores correctos

### No recibe notificaciones en n8n
1. Check `N8N_WEBHOOK_URL` es accesible
2. Run test: `curl $N8N_WEBHOOK_URL -X POST`
3. Check n8n Workflow has "Active" status

### Database issues
```bash
# Ver todos los leads
sqlite3 chatbot.db "SELECT * FROM leads;"

# Borrar leads de test
sqlite3 chatbot.db "DELETE FROM leads WHERE phone_number='56912345678';"

# Reset DB (WARNING: Borra todo)
rm -f chatbot.db
python app/main.py
```

---

## 📚 DOCUMENTOS IMPORTANTES

1. **README.md** - Overview general + arquitectura
2. **SETUP.md** - Guía paso-a-paso detallada ← START HERE
3. **INSTAGRAM_STRATEGY.md** - Estrategia completa de marketing
4. **dev-commands.sh** - Comandos útiles para testing

---

## 🚀 PRÓXIMO PASO

👉 **Lee SETUP.md y sigue los pasos**

Si tienes dudas específicas:
1. Busca en SETUP.md (tiene explicaciones detalladas)
2. Corre `test_conversations.py` para ver flujos en acción
3. Check `dev-commands.sh` para debugging

---

## 📞 SOPORTE

Para issues, revisa:
```bash
# Logs en Heroku
heroku logs --tail

# Logs en tu servidor
tail -50 /var/log/chatbot.log

# Database status
source dev-commands.sh
conversion_rate
```

---

**¡Tu sistema de automatización de ventas está listo! 🎉**

Ahora ve a configurar Meta Cloud API y despliega.

Dentro de 48h deberías tener primeros leads llegando a WhatsApp.
