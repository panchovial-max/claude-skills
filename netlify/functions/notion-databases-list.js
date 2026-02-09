import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Lista todas las bases de Notion compartidas con nuestra integración
 * Permite al usuario seleccionar cuál usar como calendario de contenido
 */
export const handler = async (event, context) => {
  // Solo permitir GET
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ success: false, message: 'Method not allowed' })
    };
  }

  try {
    // Validar sesión del usuario
    const authHeader = event.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return {
        statusCode: 401,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ success: false, message: 'Unauthorized' })
      };
    }

    const sessionToken = authHeader.replace('Bearer ', '');

    // Verificar sesión con Supabase
    const { data: { user }, error: authError } = await supabase.auth.getUser(sessionToken);

    if (authError || !user) {
      return {
        statusCode: 401,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ success: false, message: 'Invalid session' })
      };
    }

    // Obtener el token de Notion del usuario
    const { data: notionAccount, error: accountError } = await supabase
      .from('social_accounts')
      .select('access_token, account_name')
      .eq('user_id', user.id)
      .eq('platform', 'notion')
      .single();

    if (accountError || !notionAccount) {
      return {
        statusCode: 404,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          success: false,
          message: 'Notion not connected. Please connect your Notion account first.'
        })
      };
    }

    // Buscar todas las databases en Notion
    const searchResponse = await fetch('https://api.notion.com/v1/search', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${notionAccount.access_token}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        filter: {
          value: 'database',
          property: 'object'
        },
        sort: {
          direction: 'descending',
          timestamp: 'last_edited_time'
        }
      })
    });

    if (!searchResponse.ok) {
      const errorText = await searchResponse.text();
      console.error('Notion search failed:', errorText);
      return {
        statusCode: 500,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          success: false,
          message: 'Failed to fetch databases from Notion'
        })
      };
    }

    const searchData = await searchResponse.json();

    // Formatear las databases para el frontend
    const databases = searchData.results.map(db => ({
      id: db.id,
      title: db.title?.[0]?.plain_text || 'Untitled',
      icon: db.icon ? (db.icon.emoji || db.icon.external?.url || db.icon.file?.url) : null,
      created_time: db.created_time,
      last_edited_time: db.last_edited_time,
      url: db.url
    }));

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        workspace_name: notionAccount.account_name,
        databases: databases,
        total: databases.length
      })
    };

  } catch (error) {
    console.error('Error in notion-databases-list:', error);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: false,
        message: 'Internal server error'
      })
    };
  }
};
