import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Callback de OAuth para Meta (Facebook + Instagram)
 * Intercambia el código de autorización por un access token de larga duración
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
      .eq('platform', 'meta')
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

    // Paso 1: Intercambiar código por short-lived token
    const tokenUrl = 'https://graph.facebook.com/v18.0/oauth/access_token';
    const tokenParams = new URLSearchParams({
      client_id: process.env.META_APP_ID,
      client_secret: process.env.META_APP_SECRET,
      redirect_uri: `${process.env.URL}/.netlify/functions/oauth-meta-callback`,
      code: code
    });

    const tokenResponse = await fetch(`${tokenUrl}?${tokenParams}`);

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
    const shortLivedToken = tokenData.access_token;

    // Paso 2: Intercambiar short-lived token por long-lived token (60 días)
    const longLivedUrl = 'https://graph.facebook.com/v18.0/oauth/access_token';
    const longLivedParams = new URLSearchParams({
      grant_type: 'fb_exchange_token',
      client_id: process.env.META_APP_ID,
      client_secret: process.env.META_APP_SECRET,
      fb_exchange_token: shortLivedToken
    });

    const longLivedResponse = await fetch(`${longLivedUrl}?${longLivedParams}`);

    if (!longLivedResponse.ok) {
      console.error('Long-lived token exchange failed');
      return {
        statusCode: 302,
        headers: {
          Location: '/connect-accounts.html?error=long_lived_token_failed'
        }
      };
    }

    const longLivedData = await longLivedResponse.json();
    const accessToken = longLivedData.access_token;
    const expiresIn = longLivedData.expires_in || 5184000; // 60 días por defecto

    // Paso 3: Obtener información del usuario y sus cuentas de ads
    const meUrl = `https://graph.facebook.com/v18.0/me?fields=id,name,email&access_token=${accessToken}`;
    const meResponse = await fetch(meUrl);
    const meData = await meResponse.json();

    // Paso 4: Obtener Ad Accounts
    const adAccountsUrl = `https://graph.facebook.com/v18.0/me/adaccounts?fields=id,name,account_status&access_token=${accessToken}`;
    const adAccountsResponse = await fetch(adAccountsUrl);
    const adAccountsData = await adAccountsResponse.json();

    const adAccounts = adAccountsData.data || [];

    // Guardar la cuenta principal de Meta
    const accountData = {
      user_info: meData,
      ad_accounts: adAccounts,
      token_type: 'long_lived',
      expires_in: expiresIn
    };

    const { error: upsertError } = await supabase
      .from('social_accounts')
      .upsert({
        user_id: userId,
        platform: 'meta',
        account_id: meData.id,
        account_name: meData.name || 'Meta Account',
        access_token: accessToken,
        refresh_token: null, // Meta no usa refresh tokens, se renueva el long-lived token
        token_expires_at: new Date(Date.now() + expiresIn * 1000).toISOString(),
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

    // Guardar cada Ad Account por separado para mejor gestión
    for (const adAccount of adAccounts) {
      await supabase
        .from('social_accounts')
        .upsert({
          user_id: userId,
          platform: 'meta-ad-account',
          account_id: adAccount.id,
          account_name: adAccount.name,
          access_token: accessToken,
          refresh_token: null,
          token_expires_at: new Date(Date.now() + expiresIn * 1000).toISOString(),
          metadata: { parent_account: meData.id, ...adAccount },
          connected_at: new Date().toISOString(),
          last_sync_at: null
        }, {
          onConflict: 'user_id,platform,account_id'
        });
    }

    // Redirigir de vuelta a connect-accounts con éxito
    return {
      statusCode: 302,
      headers: {
        Location: '/connect-accounts.html?success=meta'
      }
    };

  } catch (error) {
    console.error('Error in oauth-meta-callback:', error);
    return {
      statusCode: 302,
      headers: {
        Location: '/connect-accounts.html?error=server_error'
      }
    };
  }
};
