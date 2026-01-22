# WhatsApp Business Ice Breaker Setup Guide

## Overview
Cómo usar WhatsApp Business para recibir contactos y empezar conversaciones naturales que califiquen y conviertan leads automáticamente.

---

## 1. SETUP: WhatsApp Business Configuration

### 1.1 WhatsApp Business Account Setup

**Prerequisites:**
```
✓ Phone number (dedicate to business, not personal)
  Recomendado: +56 9 1234 5678 (Chile)
✓ Download WhatsApp Business app (iOS/Android)
✓ Meta Business Account created
✓ Business info ready (name, category, description)
```

**Step 1: Create WhatsApp Business Account**
```
1. Download "WhatsApp Business" app
2. Sign up with your business phone number
3. Verify phone with code (SMS)
4. Add business profile:
   - Name: "PVB Estudio Creativo"
   - Category: "Photography/Creative Service"
   - Website: panchovial.com
   - Phone: +56912345678
   - Address: (Optional)
   - Description: "Fotografía y marketing digital de calidad"
```

**Step 2: Link to Meta Business Account**
```
1. Go to Meta Business Suite
2. Settings → Accounts → WhatsApp Business
3. Click "Verify phone" and confirm
4. Link WhatsApp account to Meta Business
```

**Step 3: Enable Message Replies**
```
WhatsApp Business App Settings:
1. Profile → Business tools
2. Activate "Message Templates" (for scheduled messages)
3. Go to Meta Manager → Templates
4. Create 3 templates (see section 1.2)
```

### 1.2 Create Message Templates (Ice Breakers)

WhatsApp Business requires approved templates. Create these:

**Template 1: Initial Greeting (Auto-reply when someone messages first)**
```
Template Name: greeting_initial
Category: WELCOME

Content:
---
Hola 👋 

¡Gracias por escribir a PVB Estudio Creativo!

Soy el asistente de Pancho. Te ayudaré a encontrar 
la solución perfecta para tu proyecto.

¿Qué te interesa?
---

Quick Reply Buttons:
1. "📷 Fotografía (Autos/Caballos)"
2. "📊 Marketing Digital"
3. "📹 Audiovisual"
4. "❓ Sobre PVB"
```

**Template 2: Photography Follow-up**
```
Template Name: photography_inquiry
Category: MARKETING

Content:
---
¡Perfecto, vamos con fotografía! 📸

Para darte la mejor recomendación, necesito entender 
un poco más tu proyecto:

¿Es para autos, caballos, o ambos?
---

Quick Reply Buttons:
1. "🐎 Caballos (Ecuestre)"
2. "🚗 Autos (Automotriz)"
3. "🎬 Audiovisual/Video"
```

**Template 3: Marketing Follow-up**
```
Template Name: marketing_inquiry
Category: MARKETING

Content:
---
Entiendo, marketing digital. 💡

Rápida pregunta: ¿Cuál es tu desafío principal?
---

Quick Reply Buttons:
1. "📉 Mis anuncios no funcionan"
2. "🎯 Quiero mejorar campaña actual"
3. "🚀 Quiero comenzar desde cero"
4. "💬 Otro problema"
```

**How to Create Template in Meta Manager:**
```
1. Go to ads.facebook.com
2. Tools → Message Templates
3. Create Template
4. Name: greeting_initial
5. Content: [paste above text]
6. Add Quick Reply buttons
7. Submit for approval (usually 1-2 hours)
```

### 1.3 Ice Breaker Conversation Strategy

**What is an Ice Breaker?**
- Not robotic ("Thanks for contacting us...")
- Natural, conversational tone
- Shows you're human/real business
- Asks engaging questions
- Has personality (matches brand)

**Your Ice Breaker Script:**

```
FIRST MESSAGE (When user writes first):
Bot: "Hola 👋 ¡Gracias por escribir!"

TONE: Friendly, warm, genuine
NOT: "Bienvenido a nuestro servicio automático..."
YES: "Gracias por escribir! Soy el asistente de Pancho"

KEY: Acknowledge them personally
"Veo que te interesa en fotos de calidad para tu [auto/caballo]..."

ENGAGE: Ask specific questions (not yes/no)
NOT: "¿Te interesa fotografía?"
YES: "Cuéntame, ¿cuál es el proyecto que tienes en mente?"

BUILD RAPPORT:
"Pancho ha trabajado con gente apasionada por sus autos/
caballos igual que vos. ¿Hace cuánto tienes el tuyo?"
```

---

## 2. HOW THE FLOW WORKS: Ice Breaker Conversation

### 2.1 User Journey (WhatsApp Business Ice Breaker)

```
┌─────────────────────────────────────────┐
│     USER FINDS YOUR WHATSAPP            │
│  (Instagram bio, website, Google, etc)  │
│  Clicks: "Enviar mensaje a PVB"         │
└──────────────┬──────────────────────────┘
               │
               ↓ Opens WhatsApp
               │
┌──────────────────────────────────────────┐
│   USER WRITES FIRST MESSAGE              │
│   (Can be anything: "Hola", "Info", etc)│
└──────────────┬──────────────────────────┘
               │
               ↓ Message arrives at your number
               │
┌──────────────────────────────────────────┐
│ 🎯 ICE BREAKER REPLY (automatic)         │
│                                          │
│ "Hola 👋 ¡Gracias por escribir!          │
│                                          │
│  Soy el asistente de Pancho.            │
│  Te ayudaré a encontrar la solución     │
│  perfecta para tu proyecto.              │
│                                          │
│  ¿Qué te interesa?"                      │
│                                          │
│ [4 Buttons with Quick Replies]           │
└──────────────┬──────────────────────────┘
               │
               ↓ User taps button
               │
┌──────────────────────────────────────────┐
│    CONVERSATION CONTINUES                │
│    Bot asks qualifying questions         │
│    Captures: Type, Budget, Timeline      │
│    Builds rapport (not robotic)          │
└──────────────┬──────────────────────────┘
               │
               ↓ Lead scored
               │
         ┌─────┴─────┐
         │           │
         ↓           ↓
     HOT LEAD    WARM/COLD
     (instant     (follow-up
      to Pancho)   sequence)
```

### 2.2 What Your Bot Does (Automatic)

When a new message arrives from Meta Ads:

```python
# 1. Detect incoming message
webhook_received("Hola")

# 2. Create lead record in database
lead = create_lead(
    phone="56912345678",
    source="meta_ads",  # Track origin
    timestamp=now()
)

# 3. Send greeting
send_message("Hola! 👋 Soy el asistente de PVB")
send_message("¿Qué servicio te interesa?")
show_buttons([
    "📷 Fotografía (Caballos/Autos)",
    "📊 Marketing Digital",
    "📹 Audiovisual",
    "❓ Sobre PVB"
])

# 4. Continue based on choice (Photography Flow, Marketing Flow, etc.)
# 5. Score lead: 0-10 points based on budget/timeline/context
# 6. If HOT (5+ points): Send n8n webhook notification to Pancho
# 7. Save all conversation data for follow-up
```

---

## 3. ICE BREAKER MESSAGING: Natural Conversation Examples

### 3.1 Photography Ice Breaker Conversation

```
USER: "Hola"

BOT (ICE BREAKER): 
"Hola 👋 ¡Gracias por escribir!

Soy el asistente de Pancho. Te ayudaré a encontrar 
la solución perfecta para tu proyecto.

¿Qué te interesa?"

[📷 Fotografía  | 📊 Marketing  | 📹 Audiovisual  | ❓ Sobre PVB]

USER: [Clicks "Fotografía"]

BOT:
"¡Perfecto, vamos con fotografía! 📸

Para darte la mejor recomendación, necesito entender 
un poco más tu proyecto:

¿Es para autos, caballos, o ambos?"

[🐎 Caballos  | 🚗 Autos  | 🎬 Audiovisual]

USER: [Clicks "Autos"]

BOT:
"Excelente, autos 🚗

Pancho ha trabajado con gente muy apasionada 
por sus máquinas, igual que vos.

¿Cuántos autos son en el proyecto?"

[1 auto  | 2-5 autos  | 10+ autos  | No sé aún]

USER: "3 autos"

BOT:
"Perfecto, 3 autos es un proyecto interesante.

Cuéntame: ¿Para qué necesitas las fotos?
¿Oficina, galería personal, Instagram, promoción?"

[Para mi casa/oficina  | Para Instagram  | Para venta  | Otro]

USER: "Para mi casa"

BOT:
"Hermoso, para tu colección personal. 

Last question: ¿tienes un rango de presupuesto 
en mente para este proyecto?

Ayuda mucho para saber qué opciones te podemos ofrecer."

[Menos de $1000  | $1000-3000  | $3000-10000  | Más de $10000]

USER: "$3000-10000"

BOT (LEAD QUALIFICATION - BACKGROUND):
[Scoring: +3 for budget, +2 for context clarity = 5 pts = HOT]
[Sends n8n webhook to Pancho NOW]

BOT (TO USER - CLOSING):
"Perfecto, tengo todo. 

Voy a conectarte con Pancho en los próximos minutos.
Él tiene experiencia con colecciones de autos de calidad 
y te va a contar exactamente qué opciones tienes.

Tu número es: +56912345678, ¿correcto?"

USER: "Sí, ese es"

BOT:
"Listo! Pancho te escribe en menos de 5 minutos.

Mientras, le envío tu info para que esté preparado.
¿Hay algo más que quieras que sepa?"

USER: "No, espero su mensaje"

[Conversation pauses until Pancho replies]

PANCHO (3 mins later):
"¡Hola! Soy Pancho, acabo de ver tu proyecto.
3 autos, fotos de calidad para tu colección... 

Me encanta este tipo de trabajo. ¿Podemos hacer 
una rápida llamada para verte el proyecto y saber 
qué tan viables son las fechas?"
```

### 3.2 Marketing Ice Breaker Conversation

```
USER: "Tengo problemas con mis anuncios"

BOT (ICE BREAKER):
"Hola! Entiendo completamente, es súper común.

Soy el asistente de Pancho. Te voy a hacer algunas 
preguntas rápidas para conectarte con la solución exacta 
que necesitas.

¿Cuál es tu desafío principal?"

[Anuncios no funcionan  | Mejorar actual  | Empezar cero  | Otro]

USER: [Clicks "Anuncios no funcionan"]

BOT:
"Listo, sabemos exactamente qué sucede en esos casos.

¿Dónde estás gastando dinero ahora? ¿Meta Ads, Google, 
ambas, o algo más?"

[Meta Ads  | Google  | Ambas  | Otra plataforma]

USER: "Meta Ads"

BOT:
"Perfecto, ese es el fuerte de Pancho.

Pregunta rápida: ¿cuánto estás gastando 
mensualmente en Meta?"

[Menos de $500  | $500-1000  | $1000-2000  | Más de $2000]

USER: "$800"

BOT:
"Dale, $800/mes nos da idea clara.

¿Hace cuánto tienes estas campañas activas?"

[Menos de 1 mes  | 1-3 meses  | 3-6 meses  | Más de 6 meses]

USER: "3 meses"

BOT:
"Okay, 3 meses gastando sin buenos resultados 
es frustrante, entiendo.

Último dato: ¿qué tipo de negocio es? 
(p.ej. e-commerce, servicios, B2B, etc)"

[E-commerce  | Servicios  | B2B  | Consultoría  | Otro]

USER: "E-commerce"

BOT (LEAD QUALIFICATION - BACKGROUND):
[Scoring: +3 for budget, +2 for campaign history = 5 pts = HOT]
[Sends n8n webhook to Pancho NOW]

BOT (TO USER - CLOSING):
"Perfecto, acabo de pasar tu info a Pancho.

Tiene experiencia exacta con este tipo de problemas 
en e-commerce. Va a contactarte en los próximos minutos 
con soluciones concretas.

¿Tu número es +56912345678?"

USER: "Sí"

BOT:
"Listo. Pancho te escribe en breve.

¿Hay algo más que debería saber de tu negocio?"

USER: "No, gracias"

BOT:
"¡Gracias por confiar en PVB! 
Hablamos en un toque."

[Conversation pauses until Pancho replies]

PANCHO (5 mins later):
"¡Hola! Acabo de ver tu caso: e-commerce, Meta Ads, 
3 meses sin resultados. 

En muchos casos es un problema de copy o targeting, 
fácil de arreglar. ¿Podemos ver rápidamente 
qué está pasando en tus anuncios?"
```

---

## 4. TECHNICAL SETUP: Connect Your Bot to WhatsApp Business

### 4.1 Bot Deployment

Your bot is deployed on:
```
Heroku:    https://pvb-whatsapp-bot.herokuapp.com
Railway:   https://pvb-bot.railway.app
DigitalOcean: https://bot.panchovial.com
```

Webhook endpoint:
```
POST https://[YOUR_DOMAIN]/webhook/messages
```

### 4.2 Configure Webhook in Meta

**Step 1: Get Webhook URL**
```
Production URL: https://your-domain.com/webhook/messages
Verify Token: (Generate random: openssl rand -hex 32)
```

**Step 2: Add Webhook in Meta Manager**
```
1. Go to Meta Business Suite
2. Tools → Webhooks
3. Select WhatsApp → Phone number
4. Set Webhook URL: https://your-domain.com/webhook/messages
5. Verify Token: [your-token]
6. Click "Verify and Save"
```

**Step 3: Subscribe to Events**
```
Webhooks to subscribe:
✓ messages
✓ message_template_status_update
✓ message_status
✓ read_receipts
```

### 4.3 Test Connection

```bash
# Verify webhook is live:
curl -X POST https://your-domain.com/webhook/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [ACCESS_TOKEN]" \
  -d '{
    "object": "whatsapp_business_account",
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "56912345678",
            "text": {"body": "Test message"}
          }]
        }
      }]
    }]
  }'
```

Expected: `200 OK`

---

## 5. TRACKING: How to Monitor Performance

### 5.1 What Gets Tracked Automatically

**In your database:**
```sql
-- Every conversation is logged:
SELECT * FROM leads WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY);

-- Shows:
- Phone number
- Initial message timestamp
- Which service they selected
- Full conversation history
- Lead quality score
- Contact info captured
- Response from Pancho
```

**In WhatsApp Business:**
```
WhatsApp Manager → Conversations
Shows:
- Total messages received
- Messages sent
- Average response time
- Read receipts
- Chat status
```

### 5.2 Key Metrics to Monitor

```
DAILY TRACKING:
✓ New messages received (from WhatsApp)
✓ Average response rate (bot reply speed)
✓ Conversation completion (% reaching Pancho notification)
✓ Lead quality distribution (HOT vs WARM vs COLD)

WEEKLY METRICS:
✓ Total leads captured
✓ HOT leads (should be 30-50%)
✓ Average time Pancho responds
✓ Consultation bookings
✓ Chat response quality (are people happy?)

MONTHLY ANALYSIS:
✓ Cost per lead (if using ads to drive traffic)
✓ Cost per consultation booked
✓ Conversion rate (lead → customer)
✓ Average deal value
✓ Return on ad spend (if applicable)
```

### 5.3 View Data in Dashboard

**Check daily:**
```sql
-- Show new leads from last 24 hours
SELECT 
  phone,
  created_at,
  lead_score,
  lead_quality,
  service_type,
  budget_mentioned
FROM leads
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 DAY)
ORDER BY created_at DESC;

-- Show HOT leads needing immediate action
SELECT 
  phone,
  service_type,
  budget_mentioned,
  created_at
FROM leads
WHERE lead_quality = 'HOT'
  AND pancho_replied IS NULL
  AND created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR);
```

**WhatsApp Business Dashboard:**
```
1. Open WhatsApp Business app
2. Settings → Dashboard
3. See:
   - Total conversations
   - Response time
   - Quality rating
   - Message analytics
```

---

## 6. OPTIMIZATION: Improve Your Ice Breaker

### 6.1 A/B Test Ice Breaker Messages

**Test 1: Opening Tone**

```
VERSION A (Professional):
"Hola, soy el asistente de Pancho de PVB Estudio Creativo.
¿En qué puedo ayudarte?"

VERSION B (Friendly - Current):
"Hola 👋 ¡Gracias por escribir!
Soy el asistente de Pancho. Te ayudaré a encontrar 
la solución perfecta para tu proyecto."

VERSION C (Casual):
"¡Ey! Gracias por escribir.
Pancho está aquí para ayudarte con tu proyecto.
¿Qué necesitas?"

MEASURE:
- Which version gets more button clicks?
- Which leads to higher-quality conversations?
- Keep the best performer
```

**Test 2: Call-to-Action Buttons**

```
VERSION A (Service-focused):
📷 Fotografía | 📊 Marketing | 📹 Audiovisual | ❓ Info

VERSION B (Problem-focused):
🎯 Mis anuncios no funcionan
🎨 Quiero fotos de calidad
💡 Otra consulta
ℹ️ Conocer PVB

MEASURE:
- Which buttons get clicked more?
- Do problem-focused buttons lead to HOT leads?
```

### 6.2 Improve Conversation Flow

**If users say "No thanks":**
```
Don't just die the conversation.

ADD: "¿Hay algo específico que buscabas? 
Puedo resolver dudas sin compromiso."
```

**If users ask "How much?":**
```
Don't quote prices immediately.

INSTEAD: "Depende mucho del proyecto.
¿Me cuentas qué tienes en mente?"

Then qualify before quoting.
```

**If users go silent:**
```
After 30 mins of no response, send:
"¿Seguimos? Tengo dudas claras que 
Pancho puede resolver en 2 minutos."
```

### 6.3 Retargeting & Follow-up

**For WARM leads (not hot yet):**
```
After 1 hour (if no purchase signal):
"Pancho acaba de liberar una ventana 
para consultas. ¿Te queda bien una 
llamada de 15min mañana?"
```

**For COLD leads (low budget/interest):**
```
Add to nurture sequence:
- Day 1: Initial contact
- Day 3: Share portfolio piece
- Day 7: Share client testimonial
- Day 14: Limited-time offer or reactivation
```

---

## 7. TROUBLESHOOTING

### 7.1 Ice Breaker Not Showing Up

**Problem: User writes message but no auto-reply**

**Check:**
```
1. Is WhatsApp Business linked to Meta?
   Go to Meta Manager → Settings → Accounts
2. Are templates approved?
   Go to Meta Manager → Templates → Check status
3. Is webhook receiving messages?
   Check server logs: grep "webhook" logs/*.log
4. Is response rate limiting kicking in?
   WhatsApp blocks if >10% messages fail
```

**Solution:**
```
# Verify webhook is responding
curl -v https://your-domain.com/webhook/messages

# Check template approval
# Go to Meta Manager and resend approval if needed

# Restart bot
pm2 restart pvb-whatsapp-bot

# Check rate limits
# Ensure response time < 5 seconds
```

### 7.2 Template Approval Stuck

**Problem: Template not approved after 24 hours**

**Why:**
- Low-quality template text
- Too promotional/spammy
- Grammar issues
- Policy violation

**Fix:**
```
1. Go to Meta Manager → Templates
2. Look for rejection reason
3. Edit and resubmit:

GOOD: "Hola 👋 ¡Gracias por escribir!"
BAD: "🎉 GET FREE CONSULTATION NOW!!! 🎉"

GOOD: "Soy el asistente de Pancho"
BAD: "PANCHO WILL MAKE YOU RICH!!!"

GOOD: "¿Qué te interesa?"
BAD: "CLICK HERE OR YOU'LL REGRET IT"
```

### 7.3 Messages Not Going Through

**Problem: Bot messages not reaching user**

**Check:**
```
1. User blocked your number?
   Ask them to unblock and try again
2. Your WhatsApp Business account suspended?
   Check WhatsApp Manager → Health
3. Template not approved?
   Can only send approved templates
4. User's data limit?
   WhatsApp requires active internet
```

**Solution:**
```
- Check WhatsApp account health
- Reapprove templates if rejected
- Ask user to check WhatsApp settings
- Send message directly from your phone first (test)
```

### 7.4 Lead Scoring Broken

**Problem: All leads showing as COLD**

**Check:**
```python
# In app/config/pvb_services.py:
LEAD_SCORING_WEIGHTS = {
    'budget_mentioned': {
        '<1000': 1,
        '1000-3000': 2,
        '3000-10000': 3,  # ← Check these
        '>10000': 3
    },
    'conversation_depth': {...}
}
```

**Fix:**
```python
# Verify lead scoring is being called
print(f"Lead score: {lead.lead_score}")  # Should show number

# Check if budget is being captured
print(f"Budget: {lead.budget_mentioned}")  # Should show value

# Recalculate if needed
from app.flows.lead_router import score_lead
new_score = score_lead(lead)
```

---

## 8. QUICK START CHECKLIST

```
SETUP (Day 1):
☐ Download WhatsApp Business app
☐ Create account with business number
☐ Link to Meta Business Account
☐ Create 3 message templates
☐ Submit templates for approval
☐ Deploy bot (Heroku/Railway)
☐ Get webhook URL

CONFIGURATION (Day 2):
☐ Configure webhook in Meta Manager
☐ Test webhook connection
☐ Subscribe to webhook events
☐ Create n8n notification webhook
☐ Test end-to-end (send message from personal phone)

LAUNCH (Day 3):
☐ Add WhatsApp link to Instagram bio
☐ Share WhatsApp contact on website
☐ Share in email signature
☐ Monitor first conversations
☐ Adjust ice breaker based on feedback

OPTIMIZATION (Week 2+):
☐ Review HOT vs WARM vs COLD distribution
☐ A/B test ice breaker messages
☐ Improve bot questions based on common replies
☐ Track Pancho's response time
☐ Monitor conversion rate (message → consultation)
```

---

## 9. EXAMPLE: Complete Ice Breaker Conversation Flow

**Scenario: María finds your WhatsApp link on Instagram**

```
TIME    EVENT                           WHAT'S HAPPENING
────────────────────────────────────────────────────────────────
11:45   María clicks your WhatsApp link Ice breaker is armed
        in Instagram bio               (ready to deploy)

11:46   WhatsApp opens on her phone    Pre-filled with:
        She writes: "Hola"             "Hola" to your number

11:47   Message arrives at your bot    Bot webhook receives:
                                       - Phone: +56912345678
                                       - Text: "Hola"
                                       - Timestamp: 11:47

11:47   🎯 ICE BREAKER FIRES            Bot sends:
                                       "Hola 👋 ¡Gracias por escribir!
                                        Soy el asistente de Pancho..."
                                       [4 buttons appear]

11:48   María clicks "📷 Fotografía"   Bot logs: photography service
                                       Sends next question with buttons

11:49   María: "Autos"                  Bot logs: automotive
                                       Asks: "¿Cuántos autos?"

11:52   María: "3 autos, 
        aprox $3500"                    BOT SCORES:
                                       +3 (budget $3-10k)
                                       +2 (clear context)
                                       Total: 5 pts = 🔥 HOT

11:52   HOT lead detected              n8n webhook fires to Pancho:
                                       {
                                         "lead_id": "456",
                                         "phone": "+56912345678",
                                         "quality": "HOT",
                                         "service": "Photography",
                                         "details": "3 cars, $3500"
                                       }

11:53   Pancho's phone vibrates         n8n notification:
        (WhatsApp + Push alert)         "🔥 HOT: María, autos, $3500"

11:55   Pancho replies to María         Bot asks: "¿Algo más que quiera
                                        que sepa?"

12:00   María: "Listo, espero tu
        llamada"                         Bot confirms:
                                         "Gracias María! Pancho 
                                          te contacta en poco."

12:02   PANCHO TAKES OVER               "¡Hola María! Acabo de ver
                                         tu proyecto - 3 autos, 
                                         fotos de colección...
                                         ¿Podemos hacer una 
                                         llamada para verlo?"

12:05   CONSULTATION SCHEDULED          ✓ Lead qualified
                                         ✓ In Pancho's follow-up queue
                                         ✓ Ready to close
```

**Key Metrics from This Interaction:**
```
- Time from click to HOT lead: 7 minutes
- Time from HOT to Pancho notification: 0 seconds
- Time from notification to Pancho reply: 3 minutes
- Quality: High (clear budget, specific project)
- Likelihood to book: ~70% (HOT lead)

11:53   Pancho receives notification   WhatsApp from n8n:
        on his phone                   "🔥 HOT LEAD: María
                                        +56912345678
                                        Autos, $3500 budget"

11:55   Pancho replies to María        "Hola María! Perfecto,
                                        tengo experiencia con
                                        varias colecciones...
                                        ¿Podemos agendar
                                        una llamada?"

12:00   María: "Sí! Mañana a las 3?"   Lead moves to
                                        consultation phase
```

**Result:**
- Ad cost: ~$2.00
- Lead quality: HOT (will likely convert)
- Time to Pancho notification: 5 seconds
- Time to Pancho response: 3 minutes
- Consultation scheduled: ✓

---

## 9. FURTHER READING

- [Meta Ads Messages Campaign Docs](https://www.facebook.com/business/help)
- [WhatsApp Business API Setup](https://www.whatsapp.com/business/api)
- [WhatsApp Webhook Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks)
- Back to: [README_CUSTOMIZED.md](README_CUSTOMIZED.md)
- Bot Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Services: [SERVICES_REFERENCE.md](SERVICES_REFERENCE.md)
