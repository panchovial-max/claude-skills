# 🔐 Guía Completa de Configuración OAuth

Esta guía te ayudará a configurar todas las plataformas de marketing para el Client Portal de PVB.

## 📋 Resumen de Plataformas

| Plataforma | Tiempo Setup | Dificultad | Prioridad |
|------------|--------------|------------|-----------|
| **Google Ads** | 15-20 min | Media | 🔥 Alta |
| **Meta (Facebook + Instagram)** | 20-30 min | Alta | 🔥 Alta |
| **LinkedIn** | 10-15 min | Baja | Media |
| **TikTok** | 15-20 min | Media | Media |

---

## 1️⃣ Google Ads OAuth Setup

### Requisitos Previos
- Cuenta de Google Ads activa
- Acceso a Google Cloud Console

### Paso 1: Crear Proyecto en Google Cloud Console

1. **Ir a Google Cloud Console**
   - URL: https://console.cloud.google.com/
   - Click en el dropdown de proyectos (arriba izquierda)
   - Click en **"New Project"**

2. **Configurar Proyecto**
   - Nombre: `PVB Client Portal - Ads`
   - Organization: Ninguna (o tu organización)
   - Click **"Create"**

### Paso 2: Habilitar Google Ads API

1. **En el menú lateral → APIs & Services → Library**
2. Buscar: `Google Ads API`
3. Click en **"Google Ads API"**
4. Click **"Enable"**

### Paso 3: Crear OAuth Credentials

1. **APIs & Services → Credentials**
2. Click **"+ CREATE CREDENTIALS"** → OAuth client ID
3. Si es primera vez, configurar **OAuth Consent Screen**:
   - User Type: **External**
   - App name: `PVB Client Portal`
   - User support email: tu email
   - Developer contact: tu email
   - Click **"Save and Continue"**
   - Scopes: Click **"Add or Remove Scopes"**
     - Buscar y agregar: `https://www.googleapis.com/auth/adwords`
   - Test users: Agregar tu email
   - Click **"Save and Continue"**

4. **Crear OAuth Client ID**:
   - Application type: **Web application**
   - Name: `PVB Client Portal OAuth`
   - Authorized redirect URIs:
     ```
     https://your-site.netlify.app/.netlify/functions/oauth-google-ads-callback
     ```
   - Click **"Create"**

5. **Copiar credenciales**:
   - Client ID → Guardar
   - Client Secret → Guardar

### Paso 4: Obtener Developer Token

1. **Ir a Google Ads Manager**
   - URL: https://ads.google.com/
   - Click en **Tools & Settings** (⚙️)
   - Under **SETUP**: Click **API Center**

2. **Solicitar Developer Token**:
   - Click **"Apply for access"**
   - Llenar formulario (uso: Internal/Private, Read-only)
   - Enviar solicitud

3. **Modo Test** (mientras se aprueba):
   - Token de prueba disponible inmediatamente
   - Permite usar la API con tus propias cuentas

### Paso 5: Configurar en Netlify

En Netlify Dashboard → Site Settings → Environment Variables:

```
GOOGLE_ADS_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=GOCSPX-xxxxx
GOOGLE_ADS_DEVELOPER_TOKEN=tu-developer-token
```

---

## 2️⃣ Meta (Facebook + Instagram) OAuth Setup

### Requisitos Previos
- Facebook Business Manager
- Cuenta de Meta Developer

### Paso 1: Crear App en Meta Developers

1. **Ir a Meta for Developers**
   - URL: https://developers.facebook.com/apps/
   - Click **"Create App"**

2. **Seleccionar Tipo de App**:
   - Use case: **Other**
   - App type: **Business**
   - Click **"Next"**

3. **Detalles de la App**:
   - App name: `PVB Client Portal`
   - App contact email: tu email
   - Business account: Seleccionar o crear
   - Click **"Create App"**

### Paso 2: Configurar OAuth

1. **En el Dashboard de tu App**:
   - Scroll abajo a **"Add products to your app"**
   - Buscar **"Facebook Login"** → Click **"Set Up"**

2. **Configurar Facebook Login**:
   - Quickstart: Skip (X arriba derecha)
   - En menú lateral: **Facebook Login → Settings**

3. **Valid OAuth Redirect URIs**:
   ```
   https://your-site.netlify.app/.netlify/functions/oauth-meta-callback
   ```
   - Click **"Save Changes"**

### Paso 3: Permisos de la App

1. **En menú lateral → App Review → Permissions and Features**

2. **Solicitar permisos** (algunos requieren revisión):
   - `ads_read` - Aprobación automática
   - `ads_management` - Requiere revisión
   - `business_management` - Requiere revisión
   - `instagram_basic` - Aprobación automática
   - `instagram_manage_insights` - Requiere revisión
   - `pages_read_engagement` - Requiere revisión
   - `read_insights` - Aprobación automática

3. **Para Testing** (antes de revisión):
   - App Mode: **Development**
   - Agregar usuarios de prueba en **Roles → Test Users**

### Paso 4: Obtener Credenciales

1. **Settings → Basic**:
   - App ID → Copiar
   - App Secret → Click **"Show"** → Copiar

### Paso 5: Configurar en Netlify

```
META_APP_ID=tu-app-id
META_APP_SECRET=tu-app-secret
```

### Paso 6: Cambiar a Modo Live (cuando estés listo)

1. **App Review → Requests**
   - Enviar solicitud para permisos pendientes
   - Proporcionar video demo del uso
   - Tiempo de revisión: 3-5 días laborables

2. **Una vez aprobado**:
   - Settings → Basic
   - App Mode: **Live** ✅

---

## 3️⃣ LinkedIn OAuth Setup

### Paso 1: Crear LinkedIn App

1. **Ir a LinkedIn Developers**
   - URL: https://www.linkedin.com/developers/apps
   - Click **"Create app"**

2. **Información de la App**:
   - App name: `PVB Client Portal`
   - LinkedIn Page: Seleccionar tu página de empresa
   - Privacy policy URL: Tu URL
   - App logo: Upload logo
   - Click **"Create app"**

### Paso 2: Configurar OAuth

1. **Tab "Auth"**:

2. **Redirect URLs**:
   ```
   https://your-site.netlify.app/.netlify/functions/oauth-linkedin-callback
   ```

3. **OAuth 2.0 scopes**:
   - `r_liteprofile` - Perfil básico
   - `r_emailaddress` - Email
   - `r_organization_social` - Estadísticas de organización
   - `rw_organization_admin` - Admin de página (si necesitas posting)
   - `r_ads` - Leer ads
   - `r_ads_reporting` - Reportes de ads

### Paso 3: Obtener Credenciales

En tab **"Auth"**:
- Client ID → Copiar
- Client Secret → Copiar

### Paso 4: Configurar en Netlify

```
LINKEDIN_CLIENT_ID=tu-client-id
LINKEDIN_CLIENT_SECRET=tu-client-secret
```

### Paso 5: Verificación

1. **Tab "Settings" → Verification**
2. Completar verificación de la app (requerido para producción)

---

## 4️⃣ TikTok OAuth Setup

### Paso 1: Registrarse en TikTok for Business

1. **Ir a TikTok Developers**
   - URL: https://developers.tiktok.com/
   - Click **"Get Started"**
   - Registrarse con cuenta de TikTok Business

### Paso 2: Crear App

1. **En Developer Portal → My apps**
   - Click **"+ Create an app"**

2. **Información de la App**:
   - App name: `PVB Client Portal`
   - Category: `Marketing`
   - Click **"Next"**

3. **Seleccionar APIs**:
   - ✅ **Marketing API**
   - Click **"Apply"**

### Paso 3: Configurar OAuth

1. **En App Settings → Credentials**:

2. **Redirect URLs**:
   ```
   https://your-site.netlify.app/.netlify/functions/oauth-tiktok-callback
   ```

### Paso 4: Obtener Credenciales

En **Credentials**:
- App ID (Client Key) → Copiar
- App Secret (Client Secret) → Copiar

### Paso 5: Configurar en Netlify

```
TIKTOK_CLIENT_KEY=tu-client-key
TIKTOK_CLIENT_SECRET=tu-client-secret
```

### Paso 6: Solicitar Acceso a Marketing API

1. **Submit for Review**:
   - Descripción de uso
   - Screenshot/video demo
   - Tiempo de revisión: 2-3 semanas

2. **Modo Sandbox** (mientras se aprueba):
   - Acceso limitado a tus propias cuentas
   - Datos de prueba disponibles

---

## ✅ Verificación Final

### Checklist Pre-Deploy

- [ ] Google Ads
  - [ ] OAuth credentials creadas
  - [ ] Developer token obtenido
  - [ ] Variables en Netlify configuradas

- [ ] Meta (Facebook + Instagram)
  - [ ] App creada
  - [ ] Facebook Login configurado
  - [ ] Redirect URI agregada
  - [ ] Variables en Netlify configuradas

- [ ] LinkedIn
  - [ ] App creada
  - [ ] OAuth configurado
  - [ ] Scopes seleccionados
  - [ ] Variables en Netlify configuradas

- [ ] TikTok
  - [ ] App creada
  - [ ] Marketing API habilitada
  - [ ] Redirect URI configurada
  - [ ] Variables en Netlify configuradas

### Testing

1. **Deploy a Netlify**:
   ```bash
   git add .
   git commit -m "Add OAuth integration for all platforms"
   git push origin main
   ```

2. **Configurar Variables de Entorno**:
   - Netlify Dashboard → Site settings → Environment variables
   - Agregar todas las variables del `.env.example`

3. **Probar Conexiones**:
   - Ir a `/connect-accounts.html`
   - Intentar conectar cada plataforma
   - Verificar que redirige correctamente
   - Verificar que guarda en Supabase

---

## 🚨 Troubleshooting

### Error: `redirect_uri_mismatch`
- Verificar que la Redirect URI en la plataforma coincide EXACTAMENTE con la configurada
- Formato correcto: `https://your-site.netlify.app/.netlify/functions/oauth-PLATFORM-callback`

### Error: `invalid_client`
- Verificar Client ID y Client Secret
- Asegurarse que las variables de entorno están en Netlify

### Error: `access_denied`
- Usuario rechazó autorización
- O faltan permisos en la app

### Error: `insufficient_permissions`
- Solicitar permisos adicionales en la plataforma
- O completar App Review

---

## 📞 Soporte

Si necesitas ayuda con alguna configuración:
- Google Ads: https://support.google.com/google-ads/
- Meta: https://developers.facebook.com/support/
- LinkedIn: https://www.linkedin.com/help/lms
- TikTok: https://ads.tiktok.com/help/

---

## 🎯 Próximos Pasos

Una vez configurado todo OAuth:

1. **Automatizar Sync de Métricas**:
   - Configurar Netlify Scheduled Functions
   - Sincronizar métricas cada 6-12 horas

2. **Dashboard Mejorado**:
   - Agregar gráficos con Chart.js
   - Comparativas período anterior
   - Alertas de rendimiento

3. **Reportes Automáticos**:
   - Email semanal/mensual con métricas
   - PDF downloadable
   - Insights con IA

4. **Más Integraciones**:
   - Google Analytics
   - Google Search Console
   - Email marketing (Mailchimp, SendGrid)
