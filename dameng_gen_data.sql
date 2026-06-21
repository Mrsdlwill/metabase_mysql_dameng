-- ==========================================
-- 达梦数据库测试数据生成脚本
-- 使用CONNECT BY批量生成数据
-- ==========================================

-- 清空旧数据（忽略错误）
DELETE FROM dmma_documents;
DELETE FROM dmma_standards;
DELETE FROM dmma_materials;
DELETE FROM dmma_suppliers;

-- 生成供应商数据 (100条)
INSERT INTO dmma_suppliers (supplier_name, main_focus)
SELECT '供应商_' || CAST(LEVEL AS VARCHAR(10)),
       CASE MOD(LEVEL, 5)
           WHEN 0 THEN '材料制造'
           WHEN 1 THEN '材料研发'
           WHEN 2 THEN '材料检测'
           WHEN 3 THEN '复合材料'
           WHEN 4 THEN '稀土材料'
       END
FROM DUAL
CONNECT BY LEVEL <= 100;

-- 生成材料数据 (500条)
INSERT INTO dmma_materials (name, category, application_area, yield_strength, density)
SELECT '材料_' || CAST(LEVEL AS VARCHAR(10)),
       CASE MOD(LEVEL, 8)
           WHEN 0 THEN '有色金属'
           WHEN 1 THEN '高温合金'
           WHEN 2 THEN '黑色金属'
           WHEN 3 THEN '复合材料'
           WHEN 4 THEN '特种合金'
           WHEN 5 THEN '陶瓷材料'
           WHEN 6 THEN '高分子材料'
           WHEN 7 THEN '稀土与功能材料'
       END,
       CASE MOD(LEVEL, 10)
           WHEN 0 THEN '航空航天'
           WHEN 1 THEN '船舶海工'
           WHEN 2 THEN '石油化工'
           WHEN 3 THEN '机械制造'
           WHEN 4 THEN '电子信息'
           WHEN 5 THEN '医疗器械'
           WHEN 6 THEN '建筑工程'
           WHEN 7 THEN '电力设备'
           WHEN 8 THEN '核工业'
           WHEN 9 THEN '汽车工业'
       END,
       100 + MOD(LEVEL, 2000),
       ROUND(1.0 + MOD(LEVEL, 20) * 0.5, 2)
FROM DUAL
CONNECT BY LEVEL <= 500;

-- 生成标准数据 (100条)
INSERT INTO dmma_standards (material_id, standard_code, system_type)
SELECT MOD(LEVEL - 1, 500) + 1,
       CASE MOD(LEVEL, 4)
           WHEN 0 THEN 'GB/T ' || CAST(1000 + LEVEL AS VARCHAR(10)) || '-' || CAST(2020 + MOD(LEVEL, 5) AS VARCHAR(4))
           WHEN 1 THEN 'ASTM ' || CAST(2000 + LEVEL AS VARCHAR(10))
           WHEN 2 THEN 'ISO ' || CAST(3000 + LEVEL AS VARCHAR(10))
           WHEN 3 THEN 'AMS ' || CAST(4000 + LEVEL AS VARCHAR(10))
       END,
       CASE MOD(LEVEL, 4)
           WHEN 0 THEN '国标'
           WHEN 1 THEN '国际标准'
           WHEN 2 THEN '国际标准'
           WHEN 3 THEN '国际标准'
       END
FROM DUAL
CONNECT BY LEVEL <= 100;

-- 生成文档数据 (200条)
INSERT INTO dmma_documents (title, document_type, source, related_material_id)
SELECT '技术文档_' || CAST(LEVEL AS VARCHAR(10)) || '_' ||
       CASE MOD(LEVEL, 4)
           WHEN 0 THEN '测试报告'
           WHEN 1 THEN '工艺规范'
           WHEN 2 THEN '质量标准'
           WHEN 3 THEN '设计手册'
       END,
       CASE MOD(LEVEL, 4)
           WHEN 0 THEN '测试报告'
           WHEN 1 THEN '工艺规范'
           WHEN 2 THEN '质量标准'
           WHEN 3 THEN '设计手册'
       END,
       CASE MOD(LEVEL, 3)
           WHEN 0 THEN '内部提取'
           WHEN 1 THEN '标准库抓取'
           WHEN 2 THEN '自主编写'
       END,
       MOD(LEVEL - 1, 500) + 1
FROM DUAL
CONNECT BY LEVEL <= 200;

-- 强制提交，确保数据写入硬盘
COMMIT;

-- 验证结果
SELECT 'dmma_suppliers' AS table_name, COUNT(*) AS cnt FROM dmma_suppliers
UNION ALL
SELECT 'dmma_materials', COUNT(*) FROM dmma_materials
UNION ALL
SELECT 'dmma_standards', COUNT(*) FROM dmma_standards
UNION ALL
SELECT 'dmma_documents', COUNT(*) FROM dmma_documents;
