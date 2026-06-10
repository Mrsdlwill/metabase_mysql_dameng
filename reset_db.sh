#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  Reset MySQL & Dameng + Restart Metabase"
echo "========================================="

# Step 1: Stop all services
echo ""
echo "[Step 1] 停止所有 Docker 服务..."
docker-compose down

# Step 2: Confirm and remove old MySQL data
echo ""
echo "[Step 2] 清理旧数据库数据..."
read -p "是否删除 MySQL 旧数据（会丢失数据库内容）？[y/N]: " confirm_mysql
if [[ "$confirm_mysql" =~ ^[Yy]$ ]]; then
    docker volume rm test3_db-data 2>/dev/null || true
    echo "  -> MySQL 数据卷已删除"
else
    echo "  -> 跳过 MySQL 数据清理"
fi

# Step 3: Confirm and remove old Dameng data
read -p "是否删除达梦旧数据（改字符集必须清空）？[y/N]: " confirm_dm
if [[ "$confirm_dm" =~ ^[Yy]$ ]]; then
    docker volume rm test3_dm8-data 2>/dev/null || true
    echo "  -> 达梦数据卷已删除"
else
    echo "  -> 跳过达梦数据清理"
    echo "  [警告] 达梦字符集变更需要全新实例，不清理可能导致乱码问题依旧存在"
fi

# Step 4: Restart
echo ""
echo "[Step 3] 重新启动所有服务..."
docker-compose up -d

echo ""
echo "========================================="
echo "  Done! 服务已重启"
echo "  Metabase: http://localhost:3000"
echo "  MySQL:    localhost:3306"
echo "  达梦:     localhost:5236"
echo "========================================="
