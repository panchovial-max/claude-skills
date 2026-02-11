import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Post a new comment on a calendar event
 * POST /comments
 * Body: { event_id, message }
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

    // Parse request body
    const body = JSON.parse(event.body);
    const { event_id, message } = body;

    if (!event_id || !message) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          success: false,
          message: 'event_id and message are required'
        })
      };
    }

    // Determinar el rol del usuario (cliente o agencia)
    // Por ahora, asumimos que info@panchovial.com es agencia
    const isAgency = user.email === 'info@panchovial.com' ||
                     user.email?.includes('@panchovial.com');
    const authorRole = isAgency ? 'agency' : 'client';

    // Crear el comentario
    const { data: comment, error: insertError } = await supabase
      .from('campaign_comments')
      .insert({
        event_id: event_id,
        user_id: user.id,
        author_name: user.user_metadata?.full_name || user.email,
        author_email: user.email,
        author_role: authorRole,
        message: message.trim(),
        is_read: false
      })
      .select()
      .single();

    if (insertError) {
      console.error('Error creating comment:', insertError);
      throw new Error('Failed to create comment');
    }

    // TODO: Enviar notificación por email al otro usuario
    // await sendCommentNotification(event_id, comment);

    return {
      statusCode: 201,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        comment: comment,
        message: 'Comment posted successfully'
      })
    };

  } catch (error) {
    console.error('Error in comments-post:', error);
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
 * Helper function to send email notification (to be implemented)
 */
async function sendCommentNotification(eventId, comment) {
  // TODO: Implement email notification
  // - Find the other party (client if agency commented, vice versa)
  // - Send email with comment details
  // - Link back to the event in the calendar
  console.log('TODO: Send email notification for comment on event:', eventId);
}
