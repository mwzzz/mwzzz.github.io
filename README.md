# 敲码小站

敲码人的个人学习工作台：笔记、项目与学习方向。

- 站点：https://mwzzz.github.io/
- 技术：Astro + TypeScript + Content Collections
- 部署：GitHub Actions → `gh-pages`

## 本地开发

```bash
npm install
npm run dev
```

## 写笔记

在 `src/content/blog/` 新建 Markdown，示例 frontmatter：

```md
---
title: 标题
description: 摘要
pubDate: 2026-07-22
tags: [Astro]
draft: false
---
```

## 部署

推送 `main` 后，GitHub Actions 自动构建并用官方 Pages 部署。

仓库 Settings → Pages：

1. Source: **GitHub Actions**
2. 首次推送后在 Actions 里确认 `Deploy to GitHub Pages` 成功
3. 若提示启用 Pages，按提示允许即可