# 05 - 实战：把 FastAPI 服务装进 Docker

> 这是整篇教程的重点。跟着做一遍，你就真正会用 Docker 了。
> 完整代码已经放在 [`example/`](./example/) 文件夹里，可以直接用。

我们要做的事很简单：写一个最小的 FastAPI 服务，然后把它打包成 Docker 镜像、跑起来、用浏览器访问。重点不是业务，而是**体会"打包 → 到处能跑"的完整流程**。

## Step 0 · 准备一个超简单的 FastAPI 应用

新建一个文件夹（比如就用 `example/`），在里面创建 `main.py`：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My AI App")


@app.get("/")
def home():
    return {"message": "Hello Docker! 这个 AI 服务正在容器里运行。"}


class PredictRequest(BaseModel):
    text: str


@app.post("/predict")
def predict(req: PredictRequest):
    # 这里假装做了一次 AI 推理，真实场景会在这里调用模型
    return {"input": req.text, "length": len(req.text)}
```

这就是一个最简单的 AI 服务雏形：一个首页 `/`，一个模拟推理的 `/predict`。

## Step 1 · 先理解"没有 Docker 时怎么跑"

如果不用 Docker，要在本地跑起来，你得：

1. 电脑上**装好 Python**
2. 安装依赖：`pip install fastapi uvicorn`
3. 启动：`uvicorn main:app --reload`

能跑通。**但问题来了**：换一台没装 Python、没装这些包的电脑，上面三步要重来一遍，还可能因为版本不同而报错。这正是 Docker 要解决的问题——把这些步骤"固化"进镜像。

## Step 2 · 写 requirements.txt

把依赖写进 `requirements.txt`，锁定版本，保证到哪都装一样的版本：

```text
fastapi==0.115.0
uvicorn==0.30.6
```

## Step 3 · 写 Dockerfile（核心）

`Dockerfile` 是**给 Docker 看的"打包说明书"**，告诉它怎么一步步把你的应用打包成镜像。在文件夹里新建一个名为 `Dockerfile` 的文件（没有后缀名）：

```dockerfile
# 1. 选一个基础镜像：已经装好 Python 3.11 的官方精简镜像
FROM python:3.11-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 先复制依赖文件并安装（利用缓存：依赖没变就不用重装）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 再复制项目代码进去
COPY . .

# 5. 声明对外端口
EXPOSE 8000

# 6. 容器启动时执行：启动 FastAPI 服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**逐行讲解**（这部分一定要听懂）：

| 指令 | 作用 | 大白话 |
|------|------|--------|
| `FROM` | 指定基础镜像 | "我不从零开始，先拿一个装好 Python 的环境当底子" |
| `WORKDIR` | 设置工作目录 | "接下来都在容器里的 /app 文件夹干活" |
| `COPY` | 复制文件进镜像 | "把我电脑上的文件拷进容器" |
| `RUN` | 构建时执行命令 | "打包过程中，把依赖装好" |
| `EXPOSE` | 声明端口 | "我这个服务用 8000 端口"（说明性质） |
| `CMD` | 容器启动时执行 | "容器一跑起来，就执行这条命令启动服务" |

> 一个关键技巧：为什么先 `COPY requirements.txt` 再 `COPY . .`？因为 Docker 会缓存每一层，只要 `requirements.txt` 没变，重新构建时就**跳过装依赖**这步，构建快很多。

> 另外建议加一个 `.dockerignore` 文件（见 example 文件夹），把 `.git`、`__pycache__` 等不需要的东西排除掉，让镜像更小。

## Step 4 · 构建镜像

在 `Dockerfile` 所在目录下，打开终端，执行：

```bash
docker build -t my-ai-app .
```

- `-t my-ai-app`：给镜像起名叫 `my-ai-app`
- 最后那个 `.`：表示"用当前目录下的 Dockerfile 来构建"（别漏了这个点！）

构建完，用 `docker images` 就能看到你的 `my-ai-app` 镜像了。

## Step 5 · 运行容器

```bash
docker run -d -p 8000:8000 --name ai my-ai-app
```

- `-d`：后台运行
- `-p 8000:8000`：把本机 8000 端口映射到容器 8000 端口（**没有这个，浏览器访问不到！**）
- `--name ai`：给容器起名 `ai`
- `my-ai-app`：用哪个镜像来跑

用 `docker ps` 确认它在运行。

## Step 6 · 见证奇迹

打开浏览器访问：

- [http://localhost:8000](http://localhost:8000) → 看到 `Hello Docker!` 那句话
- [http://localhost:8000/docs](http://localhost:8000/docs) → FastAPI 自动生成的交互式接口文档，可以在线测试 `/predict`

成了！你的 AI 服务现在跑在一个 Docker 容器里。

## 回顾整个流程

```
写代码(main.py) + 依赖(requirements.txt) + 说明书(Dockerfile)
        │
        │  docker build
        ▼
     镜像 my-ai-app
        │
        │  docker run -p 8000:8000
        ▼
     容器（服务跑在里面）
        │
        ▼
  浏览器访问 localhost:8000
```

## 常见小问题

- **8000 端口被占用**？把映射改成 `-p 8001:8000`，然后访问 `localhost:8001`。
- **改了代码没生效**？镜像是构建时的快照，改完代码要**重新 build**。先 `docker rm -f ai` 删旧容器，再重新 build + run。
- **想看报错**？`docker logs ai` 查看容器日志。

## 小结

- 三个文件搞定打包：`main.py`（代码）+ `requirements.txt`（依赖）+ `Dockerfile`（说明书）。
- 三条命令走天下：`docker build` → `docker run -p` → 浏览器访问。
- `Dockerfile` 是核心，本质就是"把环境配置过程写成步骤"。

你已经会用 Docker 了！下一章，我们体会 Docker 真正"封神"的时刻——换台电脑也能一键运行。

---

上一章 ← [04 - 必会命令](04-必会命令.md) ｜ 下一章 → [06 - Docker 真香时刻](06-Docker真香时刻.md)
