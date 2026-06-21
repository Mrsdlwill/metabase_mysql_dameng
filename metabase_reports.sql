-- ==========================================
-- Metabase 可视化报表 SQL 集合
-- 适用于 MySQL / 达梦数据库
-- ==========================================

-- ==========================================
-- 1材料类别分布（饼图）
-- ==========================================
SELECT
    category AS "材料类别",
    COUNT(*) AS "数量"
FROM dmma_materials
GROUP BY category
ORDER BY 2 DESC;

-- ==========================================
-- 2应用领域分布（环形图）
-- ==========================================
SELECT
    application_area AS "应用领域",
    COUNT(*) AS "数量"
FROM dmma_materials
GROUP BY application_area
ORDER BY 2 DESC;

-- ==========================================
-- 3各类别材料屈服强度箱线图数据（箱线图）
-- ==========================================
SELECT
    category AS "材料类别",
    MIN(yield_strength) AS "最小值",
    AVG(yield_strength) AS "平均值",
    MAX(yield_strength) AS "最大值",
    COUNT(*) AS "样本数"
FROM dmma_materials
GROUP BY category
ORDER BY 4 DESC;

-- ==========================================
-- 4材料性能对比 TOP20（柱状图）
-- ==========================================
SELECT
    name AS "材料名称",
    yield_strength AS "屈服强度(MPa)",
    density AS "密度(g/cm³)"
FROM dmma_materials
ORDER BY yield_strength DESC
FETCH FIRST 20 ROWS ONLY;

-- ==========================================
-- 5标准体系分布（条形图）
-- ==========================================
SELECT
    system_type AS "标准体系",
    COUNT(*) AS "标准数量"
FROM dmma_standards
GROUP BY system_type
ORDER BY 2 DESC;

-- ==========================================
-- 6文档类型统计（饼图）
-- ==========================================
SELECT
    document_type AS "文档类型",
    COUNT(*) AS "文档数量"
FROM dmma_documents
GROUP BY document_type
ORDER BY 2 DESC;

-- ==========================================
-- 7文档来源统计（条形图）
-- ==========================================
SELECT
    source AS "文档来源",
    COUNT(*) AS "文档数量"
FROM dmma_documents
GROUP BY source
ORDER BY 2 DESC;

-- ==========================================
-- 8材料-标准-文档关联全景（分组柱状图 — 核心卡片）
-- ==========================================
SELECT
    m.category AS "材料类别",
    COUNT(DISTINCT s.id) AS "关联标准数",
    COUNT(DISTINCT d.id) AS "解析文档数"
FROM dmma_materials m
LEFT JOIN dmma_standards s ON m.id = s.material_id
LEFT JOIN dmma_documents d ON m.id = d.related_material_id
GROUP BY m.category
ORDER BY 2 DESC;

-- ==========================================
-- 9各应用领域材料密度分布（散点图）
-- ==========================================
SELECT
    name AS "材料名称",
    density AS "密度(g/cm³)",
    yield_strength AS "屈服强度(MPa)",
    application_area AS "应用领域"
FROM dmma_materials
WHERE density IS NOT NULL AND yield_strength IS NOT NULL
ORDER BY application_area, density;

-- ==========================================
-- 10材料综合信息卡（详情表 — 用于 Metabase 的「详情」视图）
-- ==========================================
SELECT
    m.name AS "材料名称",
    m.category AS "类别",
    m.application_area AS "应用领域",
    m.yield_strength AS "屈服强度",
    m.density AS "密度",
    CAST(WM_CONCAT(DISTINCT s.standard_code) AS VARCHAR(2000)) AS "执行标准",
    COUNT(DISTINCT d.id) AS "关联文档数"
FROM dmma_materials m
LEFT JOIN dmma_standards s ON m.id = s.material_id
LEFT JOIN dmma_documents d ON m.id = d.related_material_id
GROUP BY m.id, m.name, m.category, m.application_area, m.yield_strength, m.density
ORDER BY m.yield_strength DESC
FETCH FIRST 50 ROWS ONLY;

-- ==========================================
-- 11各类别材料屈服强度范围（堆叠柱状图）
-- ==========================================
SELECT
    category AS "材料类别",
    CASE
        WHEN yield_strength < 200 THEN '低强度(<200MPa)'
        WHEN yield_strength BETWEEN 200 AND 500 THEN '中强度(200-500MPa)'
        WHEN yield_strength BETWEEN 500 AND 1000 THEN '高强度(500-1000MPa)'
        ELSE '超高强度(>1000MPa)'
    END AS "强度等级",
    COUNT(*) AS "数量"
FROM dmma_materials
GROUP BY category, 2
ORDER BY category, 2;

-- ==========================================
-- 12材料密度 vs 屈服强度气泡图（气泡大小=文档数）
-- ==========================================
SELECT
    m.name AS "材料名称",
    m.density AS "密度",
    m.yield_strength AS "屈服强度",
    COUNT(d.id) AS "文档数",
    m.category AS "材料类别"
FROM dmma_materials m
LEFT JOIN dmma_documents d ON m.id = d.related_material_id
WHERE m.density IS NOT NULL AND m.yield_strength IS NOT NULL
GROUP BY m.id, m.name, m.density, m.yield_strength, m.category
ORDER BY m.category;

-- ==========================================
-- 13各类别材料应用领域热力图（交叉表）
-- ==========================================
SELECT
    category AS "材料类别",
    application_area AS "应用领域",
    COUNT(*) AS "数量"
FROM dmma_materials
GROUP BY category, application_area
ORDER BY category, 3 DESC;

-- ==========================================
-- 14供应商专注领域分布（饼图）
-- ==========================================
SELECT
    main_focus AS "专注领域",
    COUNT(*) AS "供应商数量"
FROM dmma_suppliers
GROUP BY main_focus
ORDER BY 2 DESC;

-- ==========================================
-- 15材料类别与标准体系关联（桑基图数据）
-- ==========================================
SELECT
    m.category AS "材料类别",
    s.system_type AS "标准体系",
    COUNT(*) AS "关联数"
FROM dmma_materials m
JOIN dmma_standards s ON m.id = s.material_id
GROUP BY m.category, s.system_type
ORDER BY m.category, 3 DESC;
