# 06 - 体会 Docker 的"真香"时刻

上一章你把服务跑起来了。但你可能还没体会到 Docker 真正的威力。这一章我们就来感受那个"**换台电脑也能一键运行**"的瞬间——这才是 Docker 存在的意义。

## 想象一个场景

你做好了一个 AI 服务，想让同学/老师在他们电脑上也跑起来。

**没有 Docker 的世界：**

> "你先装 Python 3.11，然后 pip install 这一堆包，注意版本别装错，哦对了你系统还得装某个库，然后……"
>
> 结果对方折腾半天，还是各种报错。😩

**有了 Docker 的世界：**

> "你电脑装个 Docker，然后运行这一条命令就行。"
>
> 对方一条命令，服务跑起来了。✨

这就是差别。下面有两种分享方式。

## 方式一：通过 Docker Hub 分享（推荐）

把镜像传到 Docker Hub（免费），别人一条命令就能拉下来跑。

1. 注册 [Docker Hub](https://hub.docker.com) 账号，拿到用户名（假设叫 `yourname`）。

2. 本地登录：

```bash
docker login
```

3. 给镜像打上带用户名的标签（Docker Hub 要求这种命名格式）：

```bash
docker tag my-ai-app yourname/my-ai-app:v1
```

4. 推上去：

```bash
docker push yourname/my-ai-app:v1
```

5. **现在，任何人**（在任何装了 Docker 的电脑上）只要一条命令：

```bash
docker run -d -p 8000:8000 yourname/my-ai-app:v1
```

不用装 Python、不用装依赖、不用管版本——直接就能跑。**这就是真香时刻。**

## 方式二：导出成文件分享（不联网也行）

如果不想用 Docker Hub，也可以把镜像导出成一个文件，拷给别人。

把镜像存成 tar 文件：

```bash
docker save -o my-ai-app.tar my-ai-app
```

对方拿到 `my-ai-app.tar` 后，导入：

```bash
docker load -i my-ai-app.tar
```

然后照样：

```bash
docker run -d -p 8000:8000 my-ai-app
```

## 为什么这对 AI 开发特别重要？

AI 项目的环境是出了名的难搞：Python 版本、PyTorch、CUDA、几十个依赖包……手动配环境，一个人能配半天，团队协作更是噩梦。

有了 Docker：

- **环境一次配好，全队复用**：你打包好镜像，全组人 `docker run` 直接用。
- **本地和服务器完全一致**：本地能跑，部署到服务器就能跑，不再"线上线下两套环境"。
- **交付变简单**：给客户/老师演示，不用现场配环境，拉镜像就行。

## 小结

- Docker 的核心价值：**一次打包，到处运行**。
- 分享镜像两种方式：Docker Hub（`push`/`pull`）或导出文件（`save`/`load`）。
- 对 AI 开发者：彻底告别"在我电脑上能跑"的环境地狱。

到这里，Docker 的核心你已经全部掌握了。下一章是一些 AI 开发者特别用得上的实用技巧。

---

上一章 ← [05 - 把 FastAPI 服务装进 Docker](05-实战-把FastAPI装进Docker.md) ｜ 下一章 → [07 - AI 开发者常用技巧](07-AI开发者常用技巧.md)
