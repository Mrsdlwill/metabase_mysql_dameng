-- ==========================================
-- 达梦8 数据库表结构创建脚本
-- 兼容MySQL的dmma数据库结构
-- ==========================================

-- 供应商表
CREATE TABLE dmma_suppliers (
    id INT IDENTITY(1,1) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    main_focus VARCHAR(50) NOT NULL
);

-- 材料表
CREATE TABLE dmma_materials (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    application_area VARCHAR(50) NOT NULL,
    yield_strength INT,
    density DECIMAL(4,2)
);

-- 标准表
CREATE TABLE dmma_standards (
    id INT IDENTITY(1,1) PRIMARY KEY,
    material_id INT,
    standard_code VARCHAR(100) NOT NULL,
    system_type VARCHAR(50) NOT NULL
);

-- 文档表
CREATE TABLE dmma_documents (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    source VARCHAR(100),
    related_material_id INT
);

-- 创建索引
CREATE INDEX idx_materials_category ON dmma_materials(category);
CREATE INDEX idx_materials_area ON dmma_materials(application_area);
CREATE INDEX idx_standards_material ON dmma_standards(material_id);
CREATE INDEX idx_documents_material ON dmma_documents(related_material_id);

-- 提交
COMMIT;

-- 完成提示
SELECT '达梦数据库表结构创建完成' AS status;
