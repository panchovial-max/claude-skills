import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Autoriza la cuenta de Google Calendar del admin (info@panchovial.com)
 * Esta función se ejecuta UNA VEZ para obtener los tokens de refresh
 */
export const handler = async (event, context) => {
  const { httpMethod, queryStringParameters } = event;

  // Paso 1: Iniciar flujo OAuth (GET sin code)
  if (httpMethod === 'GET' && !queryStringParameters?.code) {
    const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');

    authUrl.searchParams.append('client_id', process.env.GOOGLE_CALENDAR_CLIENT_ID);
    authUrl.searchParams.append('redirect_uri', `${process.env.URL}/.netlify/functions/oauth-google-calendar-admin`);
    authUrl.searchParams.append('response_type', 'code');
    authUrl.searchParams.append('scope', 'https://www.googleapis.com/auth/calendar');
    authUrl.searchParams.append('access_type', 'offline');
    authUrl.searchParams.append('prompt', 'consent');

    return {
      statusCode: 302,
      headers: {
        Location: authUrl.toString()
      },
      body: ''
    };
  }

  // Paso 2: Callback - Intercambiar code por tokens
  if (httpMethod === 'GET' && queryStringParameters?.code) {
    try {
      const tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
          code: queryStringParameters.code,
          client_id: process.env.GOOGLE_CALENDAR_CLIENT_ID,
          client_secret: process.env.GOOGLE_CALENDAR_CLIENT_SECRET,
          redirect_uri: `${process.env.URL}/.netlify/functions/oauth-google-calendar-admin`,
          grant_type: 'authorization_code'
        })
      });

      if (!tokenResponse.ok) {
        throw new Error('Token exchange failed');
      }

      const tokens = await tokenResponse.json();

      // Guardar tokens en variable de entorno (mostrar para que el admin los copie)
      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'text/html'
        },
        body: `
          <!DOCTYPE html>
          <html>
          <head>
            <title>Google Calendar Autorizado</title>
            <style>
              body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
              .success { background: #d4edda; border: 1px solid #c3e6cb; padding: 20px; border-radius: 8px; }
              .token-box { background: #f8f9fa; padding: 15px; border-radius: 4px; margin: 10px 0; font-family: monospace; word-break: break-all; }
              h1 { color: #28a745; }
            </style>
          </head>
          <body>
            <div class="success">
              <h1>✅ Autorización Exitosa</h1>
              <p>Tu cuenta de Google Calendar ha sido autorizada correctamente.</p>

              <h3>Siguiente paso:</h3>
              <p>Agrega estas variables de entorno en Netlify:</p>

              <strong>GOOGLE_CALENDAR_ACCESS_TOKEN:</strong>
              <div class="token-box">${tokens.access_token}</div>

              <strong>GOOGLE_CALENDAR_REFRESH_TOKEN:</strong>
              <div class="token-box">${tokens.refresh_token}</div>

              <p><strong>Instrucciones:</strong></p>
              <ol>
                <li>Ve a: <a href="https://app.netlify.com/sites/courageous-valkyrie-15603d/configuration/env">Netlify Environment Variables</a></li>
                <li>Agrega las dos variables mostradas arriba</li>
                <li>Redeploy el sitio</li>
                <li>¡Listo! El sistema podrá crear calendarios automáticamente</li>
              </ol>

              <a href="/dashboard.html">← Volver al Dashboard</a>
            </div>
          </body>
          </html>
        `
      };

    } catch (error) {
      console.error('Error in Google Calendar admin auth:', error);
      return {
        statusCode: 500,
        headers: {
          'Content-Type': 'text/html'
        },
        body: `
          <html>
          <body>
            <h1>Error</h1>
            <p>Hubo un error al autorizar Google Calendar: ${error.message}</p>
            <a href="/.netlify/functions/oauth-google-calendar-admin">Intentar de nuevo</a>
          </body>
          </html>
        `
      };
    }
  }

  return {
    statusCode: 405,
    body: JSON.stringify({ error: 'Method not allowed' })
  };
};
