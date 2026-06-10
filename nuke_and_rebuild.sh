#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  Nuke & Rebuild: MySQL + Dameng + Metabase"
echo "========================================="

# Step 1: 停止并销毁所有容器、网桥、named volumes
echo ""
echo "[Step 1] docker-compose down -v ..."
docker-compose down -v
echo "  -> 所有容器和数据卷已销毁"

# Step 2: 重建
echo ""
echo "[Step 2] docker-compose up -d ..."
docker-compose up -d

echo ""
echo "========================================="
echo "  Done!"
echo "  Metabase: http://localhost:3000"
echo "  MySQL:    localhost:3306"
echo "  达梦:     localhost:5236"
echo "========================================="
