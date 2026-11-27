# 1. 选一个基础镜像：已经装好 Python 3.11 的官方精简镜像
FROM python:3.11-slim

# 2. 设置容器内的工作目录（之后的命令都在这个目录下执行）
WORKDIR /app

# 3. 先只复制依赖文件并安装（利用缓存：依赖没变就不用重装）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 再复制项目代码进去
COPY . .

# 5. 声明容器对外暴露的端口（文档作用，方便他人理解）
EXPOSE 8000

# 6. 容器启动时要执行的命令：启动 FastAPI 服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
