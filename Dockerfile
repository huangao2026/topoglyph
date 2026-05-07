# TCD Origin - 跨文明古文字拓扑破译引擎
# Docker 配置文件

# ============ Dockerfile ============

FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/app:$PATH

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装Python依赖
RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev

# 复制应用代码
COPY . .

# 创建必要目录
RUN mkdir -p /app/logs /app/uploads

# 暴露端口
EXPOSE 8000 7860

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
