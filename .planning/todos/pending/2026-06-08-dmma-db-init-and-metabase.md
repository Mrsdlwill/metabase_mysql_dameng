---
created: 2026-06-08T19:08:30+0800
title: 创建 DMMA 数据库初始化脚本和启动 Metabase 容器
area: database
files:
  - READ.md
---

## Problem

根据 READ.md 中的工作流指令，需要完成两个步骤：
1. 创建 `init_dmma_db.sql` 文件，包含完整的 DMMA 数据库初始化脚本（5个表：materials, standards, suppliers, documents + Mock 数据）
2. 用 Docker 启动 Metabase 容器，端口映射 3000

## Solution

1. 将 READ.md 中的完整 SQL 脚本写入 `init_dmma_db.sql` 文件
2. 执行 `docker run -d -p 3000:3000 --name metabase metabase/metabase` 启动 Metabase
3. 提示用户如何在本地 MySQL 中执行 SQL 脚本
