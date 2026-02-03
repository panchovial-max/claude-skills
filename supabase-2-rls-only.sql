-- PVB Client Portal - PARTE 2: RLS y Políticas
-- Ejecuta ESTE después de la Parte 1

-- Habilitar RLS
ALTER TABLE oauth_states ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_metrics ENABLE ROW LEVEL SECURITY;

-- Políticas para oauth_states
CREATE POLICY oauth_states_insert_policy ON oauth_states FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY oauth_states_select_policy ON oauth_states FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY oauth_states_delete_policy ON oauth_states FOR DELETE USING (auth.uid() = user_id);

-- Políticas para social_accounts
CREATE POLICY social_accounts_insert_policy ON social_accounts FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY social_accounts_select_policy ON social_accounts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY social_accounts_update_policy ON social_accounts FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY social_accounts_delete_policy ON social_accounts FOR DELETE USING (auth.uid() = user_id);

-- Políticas para social_metrics
CREATE POLICY social_metrics_insert_policy ON social_metrics FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY social_metrics_select_policy ON social_metrics FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY social_metrics_update_policy ON social_metrics FOR UPDATE USING (auth.uid() = user_id);
