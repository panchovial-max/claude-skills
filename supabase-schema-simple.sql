-- PVB Client Portal - Supabase Schema (Simplified)
-- Execute this SQL in Supabase SQL Editor
-- Part 1: Create tables without foreign keys

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- OAuth states table (for CSRF protection)
CREATE TABLE IF NOT EXISTS oauth_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    state TEXT NOT NULL UNIQUE,
    platform TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT oauth_states_platform_check CHECK (platform IN ('google-ads', 'meta', 'linkedin', 'tiktok'))
);

-- Social accounts table (stores OAuth tokens)
CREATE TABLE IF NOT EXISTS social_accounts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
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
    user_id UUID NOT NULL,
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

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can insert their own oauth states" ON oauth_states;
DROP POLICY IF EXISTS "Users can select their own oauth states" ON oauth_states;
DROP POLICY IF EXISTS "Users can delete their own oauth states" ON oauth_states;
DROP POLICY IF EXISTS "Users can insert their own social accounts" ON social_accounts;
DROP POLICY IF EXISTS "Users can select their own social accounts" ON social_accounts;
DROP POLICY IF EXISTS "Users can update their own social accounts" ON social_accounts;
DROP POLICY IF EXISTS "Users can delete their own social accounts" ON social_accounts;
DROP POLICY IF EXISTS "Users can insert their own metrics" ON social_metrics;
DROP POLICY IF EXISTS "Users can select their own metrics" ON social_metrics;
DROP POLICY IF EXISTS "Users can update their own metrics" ON social_metrics;

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
