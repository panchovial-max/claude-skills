# Estrategia Instagram → WhatsApp → Ventas

## Objective
Convertir seguidores de Instagram en clientes usando WhatsApp como canal de calificación automática.

---

## 1. INSTAGRAM STRATEGY

### 1.1 Bio Optimization
```
🎨 Fotografía Fine Art | 🎬 Producción | 🤖 Marketing Digital

📱 WhatsApp: [Link a Bot]
🌐 www.panchovial.com
```

**Call-to-Action Button:**
- Type: "Contacta por WhatsApp"
- Enlaza a: `https://wa.me/56912345678`

### 1.2 Content Strategy (30 días)

**Semana 1-2: Portfolio Showcase**
- Posts: 3-4 fotos de proyectos fine art (ecuestre, automotriz)
- Stories: Behind-the-scenes de shoots
- Caption: "Nuevo proyecto en galería X"
- CTA: "Consulta disponible en WhatsApp"

**Semana 3: Introduce Services**
- Carousel post: Tier 1 / Tier 2 / Tier 3 / Tier 4 servicios
- Reel: "¿Qué servicio necesitas?" (3 opciones)
- Story Poll: "¿Fotografía o Marketing?"
- CTA: Link a WhatsApp

**Semana 4: Social Proof + Offer**
- Testimonial posts (si tienes clientes previos)
- Staticpost: "$600 AI Ad Generation trial" 
- Story highlight: "Servicios disponibles"
- Reel: "Cómo funciona la consulta"

### 1.3 Hashtag Strategy
```
#FotografiaFineArt #FotografiaEcuestre #FotografiaAutomotriz
#ProduccionAudiovisual #MarketingDigital #EstudioCreativo
#ArtDirection #PhotographyStudio #ContenidoCreativo
```

### 1.4 Ad Campaign (Opcional - $5-10/día)

**Campaign Objective:** "Messages"

**Target:**
- Chile, Argentina, México
- 30-65 años (directores creativos, empresarios)
- Intereses: Fotografía, Branding, Marketing, Negocios

**Creative:**
- Imagen: Tu mejor fotografía fine art
- Headline: "Transforma tu marca con arte"
- Body: "Consulta gratis sobre tu proyecto. Disponible en WhatsApp"
- Button: "Enviar mensaje"

---

## 2. WhatsApp BOT FUNNEL

### 2.1 Lead Journey Map

```
Instagram Bio
    ↓
Tocan "Enviar WhatsApp"
    ↓
✨ Greeting: "¿Qué servicio te interesa?"
    ↓
╔═══════════════════════════════════════╗
║  Branch 1: Fotografía/Video           ║
║  ├─ Tipo proyecto (4 preguntas)       ║
║  ├─ Timeline & Presupuesto            ║
║  └─ Lead Quality: HOT/WARM/COLD       ║
║                                       ║
║  Branch 2: Marketing                  ║
║  ├─ Problema a resolver (4 preguntas) ║
║  ├─ Análisis de gasto actual          ║
║  └─ Recomendación: $600 o Premium     ║
╚═══════════════════════════════════════╝
    ↓
💾 Captura datos (Nombre, Email, Empresa)
    ↓
📊 Calificación automática
    ↓
🤝 Handoff a Pancho (n8n notification)
    ↓
⏰ Follow-up automático 24h
    ↓
📞 Pancho agenda call
```

### 2.2 Conversion Metrics

**Objetivo:**
- 10% de conversión (Instagram followers → WhatsApp message)
- 40% calificación (mensaje → lead cualificado)
- 20% cierre (lead → venta)

**Ejemplo con 1,000 seguidores:**
```
1,000 seguidores
  × 10% conversion = 100 mensajes
  × 40% qualification = 40 leads
  × 20% close = 8 ventas
```

---

## 3. CONTENIDO DE MENSAJES

### 3.1 Respuestas del Bot (por categoría)

#### FOTOGRAFÍA/VIDEO
```
Bot: "¿Qué tipo de proyecto te interesa?

🐴 Fotografía Ecuestre (Fine Art / Galerías)
🏎️ Fotografía Automotriz (Cinematográfica)
📸 Otro tipo de fotografía
🎬 Producción de Video"

User selecciona ↓

Bot: "¿Es para una galería, marca, o uso personal?"

Bot: "¿Tienes fecha tentativa? (ej: Febrero, Q2 2026)"

Bot: "¿Cuál es tu presupuesto aproximado?
💰 <$5,000 USD
💰💰 $5,000 - $15,000 USD
💰💰💰 $15,000 - $50,000 USD
💰💰💰💰 >$50,000 USD"
```

#### MARKETING
```
Bot: "¿Qué problema quieres resolver?

📈 Más ventas
👥 Más leads  
🎯 Mejor presencia en redes
🔄 Optimizar campañas existentes"

User selecciona ↓

Bot: "¿Ya tienes campañas activas en Meta Ads?"

Bot: "¿Cuánto inviertes actualmente en publicidad?
💵 <$500/mes
💵💵 $500-$2,000/mes
💵💵💵 $2,000-$10,000/mes
💵💵💵💵 >$10,000/mes"

Bot: "Recomendación:
💡 Si presupuesto bajo → $600 AI Ad Generation
💡 Si presupuesto alto → $2,800-$6,500 Premium Package"
```

### 3.2 Follow-up automático (n8n - 24h después)

**Para HOT leads:**
```
Pancho (WhatsApp):
"¡Hola {Name}! 🔥

Vi tu proyecto de {service}. 
Tengo algunos insights sobre presupuesto y timeline.

¿Podemos agendar 15min mañana a las [times]?

https://calendly.com/pancho"
```

**Para WARM leads:**
```
Pancho (Email):
"Hola {Name},

Gracias por tu interés en {service}.

Aquí está el desglose de opciones:
✓ Consulta básica: $600
✓ Paquete completo: $2,800-$6,500

¿Cuál resuena contigo?

Estoy disponible para una llamada si tienes preguntas.

Pancho
PVB Estudio Creativo"
```

---

## 4. ANALYTICS & OPTIMIZATION

### 4.1 Métricas clave

| Métrica | Meta | Cálculo |
|---------|------|---------|
| Reach (Instagram) | 1K+ | Posts × engagement |
| CTR (Click-to-WhatsApp) | 5-10% | Links clicked / impressions |
| Message Rate | 10-20% | Leads que envían primer mensaje |
| Qualification Rate | 40%+ | Leads que completan flujo |
| Conversion Rate | 15-25% | Leads → Clientes |
| Avg. Deal Value | $2,500 | Presupuesto promedio |

### 4.2 Dashboard (n8n o Metabase)

```
📊 Daily Stats
├─ New leads: X
├─ Qualified leads: Y
├─ Hot leads: Z
└─ Messages sent: W

💰 Revenue
├─ Pipeline value: $X
├─ Closed deals: $Y
└─ Avg deal: $Z

⏱️ Funnel
├─ Message → Qualified: X%
├─ Qualified → Call: Y%
└─ Call → Deal: Z%
```

### 4.3 A/B Testing

**Test 1: Instagram Bio Copy**
- Opción A: "Consulta en WhatsApp 💬"
- Opción B: "Envía propuesta de proyecto aquí 👇"
- Medir: CTR durante 2 semanas

**Test 2: Bot Initial Message**
- Opción A: "¿Qué servicio te interesa?"
- Opción B: "¿En qué te podemos ayudar?"
- Medir: Completion rate

**Test 3: Follow-up Timing**
- Opción A: Follow-up 24h
- Opción B: Follow-up 48h
- Medir: Response rate

---

## 5. PLAYBOOK DE PANCHO (Manual)

### 5.1 Cuando recibe notificación de Lead HOT 🔥

1. **Inmediatamente (< 1 hora):**
   - Lee el brief del lead
   - Abre WhatsApp (no el bot, tú directamente)
   - Envía: "¡Hola {Name}! Vi tu proyecto de {service}. Déjame compartirte algunas ideas..."

2. **Próximas 24 horas:**
   - Agenda llamada via Calendly link
   - Prepara propuesta de proyecto
   - Busca portfolio similar a su estilo

3. **En la llamada:**
   - 5 min: Rapport + escuchar proyecto
   - 10 min: Present relevant services + pricing
   - 5 min: Siguiente steps

### 5.2 Cuando recibe Lead WARM 🟡

1. **Próximas 48 horas:**
   - Email personalizado con insights
   - Incluir case study relevante
   - Offer: "Consulta gratis 30min"

2. **Si responden:**
   - Agendar call
   - Preparar propuesta

### 5.3 Cuando recibe Lead COLD 🔵

1. **Día 3:**
   - n8n auto-envía email con $600 offer
   - CTA: "Trial con IA Ad Generation"

2. **Si no responden:**
   - Day 7: Otro email
   - Day 14: Último email antes de marcar como "lost"

---

## 6. PRÓXIMAS FASES

### Fase 2 (Mes 2): Expand
- [ ] Agregar TikTok/YouTube funnels (misma bot)
- [ ] Implementar chatbot en website
- [ ] Crear lead nurture email sequence

### Fase 3 (Mes 3): Scale
- [ ] Escalar ads budget a $50-100/día
- [ ] Referral program (leads que refieren amigos)
- [ ] Affiliate partnerships

### Fase 4 (Mes 4+): Optimize
- [ ] Hired segundo sales person?
- [ ] Automatizar más del handoff
- [ ] Integrate con Stripe para pagos

---

**Start Date:** Jan 20, 2026
**Expected Leads/Month:** 30-50
**Expected Closes/Month:** 5-10
**Expected Revenue/Month:** $12,500 - $25,000+
