import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Get comments for a specific calendar event
 * GET /comments?event_id=xxx
 */
export const handler = async (event, context) => {
  if (event.httpMethod !== 'GET') {
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

    // Get event_id from query params
    const eventId = event.queryStringParameters?.event_id;

    if (!eventId) {
      return {
        statusCode: 400,
        body: JSON.stringify({ success: false, message: 'event_id is required' })
      };
    }

    // Fetch comments for this event
    const { data: comments, error: fetchError } = await supabase
      .from('campaign_comments')
      .select('*')
      .eq('event_id', eventId)
      .order('created_at', { ascending: true });

    if (fetchError) {
      console.error('Error fetching comments:', fetchError);
      throw new Error('Failed to fetch comments');
    }

    // Mark unread comments as read for the current user
    const unreadComments = comments.filter(c => !c.is_read && c.user_id !== user.id);
    if (unreadComments.length > 0) {
      await supabase
        .from('campaign_comments')
        .update({ is_read: true })
        .in('id', unreadComments.map(c => c.id));
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        comments: comments || [],
        total: comments?.length || 0
      })
    };

  } catch (error) {
    console.error('Error in comments-get:', error);
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
