-- 古文字破译系统 - 数据库初始化脚本
-- 此脚本会在 PostgreSQL 容器首次启动时自动执行

-- 设置编码
SET client_encoding = 'UTF8';

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ========================================
-- 用户表
-- ========================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE
);

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- ========================================
-- 会话表
-- ========================================
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    metadata JSONB
);

-- 创建索引
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_session_id ON sessions(session_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);

-- ========================================
-- 古文字分析记录表
-- ========================================
CREATE TABLE IF NOT EXISTS ancient_text_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    session_id VARCHAR(255),
    text_type VARCHAR(50) NOT NULL, -- 文字类型：甲骨文、金文、埃及圣书体等
    text_content TEXT, -- 原始文本内容
    image_url TEXT, -- 图片URL
    analysis_result JSONB NOT NULL, -- 分析结果（JSON格式）
    translation TEXT, -- 翻译结果
    historical_context TEXT, -- 历史背景
    confidence_score DECIMAL(5,4), -- 置信度分数（0-1）
    ai_tools_used JSONB, -- 使用的AI工具
    methods_applied JSONB, -- 应用方法
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_analyses_user_id ON ancient_text_analyses(user_id);
CREATE INDEX idx_analyses_session_id ON ancient_text_analyses(session_id);
CREATE INDEX idx_analyses_text_type ON ancient_text_analyses(text_type);
CREATE INDEX idx_analyses_created_at ON ancient_text_analyses(created_at);
CREATE INDEX idx_analyses_confidence ON ancient_text_analyses(confidence_score);

-- 创建全文搜索索引
CREATE INDEX idx_analyses_translation_gin ON ancient_text_analyses USING gin(to_tsvector('chinese', translation));
CREATE INDEX idx_analyses_text_content_gin ON ancient_text_analyses USING gin(to_tsvector('chinese', text_content));

-- ========================================
-- 符号库表
-- ========================================
CREATE TABLE IF NOT EXISTS symbols (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    script_type VARCHAR(50) NOT NULL, -- 文字类型：甲骨文、埃及圣书体等
    symbol_code VARCHAR(50) NOT NULL, -- 符号编码（Unicode、Gardiner编号等）
    symbol_image_url TEXT, -- 符号图片URL
    pronunciation VARCHAR(100), -- 发音
    meaning TEXT NOT NULL, -- 含义
    category VARCHAR(50), -- 符号类别：表意、表音、限定符等
    description TEXT, -- 详细描述
    examples JSONB, -- 使用示例
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(script_type, symbol_code)
);

-- 创建索引
CREATE INDEX idx_symbols_script_type ON symbols(script_type);
CREATE INDEX idx_symbols_symbol_code ON symbols(symbol_code);
CREATE INDEX idx_symbols_category ON symbols(category);
CREATE INDEX idx_symbols_meaning_gin ON symbols USING gin(to_tsvector('chinese', meaning));

-- ========================================
-- 工具使用记录表
-- ========================================
CREATE TABLE IF NOT EXISTS tool_usage_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    session_id VARCHAR(255),
    tool_name VARCHAR(100) NOT NULL, -- 工具名称
    tool_type VARCHAR(50) NOT NULL, -- 工具类型：OCR、翻译、破译等
    input_data JSONB, -- 输入数据
    output_data JSONB, -- 输出数据
    execution_time INTEGER, -- 执行时间（毫秒）
    success BOOLEAN NOT NULL, -- 是否成功
    error_message TEXT, -- 错误信息
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_tool_logs_user_id ON tool_usage_logs(user_id);
CREATE INDEX idx_tool_logs_session_id ON tool_usage_logs(session_id);
CREATE INDEX idx_tool_logs_tool_name ON tool_usage_logs(tool_name);
CREATE INDEX idx_tool_logs_created_at ON tool_usage_logs(created_at);
CREATE INDEX idx_tool_logs_success ON tool_usage_logs(success);

-- ========================================
-- 系统配置表
-- ========================================
CREATE TABLE IF NOT EXISTS system_configs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    config_type VARCHAR(50) DEFAULT 'string', -- 配置类型：string, integer, boolean, json
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_configs_config_key ON system_configs(config_key);

-- 插入默认配置
INSERT INTO system_configs (config_key, config_value, config_type, description) VALUES
    ('max_analyses_per_day', '100', 'integer', '每天最大分析次数'),
    ('enable_ai_cache', 'true', 'boolean', '是否启用AI缓存'),
    ('default_model', 'kimi-k2-5-260127', 'string', '默认模型名称')
ON CONFLICT (config_key) DO NOTHING;

-- ========================================
-- 反馈表
-- ========================================
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    analysis_id UUID REFERENCES ancient_text_analyses(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5), -- 评分（1-5）
    comment TEXT, -- 评论
    is_helpful BOOLEAN, -- 是否有帮助
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_feedback_user_id ON feedback(user_id);
CREATE INDEX idx_feedback_analysis_id ON feedback(analysis_id);
CREATE INDEX idx_feedback_rating ON feedback(rating);
CREATE INDEX idx_feedback_created_at ON feedback(created_at);

-- ========================================
-- 更新时间戳的触发器函数
-- ========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为所有表创建触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_analyses_updated_at BEFORE UPDATE ON ancient_text_analyses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_symbols_updated_at BEFORE UPDATE ON symbols
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_configs_updated_at BEFORE UPDATE ON system_configs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- 插入示例数据
-- ========================================

-- 插入示例符号（埃及象形文字）
INSERT INTO symbols (script_type, symbol_code, symbol_image_url, pronunciation, meaning, category, description) VALUES
    ('埃及圣书体', 'A19', 'https://example.com/symbols/A19.png', 'rnp.t', '老年、年岁', '限定符', '老人拄拐杖，表示老年或年岁'),
    ('埃及圣书体', 'G5', 'https://example.com/symbols/G5.png', 'ḥr', '荷鲁斯', '表意符', '隼，象征荷鲁斯神'),
    ('埃及圣书体', 'N5', 'https://example.com/symbols/N5.png', 'rˁ', '太阳', '表意符', '太阳圆盘，象征拉神')
ON CONFLICT (script_type, symbol_code) DO NOTHING;

-- 插入示例符号（甲骨文）
INSERT INTO symbols (script_type, symbol_code, symbol_image_url, pronunciation, meaning, category, description) VALUES
    ('甲骨文', '日', 'https://example.com/symbols/sun.png', 'rì', '太阳', '表意符', '太阳的象形'),
    ('甲骨文', '月', 'https://example.com/symbols/moon.png', 'yuè', '月亮', '表意符', '月亮的象形'),
    ('甲骨文', '人', 'https://example.com/symbols/person.png', 'rén', '人', '表意符', '人的象形')
ON CONFLICT (script_type, symbol_code) DO NOTHING;

-- ========================================
-- 创建视图
-- ========================================

-- 用户分析统计视图
CREATE OR REPLACE VIEW user_analysis_stats AS
SELECT
    u.id as user_id,
    u.username,
    COUNT(a.id) as total_analyses,
    COUNT(DISTINCT a.text_type) as unique_text_types,
    AVG(a.confidence_score) as avg_confidence,
    MAX(a.created_at) as last_analysis_at
FROM users u
LEFT JOIN ancient_text_analyses a ON u.id = a.user_id
GROUP BY u.id, u.username;

-- 工具使用统计视图
CREATE OR REPLACE VIEW tool_usage_stats AS
SELECT
    tool_name,
    tool_type,
    COUNT(*) as total_usage,
    COUNT(*) FILTER (WHERE success = true) as successful_usage,
    COUNT(*) FILTER (WHERE success = false) as failed_usage,
    AVG(execution_time) as avg_execution_time,
    MAX(created_at) as last_used_at
FROM tool_usage_logs
GROUP BY tool_name, tool_type;

-- ========================================
-- 创建函数
-- ========================================

-- 清理过期会话的函数
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM sessions WHERE expires_at < CURRENT_TIMESTAMP;
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- 获取用户最近分析的函数
CREATE OR REPLACE FUNCTION get_user_recent_analyses(p_user_id UUID, p_limit INTEGER DEFAULT 10)
RETURNS TABLE (
    id UUID,
    text_type VARCHAR,
    text_content TEXT,
    translation TEXT,
    confidence_score DECIMAL,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.text_type,
        a.text_content,
        a.translation,
        a.confidence_score,
        a.created_at
    FROM ancient_text_analyses a
    WHERE a.user_id = p_user_id
    ORDER BY a.created_at DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- ========================================
-- 完成
-- ========================================

-- 输出初始化完成信息
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE '数据库初始化完成！';
    RAISE NOTICE '========================================';
    RAISE NOTICE '已创建的表：';
    RAISE NOTICE '  - users (用户表)';
    RAISE NOTICE '  - sessions (会话表)';
    RAISE NOTICE '  - ancient_text_analyses (古文字分析记录表)';
    RAISE NOTICE '  - symbols (符号库表)';
    RAISE NOTICE '  - tool_usage_logs (工具使用记录表)';
    RAISE NOTICE '  - system_configs (系统配置表)';
    RAISE NOTICE '  - feedback (反馈表)';
    RAISE NOTICE '========================================';
    RAISE NOTICE '已创建的视图：';
    RAISE NOTICE '  - user_analysis_stats (用户分析统计)';
    RAISE NOTICE '  - tool_usage_stats (工具使用统计)';
    RAISE NOTICE '========================================';
    RAISE NOTICE '已创建的函数：';
    RAISE NOTICE '  - cleanup_expired_sessions()';
    RAISE NOTICE '  - get_user_recent_analyses()';
    RAISE NOTICE '========================================';
END $$;
