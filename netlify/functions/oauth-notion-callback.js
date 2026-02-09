import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Callback de OAuth para Notion
 * Valida el state, intercambia el code por un access_token y guarda la conexión
 */
export const handler = async (event, context) => {
  try {
    // Extraer code y state de los query parameters
    const { code, state, error: oauthError } = event.queryStringParameters || {};

    // Si Notion retorna error
    if (oauthError) {
      console.error('Notion OAuth error:', oauthError);
      return {
        statusCode: 302,
        headers: {
          Location: `${process.env.URL}/dashboard.html?error=notion_auth_failed`
        },
        body: ''
      };
    }

    // Validar que tenemos code y state
    if (!code || !state) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          success: false,
          message: 'Missing code or state parameter'
        })
      };
    }

    // Validar state contra la base de datos (CSRF protection)
    const { data: stateData, error: stateError } = await supabase
      .from('oauth_states')
      .select('*')
      .eq('state', state)
      .eq('platform', 'notion')
      .single();

    if (stateError || !stateData) {
      console.error('Invalid state:', stateError);
      return {
        statusCode: 302,
        headers: {
          Location: `${process.env.URL}/dashboard.html?error=invalid_state`
        },
        body: ''
      };
    }

    // Verificar que el state no ha expirado
    if (new Date(stateData.expires_at) < new Date()) {
      await supabase.from('oauth_states').delete().eq('state', state);
      return {
        statusCode: 302,
        headers: {
          Location: `${process.env.URL}/dashboard.html?error=state_expired`
        },
        body: ''
      };
    }

    const user_id = stateData.user_id;

    // Intercambiar code por access_token
    const tokenResponse = await fetch('https://api.notion.com/v1/oauth/token', {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${Buffer.from(`${process.env.NOTION_OAUTH_CLIENT_ID}:${process.env.NOTION_OAUTH_CLIENT_SECRET}`).toString('base64')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: `${process.env.URL}/.netlify/functions/oauth-notion-callback`
      })
    });

    if (!tokenResponse.ok) {
      const errorText = await tokenResponse.text();
      console.error('Notion token exchange failed:', errorText);
      return {
        statusCode: 302,
        headers: {
          Location: `${process.env.URL}/dashboard.html?error=token_exchange_failed`
        },
        body: ''
      };
    }

    const tokenData = await tokenResponse.json();

    // Extraer información del workspace
    const {
      access_token,
      bot_id,
      workspace_id,
      workspace_name,
      workspace_icon,
      owner
    } = tokenData;

    if (!access_token || !workspace_id) {
      console.error('Missing required fields in token response');
      return {
        statusCode: 302,
        headers: {
          Location: `${process.env.URL}/dashboard.html?error=invalid_token_response`
        },
        body: ''
      };
    }

    // Guardar o actualizar la conexión en social_accounts
    const { error: upsertError } = await supabase
      .from('social_accounts')
      .upsert({
        user_id: user_id,
        platform: 'notion',
        account_id: workspace_id,
        account_name: workspace_name || 'Notion Workspace',
        access_token: access_token,
        refresh_token: null, // Notion no usa refresh tokens
        token_expires_at: null, // Notion tokens no expiran
        metadata: {
          bot_id,
          workspace_icon,
          owner
        },
        connected_at: new Date().toISOString(),
        last_sync_at: null
      }, {
        onConflict: 'user_id,platform,account_id'
      });

    if (upsertError) {
      console.error('Error saving Notion connection:', upsertError);
      return {
        statusCode: 302,
        headers: {
          Location: `${process.env.URL}/dashboard.html?error=save_failed`
        },
        body: ''
      };
    }

    // Limpiar el state usado
    await supabase.from('oauth_states').delete().eq('state', state);

    // Redirect al dashboard con éxito
    return {
      statusCode: 302,
      headers: {
        Location: `${process.env.URL}/dashboard.html?notion_connected=true`
      },
      body: ''
    };

  } catch (error) {
    console.error('Error in oauth-notion-callback:', error);
    return {
      statusCode: 302,
      headers: {
        Location: `${process.env.URL}/dashboard.html?error=internal_error`
      },
      body: ''
    };
  }
};
