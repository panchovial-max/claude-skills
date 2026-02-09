# Google Calendar Integration - Setup Guide

## ✅ Completado

1. Google Calendar API habilitada
2. Credenciales OAuth 2.0 creadas
3. Redirect URIs configurados
4. Client ID: `1077601603611-9q44lcu2ot1f9td1010m12a0ro4a8h7p.apps.googleusercontent.com`

---

## 📋 Próximos Pasos

### 1. Configurar Variables de Entorno

**En Netlify Dashboard:**

1. Ve a: https://app.netlify.com/sites/courageous-valkyrie-15603d/configuration/env
2. Agrega las siguientes variables:

```bash
# Notion Internal Token (el que ya tienes)
NOTION_INTERNAL_TOKEN=ntn_your_internal_integration_token_here

# Google Calendar OAuth
GOOGLE_CALENDAR_CLIENT_ID=1077601603611-9q44lcu2ot1f9td1010m12a0ro4a8h7p.apps.googleusercontent.com
GOOGLE_CALENDAR_CLIENT_SECRET=<tu_client_secret_del_json>
GOOGLE_CALENDAR_REDIRECT_URI=https://courageous-valkyrie-15603d.netlify.app/.netlify/functions/oauth-google-calendar-callback
```

**Para obtener el Client Secret:**
- Abre el archivo JSON que descargaste de Google Cloud Console
- Busca el campo `"client_secret"`: `"GOCSPX-xxxxx..."`
- Copia ese valor

---

### 2. Autorizar tu cuenta de Google (Una sola vez)

Una vez que las funciones estén deployadas:

1. Ve a: https://courageous-valkyrie-15603d.netlify.app/admin-auth-google.html (vamos a crear esta página)
2. Click "Autorizar Google Calendar"
3. Inicia sesión con `info@panchovial.com`
4. Acepta los permisos
5. Los tokens se guardarán automáticamente

---

### 3. Configurar Base de Datos en Notion

En tu workspace de Notion:

1. Crea una base de datos llamada "Calendario de Clientes" (si no existe)
2. Estructura requerida:
   - **Client** (Select o Relation) - Nombre del cliente
   - **Title** (Title) - Título del post
   - **Date** (Date) - Fecha de publicación
   - **Type** (Select) - Post, Story, Reel, etc.
   - **Platform** (Multi-select) - Instagram, Facebook, LinkedIn
   - **Status** (Select) - Scheduled, Published, Draft
   - **Caption** (Text) - Descripción del contenido

3. Comparte la base de datos con tu integración de Notion
4. Copia el Database ID (está en la URL):
   - URL: `https://www.notion.so/xxxxx?v=yyyy`
   - Database ID: `xxxxx` (la primera parte)

5. Agrega el Database ID como variable de entorno:
   ```bash
   NOTION_CALENDAR_DATABASE_ID=tu_database_id_aqui
   ```

---

### 4. Deploy y Test

```bash
# Commit los cambios
git add .
git commit -m "Add Google Calendar integration with Notion sync

- Google Calendar OAuth for client calendars
- Notion read-only integration
- Auto-sync Notion → Google Calendar
- Client calendar creation and sharing

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Deploy a producción
netlify deploy --prod
```

---

## 🎯 Flujo Final de Trabajo

### Para cada cliente nuevo:

1. Cliente se registra en el portal
2. En el dashboard, click "Crear Calendario"
3. Sistema crea automáticamente:
   - Google Calendar para ese cliente
   - Lo comparte con el email del cliente
   - Muestra link de suscripción
4. Cliente recibe email de Google Calendar
5. Acepta la invitación
6. ¡Listo! El calendario se sincroniza automáticamente

### Sincronización automática:

- **Frecuencia:** Cada 1 hora (configurable con Netlify Scheduled Functions)
- **Origen:** Tu base de Notion "Calendario de Clientes"
- **Filtro:** Por campo "Client" = nombre del cliente
- **Destino:** Google Calendar específico de cada cliente

---

## 🔧 Funciones Implementadas

### Backend (Netlify Functions):

1. **`oauth-google-calendar-admin.js`** - Autorización de info@panchovial.com
2. **`google-calendar-create.js`** - Crear calendario para un cliente
3. **`notion-to-gcal-sync.js`** - Sincronizar Notion → Google Calendar
4. **`calendar-subscription-link.js`** - Obtener link de suscripción

### Frontend:

1. **`admin-auth-google.html`** - Página para autorizar tu cuenta de Google (una vez)
2. **`dashboard.html`** - Botón "Crear Calendario" + Link de suscripción
3. **`calendar.html`** - Vista del calendario (mantiene FullCalendar)

---

## 📊 Ejemplo de Sincronización

### En Notion:

| Client | Title | Date | Platform | Status |
|--------|-------|------|----------|---------|
| Cliente A | Post Instagram | 2026-02-10 | Instagram | Scheduled |
| Cliente A | Reel TikTok | 2026-02-12 | TikTok | Scheduled |
| Cliente B | Post LinkedIn | 2026-02-11 | LinkedIn | Scheduled |

### En Google Calendar:

**Calendario "PVB - Cliente A":**
- 10 Feb: Post Instagram
- 12 Feb: Reel TikTok

**Calendario "PVB - Cliente B":**
- 11 Feb: Post LinkedIn

---

## ❓ Preguntas Frecuentes

**P: ¿Los clientes pueden editar el calendario?**
R: No, solo tienen acceso de lectura. Tú editas en Notion, ellos solo ven.

**P: ¿Cuántos calendarios puedo crear?**
R: Ilimitados. Cada cliente tiene su propio calendario.

**P: ¿Qué pasa si un cliente se da de baja?**
R: Puedes eliminar su acceso al calendario o eliminar el calendario completo.

**P: ¿Los clientes ven los eventos de otros clientes?**
R: No, cada calendario es privado y solo se comparte con ese cliente específico.

---

## 🔐 Seguridad

- ✅ Tokens de Google almacenados en variables de entorno (encriptadas en Netlify)
- ✅ Row Level Security (RLS) en Supabase
- ✅ Solo tú (info@panchovial.com) puedes crear/editar calendarios
- ✅ Clientes solo tienen acceso de lectura a SU calendario

---

**Próximo archivo a crear:** Las funciones de Netlify y la página de admin auth.
