#!/bin/bash

# 古文字破译系统 - 功能测试脚本
# 使用方法: ./test_system.sh

set -e

BASE_URL="http://localhost:8000"
API_URL="$BASE_URL/api/v1"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数器
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 测试函数
test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo -e "\n${YELLOW}测试 $TOTAL_TESTS: $name${NC}"
    echo "请求: $method $endpoint"

    if [ -z "$data" ]; then
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" -w "\n%{http_code}")
    else
        response=$(curl -s -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" \
            -w "\n%{http_code}")
    fi

    # 分离响应体和HTTP状态码
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ 测试通过${NC} (HTTP $http_code)"
        echo "响应: $body" | head -c 200
        echo "..."
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ 测试失败${NC} (HTTP $http_code)"
        echo "响应: $body"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

echo "=================================="
echo "古文字破译系统 - 功能测试"
echo "=================================="
echo ""
echo "测试目标: $BASE_URL"
echo ""

# ========================================
# 1. 系统健康检查
# ========================================
echo "=================================="
echo "1. 系统健康检查"
echo "=================================="

test_endpoint "健康检查" "GET" "/health"

# ========================================
# 2. API 基础测试
# ========================================
echo ""
echo "=================================="
echo "2. API 基础测试"
echo "=================================="

test_endpoint "获取监控指标" "GET" "/api/v1/metrics"
test_endpoint "获取版本信息" "GET" "/api/v1/version"

# ========================================
# 3. 工具管理测试
# ========================================
echo ""
echo "=================================="
echo "3. 工具管理测试"
echo "=================================="

test_endpoint "获取工具列表" "GET" "/api/v1/tools"
test_endpoint "获取OCR工具详情" "GET" "/api/v1/tools/ocr-recognition"
test_endpoint "推荐工具" "POST" "/api/v1/tools/recommend" \
    '{"requirements": ["识别甲骨文", "图像处理"], "limit": 3}'

# ========================================
# 4. 插件管理测试
# ========================================
echo ""
echo "=================================="
echo "4. 插件管理测试"
echo "=================================="

test_endpoint "获取插件列表" "GET" "/api/v1/plugins"
test_endpoint "检查OCR插件健康状态" "GET" "/api/v1/plugins/ocr-tool-plugin/health"

# ========================================
# 5. 文本分析测试
# ========================================
echo ""
echo "=================================="
echo "5. 文本分析测试"
echo "=================================="

test_endpoint "基础文本分析" "POST" "/api/v1/analyze" \
    '{"text": "什么是甲骨文？"}'

test_endpoint "甲骨文分析" "POST" "/api/v1/analyze" \
    '{"text": "王贞卜，旬亡祸？在十月又二。请分析这段甲骨文的含义。"}'

test_endpoint "金文分析" "POST" "/api/v1/analyze" \
    '{"text": "请介绍西周金文的特点和用途。"}'

# ========================================
# 6. 对话交互测试
# ========================================
echo ""
echo "=================================="
echo "6. 对话交互测试"
echo "=================================="

SESSION_ID="test-session-$(date +%s)"

test_endpoint "第一轮对话" "POST" "/api/v1/chat" \
    "{\"message\": \"你好，请介绍一下古文字破译的方法。\", \"session_id\": \"$SESSION_ID\"}"

test_endpoint "第二轮对话（保持上下文）" "POST" "/api/v1/chat" \
    "{\"message\": \"这些方法有什么优缺点？\", \"session_id\": \"$SESSION_ID\"}"

test_endpoint "第三轮对话（保持上下文）" "POST" "/api/v1/chat" \
    "{\"message\": \"推荐一些常用的AI工具。\", \"session_id\": \"$SESSION_ID\"}"

# ========================================
# 7. 会话管理测试
# ========================================
echo ""
echo "=================================="
echo "7. 会话管理测试"
echo "=================================="

test_endpoint "获取会话历史" "GET" "/api/v1/sessions/$SESSION_ID"

# ========================================
# 测试总结
# ========================================
echo ""
echo "=================================="
echo "测试总结"
echo "=================================="
echo -e "总测试数: $TOTAL_TESTS"
echo -e "${GREEN}通过: $PASSED_TESTS${NC}"
echo -e "${RED}失败: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}🎉 所有测试通过！系统运行正常！${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  有 $FAILED_TESTS 个测试失败，请检查系统状态。${NC}"
    exit 1
fi
