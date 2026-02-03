import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Callback de OAuth para Google Ads
 * Intercambia el código de autorización por un access token
 */
export const handler = async (event, context) => {
  try {
    const params = event.queryStringParameters;
    const code = params?.code;
    const state = params?.state;
    const error = params?.error;

    // Si el usuario rechazó la autorización
    if (error) {
      return {
        statusCode: 302,
        headers: {
          Location: '/connect-accounts.html?error=access_denied'
        }
      };
    }

    if (!code || !state) {
      return {
        statusCode: 400,
        body: JSON.stringify({ success: false, message: 'Missing code or state' })
      };
    }

    // Verificar state parameter
    const { data: stateData, error: stateError } = await supabase
      .from('oauth_states')
      .select('user_id, platform')
      .eq('state', state)
      .eq('platform', 'google-ads')
      .gt('expires_at', new Date().toISOString())
      .single();

    if (stateError || !stateData) {
      return {
        statusCode: 400,
        body: JSON.stringify({ success: false, message: 'Invalid or expired state' })
      };
    }

    const userId = stateData.user_id;

    // Borrar state usado
    await supabase
      .from('oauth_states')
      .delete()
      .eq('state', state);

    // Intercambiar código por access token
    const tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        code: code,
        client_id: process.env.GOOGLE_ADS_CLIENT_ID,
        client_secret: process.env.GOOGLE_ADS_CLIENT_SECRET,
        redirect_uri: `${process.env.URL}/.netlify/functions/oauth-google-ads-callback`,
        grant_type: 'authorization_code'
      })
    });

    if (!tokenResponse.ok) {
      const errorData = await tokenResponse.text();
      console.error('Token exchange error:', errorData);
      return {
        statusCode: 302,
        headers: {
          Location: '/connect-accounts.html?error=token_exchange_failed'
        }
      };
    }

    const tokenData = await tokenResponse.json();
    const accessToken = tokenData.access_token;
    const refreshToken = tokenData.refresh_token;
    const expiresIn = tokenData.expires_in;

    // Obtener información del cliente de Google Ads
    // Nota: Para esto necesitamos el Customer ID que el usuario debe proporcionar
    // Por ahora guardamos el token y después podemos pedir el Customer ID

    const accountData = {
      access_token: accessToken,
      refresh_token: refreshToken,
      expires_at: new Date(Date.now() + expiresIn * 1000).toISOString(),
      token_type: tokenData.token_type
    };

    // Guardar o actualizar la cuenta en la base de datos
    const { error: upsertError } = await supabase
      .from('social_accounts')
      .upsert({
        user_id: userId,
        platform: 'google-ads',
        account_id: 'pending', // Se actualizará cuando el usuario proporcione el Customer ID
        account_name: 'Google Ads Account',
        access_token: accessToken,
        refresh_token: refreshToken,
        token_expires_at: accountData.expires_at,
        metadata: accountData,
        connected_at: new Date().toISOString(),
        last_sync_at: null
      }, {
        onConflict: 'user_id,platform,account_id'
      });

    if (upsertError) {
      console.error('Error saving account:', upsertError);
      return {
        statusCode: 302,
        headers: {
          Location: '/connect-accounts.html?error=save_failed'
        }
      };
    }

    // Redirigir de vuelta a connect-accounts con éxito
    return {
      statusCode: 302,
      headers: {
        Location: '/connect-accounts.html?success=google-ads'
      }
    };

  } catch (error) {
    console.error('Error in oauth-google-ads-callback:', error);
    return {
      statusCode: 302,
      headers: {
        Location: '/connect-accounts.html?error=server_error'
      }
    };
  }
};
