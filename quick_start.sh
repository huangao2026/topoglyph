#!/bin/bash

# 古文字破译系统 - 快速启动脚本
# 使用方法: ./quick_start.sh

set -e

echo "=================================="
echo "古文字破译系统 - 快速启动"
echo "=================================="
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "当前 Python 版本: $python_version"

# 检查是否存在 .env 文件
if [ ! -f .env ]; then
    echo "未找到 .env 文件，从 .env.example 创建..."
    cp .env.example .env
    echo "✓ 已创建 .env 文件"
    echo ""
    echo "⚠️  请先编辑 .env 文件，填入您的 API Key："
    echo "   nano .env"
    echo ""
    read -p "是否现在编辑 .env 文件？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    else
        echo "请稍后手动编辑 .env 文件"
        exit 1
    fi
fi

# 检查 API Key 是否配置
if grep -q "your_moonshot_api_key_here" .env; then
    echo "⚠️  警告：API Key 未配置！"
    echo "请编辑 .env 文件，填入您的 Moonshot AI API Key"
    exit 1
fi

# 加载环境变量
export $(cat .env | grep -v '^#' | xargs)

# 显示配置
echo "=================================="
echo "配置信息："
echo "=================================="
echo "工作空间路径: $COZE_WORKSPACE_PATH"
echo "API 基础 URL: $COZE_INTEGRATION_MODEL_BASE_URL"
echo "服务端口: ${PORT:-8000}"
echo ""

# 选择启动方式
echo "请选择启动方式："
echo "1) 本地开发模式（使用 uvicorn，支持热重载）"
echo "2) 本地生产模式（使用 uvicorn）"
echo "3) Docker 模式（推荐）"
echo ""
read -p "请输入选项 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "启动本地开发模式..."
        uvicorn src.web_api_new:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --reload
        ;;
    2)
        echo ""
        echo "启动本地生产模式..."
        uvicorn src.web_api_new:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --workers 4
        ;;
    3)
        echo ""
        echo "启动 Docker 模式..."
        if command -v docker &> /dev/null; then
            docker-compose up -d
            echo "✓ Docker 容器已启动"
            echo ""
            echo "查看日志: docker-compose logs -f"
            echo "停止服务: docker-compose down"
        else
            echo "✗ 未安装 Docker"
            echo "请先安装 Docker: https://docs.docker.com/get-docker/"
            exit 1
        fi
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac
