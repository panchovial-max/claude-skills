# E-Commerce Photography Flow - Updated

## New Flow Diagram

```
USER ENTERS PHOTOGRAPHY FLOW
│
├─ "Ecuestre" / "Automotriz" / "Video"
│  └─ [Context question]
│     └─ location → date → budget → contact
│
└─ "E-commerce" / "Productos"
   ├─ PHOTOGRAPHY_CONTEXT_ECOMMERCE
   │  "¿Para qué necesitas las fotos?"
   │  [Tienda online | Catálogo | Redes | Lanzamiento]
   │
   ├─ PHOTOGRAPHY_PRODUCTS
   │  "¿Cuántos productos necesitas fotografiar?"
   │  [1-5 | 6-15 | 16-50 | +50]
   │
   ├─ PHOTOGRAPHY_PRODUCT_ANGLES (NEW!)
   │  "¿Qué estilos de fotos necesitas para cada producto?"
   │  │
   │  ├─ Pack básico (3 fotos)
   │  │  • Frente
   │  │  • 3/4
   │  │  • Lado
   │  │
   │  └─ Pack completo (5 fotos)
   │     • Frente
   │     • 3/4
   │     • Lado
   │     • Detalle (zoom)
   │     • Lifestyle (en contexto)
   │
   └─ date → budget → contact
```

---

## Conversation Example

```
BOT: "¿Qué tipo de proyecto tienes en mente?"
     [🐴 Ecuestre] [🚗 Automotriz] [🛍️ E-commerce] [🎬 Video]

USER: [Clicks E-commerce]

BOT: "La fotografía de productos para e-commerce es crucial para vender online.
      Pancho crea imágenes de alta calidad que muestran tus productos 
      de la mejor manera, aumentando conversiones y atrayendo clientes.
      
      ¿Para qué necesitas las fotos de productos?
      [🛒 Tienda online] [📦 Catálogo] [📱 Redes sociales] [🎯 Lanzamiento]"

USER: "Tienda online"

BOT: "¿Cuántos productos necesitas fotografiar?
      [📦 1-5] [📦📦 6-15] [📦📦📦 16-50] [📦📦📦📦 +50]"

USER: "20 productos"

BOT: "¿Qué estilos de fotos necesitas para cada producto?
      
      📸 Pack básico (3 fotos)
         • Frente
         • 3/4
         • Lado
      
      📸📸 Pack completo (5 fotos)
         • Frente
         • 3/4
         • Lado
         • Detalle (zoom)
         • Estilo/Lifestyle (en contexto)
      
      [Pack básico (3)] [Pack completo (5)] [Ambos]"

USER: "Pack completo (5)"

BOT: "Perfecto! 20 productos con 5 fotos cada uno.
      📅 ¿Tienes una fecha tentativa para el proyecto?"

USER: "Febrero"

BOT: "¿Tienes un presupuesto aproximado en mente?
      [💰 <$1k] [💰 $1-3k] [💰 $3-10k] [💰💰 >$10k]"

USER: "$5000"

BOT: "Perfecto. Para poder contactarte necesitamos algunos datos...
      [Capture: Name, Email, Phone]"

[Lead is qualified and scored based on:
 - Product count (20 = medium-high)
 - Pack selected (5 = premium)
 - Budget ($5k = substantial)
 - Context (Tienda online = commercial)]

BOT (to Pancho): "🔥 HOT LEAD: E-commerce, 20 productos, Pack 5, $5k"
```

---

## Files Updated

```
✅ app/config/pvb_services.py
   - PHOTOGRAPHY_PRODUCT_ANGLES (NEW)
   - Line: "¿Qué estilos de fotos necesitas para cada producto?"

✅ app/flows/conversation_engine.py
   - Imports: PHOTOGRAPHY_PRODUCT_ANGLES (added)
   - Flow: products → angles → date (NEW step: 'angles')
   - Quick replies: ['Pack básico (3)', 'Pack completo (5)', 'Ambos']

✅ SERVICES_REFERENCE.md
   - E-commerce section updated with new questions
   - Pricing note about pack selection
   - Lead scoring consideration
```

---

## Conversation Steps Comparison

### Ecuestre / Automotriz / Video
```
Type → Context → Location → Date → Budget → Contact
```

### E-commerce (NEW)
```
Type → Context → Products → Angles → Date → Budget → Contact
```

---

## Key Changes

1. **Replaces "¿Dónde se realizaría?"** (location)
   - Only asked for Ecuestre/Automotriz/Video
   - E-commerce doesn't need location (studio or online)

2. **Adds Photo Style Options**
   - Basic: 3-angle shots (front, 3/4, side)
   - Premium: 5-angle shots (basic + detail + lifestyle)
   - Helps qualify budget and scope

3. **Lead Scoring Enhancement**
   - E-commerce leads with 5-photo pack and large quantity = higher budget
   - More qualified leads for high-value projects

---

## Example Pricing Calculations

```
20 products × 3 photos × $50/product = $3,000 (basic pack)
20 products × 5 photos × $100/product = $10,000 (complete pack)

50 products × 5 photos × $150/product = $37,500 (bulk, premium)
```

These are estimates - final quote depends on additional factors (studio rental, props, post-processing, etc).

---

## Next Steps

1. Test with real users to validate pack preferences
2. Track which pack (3 vs 5) is more popular
3. Monitor average project values (basic vs complete)
4. Consider adding "Customized" pack option if needed
5. Build e-commerce portfolio examples to show on panchovial.com
