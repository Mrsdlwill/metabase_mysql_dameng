### 给 Claude Code 的工作流指令

你可以在终端中启动 Claude Code，然后按照以下步骤给它下达指令，让它帮你自动化完成繁琐的准备工作。

#### 第一步：让 Claude Code 生成并执行 SQL 脚本

你可以直接复制这段话发给 Claude Code：

> “帮我在当前目录下创建一个名为 `init_dmma_db.sql` 的文件，并将下面这段完整的 DMMA 数据库初始化脚本写入其中。写完后，请提示我如何在本地 MySQL 中执行它。”

**（附：需要写入的终极版 SQL 脚本）**

```sql
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

```

#### 第二步：启动 Metabase 容器

在 SQL 脚本成功导入你本地的 MySQL 后，告诉 Claude Code：

> “我现在需要部署 Metabase。请帮我执行 Docker 命令，在后台拉取并运行最新的 Metabase 镜像，将端口映射为 3000。并在执行成功后告诉我访问地址。”

*(它会自动帮你执行 `docker run -d -p 3000:3000 --name metabase metabase/metabase` 并确认运行状态)*

---

### 人工操作环节 (Metabase 配置与截图)

Claude Code 帮你把脚手架搭好后，剩下的就是你在浏览器里大展身手了：

1. 打开 `http://127.0.0.1:3000`。
2. 连接你的本地 MySQL（如果遇到 127.0.0.1 连不上的情况，因为在 Docker 容器里，可能需要将地址填为 `host.docker.internal`，账号密码用你本地的）。
3. **立刻去写你提到的那段满分 SQL，并存为 Dashboard 的一张核心卡片**：
```sql
-- 核心知识库业务图表：不同材料类别关联标准与文档数量
SELECT 
    m.category AS '材料类别', 
    COUNT(DISTINCT s.id) AS '关联标准数',
    COUNT(DISTINCT d.id) AS '解析文档数'
FROM dmma_materials m
LEFT JOIN dmma_standards s ON m.id = s.material_id
LEFT JOIN dmma_documents d ON m.id = d.related_material_id
GROUP BY m.category
ORDER BY '关联标准数' DESC;

```


4. 再配几个简单的 COUNT 卡片（总材料数、总文档数）和饼图（文档类型分布）。

