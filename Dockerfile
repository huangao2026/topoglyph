# TCD Origin - 古文字拓扑破译引擎
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（解决cairo等库缺失问题）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY web_app.py .
COPY api/ ./api/
COPY src/ ./src/

# 暴露端口
EXPOSE 7860

# 启动命令
CMD ["python", "web_app.py", "--server.port=7860", "--server.address=0.0.0.0"]
