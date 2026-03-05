#!/bin/bash

# 古文字破译系统 - 错误修复脚本
# 快速修复401/404错误

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印标题
echo -e "${BLUE}======================================"
echo -e "古文字破译系统 - 错误修复脚本"
echo -e "======================================${NC}"
echo ""

# 步骤1: 停止现有服务
log_info "步骤1: 停止现有服务..."
pkill -f "uvicorn\|python.*main.py" || true
sleep 2
log_success "已停止现有服务"

# 步骤2: 检查环境变量
log_info "步骤2: 检查环境变量..."
if [ -f .env ]; then
    if grep -q "sk-your-moonshot-api-key-here" .env || \
       grep -q "your_api_key_here" .env || \
       ! grep -q "^COZE_WORKLOAD_IDENTITY_API_KEY=sk-" .env; then
        log_warning "⚠️  API Key未配置或无效！"
        echo ""
        echo "请先配置Moonshot AI API Key："
        echo "  1. 访问：https://platform.moonshot.cn/console/api-keys"
        echo "  2. 创建API Key"
        echo "  3. 复制API Key"
        echo ""
        read -p "请输入您的 Moonshot AI API Key: " api_key

        if [ -z "$api_key" ]; then
            log_error "API Key不能为空！"
            exit 1
        fi

        # 更新.env文件
        if grep -q "^COZE_WORKLOAD_IDENTITY_API_KEY=" .env; then
            sed -i "s|^COZE_WORKLOAD_IDENTITY_API_KEY=.*|COZE_WORKLOAD_IDENTITY_API_KEY=$api_key|" .env
        else
            echo "COZE_WORKLOAD_IDENTITY_API_KEY=$api_key" >> .env
        fi

        log_success "API Key已配置"
    else
        log_success "API Key已配置"
    fi
else
    log_error ".env文件不存在！"
    exit 1
fi

# 步骤3: 启动服务
log_info "步骤3: 启动服务..."
nohup python src/main.py -m http -p 5000 > /tmp/ancient-script-service.log 2>&1 &
SERVICE_PID=$!
log_success "服务已启动 (PID: $SERVICE_PID)"

# 步骤4: 等待服务启动
log_info "步骤4: 等待服务启动..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:5000/health | grep -q "ok"; then
        log_success "服务已就绪！"
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -n "."
    sleep 1
done

echo ""

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    log_error "服务启动超时！"
    log_info "查看日志：tail -f /tmp/ancient-script-service.log"
    exit 1
fi

# 步骤5: 验证服务
log_info "步骤5: 验证服务..."

# 测试健康端点
if curl -s http://localhost:5000/health | grep -q "ok"; then
    log_success "✅ 健康检查通过"
else
    log_error "❌ 健康检查失败"
    exit 1
fi

# 测试API文档
if curl -s http://localhost:5000/docs | grep -q "古文字破译系统 API"; then
    log_success "✅ API文档可访问"
else
    log_warning "⚠️  API文档可能需要额外配置"
fi

# 测试前端界面
if curl -s http://localhost:5000/static/index.html | grep -q "古代文字破解智能体"; then
    log_success "✅ 前端界面可访问"
else
    log_warning "⚠️  前端界面可能需要额外配置"
fi

# 完成
echo ""
echo -e "${GREEN}======================================"
echo -e "修复完成！🎉"
echo -e "======================================${NC}"
echo ""
echo "访问地址："
echo "  📡 API文档: http://localhost:5000/docs"
echo "  🌐 前端界面: http://localhost:5000/static/index.html"
echo "  ❤️  健康检查: http://localhost:5000/health"
echo ""
echo "服务信息："
echo "  进程ID: $SERVICE_PID"
echo "  端口: 5000"
echo "  日志: /tmp/ancient-script-service.log"
echo ""
echo "常用命令："
echo "  📋 查看状态: ps aux | grep python"
echo "  📜 查看日志: tail -f /tmp/ancient-script-service.log"
echo "  🔄 重启服务: ./fix-401-error.sh"
echo "  ⏹️  停止服务: pkill -f 'python.*main.py'"
echo ""
echo -e "${YELLOW}提示：${NC}"
echo "  • 如果仍然遇到问题，请查看日志"
echo "  • 确保5000端口未被占用"
echo "  • 确保API Key有效"
echo ""
