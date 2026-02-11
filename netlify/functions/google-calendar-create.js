import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Crea un Google Calendar para un cliente y lo comparte con su email
 */
export const handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ success: false, message: 'Method not allowed' })
    };
  }

  try {
    // Validar sesión
    const authHeader = event.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return {
        statusCode: 401,
        body: JSON.stringify({ success: false, message: 'Unauthorized' })
      };
    }

    const sessionToken = authHeader.replace('Bearer ', '');
    const { data: { user }, error: authError } = await supabase.auth.getUser(sessionToken);

    if (authError || !user) {
      return {
        statusCode: 401,
        body: JSON.stringify({ success: false, message: 'Invalid session' })
      };
    }

    // Verificar si ya tiene un calendario creado
    const { data: existingCal } = await supabase
      .from('google_calendar_connections')
      .select('*')
      .eq('user_id', user.id)
      .single();

    if (existingCal) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          success: true,
          calendar_id: existingCal.calendar_id,
          subscription_link: `https://calendar.google.com/calendar/u/0/r?cid=${encodeURIComponent(existingCal.calendar_id)}`,
          message: 'Calendar already exists'
        })
      };
    }

    // Obtener access token (puede necesitar refresh)
    let accessToken = process.env.GOOGLE_CALENDAR_ACCESS_TOKEN;

    // TODO: Implementar refresh token si es necesario
    // Por ahora asumimos que el token es válido

    // Crear calendario
    const calendarName = `PVB Marketing - ${user.user_metadata?.full_name || user.email}`;

    const createResponse = await fetch('https://www.googleapis.com/calendar/v3/calendars', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        summary: calendarName,
        description: 'Calendario de marketing y contenido programado - PVB',
        timeZone: 'America/Santiago'
      })
    });

    if (!createResponse.ok) {
      const error = await createResponse.text();
      console.error('Failed to create calendar:', error);
      throw new Error('Failed to create calendar');
    }

    const calendar = await createResponse.json();

    // Compartir calendario con el cliente (acceso de lectura)
    await fetch(`https://www.googleapis.com/calendar/v3/calendars/${calendar.id}/acl`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        role: 'reader',
        scope: {
          type: 'user',
          value: user.email
        }
      })
    });

    // Guardar en base de datos
    await supabase
      .from('google_calendar_connections')
      .insert({
        user_id: user.id,
        calendar_id: calendar.id,
        calendar_name: calendarName,
        created_at: new Date().toISOString(),
        sync_enabled: true
      });

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        calendar_id: calendar.id,
        calendar_name: calendarName,
        subscription_link: `https://calendar.google.com/calendar/u/0/r?cid=${encodeURIComponent(calendar.id)}`,
        message: 'Calendar created successfully'
      })
    };

  } catch (error) {
    console.error('Error in google-calendar-create:', error);
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
