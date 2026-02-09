import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Sincroniza eventos desde Notion a Google Calendar de cada cliente
 * Se ejecuta automáticamente cada hora o manualmente via POST
 */
export const handler = async (event, context) => {
  try {
    // Obtener todos los clientes que tienen calendario
    const { data: calendars, error: calError } = await supabase
      .from('google_calendar_connections')
      .select('*')
      .eq('sync_enabled', true);

    if (calError) {
      throw new Error('Failed to fetch calendars');
    }

    if (!calendars || calendars.length === 0) {
      return {
        statusCode: 200,
        body: JSON.stringify({
          success: true,
          message: 'No calendars to sync',
          synced: 0
        })
      };
    }

    // Obtener access token de Google Calendar
    let accessToken = process.env.GOOGLE_CALENDAR_ACCESS_TOKEN;

    // Obtener Database ID de Notion
    const notionDatabaseId = process.env.NOTION_CALENDAR_DATABASE_ID;
    const notionToken = process.env.NOTION_INTERNAL_TOKEN;

    if (!notionDatabaseId || !notionToken) {
      throw new Error('Notion configuration missing');
    }

    // Query Notion para obtener eventos futuros
    const notionResponse = await fetch(`https://api.notion.com/v1/databases/${notionDatabaseId}/query`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${notionToken}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        filter: {
          property: 'Date',
          date: {
            on_or_after: new Date().toISOString().split('T')[0]
          }
        },
        sorts: [
          {
            property: 'Date',
            direction: 'ascending'
          }
        ]
      })
    });

    if (!notionResponse.ok) {
      throw new Error('Failed to fetch from Notion');
    }

    const notionData = await notionResponse.json();
    let totalSynced = 0;

    // Por cada cliente
    for (const calendarConn of calendars) {
      // Obtener user info
      const { data: userData } = await supabase.auth.admin.getUserById(calendarConn.user_id);
      if (!userData) continue;

      const clientName = userData.user.user_metadata?.full_name || userData.user.email;

      // Filtrar eventos de este cliente específico
      const clientEvents = notionData.results.filter(page => {
        const clientProp = page.properties['Client'] || page.properties['Cliente'];
        if (!clientProp) return false;

        if (clientProp.select) {
          return clientProp.select.name === clientName;
        }
        if (clientProp.rich_text && clientProp.rich_text.length > 0) {
          return clientProp.rich_text[0].plain_text === clientName;
        }
        return false;
      });

      // Sincronizar cada evento
      for (const page of clientEvents) {
        try {
          const event = parseNotionPage(page);
          if (!event || !event.date) continue;

          // Crear o actualizar evento en Google Calendar
          await upsertGoogleCalendarEvent(
            accessToken,
            calendarConn.calendar_id,
            event,
            page.id
          );

          totalSynced++;
        } catch (err) {
          console.error('Error syncing event:', err);
        }
      }

      // Actualizar last_sync_at
      await supabase
        .from('google_calendar_connections')
        .update({ last_sync_at: new Date().toISOString() })
        .eq('id', calendarConn.id);
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        synced: totalSynced,
        calendars: calendars.length,
        message: `Synced ${totalSynced} events to ${calendars.length} calendars`
      })
    };

  } catch (error) {
    console.error('Error in notion-to-gcal-sync:', error);
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
 * Parsea una página de Notion y extrae los datos del evento
 */
function parseNotionPage(page) {
  const props = page.properties;

  // Título
  const titleProp = props['Title'] || props['Título'] || props['Content Title'];
  let title = 'Sin título';
  if (titleProp && titleProp.title && titleProp.title.length > 0) {
    title = titleProp.title[0].plain_text;
  }

  // Fecha
  const dateProp = props['Date'] || props['Fecha'] || props['Publish Date'];
  let date = null;
  if (dateProp && dateProp.date) {
    date = dateProp.date.start;
  }

  // Tipo
  const typeProp = props['Type'] || props['Tipo'];
  let type = '';
  if (typeProp && typeProp.select) {
    type = typeProp.select.name;
  }

  // Plataformas
  const platformProp = props['Platform'] || props['Plataforma'];
  let platforms = [];
  if (platformProp && platformProp.multi_select) {
    platforms = platformProp.multi_select.map(p => p.name);
  }

  // Caption
  const captionProp = props['Caption'] || props['Copy'];
  let description = '';
  if (captionProp && captionProp.rich_text && captionProp.rich_text.length > 0) {
    description = captionProp.rich_text[0].plain_text;
  }

  return {
    title,
    date,
    type,
    platforms,
    description,
    notionUrl: page.url
  };
}

/**
 * Crea o actualiza un evento en Google Calendar
 */
async function upsertGoogleCalendarEvent(accessToken, calendarId, event, notionPageId) {
  // Buscar si el evento ya existe (usando ID privado extendido)
  const eventId = `notion_${notionPageId.replace(/-/g, '')}`.substring(0, 64);

  const googleEvent = {
    summary: `${event.type ? `[${event.type}] ` : ''}${event.title}`,
    description: [
      event.description,
      event.platforms.length > 0 ? `\n\nPlataformas: ${event.platforms.join(', ')}` : '',
      `\n\nVer en Notion: ${event.notionUrl}`
    ].filter(Boolean).join(''),
    start: {
      date: event.date.split('T')[0], // Solo fecha, sin hora
      timeZone: 'America/Santiago'
    },
    end: {
      date: event.date.split('T')[0],
      timeZone: 'America/Santiago'
    },
    colorId: event.platforms.includes('Instagram') ? '4' : '9' // Rojo para Instagram, azul por defecto
  };

  try {
    // Intentar actualizar primero
    const updateResponse = await fetch(
      `https://www.googleapis.com/calendar/v3/calendars/${calendarId}/events/${eventId}`,
      {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(googleEvent)
      }
    );

    if (updateResponse.ok) {
      return; // Actualizado exitosamente
    }

    // Si no existe, crear nuevo
    await fetch(`https://www.googleapis.com/calendar/v3/calendars/${calendarId}/events`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...googleEvent,
        id: eventId
      })
    });

  } catch (err) {
    console.error('Error upserting Google Calendar event:', err);
  }
}
