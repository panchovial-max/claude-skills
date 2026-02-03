import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

/**
 * Sincroniza métricas desde todas las plataformas conectadas
 * Puede ser llamado manualmente o programado (cron job)
 */
export const handler = async (event, context) => {
  try {
    // Validar sesión del usuario (si se llama manualmente)
    const authHeader = event.headers.authorization;
    let userId = null;

    if (authHeader && authHeader.startsWith('Bearer ')) {
      const sessionToken = authHeader.replace('Bearer ', '');
      const { data: { user }, error: authError } = await supabase.auth.getUser(sessionToken);

      if (!authError && user) {
        userId = user.id;
      }
    }

    // Si no hay userId, es una ejecución programada - sincronizar todos los usuarios
    let accountsToSync = [];

    if (userId) {
      // Sincronizar solo las cuentas de este usuario
      const { data: accounts } = await supabase
        .from('social_accounts')
        .select('*')
        .eq('user_id', userId);

      accountsToSync = accounts || [];
    } else {
      // Sincronizar todas las cuentas (cron job)
      const { data: accounts } = await supabase
        .from('social_accounts')
        .select('*');

      accountsToSync = accounts || [];
    }

    const results = {
      success: true,
      synced: 0,
      failed: 0,
      errors: []
    };

    // Sincronizar cada cuenta
    for (const account of accountsToSync) {
      try {
        let metrics = null;

        switch (account.platform) {
          case 'google-ads':
            metrics = await fetchGoogleAdsMetrics(account);
            break;
          case 'meta':
          case 'meta-ad-account':
            metrics = await fetchMetaMetrics(account);
            break;
          case 'linkedin':
            metrics = await fetchLinkedInMetrics(account);
            break;
          case 'tiktok':
            metrics = await fetchTikTokMetrics(account);
            break;
          default:
            console.log(`Unknown platform: ${account.platform}`);
            continue;
        }

        if (metrics) {
          // Guardar métricas en la base de datos
          await saveMetrics(account.user_id, account.platform, account.account_id, metrics);

          // Actualizar last_sync_at
          await supabase
            .from('social_accounts')
            .update({ last_sync_at: new Date().toISOString() })
            .eq('id', account.id);

          results.synced++;
        }
      } catch (error) {
        console.error(`Error syncing ${account.platform} (${account.account_id}):`, error);
        results.failed++;
        results.errors.push({
          platform: account.platform,
          account_id: account.account_id,
          error: error.message
        });
      }
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(results)
    };

  } catch (error) {
    console.error('Error in metrics-sync:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        message: 'Internal server error',
        error: error.message
      })
    };
  }
};

/**
 * Fetch Google Ads metrics
 */
async function fetchGoogleAdsMetrics(account) {
  const accessToken = account.access_token;
  const customerId = account.metadata?.customer_id;

  if (!customerId || customerId === 'pending') {
    console.log('Google Ads Customer ID not configured yet');
    return null;
  }

  // Google Ads API v14
  const apiUrl = `https://googleads.googleapis.com/v14/customers/${customerId}/googleAds:searchStream`;

  // Query para obtener métricas de los últimos 7 días
  const query = `
    SELECT
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.ctr,
      metrics.average_cpc,
      metrics.conversion_rate,
      metrics.cost_per_conversion
    FROM campaign
    WHERE segments.date DURING LAST_7_DAYS
  `;

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
      'developer-token': process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
      'login-customer-id': customerId
    },
    body: JSON.stringify({ query })
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Google Ads API error: ${errorText}`);
  }

  const data = await response.json();

  // Agregar métricas
  let totalImpressions = 0;
  let totalClicks = 0;
  let totalCost = 0;
  let totalConversions = 0;

  if (data.results) {
    data.results.forEach(row => {
      const metrics = row.metrics;
      totalImpressions += parseInt(metrics.impressions || 0);
      totalClicks += parseInt(metrics.clicks || 0);
      totalCost += parseInt(metrics.cost_micros || 0) / 1000000; // Convert micros to currency
      totalConversions += parseFloat(metrics.conversions || 0);
    });
  }

  const avgCtr = totalImpressions > 0 ? (totalClicks / totalImpressions) * 100 : 0;
  const avgCpc = totalClicks > 0 ? totalCost / totalClicks : 0;
  const conversionRate = totalClicks > 0 ? (totalConversions / totalClicks) * 100 : 0;
  const costPerConversion = totalConversions > 0 ? totalCost / totalConversions : 0;

  return {
    impressions: totalImpressions,
    clicks: totalClicks,
    spend: totalCost,
    conversions: totalConversions,
    ctr: avgCtr,
    cpc: avgCpc,
    conversion_rate: conversionRate,
    cost_per_conversion: costPerConversion,
    period: 'last_7_days'
  };
}

/**
 * Fetch Meta (Facebook + Instagram) metrics
 */
async function fetchMetaMetrics(account) {
  const accessToken = account.access_token;
  const accountId = account.account_id;

  // Para Meta Ad Accounts
  let adAccountId = accountId;
  if (account.platform === 'meta') {
    // Es la cuenta principal, obtener el primer ad account
    const adAccounts = account.metadata?.ad_accounts;
    if (!adAccounts || adAccounts.length === 0) {
      console.log('No ad accounts found for Meta account');
      return null;
    }
    adAccountId = adAccounts[0].id;
  }

  // Fecha de hoy y 7 días atrás
  const today = new Date();
  const sevenDaysAgo = new Date(today);
  sevenDaysAgo.setDate(today.getDate() - 7);

  const dateFormat = (date) => date.toISOString().split('T')[0];

  // Insights API
  const insightsUrl = `https://graph.facebook.com/v18.0/${adAccountId}/insights`;
  const params = new URLSearchParams({
    access_token: accessToken,
    time_range: JSON.stringify({
      since: dateFormat(sevenDaysAgo),
      until: dateFormat(today)
    }),
    fields: 'impressions,clicks,spend,cpc,cpm,ctr,reach,frequency,actions,conversions',
    level: 'account'
  });

  const response = await fetch(`${insightsUrl}?${params}`);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Meta API error: ${errorText}`);
  }

  const data = await response.json();

  if (!data.data || data.data.length === 0) {
    return {
      impressions: 0,
      clicks: 0,
      spend: 0,
      reach: 0,
      ctr: 0,
      cpc: 0,
      cpm: 0,
      period: 'last_7_days'
    };
  }

  const metrics = data.data[0];

  return {
    impressions: parseInt(metrics.impressions || 0),
    clicks: parseInt(metrics.clicks || 0),
    spend: parseFloat(metrics.spend || 0),
    reach: parseInt(metrics.reach || 0),
    ctr: parseFloat(metrics.ctr || 0),
    cpc: parseFloat(metrics.cpc || 0),
    cpm: parseFloat(metrics.cpm || 0),
    frequency: parseFloat(metrics.frequency || 0),
    conversions: metrics.conversions ? parseInt(metrics.conversions) : 0,
    period: 'last_7_days'
  };
}

/**
 * Fetch LinkedIn metrics
 */
async function fetchLinkedInMetrics(account) {
  const accessToken = account.access_token;
  const organizationId = account.account_id;

  // LinkedIn Analytics API
  const analyticsUrl = `https://api.linkedin.com/v2/organizationalEntityShareStatistics`;
  const params = new URLSearchParams({
    q: 'organizationalEntity',
    organizationalEntity: `urn:li:organization:${organizationId}`
  });

  const response = await fetch(`${analyticsUrl}?${params}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'LinkedIn-Version': '202310'
    }
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`LinkedIn API error: ${errorText}`);
  }

  const data = await response.json();

  // Procesar métricas de LinkedIn
  let totalImpressions = 0;
  let totalClicks = 0;
  let totalEngagement = 0;

  if (data.elements) {
    data.elements.forEach(element => {
      const stats = element.totalShareStatistics;
      totalImpressions += parseInt(stats.impressionCount || 0);
      totalClicks += parseInt(stats.clickCount || 0);
      totalEngagement += parseInt(stats.engagement || 0);
    });
  }

  return {
    impressions: totalImpressions,
    clicks: totalClicks,
    engagement: totalEngagement,
    ctr: totalImpressions > 0 ? (totalClicks / totalImpressions) * 100 : 0,
    period: 'last_7_days'
  };
}

/**
 * Fetch TikTok metrics
 */
async function fetchTikTokMetrics(account) {
  const accessToken = account.access_token;
  const advertiserId = account.account_id;

  // TikTok Ads Reporting API
  const reportUrl = 'https://business-api.tiktok.com/open_api/v1.3/reports/integrated/get/';

  const today = new Date();
  const sevenDaysAgo = new Date(today);
  sevenDaysAgo.setDate(today.getDate() - 7);

  const dateFormat = (date) => date.toISOString().split('T')[0];

  const requestBody = {
    advertiser_id: advertiserId,
    service_type: 'AUCTION',
    report_type: 'BASIC',
    data_level: 'AUCTION_ADVERTISER',
    dimensions: ['advertiser_id'],
    metrics: [
      'impressions',
      'clicks',
      'spend',
      'cpc',
      'cpm',
      'ctr',
      'conversions',
      'conversion_rate'
    ],
    start_date: dateFormat(sevenDaysAgo),
    end_date: dateFormat(today),
    page: 1,
    page_size: 1000
  };

  const response = await fetch(reportUrl, {
    method: 'POST',
    headers: {
      'Access-Token': accessToken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`TikTok API error: ${errorText}`);
  }

  const data = await response.json();

  if (!data.data || !data.data.list || data.data.list.length === 0) {
    return {
      impressions: 0,
      clicks: 0,
      spend: 0,
      ctr: 0,
      cpc: 0,
      cpm: 0,
      conversions: 0,
      period: 'last_7_days'
    };
  }

  const metrics = data.data.list[0].metrics;

  return {
    impressions: parseInt(metrics.impressions || 0),
    clicks: parseInt(metrics.clicks || 0),
    spend: parseFloat(metrics.spend || 0),
    ctr: parseFloat(metrics.ctr || 0),
    cpc: parseFloat(metrics.cpc || 0),
    cpm: parseFloat(metrics.cpm || 0),
    conversions: parseInt(metrics.conversions || 0),
    conversion_rate: parseFloat(metrics.conversion_rate || 0),
    period: 'last_7_days'
  };
}

/**
 * Guarda las métricas en la base de datos
 */
async function saveMetrics(userId, platform, accountId, metrics) {
  const { error } = await supabase
    .from('social_metrics')
    .insert({
      user_id: userId,
      platform: platform,
      account_id: accountId,
      metric_date: new Date().toISOString().split('T')[0],
      metrics_data: metrics,
      created_at: new Date().toISOString()
    });

  if (error) {
    // Si ya existe un registro para hoy, actualizarlo
    if (error.code === '23505') { // Duplicate key
      await supabase
        .from('social_metrics')
        .update({
          metrics_data: metrics,
          updated_at: new Date().toISOString()
        })
        .eq('user_id', userId)
        .eq('platform', platform)
        .eq('account_id', accountId)
        .eq('metric_date', new Date().toISOString().split('T')[0]);
    } else {
      throw error;
    }
  }
}
