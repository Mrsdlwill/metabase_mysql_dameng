-- 1. 创建核心材料表
CREATE TABLE dmma_materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '材料名称',
    category VARCHAR(50) NOT NULL COMMENT '材料分类',
    application_area VARCHAR(50) NOT NULL COMMENT '主要应用领域',
    yield_strength INT COMMENT '屈服强度(MPa)',
    density DECIMAL(4,2) COMMENT '密度(g/cm³)'
);

-- 2. 创建标准表
CREATE TABLE dmma_standards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT,
    standard_code VARCHAR(100) NOT NULL,
    system_type VARCHAR(50) NOT NULL
);

-- 3. 创建供应商表
CREATE TABLE dmma_suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    main_focus VARCHAR(50) NOT NULL
);

-- 4. 创建文档资源表 (体现知识库与RAG潜力的核心表)
CREATE TABLE dmma_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    document_type VARCHAR(50) NOT NULL COMMENT '文档类型(如: PDF国标, 测试报告)',
    source VARCHAR(100),
    related_material_id INT COMMENT '关联材料ID'
);

-- =========================================
-- 注入 Mock 数据
-- =========================================
INSERT INTO dmma_materials (name, category, application_area, yield_strength, density) VALUES
('TC4钛合金', '有色金属', '航空航天', 895, 4.43),
('GH4169', '高温合金', '航空航天', 1030, 8.24),
('EH36船体钢', '黑色金属', '船舶海工', 355, 7.84),
('T800碳纤维', '复合材料', '航空航天', 5490, 1.80),
('Hastelloy C-276', '特种合金', '石油化工', 690, 8.89);

INSERT INTO dmma_standards (material_id, standard_code, system_type) VALUES
(1, 'GB/T 3620.1-2016', '国标'), (1, 'AMS 4911', '国际标准'),
(2, 'GB/T 14992-2005', '国标'), (3, 'GB 712-2011', '国标');

INSERT INTO dmma_suppliers (supplier_name, main_focus) VALUES
('西部超导', '材料制造'), ('SGS', '材料检测'), ('钢研纳克', '材料检测');

INSERT INTO dmma_documents (title, document_type, source, related_material_id) VALUES
('TC4钛合金锻件超声波检测规范.pdf', '测试报告', '内部OCR提取', 1),
('GB/T 3620.1-2016 钛及钛合金牌号和化学成分.pdf', 'PDF国标', '标准库抓取', 1),
('GH4169合金高温疲劳性能研究.docx', '研究论文', '知网导入', 2),
('EH36高强度船板钢焊接工艺评定.pdf', '工艺规范', '历史项目积累', 3);
