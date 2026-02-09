import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Retorna eventos del calendario de un usuario
 * Formato compatible con FullCalendar
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

    // Obtener query parameters
    const params = event.queryStringParameters || {};
    const startDate = params.start_date;
    const endDate = params.end_date;
    const eventType = params.type;

    // Construir query
    let query = supabase
      .from('notion_calendar_events')
      .select('*')
      .eq('user_id', user.id)
      .order('event_date', { ascending: true });

    // Filtrar por rango de fechas si se proporciona
    if (startDate) {
      query = query.gte('event_date', startDate);
    }
    if (endDate) {
      query = query.lte('event_date', endDate);
    }

    // Filtrar por tipo si se proporciona
    if (eventType) {
      query = query.eq('event_type', eventType);
    }

    const { data: events, error: queryError } = await query;

    if (queryError) {
      console.error('Error querying events:', queryError);
      return {
        statusCode: 500,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          success: false,
          message: 'Failed to fetch events'
        })
      };
    }

    // Formatear para FullCalendar
    const formattedEvents = events.map(event => ({
      id: event.page_id,
      title: event.title,
      start: event.event_date,
      allDay: true, // Eventos de calendario sin hora específica
      extendedProps: {
        type: event.event_type,
        status: event.status,
        platforms: event.platform || [],
        notionUrl: event.metadata?.notion_url,
        caption: event.metadata?.caption,
        cta_link: event.metadata?.cta_link,
        campaign: event.metadata?.campaign,
        funnel_stage: event.metadata?.funnel_stage,
        topic_cluster: event.metadata?.topic_cluster,
        database_id: event.database_id,
        synced_at: event.synced_at
      }
    }));

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formattedEvents)
    };

  } catch (error) {
    console.error('Error in calendar-events:', error);
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
