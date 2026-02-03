import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Obtiene el estado de conexión de todas las plataformas para el usuario actual
 */
export const handler = async (event, context) => {
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

    // Obtener todas las cuentas del usuario
    const { data: accounts, error: accountsError } = await supabase
      .from('social_accounts')
      .select('platform, account_id, account_name, connected_at, last_sync_at')
      .eq('user_id', user.id);

    if (accountsError) {
      console.error('Error fetching accounts:', accountsError);
      return {
        statusCode: 500,
        body: JSON.stringify({ success: false, message: 'Error fetching accounts' })
      };
    }

    // Organizar por plataforma
    const status = {
      'google-ads': false,
      'meta': false,
      'linkedin': false,
      'tiktok': false
    };

    const accountDetails = {};

    if (accounts) {
      accounts.forEach(account => {
        let platformKey = account.platform;

        // Normalizar nombres de plataforma
        if (platformKey === 'meta' || platformKey === 'meta-ad-account') {
          status['meta'] = true;
          if (!accountDetails['meta']) {
            accountDetails['meta'] = [];
          }
          accountDetails['meta'].push({
            id: account.account_id,
            name: account.account_name,
            connected_at: account.connected_at,
            last_sync: account.last_sync_at
          });
        } else if (platformKey === 'google-ads') {
          status['google-ads'] = true;
          accountDetails['google-ads'] = {
            id: account.account_id,
            name: account.account_name,
            connected_at: account.connected_at,
            last_sync: account.last_sync_at
          };
        } else if (platformKey === 'linkedin') {
          status['linkedin'] = true;
          accountDetails['linkedin'] = {
            id: account.account_id,
            name: account.account_name,
            connected_at: account.connected_at,
            last_sync: account.last_sync_at
          };
        } else if (platformKey === 'tiktok') {
          status['tiktok'] = true;
          accountDetails['tiktok'] = {
            id: account.account_id,
            name: account.account_name,
            connected_at: account.connected_at,
            last_sync: account.last_sync_at
          };
        }
      });
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        success: true,
        accounts: status,
        details: accountDetails
      })
    };

  } catch (error) {
    console.error('Error in accounts-status:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        message: 'Internal server error'
      })
    };
  }
};
