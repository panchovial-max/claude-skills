# E-Commerce Photography Feature Added

## Overview
Se agregó un nuevo tipo de fotografía: **E-commerce** para tiendas online y emprendedores digitales.

---

## Changes Made

### 1. `app/config/pvb_services.py`

**Updated:** `PHOTOGRAPHY_TYPE_ES` message
- Added: 🛍️ Fotografía de productos (e-commerce)

**New:** `PHOTOGRAPHY_CONTEXT_ECOMMERCE` message
```
La fotografía de productos para e-commerce es crucial para vender online.

Pancho crea imágenes de alta calidad que muestran tus productos de la mejor manera, 
aumentando conversiones y atrayendo clientes.

¿Para qué necesitas las fotos de productos?
🛒 Para tu tienda online
📦 Para catálogo de precios
📱 Para Instagram y redes
🎯 Para lanzamiento de productos
```

**New:** `PHOTOGRAPHY_PRODUCTS` message
```
¿Cuántos productos necesitas fotografiar?

📦 1-5 productos
📦📦 6-15 productos
📦📦📦 16-50 productos
📦📦📦📦 Más de 50 productos
```

### 2. `app/flows/conversation_engine.py`

**Updated imports:**
- Added: `PHOTOGRAPHY_CONTEXT_ECOMMERCE`
- Added: `PHOTOGRAPHY_PRODUCTS`

**Updated conversation flow:**
- New condition: `elif user_input and 'ecommerce' in user_input.lower() or 'productos' in user_input.lower()`
- Routes to: `'next_step': 'products'`
- Returns E-commerce context with 4 options

**New step:** `elif current_step == 'products'`
```python
Captures: self.data['context'] = user_input
Shows: PHOTOGRAPHY_PRODUCTS message
Next step: 'location'
Saves: self.data['product_count'] = user_input
```

**Updated:** `elif current_step == 'location'` for e-commerce flow
- Now captures product count before location

### 3. `SERVICES_REFERENCE.md`

**New section:** E-commerce (Product Photography)
```markdown
### E-commerce (Product Photography)
- **Especialidad**: Fotografía de productos de alta calidad para vender online
- **Para quién**: Tiendas online, pequeños negocios, emprendedores
- **Approach**: Imágenes limpias, profesionales y optimizadas para conversión
- **Portfolio**: panchovial.com
- **Contexts**:
  - Tienda online (Shopify, WooCommerce, etc)
  - Catálogo para distribuidores
  - Instagram y redes sociales
  - Campaña de lanzamiento
- **Key Questions**: ¿Cuántos productos?
- **Typical Pricing**: $50-200 por producto
- **Timeline**: 1-3 semanas según cantidad
```

---

## Conversation Flow Example

```
USER: "Hola, tengo una tienda online"

BOT: "¿Qué tipo de proyecto tienes en mente?"
     [🐴 Ecuestre] [🚗 Automotriz] [🛍️ E-commerce] [🎬 Video]

USER: [Clicks "E-commerce"]

BOT: "La fotografía de productos para e-commerce es crucial...
      ¿Para qué necesitas las fotos?
      [Tienda online] [Catálogo] [Redes sociales] [Lanzamiento]"

USER: [Clicks "Tienda online"]

BOT: "¿Cuántos productos necesitas fotografiar?
      [1-5] [6-15] [16-50] [+50]"

USER: "16-50"

BOT: "Perfecto, 16-50 productos. ¿Dónde se realizaría el proyecto?"

[Conversation continues: location → date → budget → contact]
```

---

## Lead Scoring Updates

E-commerce leads get scored based on:
- **Product count**: 1-5 (small), 6-15 (medium), 16-50 (large), 50+ (bulk)
- **Context**: Tienda online, Catálogo, Redes, Lanzamiento
- **Budget**: Same tiers as other photography ($1k-$10k+)

---

## Files Modified

```
✅ app/config/pvb_services.py
   - PHOTOGRAPHY_TYPE_ES (updated)
   - PHOTOGRAPHY_CONTEXT_ECOMMERCE (new)
   - PHOTOGRAPHY_PRODUCTS (new)

✅ app/flows/conversation_engine.py
   - Imports (updated)
   - context_or_type flow (updated)
   - products step (new)
   - location flow (updated for products)

✅ SERVICES_REFERENCE.md
   - E-commerce section (new)
```

---

## Testing

**To test the flow manually:**

```
1. Send: "Hola"
2. Bot shows photography options
3. Send: "E-commerce" or "Productos"
4. Bot shows PHOTOGRAPHY_CONTEXT_ECOMMERCE
5. Send: "Tienda online"
6. Bot shows PHOTOGRAPHY_PRODUCTS with options
7. Send: "16-50"
8. Continue with location, date, budget
```

---

## Next Steps

1. Test with real user on WhatsApp
2. Monitor e-commerce lead quality
3. Consider adding sub-categories:
   - Clothing/fashion products
   - Food/beverages
   - Electronics
   - Artisan/handmade
4. Add e-commerce portfolio examples on panchovial.com

---

## Notes

- E-commerce has additional "products" step between type and location
- Other photography types (Ecuestre, Automotriz, Video) maintain original flow
- Lead scoring compatible with existing system
- Budget pricing for e-commerce: $50-200 per product (can be adjusted)
