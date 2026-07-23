---
title: 用 Astro 搭建个人站并部署到 GitHub Pages
description: 源码在 main，Actions 构建 dist 并发布到 gh-pages，适合长期维护的个人站。
pubDate: 2026-07-20
tags: [Astro, GitHub Pages, 部署]
---

和很多程序员站点一样，「ONE」采用静态方案：本地写 Markdown，构建成 HTML，再托管到 GitHub Pages。

## 为什么选这套方案

| 优点 | 说明 |
| --- | --- |
| 免费 | GitHub Pages 免费托管 |
| 稳定 | 静态文件，几乎不用运维 |
| 清晰 | 源码与产物分离，Actions 自动发布 |

## 本地常用命令

```bash
npm run dev      # 本地预览
npm run build    # 生成 dist/
npm run preview  # 预览构建结果
```

## 部署注意点

1. `astro.config.mjs` 里的 `site` 要写成你的 Pages 地址
2. 仓库 Settings → Pages 选择 `gh-pages` 分支
3. 推送 `main` 后等待 Actions 完成

源码仓库不要只提交生成后的 HTML，否则后续改主题和内容都会很痛苦。
