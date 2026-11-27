# example · 可复用示例代码

这里放本教程实战用到的示例文件，复制到你自己的项目里按注释改改就能用。

## 文件说明

| 文件 | 用途 | 对应章节 |
|------|------|---------|
| `Dockerfile` | 把 FastAPI 后端打成 Docker 镜像 | 13、15 |
| `main.py` | 一个最小的后端示例（连库 + 调 AI + CORS） | 15、21、23 |
| `requirements.txt` | 后端依赖 | 15 |
| `deploy-frontend.yml` | 前端 CI/CD：build → OSS → 刷 CDN | 08、11 |
| `deploy-backend.yml` | 后端 CI/CD：docker build → 推 ACR → 部署 Serverless | 08、15 |

## 使用提示

- `deploy-*.yml` 放到你项目的 `.github/workflows/` 目录下才会被 GitHub Actions 识别。
- 所有密钥（OSS/ACR 凭证、数据库串、AI Key）都通过仓库 **Settings → Secrets** 配置，**不要写进代码**。
- 这些示例以阿里云为例（OSS + ACR + Serverless），换腾讯云思路一致，改命令和地址即可。

---

← 返回 [README 目录](培训班/基础阶段/系统架构体系/项目到底如何部署？/README.md)
