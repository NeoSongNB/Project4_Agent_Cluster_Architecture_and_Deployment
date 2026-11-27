# 11 - 实战：把前端部署到 OSS + CDN

理论讲完，这一章动手把一个前端项目部署到 **OSS + CDN**。我们先手动走一遍（理解每一步在干嘛），再用 **CI/CD** 自动化掉。以阿里云 OSS + CDN 为例，腾讯云 COS + CDN 步骤几乎一样。

> 本章目标是让你看懂**完整链路**，不同云厂商控制台按钮位置略有差异，跟着思路走即可。

## 第一步：构建出静态文件

在项目根目录执行：

```bash
npm install
npm run build
```

得到 `dist/` 目录，里面就是要上线的静态文件。

## 第二步：开通并配置 OSS

1. 登录阿里云 → 开通**对象存储 OSS**
2. **创建一个 Bucket（桶）**，选个地域（就近选，比如华东-杭州）
3. 权限设置为**公共读**（允许别人访问下载你的前端文件）
4. 开启**静态网站托管**功能：把默认首页设为 `index.html`

> 静态网站托管这个开关很关键：它让用户访问桶的根地址时，自动返回 `index.html`，你的单页应用（SPA）才能正常打开。

## 第三步：上传 dist 文件

把 `dist/` 里所有文件上传到 Bucket。手动可以直接在控制台拖拽，或用官方命令行工具 `ossutil`：

```bash
ossutil cp -r ./dist oss://your-bucket-name/ --update
```

传完后，OSS 会给你一个访问域名，此时你的网站**已经能访问了**（只是远处慢）。

## 第四步：套上 CDN 加速

1. 开通**CDN** 服务
2. 添加一个**加速域名**（比如 `www.你的域名.com`），把**源站设置为你的 OSS Bucket**
3. CDN 会给你一个 **CNAME 地址**
4. 到你的**域名解析**里，把域名 CNAME 指向这个地址（域名和解析的细节见第 19 章）

配好后，用户访问 `www.你的域名.com`，就会走 CDN 就近拿文件，OSS 作为源站在背后兜底。

> [配图：四步流程条——build → 传 OSS → 配 CDN → 域名 CNAME 指向 CDN，用户从 CDN 就近访问]

## 第五步（重要）：处理单页应用的路由

Vue/React 这类单页应用（SPA），用户刷新 `/about` 这种子路由时，服务器上并没有 `about.html`，会 404。解决办法：

- 在 OSS 静态网站托管里，把**默认 404 页面也设为 `index.html`**（或设置"子目录首页"回退到 index）
- 这样所有路径都回到 `index.html`，交给前端路由去处理

## 第六步：用 CI/CD 自动化

手动传文件太原始，回顾第 08 章的前端支线，我们用 GitHub Actions 让它**push 即部署**。核心步骤（完整示例见 [example/](./example/)）：

```yaml
# .github/workflows/deploy-frontend.yml（示意）
name: 部署前端
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4          # ①拉代码
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm install                   # ②装依赖
      - run: npm run build                 # ④构建，产出 dist/
      - name: 上传到 OSS 并刷新 CDN         # ⑤部署
        run: |
          ossutil cp -r ./dist oss://your-bucket/ --update
          # 再调用 CDN 刷新缓存的命令
        env:
          OSS_KEY: ${{ secrets.OSS_KEY }}      # 密钥存在仓库 Secrets 里，不写进代码
          OSS_SECRET: ${{ secrets.OSS_SECRET }}
```

> 注意：访问密钥（AccessKey）等敏感信息，一定要放在仓库的 **Secrets** 里，**绝不能写进代码提交上去**。

配好之后，你每次 `git push`，前端就自动 build 并更新到 OSS+CDN，全程不用管。

## 部署后检查清单

- [ ] 访问 CDN 域名，首页能正常打开
- [ ] 刷新子路由（如 `/about`）不 404
- [ ] 改一行代码 push，几分钟后线上自动更新
- [ ] 更新后没看到新内容？多半是 **CDN 缓存**，去刷新缓存

## 小结

- 前端部署实战链路：**build → 传 OSS → 配 CDN → 域名 CNAME 指向 CDN**。
- SPA 记得把 404 回退到 `index.html`，否则刷新子路由会挂。
- 用 GitHub Actions 把这套自动化，**push 即部署**；密钥放 Secrets。
- 更新后不生效，先想到是 CDN 缓存，刷新即可。

前端这条支线通了。接下来进入第四部分——难度更高、但也是现代方案精髓的**后端：Docker + Serverless**。

---

下一章 → [12 - 什么是 Serverless（无服务器）](12-什么是Serverless.md)
