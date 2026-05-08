# TCD Origin - 古文字拓扑破译引擎
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY web_app.py .
COPY src/ ./src/

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "web_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
