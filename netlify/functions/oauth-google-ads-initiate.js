import { createClient } from '@supabase/supabase-js';
import crypto from 'crypto';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Inicia el flujo de OAuth para Google Ads
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
        platform: 'google-ads',
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

    // Construir URL de autorización de Google
    const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');

    authUrl.searchParams.append('client_id', process.env.GOOGLE_ADS_CLIENT_ID);
    authUrl.searchParams.append('redirect_uri', `${process.env.URL}/.netlify/functions/oauth-google-ads-callback`);
    authUrl.searchParams.append('response_type', 'code');
    authUrl.searchParams.append('scope', 'https://www.googleapis.com/auth/adwords');
    authUrl.searchParams.append('access_type', 'offline');
    authUrl.searchParams.append('prompt', 'consent');
    authUrl.searchParams.append('state', state);

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        authorization_url: authUrl.toString()
      })
    };

  } catch (error) {
    console.error('Error in oauth-google-ads-initiate:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        message: 'Internal server error'
      })
    };
  }
};
