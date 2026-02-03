# 🎯 PVB Client Portal

Portal de clientes para PVB Estudio Creativo que permite a los clientes ver sus métricas de marketing digital en tiempo real desde un único dashboard integrado.

## 🌟 Características Principales

### Para Clientes
- ✅ **Login simple con Google** - 1 click para acceder
- 📊 **Dashboard unificado** - Todas las métricas en un solo lugar
- 🔗 **Conexión fácil** - Conecta tus plataformas en 1 click
- 📈 **Métricas en tiempo real** - Datos actualizados automáticamente
- 🎨 **Interfaz intuitiva** - Diseño limpio y profesional

### Para la Agencia
- 🚀 **Diferenciador competitivo** - Experiencia de cliente superior
- 💼 **Menos fricción** - Clientes autónomos para ver sus datos
- 🔐 **Seguro** - OAuth 2.0, Row Level Security, tokens encriptados
- 📊 **4 plataformas integradas** - Google Ads, Meta, LinkedIn, TikTok
- ⚡ **Serverless** - Sin servidores que mantener

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    Cliente (Browser)                     │
│  - login.html (Google OAuth)                            │
│  - dashboard.html (KPIs + Charts)                       │
│  - connect-accounts.html (OAuth Platforms)              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Netlify (Static + Functions)               │
│  Functions:                                             │
│  - oauth-google-ads-initiate/callback                   │
│  - oauth-meta-initiate/callback                         │
│  - oauth-linkedin-initiate/callback                     │
│  - oauth-tiktok-initiate/callback                       │
│  - metrics-sync (fetch from APIs)                       │
│  - metrics-get (serve to dashboard)                     │
│  - accounts-status                                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                  Supabase (Backend)                     │
│  - PostgreSQL Database                                  │
│  - Authentication (Google OAuth)                        │
│  - Row Level Security (RLS)                             │
│  Tables:                                                │
│  - users                                                │
│  - social_accounts (tokens)                             │
│  - social_metrics (daily data)                          │
│  - oauth_states (CSRF protection)                       │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              Platform APIs (Data Sources)               │
│  - Google Ads API                                       │
│  - Meta Graph API (Facebook + Instagram)               │
│  - LinkedIn Marketing API                               │
│  - TikTok Marketing API                                 │
└─────────────────────────────────────────────────────────┘
```

## 📊 Métricas Disponibles

### Google Ads
- 💰 Spend (gasto total)
- 👁️ Impressions
- 🖱️ Clicks
- 📈 CTR (Click-through rate)
- 💵 CPC (Cost per click)
- ✅ Conversions
- 🎯 Conversion Rate
- 💸 Cost per Conversion

### Meta (Facebook + Instagram)
- 👁️ Impressions
- 🖱️ Clicks
- 💰 Spend
- 📊 Reach
- 📈 CTR
- 💵 CPC
- 📊 CPM (Cost per mille)
- 🔄 Frequency

### LinkedIn
- 👁️ Impressions
- 🖱️ Clicks
- 💼 Engagement
- 📈 CTR

### TikTok
- 👁️ Impressions
- 🖱️ Clicks
- 💰 Spend
- 📈 CTR
- 💵 CPC
- 📊 CPM
- ✅ Conversions

## 🚀 Setup y Deployment

### 1. Requisitos Previos

- Cuenta de Netlify
- Cuenta de Supabase
- Cuentas de desarrollador en:
  - Google Cloud Console
  - Meta for Developers
  - LinkedIn Developers
  - TikTok for Business

### 2. Configuración de Supabase

1. **Crear proyecto en Supabase**
   - Ir a https://supabase.com
   - Crear nuevo proyecto

2. **Ejecutar schema SQL**
   - SQL Editor → New Query
   - Copiar contenido de `supabase-schema.sql`
   - Run

3. **Habilitar Google OAuth**
   - Authentication → Providers
   - Google → Enable
   - Configurar Client ID y Secret

4. **Obtener credenciales**
   - Settings → API
   - Copiar:
     - URL
     - anon (public) key
     - service_role key

### 3. Configuración de OAuth Platforms

Ver guía completa en [`OAUTH_SETUP_COMPLETE.md`](./OAUTH_SETUP_COMPLETE.md)

Resumen:
1. **Google Ads**: OAuth + Developer Token
2. **Meta**: App de Facebook + Permisos
3. **LinkedIn**: LinkedIn App + Scopes
4. **TikTok**: TikTok Business App + Marketing API

### 4. Deploy a Netlify

#### Opción A: Netlify UI (Recomendado)

1. **Conectar Repositorio**
   - Netlify Dashboard → New site from Git
   - Conectar GitHub
   - Seleccionar repositorio

2. **Configurar Build**
   - Build command: (dejar vacío)
   - Publish directory: `.`
   - Functions directory: `netlify/functions`

3. **Variables de Entorno**
   - Site settings → Environment variables
   - Agregar todas las variables de `.env.example`:

   ```
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_ANON_KEY=eyJhbGci...
   SUPABASE_SERVICE_KEY=eyJhbGci...
   URL=https://your-site.netlify.app

   GOOGLE_ADS_CLIENT_ID=xxx
   GOOGLE_ADS_CLIENT_SECRET=xxx
   GOOGLE_ADS_DEVELOPER_TOKEN=xxx

   META_APP_ID=xxx
   META_APP_SECRET=xxx

   LINKEDIN_CLIENT_ID=xxx
   LINKEDIN_CLIENT_SECRET=xxx

   TIKTOK_CLIENT_KEY=xxx
   TIKTOK_CLIENT_SECRET=xxx
   ```

4. **Deploy**
   - Click "Deploy site"
   - Esperar deploy (2-3 minutos)

#### Opción B: Netlify CLI

```bash
# Instalar dependencias
npm install

# Login a Netlify
npx netlify login

# Deploy
npx netlify deploy --prod
```

### 5. Actualizar Redirect URLs

Una vez deployado, actualizar las Redirect URIs en cada plataforma:

**Google Ads**:
```
https://your-site.netlify.app/.netlify/functions/oauth-google-ads-callback
```

**Meta**:
```
https://your-site.netlify.app/.netlify/functions/oauth-meta-callback
```

**LinkedIn**:
```
https://your-site.netlify.app/.netlify/functions/oauth-linkedin-callback
```

**TikTok**:
```
https://your-site.netlify.app/.netlify/functions/oauth-tiktok-callback
```

**Supabase (Google OAuth)**:
```
https://your-site.netlify.app/dashboard.html
```

## 🔒 Seguridad

### Row Level Security (RLS)

Todas las tablas tienen RLS habilitada:

```sql
-- Ejemplo: social_accounts
CREATE POLICY "Users can only access their own accounts"
ON social_accounts
FOR ALL
USING (auth.uid() = user_id);
```

### OAuth State Validation

Prevención de CSRF attacks:
- State parameter generado aleatoriamente
- Guardado temporalmente en DB
- Validado en callback
- Expiración de 10 minutos

### Token Storage

- Access tokens encriptados en Supabase
- Service role key solo en backend (Netlify Functions)
- Refresh tokens para renovación automática

## 📱 Flujo de Usuario

### 1. Login Inicial

```
Usuario → login.html
  ↓
Click "Sign in with Google"
  ↓
Google OAuth Consent
  ↓
Redirect a dashboard.html
  ↓
✅ Logged in
```

### 2. Conectar Plataformas

```
Usuario → connect-accounts.html
  ↓
Click "Conectar Google Ads"
  ↓
oauth-google-ads-initiate
  ↓
Google OAuth Consent
  ↓
oauth-google-ads-callback
  ↓
Guardar token en Supabase
  ↓
Redirect a connect-accounts.html?success=google-ads
  ↓
✅ Conectado
```

### 3. Ver Métricas

```
Usuario → dashboard.html
  ↓
JavaScript llama metrics-get
  ↓
Netlify Function valida sesión
  ↓
Query a Supabase (social_metrics)
  ↓
Formatear datos para charts
  ↓
Return JSON
  ↓
Dashboard renderiza gráficos
  ↓
✅ Métricas visibles
```

### 4. Sincronizar Datos

```
Cron job (cada 6 horas)
  ↓
Llamar metrics-sync
  ↓
Para cada cuenta:
  - Fetch desde API de plataforma
  - Guardar en social_metrics
  - Actualizar last_sync_at
  ↓
✅ Datos actualizados
```

## 🛠️ Desarrollo Local

```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Iniciar servidor local
npm run dev

# Abrir en navegador
open http://localhost:8888
```

## 📁 Estructura de Archivos

```
pvb-client-portal/
│
├── 📄 HTML Files
│   ├── login.html              # Login con Google
│   ├── dashboard.html          # Dashboard principal
│   └── connect-accounts.html   # Conectar plataformas
│
├── 🔧 Netlify Functions
│   └── netlify/functions/
│       ├── oauth-google-ads-initiate.js
│       ├── oauth-google-ads-callback.js
│       ├── oauth-meta-initiate.js
│       ├── oauth-meta-callback.js
│       ├── oauth-linkedin-initiate.js
│       ├── oauth-linkedin-callback.js
│       ├── oauth-tiktok-initiate.js
│       ├── oauth-tiktok-callback.js
│       ├── accounts-status.js
│       ├── metrics-sync.js
│       └── metrics-get.js
│
├── 📚 Documentación
│   ├── README.md
│   ├── OAUTH_SETUP_COMPLETE.md
│   └── DEPLOYMENT_READY.md
│
├── ⚙️ Configuración
│   ├── package.json
│   ├── netlify.toml
│   ├── .env.example
│   └── supabase-schema.sql
│
└── 🎨 Assets (futuro)
    ├── css/
    ├── js/
    └── images/
```

## 🔄 Roadmap

### Fase 1 - MVP ✅ (Actual)
- [x] Login con Google
- [x] OAuth para 4 plataformas
- [x] Dashboard básico
- [x] Sync de métricas

### Fase 2 - Mejoras UX
- [ ] Gráficos interactivos (Chart.js)
- [ ] Comparación con período anterior
- [ ] Filtros por fecha
- [ ] Export a PDF

### Fase 3 - Automatización
- [ ] Reportes automáticos por email
- [ ] Alertas de rendimiento
- [ ] Recomendaciones con IA
- [ ] Predicciones de tendencias

### Fase 4 - Más Integraciones
- [ ] Google Analytics
- [ ] Google Search Console
- [ ] Email Marketing (Mailchimp)
- [ ] CRM integration

## 🐛 Troubleshooting

### "redirect_uri_mismatch"
- Verificar que Redirect URI coincida exactamente
- Incluir `https://` y path completo
- Sin trailing slash

### "Unauthorized" en Netlify Functions
- Verificar que variables de entorno estén en Netlify
- Verificar que `SUPABASE_SERVICE_KEY` sea correcta
- Verificar que sesión del usuario sea válida

### "Token expired" al sincronizar
- Google Ads: Renovar con refresh token
- Meta: Renovar long-lived token (60 días)
- TikTok: Renovar cada 24 horas

## 📞 Soporte

- **Documentación OAuth**: Ver `OAUTH_SETUP_COMPLETE.md`
- **Deployment**: Ver `DEPLOYMENT_READY.md`
- **Issues**: GitHub Issues

## 📄 Licencia

Propietario: PVB Estudio Creativo
Uso interno solamente

---

Creado con ❤️ por PVB Estudio Creativo
