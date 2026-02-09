-- PVB Client Portal - Supabase Schema
-- Execute this SQL in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- OAuth states table (for CSRF protection)
CREATE TABLE IF NOT EXISTS oauth_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    state TEXT NOT NULL UNIQUE,
    platform TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT oauth_states_platform_check CHECK (platform IN ('google-ads', 'meta', 'linkedin', 'tiktok', 'notion'))
);

-- Social accounts table (stores OAuth tokens)
CREATE TABLE IF NOT EXISTS social_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    account_id TEXT NOT NULL,
    account_name TEXT,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_expires_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}'::jsonb,
    connected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_sync_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, platform, account_id)
);

-- Social metrics table (stores daily metrics)
CREATE TABLE IF NOT EXISTS social_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    account_id TEXT NOT NULL,
    metric_date DATE NOT NULL,
    metrics_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, platform, account_id, metric_date)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_oauth_states_user_id ON oauth_states(user_id);
CREATE INDEX IF NOT EXISTS idx_oauth_states_state ON oauth_states(state);
CREATE INDEX IF NOT EXISTS idx_oauth_states_expires_at ON oauth_states(expires_at);

CREATE INDEX IF NOT EXISTS idx_social_accounts_user_id ON social_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_social_accounts_platform ON social_accounts(platform);

CREATE INDEX IF NOT EXISTS idx_social_metrics_user_id ON social_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_social_metrics_platform ON social_metrics(platform);
CREATE INDEX IF NOT EXISTS idx_social_metrics_date ON social_metrics(metric_date);

-- Row Level Security (RLS)
ALTER TABLE oauth_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_metrics ENABLE ROW LEVEL SECURITY;

-- RLS Policies
-- oauth_states: Users can only access their own states
CREATE POLICY "Users can insert their own oauth states"
    ON oauth_states FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can select their own oauth states"
    ON oauth_states FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own oauth states"
    ON oauth_states FOR DELETE
    USING (auth.uid() = user_id);

-- social_accounts: Users can only access their own accounts
CREATE POLICY "Users can insert their own social accounts"
    ON social_accounts FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can select their own social accounts"
    ON social_accounts FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own social accounts"
    ON social_accounts FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own social accounts"
    ON social_accounts FOR DELETE
    USING (auth.uid() = user_id);

-- social_metrics: Users can only access their own metrics
CREATE POLICY "Users can insert their own metrics"
    ON social_metrics FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can select their own metrics"
    ON social_metrics FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own metrics"
    ON social_metrics FOR UPDATE
    USING (auth.uid() = user_id);

-- Function to clean up expired oauth states (run periodically)
CREATE OR REPLACE FUNCTION cleanup_expired_oauth_states()
RETURNS void AS $$
BEGIN
    DELETE FROM oauth_states WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Notion calendar events table (stores content calendar items from Notion)
CREATE TABLE IF NOT EXISTS notion_calendar_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    notion_account_id TEXT NOT NULL, -- workspace_id
    database_id TEXT NOT NULL, -- ID de la base de Notion
    page_id TEXT NOT NULL UNIQUE, -- ID del page/evento
    title TEXT NOT NULL,
    event_date DATE NOT NULL,
    event_type TEXT, -- 'post', 'task', 'campaign', etc.
    status TEXT, -- 'scheduled', 'published', 'draft'
    platform TEXT[], -- ['instagram', 'facebook', 'linkedin']
    metadata JSONB DEFAULT '{}'::jsonb, -- Datos completos del page
    synced_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, page_id)
);

-- Indexes for notion_calendar_events
CREATE INDEX IF NOT EXISTS idx_notion_events_user_id ON notion_calendar_events(user_id);
CREATE INDEX IF NOT EXISTS idx_notion_events_date ON notion_calendar_events(event_date);
CREATE INDEX IF NOT EXISTS idx_notion_events_database_id ON notion_calendar_events(database_id);

-- RLS for notion_calendar_events
ALTER TABLE notion_calendar_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can select their own notion events"
    ON notion_calendar_events FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own notion events"
    ON notion_calendar_events FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own notion events"
    ON notion_calendar_events FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own notion events"
    ON notion_calendar_events FOR DELETE
    USING (auth.uid() = user_id);

-- Google Calendar connections table (stores client calendar IDs)
CREATE TABLE IF NOT EXISTS google_calendar_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    calendar_id TEXT NOT NULL, -- Google Calendar ID created for this client
    calendar_name TEXT NOT NULL DEFAULT 'PVB - Contenido Programado',
    access_token TEXT, -- Optional: if client grants write access
    refresh_token TEXT,
    token_expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_sync_at TIMESTAMP WITH TIME ZONE,
    sync_enabled BOOLEAN DEFAULT true,
    UNIQUE(user_id)
);

-- Indexes for google_calendar_connections
CREATE INDEX IF NOT EXISTS idx_gcal_user_id ON google_calendar_connections(user_id);
CREATE INDEX IF NOT EXISTS idx_gcal_calendar_id ON google_calendar_connections(calendar_id);

-- RLS for google_calendar_connections
ALTER TABLE google_calendar_connections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can select their own calendar connection"
    ON google_calendar_connections FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own calendar connection"
    ON google_calendar_connections FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own calendar connection"
    ON google_calendar_connections FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own calendar connection"
    ON google_calendar_connections FOR DELETE
    USING (auth.uid() = user_id);
