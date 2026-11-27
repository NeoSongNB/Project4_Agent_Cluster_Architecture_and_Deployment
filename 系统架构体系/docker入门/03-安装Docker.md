# 03 - 安装 Docker

个人电脑上装 Docker，最省事的方式就是装 **Docker Desktop**（带图形界面，Windows / Mac 都有）。

## Windows 安装

1. 打开官网 [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)，下载 **Docker Desktop for Windows**。
2. 双击安装，一路下一步。安装时会提示启用 **WSL 2**（Windows 的 Linux 子系统），按提示装上即可。
3. 安装完重启电脑，启动 Docker Desktop，等右下角小鲸鱼图标不再转圈、变成稳定状态，就绪。

> 小贴士：Windows 家庭版也能用，靠的就是 WSL 2。第一次启动会让你装/更新 WSL，跟着提示走就行。

## Mac 安装

1. 同样去官网下载 **Docker Desktop for Mac**。
2. 注意区分芯片：**Apple 芯片（M1/M2/M3…）** 和 **Intel 芯片** 下载的版本不一样，别下错。
3. 把 Docker 拖进"应用程序"，启动，等顶部菜单栏的小鲸鱼稳定即可。

## 验证安装成功

打开终端（Windows 用 PowerShell，Mac 用 Terminal），输入：

```bash
docker --version
```

能看到版本号（类似 `Docker version 27.x.x`），说明装好了。

再来跑一个官方的"hello world"，确认能真正运行容器：

```bash
docker run hello-world
```

如果看到一段以 **"Hello from Docker!"** 开头的文字，恭喜，一切正常。

## `docker run hello-world` 背后发生了什么？

这条命令虽小，却完整展示了 Docker 的工作流程，值得讲清楚：

1. Docker 先在**本地**找有没有 `hello-world` 这个镜像。
2. 本地没有 → 自动去**仓库 Docker Hub** 把它 **拉（pull）** 下来。
3. 用这个镜像**运行出一个容器**。
4. 容器里的程序打印出 "Hello from Docker!" 这段话，然后结束。

看，这就是上一章说的：**从仓库拉镜像 → 运行成容器**。你刚刚已经亲手跑通了一遍 Docker 的核心流程。

## 关于 Docker Desktop 界面

Docker Desktop 提供了图形界面，你可以在里面：

- **Images**：看本地有哪些镜像
- **Containers**：看有哪些容器在跑、查看日志、一键停止/删除

不过这门课我们**主要用命令行**，因为命令行才是通用、跨平台、能写进部署脚本的方式。界面看看就好，命令才是真功夫。

## 小结

- 个人电脑装 **Docker Desktop** 最省事（Win 需要 WSL 2，Mac 注意芯片型号）。
- 验证：`docker --version` + `docker run hello-world`。
- `hello-world` 跑通 = 你已经完整体验了"拉镜像 → 跑容器"的流程。

环境就绪，下一章我们把最常用的命令一次性过一遍。

---

上一章 ← [02 - 三个核心概念](02-三个核心概念.md) ｜ 下一章 → [04 - 必会命令](04-必会命令.md)
