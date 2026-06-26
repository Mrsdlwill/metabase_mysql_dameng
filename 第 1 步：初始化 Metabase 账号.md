

### 路线 A：版本对齐

这是**工程落地最稳、成功率最高**的办法。

面对紧急交付（比如明天的面试），最忌讳的就是为了追求完美技术而导致最终系统跑不起来。

- **实操建议**：那个 3 年前的驱动大概率是在 Metabase `v0.40.x` 或 `v0.41.x` 时代写的。你直接在 `docker-compose.yml` 里把镜像改成 `metabase/metabase:v0.41.0`。
- **面试话术**：*“为了保证核心业务流程的快速验证，我采取了稳妥的版本锁定策略。MVP 阶段，稳定压倒一切。”*

### 路线 B：达梦开 MySQL 兼容模式

这是一个真正的**神仙级思路**。它把问题从“如何让 BI 软件去适配冷门数据库”直接翻转成了“如何让强大的数据库主动去迎合主流生态”。

达梦 8 确实有一个强大的特性：通过修改配置文件（`dm.ini` 中的 `COMPATIBLE_MODE = 4`），它可以伪装成 MySQL，甚至连端口、SQL 语法习惯都能做到高度兼容。

- **实操的现实阻力**：在使用开源的 Docker 镜像（如 `shirlt/dm8:latest`）时，它的启动脚本可能已经锁死了默认配置。你要开启这个模式，通常需要把容器里的 `dm.ini` 挂载出来，修改后再重新启动数据库实例。这个折腾的时间成本在今晚可能有点高，容易节外生枝。

- **无敌的面试话术（重点！）**：你可以把它写进文档作为终极演进路线：

  > *“在解决达梦驱动适配时，我进行了架构层面的双向推演。除了传统的客户端驱动适配（路线A），我更倾向于在未来的生产环境使用达梦 DM8 的原生 MySQL 兼容模式（COMPATIBLE_MODE=4）。这样可以彻底甩掉第三方老旧插件的包袱，利用成熟的 MySQL JDBC 体系实现直连，大幅降低系统维护成本和漏洞风险。”*



作为今晚的执行者，**坚决执行路线 A**，不折腾，让系统能在本地顺滑地跑起来，图表能画出来。

但在你提交的总结文档、或者明天的面试沟通中，**一定要抛出路线 B**。

当产品总监问你：“那个达梦数据库的插件好找吗？”

你微笑着回答：“其实我准备了两套方案……” 然后把路线 A 的实操和路线 B 的底层思考讲一遍。





现在你的 MySQL \ 达梦（`dm8`）和 Metabase 都已经稳稳地跑在 Docker 里面 



你能通过 `date-2` 命名空间的重构节点和 `HoneySQL v1` 的特征，精准反推出这是 2023 年 `v0.45 - v0.46` 时代的产物 

### 1.提取真正的“翻译官”（Plugin 包）

这里有一个极易踩坑的盲点：目录根下的 `DmJdbcDriver18.jar` 是达梦官方的“裸” JDBC 驱动，**它不是 Metabase 插件**。真正的插件是由 `src/metabase/driver/dameng.clj` 编译出来的。

1. 展开你截图里的 `target/` 文件夹。
2. 在里面寻找一个名字类似 **`dameng.metabase-driver.jar`** 的文件。
3. **将这个文件复制出来**，放入你本地准备好的 `./plugins` 文件夹中。

*(注：通常这个编译好的插件包内部已经将原生的 `DmJdbcDriver18.jar` 打包进去了，所以你只需要这一个文件即可。)*

### 2.修改 Docker Compose 锁定“时间线”

既然源码是针对 v0.45 - v0.46 开发的，我们直接让 Metabase “穿越”回 2023 年的黄金稳定版 **v0.46.0**。

打开你的 `docker-compose.yml`，修改 `metabase` 服务的镜像版本：

YAML

```
version: '3.8'
services:
  dm8:
    image: shirlt/dm8:latest
    container_name: dm8
    ports:
      - "5236:5236"
    environment:
      SYSDBA_PWD: "Dameng123"
    volumes:
      - dm8-data:/opt/dmdbms/data

  metabase:
    # 【核心修改点】将 latest 改为 v0.46.0
    image: metabase/metabase:v0.46.0
    container_name: metabase
    ports:
      - "3000:3000"
    volumes:
      # 确保 plugins 目录里有 dameng.metabase-driver.jar
      - ./plugins:/plugins
    depends_on:
      - dm8

volumes:
  dm8-data:
```

### 3.一键启动与日志抓虫

1. 在终端中，确保你处于 `docker-compose.yml` 所在的目录。

2. 执行启动命令：

   Bash

   ```
   docker-compose down  # 先清理掉之前可能存在的残留容器
   docker-compose up -d
   ```

3. **关键验证动作：看日志！**

   在启动后，立刻运行以下命令查看 Metabase 的启动日志，这是排错的黄金标准：

   Bash

   ```
   docker logs -f metabase
   ```

   盯着滚动的日志，如果你能在其中看到类似 `Registered driver :dameng` 或者 `Initializing plugin Dameng` 且没有报红色的 `Exception` 错误，说明底层的 Clojure API 握手成功，路线 A 圆满通关！



### 4.：初始化 Metabase 账号

1. 打开浏览器，访问：**[http://127.0.0.1:3000](http://127.0.0.1:3000/)**
2. 你会看到 Metabase 的欢迎界面，点击 **“开始使用” (Let's get started)**。
3. 按照提示，设置你的管理员账号（姓名、邮箱、密码、公司名随意填）。
4. 在初始化引导中，它可能会直接问你要不要添加数据。你可以直接在那里添加，或者点击下方的小字 **“稍后添加” (I'll add my data later)** 跳过向导，进入主界面后再统一添加。

### 5.连接 MySQL 数据库 (dmma)

进入 Metabase 主界面后，按照以下路径操作：

1. 点击右上角的 **齿轮图标 (Settings)**，选择 **“管理员设置” (Admin settings)**。
2. 在左侧菜单栏选择 **“数据库” (Databases)**。
3. 点击右上角的 **“添加数据库” (Add database)** 按钮。

接下来是关键的参数填写：

- **数据库类型 (Database type)**：选择 `MySQL`。

- **显示名称 (Display name)**：随便起，比如填 `DMMA主库`（这个名字只用于你在界面上识别）。

- **主机 (Host)**：填 **`db`**。

  > **💡 架构师划重点**：千万不要填 `127.0.0.1` 或 `localhost`！因为 Metabase 跑在容器里，它的 localhost 是它自己。在刚才的 `docker-compose.yml` 中，你给 MySQL 命名的服务叫 `db`，在 Docker 网络里，这个名字就相当于它的 IP 地址，Metabase 会自动解析它。

- **端口 (Port)**：`3306`

- **数据库名 (Database name)**：`dmma`

- **用户名 (Username)**：`root`

- **密码 (Password)**：`root`

拉到最下面，点击 **“保存” (Save)**。如果没报错，Metabase 就会开始自动扫描你的 `dmma` 库里的表结构了！



1. **展开高级选项：** 在 界面 下方蓝色的 **"Show advanced options"**（显示高级选项）。

2. **找到附加参数框：** 向下滚动，找到名为 **"Additional JDBC connection string options"**（附加的 JDBC 连接字符串选项）的文本输入框。

3. **注入魔法参数：** 在这个框里填入以下代码：

   Plaintext

   ```
   allowPublicKeyRetrieval=true
   ```

   *(这行代码的作用是直接允许客户端在不使用 SSL 的情况下获取服务器的 RSA 公钥。)*

4. **重试连接：** 滚动到最底部，再次点击保存/连接即可。

### 6.达梦（`dm8`）数据库

由于你的 Metabase 和达梦（`dm8`）都是在 Docker 里面跑的容器，请严格按照以下参数重新配置：

1. **进入 Metabase 管理员设置**：
   - 点击 Metabase 右上角的齿轮图标 ⚙️ -> **管理员设置 (Admin settings)**。
   - 在左侧菜单找到 **数据库 (Databases)**。
   - 点击你目前正在用的那个达梦数据库连接（或者新建一个）。
2. **核对并修改连接详情**： 请确保填入的是以下信息，绝对不能填错：
   - **数据库类型 (Database type)**: 达梦 (Dameng)
   - **主机 (Host)**: 填 **`dm8`**（绝对不能填 `localhost` 或 `127.0.0.1`，因为 Metabase 在自己的容器里，`localhost` 指的是它自己，必须填达梦的容器名 `dm8` 才能在 Docker 网络里互通）。
   - **端口 (Port)**: **`5236`**
   - **数据库名称 (Database name)**: 默认填 **`SYSDBA`** 即可。
   - **用户名 (Username)**: **`SYSDBA`**
   - **密码 (Password)**: **`Dameng123`**（注意大小写，D 是大写）。
3. **保存并重新扫描**：
   - 点击页面底部的 **保存 (Save)**。
   - 如果保存成功，说明 Metabase 终于连上达梦了。



### 第 3 步：跑通第一条数据测试

进入 Metabase 首页后，我们来验证一下数据是不是都在里面了：

1. 点击右上角的 **+ New**（新建） -> **SQL query**（SQL 查询）。

2. 在左上角的数据库下拉菜单里，选中你刚添加的 `DMMA 核心材料库`。

3. 把 Claude 刚才给你的那段核心 SQL 复制粘贴进代码框：

   SQL

   ```
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

4. 点击右下角的 **Run**（运行）或者按 `Ctrl+Enter`。

你应该能立刻在下方看到查询结果——展示了不同材料类别下关联的标准数和解析文档数。











在 BI 系统里写 SQL，其实你只需要掌握 4 个核心动作：**拿什么（SELECT）、怎么挑（WHERE）、怎么分组算（GROUP BY）、怎么排（ORDER BY）**。

#### 1. 基础查询：全表检索与条件过滤

- **概念**：就跟 Excel 里的“筛选”一样。
- **业务场景**：老板说：“把屈服强度大于 1000 的航空航天材料都给我找出来。”
- **代码**：

SQL

```
SELECT name, category, yield_strength 
FROM dmma_materials 
WHERE yield_strength > 1000 
  AND application_area = '航空航天';
```

*(在 Metabase 里跑完这段，可以直接选“表格”进行展示)*

#### 2. 聚合统计：万物皆可 GROUP BY

- **概念**：这是 BI 看板的灵魂！只要你想画**饼图**或者**柱状图**，99% 都要用到 `GROUP BY`。它就像把桌子上散落的扑克牌按花色分堆，然后数每堆有几张（`COUNT`），或者算每堆的平均大小（`AVG`）。
- **业务场景**：画一个饼图，看各个“应用领域”的材料数量占比。
- **代码**：

SQL

```
SELECT application_area AS '应用领域', COUNT(*) AS '材料数量'
FROM dmma_materials 
GROUP BY application_area;
```

#### 3. 排名与限制：做 Top N 榜单

- **概念**：数据太多看不过来，只看最好的前几个。`ORDER BY` 负责排序（`DESC` 是从大到小），`LIMIT` 负责截断。
- **业务场景**：在首页做一个“尖端高强材料 Top 10 龙虎榜”。
- **代码**：

SQL

```
SELECT name AS '材料名称', yield_strength AS '屈服强度(MPa)'
FROM dmma_materials 
ORDER BY yield_strength DESC 
LIMIT 10;
```

#### 4. 多表联查 (JOIN)：知识库关联的核心

- **概念**：这稍微有一点点绕，但非常强大。比如材料的名字在 `materials` 表里，但它的 PDF 文档在 `documents` 表里。你需要用 `JOIN` 把它们“拼”在一起。
- **业务场景**：统计每种材料各挂载了多少份标准文档（面试加分项大招）。
- **代码**：

SQL

```
SELECT 
    m.name AS '材料名称', 
    COUNT(d.id) AS '挂载文档数'
FROM dmma_materials m
LEFT JOIN dmma_documents d ON m.id = d.related_material_id
GROUP BY m.name
ORDER BY '挂载文档数' DESC
LIMIT 10;
```

*(这段代码翻译成大白话：拿材料表（m），去左贴合文档表（d），贴合的依据是材料的 id 等于文档的 related_material_id，然后按材料名字分堆，数一数每堆有几个文档。)*



太棒了！160条材料数据和64条关联文档，这个数据量已经完全达到了一个中小型项目原型（MVP）的标准，足以让 Metabase 的图表变得极其充实和美观。

在 Metabase 这种 BI（商业智能）工具中，写 SQL 的核心逻辑非常固定。你不需要像后端开发那样考虑高并发或复杂的事务，你的唯一目标就是**把杂乱的多行数据变成“有维度、有指标”的统计结果**，从而直接喂给图表。

下面为你梳理在当前 160 条海量数据下，最实用的 4 个经典数据大屏 SQL 模版，你可以直接复制到 Metabase 的 SQL 编辑器中运行：

### 1. 核心看板指标

各应用领域的材料数量与平均强度（适合做柱状图/折线图）

- **业务场景**：一眼看出哪个领域（如航空航天、船舶海工）的材料分布最多，以及哪个领域的技术门槛（平均屈服强度）最高。

- **SQL 代码**：

  SQL

  ```
  SELECT 
      application_area AS '应用领域', 
      COUNT(*) AS '材料种类数量', 
      ROUND(AVG(yield_strength), 1) AS '平均屈服强度(MPa)'
  FROM dmma_materials
  GROUP BY application_area
  ORDER BY  COUNT(*) DESC;
  ```

- **Metabase 配置推荐**：在可视化设置中选择 **Combo（组合图）**，将“材料种类数量”设为**柱状图（左轴）**，“平均屈服强度”设为**折线图（右轴）**。

### 2. 研发龙虎榜

尖端超高强度材料 Top 10（适合做横向条形图）

- **业务场景**：展示数据库中性能最强悍的明星材料，通常放在大屏最显眼的位置。

- **SQL 代码**：

  SQL

  ```
  SELECT 
      name AS '材料名称', 
      category AS '材料分类', 
      yield_strength AS '屈服强度(MPa)'
  FROM dmma_materials
  WHERE yield_strength IS NOT NULL
  ORDER BY yield_strength DESC
  LIMIT 10;
  ```

- **Metabase 配置推荐**：选择 **Row（横向条形图）**，按强度从大到小排列，视觉冲击力极强。

### 3. 知识库完备度分析：材料挂载文档与标准数量统计

（适合做数据表格/散点图）

- **业务场景**：由于你做了数据裂变，很多新材料可能还没有挂载文档。这个查询可以帮你盘点哪些材料的知识库建设最完善。

- **SQL 代码**：

  SQL

  ```
  SELECT 
      m.name AS '材料名称', 
      m.category AS '材料分类',
      COUNT(DISTINCT d.id) AS '关联解析文档数',
      COUNT(DISTINCT s.id) AS '关联标准数'
  FROM dmma_materials m
  LEFT JOIN dmma_documents d ON m.id = d.related_material_id
  LEFT JOIN dmma_standards s ON m.id = s.material_id
  GROUP BY m.id, m.name, m.category
  ORDER BY COUNT(DISTINCT d.id) DESC
  LIMIT 15;
  ```

- **Metabase 配置推荐**：直接保留为 **Table（智能表格）**，并在 Metabase 属性里开启“条件格式”，把文档数少的行用轻微颜色标出，作为“急需补充文档”的预警。

### 4. 预警看板：没有任何文档支撑的“孤儿材料”清单（适合做指标卡或列表）

- **业务场景**：找出那些通过了数据裂变，但在知识库中（`dmma_documents`）完全找不到对应 PDF 或报告的材料，方便后续做 RAG（检索增强生成）时进行针对性补充。

- **SQL 代码**：

  SQL

  ```
  SELECT 
      m.id AS '材料ID', 
      m.name AS '材料名称', 
      m.application_area AS '应用领域'
  FROM dmma_materials m
  LEFT JOIN dmma_documents d ON m.id = d.related_material_id
  WHERE d.id IS NULL
  ORDER BY m.id ASC;
  ```

为了让你在把这些代码敲入 Metabase 之前，能更直观地理解每一句 SQL 的各个子句（SELECT、WHERE、GROUP BY、ORDER BY）是如何切分、过滤并最终决定图表形态的，我为你制作了一个 **DMMA 大数据看板 SQL 交互教学模拟器**。

你可以在下方自由切换不同的看板业务需求，实时查看其背后的 SQL 构造逻辑、字段拆解，以及它在真实 BI 大屏中对应的可视化呈现效果：













