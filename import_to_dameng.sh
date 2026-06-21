#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  达梦数据库数据导入"
echo "========================================="

# Step 1: 创建表结构
echo ""
echo "[Step 1] 创建达梦表结构..."
docker exec dm8 bash -c "export LD_LIBRARY_PATH=/dm8/bin && /dm8/bin/disql -S SYSDBA/'Dameng@123@localhost' -e \"
SP_SET_PARA_VALUE(1, 'UNICODE_IDENTIFIER', 1);
CONNECT SYSDBA/'Dameng@123@localhost';
\""
echo "  -> 表结构创建完成"

# Step 2: 导入数据
echo ""
echo "[Step 2] 导入数据到达梦..."
# 使用 dimp 工具通过标准输入导入
cat dameng_data.sql | docker exec -i dm8 bash -c "export LD_LIBRARY_PATH=/dm8/bin && /dm8/bin/disql -S SYSDBA/'Dameng@123@localhost'"
echo "  -> 数据导入完成"

# Step 3: 验证
echo ""
echo "[Step 3] 验证数据..."
docker exec dm8 bash -c "export LD_LIBRARY_PATH=/dm8/bin && /dm8/bin/disql -S SYSDBA/'Dameng@123@localhost' -e \"
SELECT 'dmma_suppliers' AS table_name, COUNT(*) AS cnt FROM SYSDBA.dmma_suppliers;
SELECT 'dmma_materials' AS table_name, COUNT(*) AS cnt FROM SYSDBA.dmma_materials;
SELECT 'dmma_standards' AS table_name, COUNT(*) AS cnt FROM SYSDBA.dmma_standards;
SELECT 'dmma_documents' AS table_name, COUNT(*) AS cnt FROM SYSDBA.dmma_documents;
\""

echo ""
echo "========================================="
echo "  导入完成！"
echo "========================================="
