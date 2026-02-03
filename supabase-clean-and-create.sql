-- PVB Client Portal - Supabase Schema
-- LIMPIEZA COMPLETA Y RECREACIÓN

-- Paso 1: ELIMINAR tablas viejas (si existen)
DROP TABLE IF EXISTS social_metrics CASCADE;
DROP TABLE IF EXISTS social_accounts CASCADE;
DROP TABLE IF EXISTS oauth_states CASCADE;

-- Paso 2: Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Paso 3: Crear tablas NUEVAS

-- OAuth states table (for CSRF protection)
CREATE TABLE oauth_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    state TEXT NOT NULL UNIQUE,
    platform TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT oauth_states_platform_check CHECK (platform IN ('google-ads', 'meta', 'linkedin', 'tiktok'))
);

-- Social accounts table (stores OAuth tokens)
CREATE TABLE social_accounts (
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
CREATE TABLE social_metrics (
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

-- Paso 4: Crear índices
CREATE INDEX idx_oauth_states_user_id ON oauth_states(user_id);
CREATE INDEX idx_oauth_states_state ON oauth_states(state);
CREATE INDEX idx_oauth_states_expires_at ON oauth_states(expires_at);

CREATE INDEX idx_social_accounts_user_id ON social_accounts(user_id);
CREATE INDEX idx_social_accounts_platform ON social_accounts(platform);

CREATE INDEX idx_social_metrics_user_id ON social_metrics(user_id);
CREATE INDEX idx_social_metrics_platform ON social_metrics(platform);
CREATE INDEX idx_social_metrics_date ON social_metrics(metric_date);

-- Paso 5: Habilitar RLS
ALTER TABLE oauth_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_metrics ENABLE ROW LEVEL SECURITY;

-- Paso 6: Crear políticas RLS
CREATE POLICY oauth_states_insert_policy
    ON oauth_states FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY oauth_states_select_policy
    ON oauth_states FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY oauth_states_delete_policy
    ON oauth_states FOR DELETE
    USING (auth.uid() = user_id);

CREATE POLICY social_accounts_insert_policy
    ON social_accounts FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY social_accounts_select_policy
    ON social_accounts FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY social_accounts_update_policy
    ON social_accounts FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY social_accounts_delete_policy
    ON social_accounts FOR DELETE
    USING (auth.uid() = user_id);

CREATE POLICY social_metrics_insert_policy
    ON social_metrics FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY social_metrics_select_policy
    ON social_metrics FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY social_metrics_update_policy
    ON social_metrics FOR UPDATE
    USING (auth.uid() = user_id);
