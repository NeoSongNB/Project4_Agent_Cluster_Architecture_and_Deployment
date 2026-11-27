# 后端示例镜像：把 FastAPI 服务打包（对应第 13、15 章）
FROM python:3.11-slim

WORKDIR /app

# 先拷依赖清单并安装，利用 Docker 缓存（依赖没变就不重装）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷业务代码
COPY . .

# 监听端口：不同 Serverless 平台要求可能不同，按平台文档调整
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
