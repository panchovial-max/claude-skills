-- PVB Client Portal - Supabase Schema
-- PASO 2: Habilitar RLS y crear políticas

-- Enable Row Level Security
ALTER TABLE oauth_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_metrics ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS oauth_states_insert_policy ON oauth_states;
DROP POLICY IF EXISTS oauth_states_select_policy ON oauth_states;
DROP POLICY IF EXISTS oauth_states_delete_policy ON oauth_states;

DROP POLICY IF EXISTS social_accounts_insert_policy ON social_accounts;
DROP POLICY IF EXISTS social_accounts_select_policy ON social_accounts;
DROP POLICY IF EXISTS social_accounts_update_policy ON social_accounts;
DROP POLICY IF EXISTS social_accounts_delete_policy ON social_accounts;

DROP POLICY IF EXISTS social_metrics_insert_policy ON social_metrics;
DROP POLICY IF EXISTS social_metrics_select_policy ON social_metrics;
DROP POLICY IF EXISTS social_metrics_update_policy ON social_metrics;

-- oauth_states policies
CREATE POLICY oauth_states_insert_policy
    ON oauth_states FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY oauth_states_select_policy
    ON oauth_states FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY oauth_states_delete_policy
    ON oauth_states FOR DELETE
    USING (auth.uid() = user_id);

-- social_accounts policies
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

-- social_metrics policies
CREATE POLICY social_metrics_insert_policy
    ON social_metrics FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY social_metrics_select_policy
    ON social_metrics FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY social_metrics_update_policy
    ON social_metrics FOR UPDATE
    USING (auth.uid() = user_id);
