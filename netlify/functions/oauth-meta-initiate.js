import { createClient } from '@supabase/supabase-js';
import crypto from 'crypto';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Inicia el flujo de OAuth para Meta (Facebook + Instagram)
 * Genera la URL de autorización y guarda el state para validación
 */
export const handler = async (event, context) => {
  // Solo permitir POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ success: false, message: 'Method not allowed' })
    };
  }

  try {
    // Validar sesión del usuario
    const authHeader = event.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return {
        statusCode: 401,
        body: JSON.stringify({ success: false, message: 'Unauthorized' })
      };
    }

    const sessionToken = authHeader.replace('Bearer ', '');

    // Verificar sesión con Supabase
    const { data: { user }, error: authError } = await supabase.auth.getUser(sessionToken);

    if (authError || !user) {
      return {
        statusCode: 401,
        body: JSON.stringify({ success: false, message: 'Invalid session' })
      };
    }

    // Generar state parameter para CSRF protection
    const state = crypto.randomBytes(32).toString('hex');

    // Guardar state en la base de datos temporalmente
    const { error: stateError } = await supabase
      .from('oauth_states')
      .insert({
        user_id: user.id,
        state: state,
        platform: 'meta',
        created_at: new Date().toISOString(),
        expires_at: new Date(Date.now() + 10 * 60 * 1000).toISOString() // 10 minutos
      });

    if (stateError) {
      console.error('Error saving state:', stateError);
      return {
        statusCode: 500,
        body: JSON.stringify({ success: false, message: 'Error initializing OAuth' })
      };
    }

    // Construir URL de autorización de Facebook
    const authUrl = new URL('https://www.facebook.com/v18.0/dialog/oauth');

    authUrl.searchParams.append('client_id', process.env.META_APP_ID);
    authUrl.searchParams.append('redirect_uri', `${process.env.URL}/.netlify/functions/oauth-meta-callback`);
    authUrl.searchParams.append('state', state);

    // Permisos para Facebook e Instagram Ads
    const scopes = [
      'ads_read',                    // Leer datos de anuncios
      'ads_management',              // Gestión de anuncios
      'business_management',         // Gestión de Business Manager
      'instagram_basic',             // Datos básicos de Instagram
      'instagram_manage_insights',   // Insights de Instagram
      'pages_read_engagement',       // Engagement de páginas
      'read_insights'                // Insights generales
    ];

    authUrl.searchParams.append('scope', scopes.join(','));

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        authorization_url: authUrl.toString()
      })
    };

  } catch (error) {
    console.error('Error in oauth-meta-initiate:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        message: 'Internal server error'
      })
    };
  }
};
