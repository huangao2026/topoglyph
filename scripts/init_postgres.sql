-- 古文字破译系统 - PostgreSQL 初始化脚本
-- 此脚本在数据库首次创建时自动执行

-- 创建扩展（如果需要）
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 设置数据库编码
ALTER DATABASE ancient_script SET client_encoding TO 'utf8';

-- 设置时区
ALTER DATABASE ancient_script SET timezone TO 'Asia/Shanghai';

-- 创建函数：自动更新 updated_at 字段
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 创建触发器：自动更新 updated_at
-- 注意：这些触发器会在 SQLAlchemy 创建表时自动创建
-- 如果需要手动创建，请取消以下注释并执行

-- -- 用户表
-- CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
--     FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- -- 会话表
-- CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
--     FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- -- 对话记录表
-- CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
--     FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- -- 插件表
-- CREATE TRIGGER update_plugins_updated_at BEFORE UPDATE ON plugins
--     FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- -- 工具表
-- CREATE TRIGGER update_tools_updated_at BEFORE UPDATE ON tools
--     FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 创建索引优化查询性能
-- 这些索引会在 SQLAlchemy 模型中自动创建
-- 如果需要手动创建，请取消以下注释并执行

-- -- 用户表索引
-- CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
-- CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
-- CREATE INDEX IF NOT EXISTS idx_users_api_key ON users(api_key);
-- CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- -- 会话表索引
-- CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON sessions(session_id);
-- CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
-- CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at);
-- CREATE INDEX IF NOT EXISTS idx_sessions_is_active ON sessions(is_active);

-- -- 消息表索引
-- CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);
-- CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role);
-- CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
-- CREATE INDEX IF NOT EXISTS idx_messages_session_created ON messages(session_id, created_at);

-- -- 对话记录表索引
-- CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
-- CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
-- CREATE INDEX IF NOT EXISTS idx_conversations_script_type ON conversations(script_type);
-- CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);

-- -- 分析历史表索引
-- CREATE INDEX IF NOT EXISTS idx_analysis_history_user_id ON analysis_history(user_id);
-- CREATE INDEX IF NOT EXISTS idx_analysis_history_session_id ON analysis_history(session_id);
-- CREATE INDEX IF NOT EXISTS idx_analysis_history_script_type ON analysis_history(script_type);
-- CREATE INDEX IF NOT EXISTS idx_analysis_history_created_at ON analysis_history(created_at);

-- -- 插件表索引
-- CREATE INDEX IF NOT EXISTS idx_plugins_name ON plugins(name);
-- CREATE INDEX IF NOT EXISTS idx_plugins_enabled ON plugins(enabled);
-- CREATE INDEX IF NOT EXISTS idx_plugins_created_at ON plugins(created_at);

-- -- 工具表索引
-- CREATE INDEX IF NOT EXISTS idx_tools_name ON tools(name);
-- CREATE INDEX IF NOT EXISTS idx_tools_category ON tools(category);
-- CREATE INDEX IF NOT EXISTS idx_tools_enabled ON tools(enabled);

-- -- 系统日志表索引
-- CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(level);
-- CREATE INDEX IF NOT EXISTS idx_system_logs_module ON system_logs(module);
-- CREATE INDEX IF NOT EXISTS idx_system_logs_user_id ON system_logs(user_id);
-- CREATE INDEX IF NOT EXISTS idx_system_logs_session_id ON system_logs(session_id);
-- CREATE INDEX IF NOT EXISTS idx_system_logs_created_at ON system_logs(created_at);
-- CREATE INDEX IF NOT EXISTS idx_system_logs_level_created ON system_logs(level, created_at);

-- -- 系统指标表索引
-- CREATE INDEX IF NOT EXISTS idx_system_metrics_metric_name ON system_metrics(metric_name);
-- CREATE INDEX IF NOT EXISTS idx_system_metrics_created_at ON system_metrics(created_at);

-- 创建视图：常用查询
CREATE OR REPLACE VIEW v_user_stats AS
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(DISTINCT s.id) as session_count,
    COUNT(DISTINCT c.id) as conversation_count,
    MAX(s.updated_at) as last_activity,
    u.created_at
FROM users u
LEFT JOIN sessions s ON u.id = s.user_id
LEFT JOIN conversations c ON s.id = c.session_id
GROUP BY u.id, u.username, u.email, u.created_at;

-- 创建视图：会话统计
CREATE OR REPLACE VIEW v_session_stats AS
SELECT 
    s.id,
    s.session_id,
    s.title,
    s.user_id,
    s.is_active,
    COUNT(m.id) as message_count,
    MIN(m.created_at) as first_message_time,
    MAX(m.created_at) as last_message_time,
    s.created_at
FROM sessions s
LEFT JOIN messages m ON s.session_id = m.session_id
GROUP BY s.id, s.session_id, s.title, s.user_id, s.is_active, s.created_at;

-- 创建视图：工具使用统计
CREATE OR REPLACE VIEW v_tool_stats AS
SELECT 
    t.id,
    t.name,
    t.display_name,
    t.category,
    t.enabled,
    t.usage_count,
    t.success_rate,
    COUNT(c.id) as conversation_count,
    MAX(c.created_at) as last_used
FROM tools t
LEFT JOIN conversations c ON t.name = ANY(c.tools_used)
GROUP BY t.id, t.name, t.display_name, t.category, t.enabled, t.usage_count, t.success_rate;

-- 创建视图：分析历史统计
CREATE OR REPLACE VIEW v_analysis_stats AS
SELECT 
    DATE(created_at) as date,
    script_type,
    COUNT(*) as count,
    AVG(confidence_score) as avg_confidence,
    AVG(processing_time) as avg_processing_time,
    SUM(tokens_used) as total_tokens
FROM analysis_history
GROUP BY DATE(created_at), script_type
ORDER BY date DESC, count DESC;

-- 创建函数：清理过期数据
CREATE OR REPLACE FUNCTION cleanup_expired_data()
RETURNS void AS $$
BEGIN
    -- 删除90天前的系统日志
    DELETE FROM system_logs
    WHERE created_at < NOW() - INTERVAL '90 days';
    
    -- 删除180天前的系统指标
    DELETE FROM system_metrics
    WHERE created_at < NOW() - INTERVAL '180 days';
    
    -- 删除365天前的非活跃会话
    DELETE FROM messages
    WHERE session_id IN (
        SELECT session_id FROM sessions
        WHERE updated_at < NOW() - INTERVAL '365 days'
        AND is_active = false
    );
    
    DELETE FROM conversations
    WHERE session_id IN (
        SELECT session_id FROM sessions
        WHERE updated_at < NOW() - INTERVAL '365 days'
        AND is_active = false
    );
    
    DELETE FROM sessions
    WHERE updated_at < NOW() - INTERVAL '365 days'
    AND is_active = false;
    
    RAISE NOTICE '过期数据清理完成';
END;
$$ LANGUAGE plpgsql;

-- 创建函数：生成统计报告
CREATE OR REPLACE FUNCTION generate_daily_stats()
RETURNS TABLE (
    stat_date date,
    total_users int,
    active_users int,
    total_sessions int,
    active_sessions int,
    total_messages int,
    total_analyses int,
    avg_confidence float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CURRENT_DATE as stat_date,
        (SELECT COUNT(*) FROM users WHERE created_at <= CURRENT_DATE) as total_users,
        (SELECT COUNT(DISTINCT user_id) FROM sessions WHERE updated_at >= CURRENT_DATE) as active_users,
        (SELECT COUNT(*) FROM sessions WHERE created_at <= CURRENT_DATE) as total_sessions,
        (SELECT COUNT(*) FROM sessions WHERE updated_at >= CURRENT_DATE AND is_active = true) as active_sessions,
        (SELECT COUNT(*) FROM messages WHERE created_at >= CURRENT_DATE) as total_messages,
        (SELECT COUNT(*) FROM analysis_history WHERE created_at >= CURRENT_DATE) as total_analyses,
        (SELECT AVG(confidence_score) FROM analysis_history WHERE created_at >= CURRENT_DATE) as avg_confidence;
END;
$$ LANGUAGE plpgsql;

-- 创建定时任务（需要 pg_cron 扩展）
-- 如果需要启用定时任务，请先安装 pg_cron 扩展：
-- CREATE EXTENSION pg_cron;

-- 每天凌晨2点清理过期数据
-- SELECT cron.schedule('cleanup_expired_data', '0 2 * * *', 'SELECT cleanup_expired_data()');

-- 每小时生成统计报告
-- SELECT cron.schedule('generate_hourly_stats', '0 * * * *', 'SELECT * FROM generate_daily_stats()');

-- 打印初始化完成信息
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'PostgreSQL 数据库初始化完成';
    RAISE NOTICE '========================================';
    RAISE NOTICE '已创建的内容：';
    RAISE NOTICE '  - 更新时间戳触发器函数';
    RAISE NOTICE '  - 统计视图（用户、会话、工具、分析）';
    RAISE NOTICE '  - 数据清理函数';
    RAISE NOTICE '  - 统计报告函数';
    RAISE NOTICE '';
    RAISE NOTICE '注意：数据库表和索引由 SQLAlchemy 自动创建';
    RAISE NOTICE '========================================';
END $$;
