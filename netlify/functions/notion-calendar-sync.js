import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Sincroniza eventos/posts desde una base de Notion del cliente
 * a la tabla notion_calendar_events
 */
export const handler = async (event, context) => {
  // Solo permitir POST
  if (event.httpMethod !== 'POST') {
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

    // Parsear body
    const body = JSON.parse(event.body || '{}');
    const databaseId = body.database_id;
    const daysAhead = body.days_ahead || 30;

    if (!databaseId) {
      return {
        statusCode: 400,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ success: false, message: 'database_id is required' })
      };
    }

    // Obtener el token de Notion y workspace_id del usuario
    const { data: notionAccount, error: accountError } = await supabase
      .from('social_accounts')
      .select('access_token, account_id')
      .eq('user_id', user.id)
      .eq('platform', 'notion')
      .single();

    if (accountError || !notionAccount) {
      return {
        statusCode: 404,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          success: false,
          message: 'Notion not connected'
        })
      };
    }

    // Calcular rango de fechas
    const today = new Date().toISOString().split('T')[0];
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + daysAhead);
    const endDate = futureDate.toISOString().split('T')[0];

    // Query la database de Notion
    // Intentamos con diferentes nombres de propiedad de fecha comunes
    const datePropertyNames = ['Publish Date', 'Date', 'Fecha', 'Fecha de Publicación'];

    let queryData = null;
    let lastError = null;

    // Intentar con cada nombre de propiedad de fecha
    for (const dateProp of datePropertyNames) {
      try {
        const queryResponse = await fetch(`https://api.notion.com/v1/databases/${databaseId}/query`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${notionAccount.access_token}`,
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            filter: {
              and: [
                {
                  property: dateProp,
                  date: {
                    on_or_after: today
                  }
                },
                {
                  property: dateProp,
                  date: {
                    on_or_before: endDate
                  }
                }
              ]
            },
            sorts: [
              {
                property: dateProp,
                direction: 'ascending'
              }
            ]
          })
        });

        if (queryResponse.ok) {
          queryData = await queryResponse.json();
          break; // Encontramos la propiedad correcta
        } else {
          lastError = await queryResponse.text();
        }
      } catch (err) {
        lastError = err.message;
      }
    }

    // Si no pudimos query con ningún nombre de fecha, intentar sin filtro
    if (!queryData) {
      console.warn('Could not filter by date property, fetching all pages');
      const queryResponse = await fetch(`https://api.notion.com/v1/databases/${databaseId}/query`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${notionAccount.access_token}`,
          'Notion-Version': '2022-06-28',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
      });

      if (!queryResponse.ok) {
        const errorText = await queryResponse.text();
        console.error('Notion query failed:', errorText);
        return {
          statusCode: 500,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            success: false,
            message: 'Failed to query Notion database',
            error: errorText
          })
        };
      }

      queryData = await queryResponse.json();
    }

    // Procesar cada page y sincronizar a la BD
    let synced = 0;
    let errors = 0;

    for (const page of queryData.results) {
      try {
        const event = parseNotionPage(page, notionAccount.account_id, databaseId);

        if (!event) {
          errors++;
          continue;
        }

        // Upsert en la tabla notion_calendar_events
        const { error: upsertError } = await supabase
          .from('notion_calendar_events')
          .upsert({
            user_id: user.id,
            notion_account_id: notionAccount.account_id,
            database_id: databaseId,
            page_id: page.id,
            title: event.title,
            event_date: event.event_date,
            event_type: event.event_type,
            status: event.status,
            platform: event.platform,
            metadata: event.metadata,
            synced_at: new Date().toISOString()
          }, {
            onConflict: 'user_id,page_id'
          });

        if (upsertError) {
          console.error('Error upserting event:', upsertError);
          errors++;
        } else {
          synced++;
        }
      } catch (err) {
        console.error('Error processing page:', err);
        errors++;
      }
    }

    // Actualizar last_sync_at
    await supabase
      .from('social_accounts')
      .update({ last_sync_at: new Date().toISOString() })
      .eq('user_id', user.id)
      .eq('platform', 'notion');

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        synced,
        errors,
        total: queryData.results.length
      })
    };

  } catch (error) {
    console.error('Error in notion-calendar-sync:', error);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: false,
        message: 'Internal server error',
        error: error.message
      })
    };
  }
};

/**
 * Parsea un page de Notion y extrae las propiedades relevantes
 */
function parseNotionPage(page, workspaceId, databaseId) {
  const props = page.properties || {};

  // Intentar extraer título de diferentes propiedades
  const titleProp = props['Content Title'] || props['Title'] || props['Name'] || props['Título'];
  let title = 'Untitled';
  if (titleProp) {
    if (titleProp.title && titleProp.title.length > 0) {
      title = titleProp.title[0].plain_text || title;
    } else if (titleProp.rich_text && titleProp.rich_text.length > 0) {
      title = titleProp.rich_text[0].plain_text || title;
    }
  }

  // Intentar extraer fecha
  const dateProp = props['Publish Date'] || props['Date'] || props['Fecha'] || props['Fecha de Publicación'];
  let eventDate = null;
  if (dateProp && dateProp.date && dateProp.date.start) {
    eventDate = dateProp.date.start.split('T')[0]; // Solo la fecha, sin hora
  }

  // Si no hay fecha, no sincronizar este item
  if (!eventDate) {
    return null;
  }

  // Extraer tipo
  const typeProp = props['Type'] || props['Tipo'] || props['Content Type'];
  let eventType = null;
  if (typeProp && typeProp.select) {
    eventType = typeProp.select.name;
  }

  // Extraer status
  const statusProp = props['Status'] || props['Estado'];
  let status = null;
  if (statusProp) {
    if (statusProp.status) {
      status = statusProp.status.name;
    } else if (statusProp.select) {
      status = statusProp.select.name;
    }
  }

  // Extraer plataformas (multi-select)
  const platformProp = props['Platform'] || props['Channel'] || props['Plataforma'] || props['Canal'];
  let platforms = [];
  if (platformProp && platformProp.multi_select) {
    platforms = platformProp.multi_select.map(p => p.name);
  }

  // Metadata adicional
  const metadata = {};

  // Funnel Stage
  const funnelProp = props['Funnel Stage'] || props['Etapa del Funnel'];
  if (funnelProp && funnelProp.select) {
    metadata.funnel_stage = funnelProp.select.name;
  }

  // Topic Cluster
  const topicProp = props['Topic Cluster'] || props['Tema'];
  if (topicProp && topicProp.select) {
    metadata.topic_cluster = topicProp.select.name;
  }

  // Caption
  const captionProp = props['Caption'] || props['Copy'] || props['Texto'];
  if (captionProp && captionProp.rich_text && captionProp.rich_text.length > 0) {
    metadata.caption = captionProp.rich_text[0].plain_text;
  }

  // CTA Link
  const linkProp = props['CTA Link'] || props['Link'] || props['URL'];
  if (linkProp && linkProp.url) {
    metadata.cta_link = linkProp.url;
  }

  // Campaign
  const campaignProp = props['Campaign'] || props['Campaña'];
  if (campaignProp && campaignProp.rich_text && campaignProp.rich_text.length > 0) {
    metadata.campaign = campaignProp.rich_text[0].plain_text;
  }

  // Notion URL
  metadata.notion_url = page.url;

  return {
    title,
    event_date: eventDate,
    event_type: eventType,
    status,
    platform: platforms,
    metadata
  };
}
