# 15 - 实战：把 FastAPI 打成 Docker 部署到 Serverless

这一章把后端这条支线跑通：**写 Dockerfile → 打镜像 → 推镜像仓库 → 部署到 Serverless → 用 CI/CD 自动化**。以一个 FastAPI 服务为例，衔接 [Docker 入门](培训班/基础阶段/系统架构体系/docker入门/README.md)。

## 第一步：准备一个 FastAPI 服务

一个最小后端 `main.py`：

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Serverless!"}
```

依赖 `requirements.txt`：

```
fastapi
uvicorn[standard]
```

## 第二步：写 Dockerfile

把它打成镜像（详细写法见 Docker 系列第 05 章）：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Serverless 平台通常通过环境变量 PORT 指定端口，这里监听它
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> 提示：不同 Serverless 平台对"监听哪个端口"有要求，有的固定 9000、有的通过 `PORT` 环境变量下发。部署前看一眼平台文档，把端口对上。

## 第三步：本地构建并验证

```bash
docker build -t my-backend .
docker run -p 8000:8000 my-backend
```

访问 `http://localhost:8000/api/hello` 能返回 JSON，就说明镜像没问题。**本地能跑，线上就能跑**——这就是 Docker 的价值。

## 第四步：推送到镜像仓库

先开通云厂商的**镜像仓库**（阿里云 ACR / 腾讯云 TCR），登录后打标签并推送：

```bash
# 登录镜像仓库
docker login registry.cn-hangzhou.aliyuncs.com

# 打标签（指向你的仓库地址）
docker tag my-backend registry.cn-hangzhou.aliyuncs.com/your-namespace/my-backend:v1

# 推送
docker push registry.cn-hangzhou.aliyuncs.com/your-namespace/my-backend:v1
```

## 第五步：部署到 Serverless

以"Serverless 容器"类产品为例（阿里云 SAE / 函数计算容器镜像、腾讯云云托管）：

1. 新建一个服务/应用
2. 部署方式选**容器镜像**，填入刚才推送的镜像地址
3. 配置端口（和 Dockerfile 里一致）、内存规格、实例伸缩范围（如最小 0、最大 10）
4. 配置需要的**环境变量**（数据库连接串、AI API 密钥等，见第 5、6 部分）
5. 部署，平台会拉取镜像、启动实例，给你一个访问地址

访问 `https://你的服务地址/api/hello`，能返回 JSON，后端就上线了。

> [配图：Dockerfile → build → 推 ACR → Serverless 部署 → 拿到访问地址，一条流水线]

## 第六步：用 CI/CD 自动化

回顾第 08 章后端支线，用 GitHub Actions 让它 push 即部署（完整示例见 [example/](./example/)）：

```yaml
# .github/workflows/deploy-backend.yml（示意）
name: 部署后端
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 登录镜像仓库
        run: docker login -u ${{ secrets.ACR_USER }} -p ${{ secrets.ACR_PASS }} registry.cn-hangzhou.aliyuncs.com
      - name: 构建并推送镜像
        run: |
          IMG=registry.cn-hangzhou.aliyuncs.com/your-namespace/my-backend:${{ github.sha }}
          docker build -t $IMG .
          docker push $IMG
      - name: 通知 Serverless 用新镜像部署
        run: |
          # 调用云厂商 CLI / API，把服务更新为新镜像
          echo "deploy $IMG ..."
```

> 用 `github.sha`（本次提交号）当镜像标签，好处是**每个版本镜像都不同，方便回滚**——想回退就让 Serverless 换回上一个 tag。

## 部署后检查清单

- [ ] 访问 `/api/hello` 能正常返回
- [ ] 没请求一段时间后再访问，第一次略慢（冷启动，正常）
- [ ] 改代码 push，几分钟后线上自动更新
- [ ] 密钥/连接串都放在**环境变量 / Secrets**，没写进代码

## 小结

- 后端实战链路：**FastAPI → 写 Dockerfile → build → 本地验证 → 推镜像仓库 → 部署 Serverless → CI/CD 自动化**。
- 端口要和平台要求对齐；敏感信息走环境变量 / Secrets。
- 用提交号做镜像 tag，方便回滚。

前端、后端都上线了。但后端要存数据、要调 AI——这些"状态"和"能力"放哪？进入第五部分：**数据库与 AI，全用云端服务**。

---

下一章 → [16 - 为什么数据库要用云托管](16-为什么数据库要用云托管.md)
