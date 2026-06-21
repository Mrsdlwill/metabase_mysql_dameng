#!/usr/bin/env python3
"""生成材料管理系统数据扩充SQL脚本"""
import random

random.seed(42)

# ==================== 基础数据定义 ====================

CATEGORIES = {
    "有色金属": {
        "materials": [
            ("TC4钛合金", "航空航天", (800, 950), (4.40, 4.60)),
            ("TC21钛合金", "航空航天", (850, 1000), (4.45, 4.65)),
            ("TA7钛合金", "航空航天", (750, 900), (4.50, 4.60)),
            ("Ti-6Al-2Sn-4Zr-2Mo", "航空航天", (900, 1050), (4.50, 4.65)),
            ("2024铝合金", "航空航天", (300, 400), (2.70, 2.80)),
            ("7075铝合金", "航空航天", (450, 550), (2.75, 2.85)),
            ("6061铝合金", "船舶海工", (240, 310), (2.65, 2.75)),
            ("5083铝合金", "船舶海工", (210, 280), (2.65, 2.70)),
            ("2A12铝合金", "航空航天", (330, 420), (2.75, 2.80)),
            ("7050铝合金", "航空航天", (420, 520), (2.75, 2.85)),
            ("紫铜T2", "电子信息", (60, 120), (8.90, 8.95)),
            ("黄铜H62", "船舶海工", (120, 200), (8.40, 8.50)),
            ("青铜QBe2", "电子信息", (200, 400), (8.20, 8.30)),
            ("白铜B30", "船舶海工", (150, 250), (8.90, 8.95)),
            ("镁合金AZ91D", "航空航天", (150, 230), (1.75, 1.85)),
            ("镁合金AZ31B", "航空航天", (130, 200), (1.70, 1.80)),
            ("纯铝1060", "石油化工", (30, 80), (2.70, 2.71)),
            ("铝合金5052", "船舶海工", (170, 230), (2.65, 2.70)),
            ("铝合金6063", "建筑工程", (120, 180), (2.65, 2.70)),
            ("铝合金2A14", "航空航天", (360, 450), (2.75, 2.80)),
        ],
    },
    "高温合金": {
        "materials": [
            ("GH4169", "航空航天", (950, 1100), (8.15, 8.30)),
            ("GH4141", "航空航天", (900, 1050), (8.20, 8.35)),
            ("GH3030", "航空航天", (600, 750), (8.35, 8.45)),
            ("GH3128", "航空航天", (700, 850), (8.15, 8.25)),
            ("GH901", "航空航天", (800, 950), (8.10, 8.20)),
            ("K418铸造高温合金", "航空航天", (700, 850), (7.90, 8.10)),
            ("DZ125定向凝固合金", "航空航天", (850, 1000), (8.40, 8.60)),
            ("DD6单晶高温合金", "航空航天", (800, 950), (8.70, 8.90)),
            ("Inconel 718", "石油化工", (950, 1100), (8.15, 8.30)),
            ("Inconel 625", "石油化工", (600, 800), (8.40, 8.50)),
            ("Inconel 600", "石油化工", (350, 550), (8.40, 8.50)),
            ("Waspaloy", "航空航天", (800, 950), (8.15, 8.25)),
            ("René 88DT", "航空航天", (900, 1050), (8.30, 8.50)),
            ("Udimet 720", "航空航天", (950, 1100), (8.25, 8.40)),
            ("Nimonic 80A", "航空航天", (550, 700), (8.15, 8.25)),
            ("Nimonic 90", "航空航天", (650, 800), (8.15, 8.25)),
            ("Hastelloy X", "石油化工", (350, 500), (8.20, 8.30)),
            ("GH2036", "航空航天", (600, 750), (7.80, 8.00)),
            ("GH2132", "航空航天", (600, 750), (7.90, 8.10)),
            ("GH742", "航空航天", (900, 1050), (8.30, 8.50)),
        ],
    },
    "黑色金属": {
        "materials": [
            ("EH36船体钢", "船舶海工", (340, 380), (7.80, 7.90)),
            ("Q345B结构钢", "建筑工程", (300, 380), (7.80, 7.90)),
            ("Q235B碳素钢", "建筑工程", (210, 260), (7.80, 7.90)),
            ("45号碳钢", "机械制造", (330, 400), (7.80, 7.90)),
            ("40Cr合金钢", "机械制造", (750, 950), (7.80, 7.90)),
            ("20CrMnTi齿轮钢", "机械制造", (800, 1000), (7.80, 7.90)),
            ("304不锈钢", "石油化工", (200, 300), (7.85, 7.95)),
            ("316L不锈钢", "船舶海工", (170, 280), (7.85, 7.95)),
            ("2205双相不锈钢", "石油化工", (450, 600), (7.80, 7.90)),
            ("904L超级不锈钢", "石油化工", (220, 320), (7.95, 8.05)),
            ("4Cr13模具钢", "机械制造", (500, 700), (7.70, 7.80)),
            ("Cr12MoV模具钢", "机械制造", (550, 750), (7.65, 7.75)),
            ("T10碳素工具钢", "机械制造", (350, 500), (7.80, 7.90)),
            ("W18Cr4V高速钢", "机械制造", (800, 1000), (8.60, 8.80)),
            ("GCr15轴承钢", "机械制造", (800, 1000), (7.80, 7.90)),
            ("16MnDR低温钢", "石油化工", (300, 400), (7.80, 7.90)),
            ("09MnNiDR低温钢", "石油化工", (260, 350), (7.80, 7.90)),
            ("Q345R容器钢", "石油化工", (320, 400), (7.80, 7.90)),
            ("15CrMoR耐热钢", "石油化工", (300, 420), (7.80, 7.90)),
            ("12Cr1MoV耐热钢", "石油化工", (280, 400), (7.80, 7.90)),
            ("0Cr18Ni9不锈钢", "电子信息", (200, 300), (7.85, 7.95)),
            ("1Cr17不锈钢", "石油化工", (200, 280), (7.70, 7.80)),
            ("SUS301不锈钢", "电子信息", (500, 700), (7.90, 8.00)),
            ("SUS430不锈钢", "石油化工", (200, 280), (7.70, 7.80)),
            ("马氏体不锈钢0Cr13", "石油化工", (350, 500), (7.70, 7.80)),
            ("沉淀硬化不锈钢17-4PH", "航空航天", (1000, 1200), (7.70, 7.80)),
            ("超级双相钢SAF2507", "石油化工", (550, 700), (7.80, 7.90)),
            ("耐磨钢NM400", "机械制造", (1000, 1200), (7.80, 7.90)),
            ("耐磨钢NM500", "机械制造", (1200, 1400), (7.80, 7.90)),
            ("高强钢Q690", "建筑工程", (650, 750), (7.80, 7.90)),
        ],
    },
    "复合材料": {
        "materials": [
            ("T300碳纤维/环氧", "航空航天", (1500, 2000), (1.50, 1.65)),
            ("T700碳纤维/环氧", "航空航天", (2000, 2600), (1.55, 1.65)),
            ("T800碳纤维/环氧", "航空航天", (2500, 3200), (1.55, 1.65)),
            ("T1000碳纤维/环氧", "航空航天", (3000, 4000), (1.55, 1.65)),
            ("T1100碳纤维/环氧", "航空航天", (3500, 4500), (1.55, 1.65)),
            ("M40J碳纤维/环氧", "航空航天", (1800, 2400), (1.55, 1.65)),
            ("M55J碳纤维/环氧", "航空航天", (2000, 2600), (1.55, 1.65)),
            ("M60J碳纤维/环氧", "航空航天", (2200, 2800), (1.55, 1.65)),
            ("AS4碳纤维/环氧", "航空航天", (1600, 2200), (1.55, 1.65)),
            ("IM7碳纤维/环氧", "航空航天", (2500, 3200), (1.55, 1.65)),
            ("玻璃纤维/环氧", "船舶海工", (500, 800), (1.80, 2.00)),
            ("S-2玻璃纤维/环氧", "航空航天", (800, 1200), (1.90, 2.10)),
            ("芳纶纤维/环氧", "航空航天", (1200, 1800), (1.30, 1.45)),
            ("Kevlar 49/环氧", "航空航天", (1200, 1600), (1.35, 1.45)),
            ("UHMWPE纤维复合材料", "船舶海工", (800, 1200), (0.95, 1.05)),
            ("碳纤维/双马来酰亚胺", "航空航天", (1800, 2400), (1.55, 1.65)),
            ("碳纤维/聚酰亚胺", "航空航天", (1200, 1800), (1.50, 1.65)),
            ("碳纤维/PEEK热塑性", "航空航天", (1500, 2000), (1.55, 1.65)),
            ("碳纤维/PPS热塑性", "航空航天", (1200, 1600), (1.50, 1.60)),
            ("硼纤维/环氧", "航空航天", (2000, 2800), (2.00, 2.20)),
        ],
    },
    "特种合金": {
        "materials": [
            ("Hastelloy C-276", "石油化工", (650, 780), (8.85, 8.95)),
            ("Hastelloy C-22", "石油化工", (600, 750), (8.65, 8.75)),
            ("Hastelloy B-3", "石油化工", (550, 700), (9.20, 9.30)),
            ("Hastelloy X", "航空航天", (350, 500), (8.20, 8.30)),
            ("Inconel 718", "航空航天", (950, 1100), (8.15, 8.30)),
            ("Inconel 625", "石油化工", (600, 800), (8.40, 8.50)),
            ("Inconel 600", "石油化工", (350, 550), (8.40, 8.50)),
            ("Inconel 690", "核工业", (350, 550), (8.30, 8.40)),
            ("Monel 400", "船舶海工", (200, 350), (8.80, 8.90)),
            ("Monel K-500", "船舶海工", (550, 750), (8.40, 8.50)),
            ("纯钛TA1", "医疗器械", (170, 280), (4.50, 4.55)),
            ("纯钛TA2", "医疗器械", (250, 380), (4.50, 4.55)),
            ("钛合金TC4", "航空航天", (800, 950), (4.40, 4.55)),
            ("钛合金TC11", "航空航天", (900, 1050), (4.45, 4.55)),
            ("钛合金TC21", "航空航天", (850, 1000), (4.45, 4.60)),
            ("锆合金Zr-702", "核工业", (250, 400), (6.50, 6.60)),
            ("锆合金Zr-705", "核工业", (350, 500), (6.50, 6.60)),
            ("铌合金C-103", "航空航天", (200, 350), (8.80, 9.00)),
            ("钼合金TZM", "航空航天", (500, 700), (10.10, 10.20)),
            ("钨合金W-25Re", "航空航天", (800, 1000), (19.50, 20.00)),
        ],
    },
    "陶瓷材料": {
        "materials": [
            ("氧化铝陶瓷99%", "电子信息", (2000, 3000), (3.85, 3.95)),
            ("氧化铝陶瓷95%", "电子信息", (1500, 2500), (3.70, 3.85)),
            ("氧化锆陶瓷3Y-TZP", "医疗器械", (800, 1200), (5.90, 6.10)),
            ("氧化锆陶瓷8Y-PSZ", "机械制造", (600, 900), (5.70, 5.90)),
            ("碳化硅陶瓷", "航空航天", (400, 600), (3.10, 3.25)),
            ("氮化硅陶瓷", "机械制造", (600, 900), (3.15, 3.30)),
            ("氮化铝陶瓷", "电子信息", (300, 500), (3.20, 3.35)),
            ("硼化锆陶瓷", "航空航天", (350, 550), (5.90, 6.10)),
            ("石英玻璃", "电子信息", (500, 800), (2.20, 2.25)),
            ("莫来石陶瓷", "石油化工", (200, 400), (2.50, 2.70)),
        ],
    },
    "高分子材料": {
        "materials": [
            ("PEEK聚醚醚酮", "航空航天", (90, 120), (1.25, 1.35)),
            ("PEI聚醚酰亚胺", "航空航天", (100, 130), (1.25, 1.35)),
            ("PPS聚苯硫醚", "航空航天", (60, 100), (1.30, 1.40)),
            ("PA66尼龙66", "机械制造", (60, 90), (1.12, 1.16)),
            ("PA6尼龙6", "机械制造", (50, 80), (1.12, 1.16)),
            ("POM聚甲醛", "机械制造", (55, 80), (1.38, 1.45)),
            ("PTFE聚四氟乙烯", "石油化工", (15, 30), (2.12, 2.20)),
            ("PVDF聚偏氟乙烯", "石油化工", (25, 45), (1.75, 1.80)),
            ("PC聚碳酸酯", "电子信息", (50, 70), (1.18, 1.22)),
            ("PMMA有机玻璃", "电子信息", (50, 80), (1.17, 1.20)),
            ("ABS塑料", "机械制造", (30, 55), (1.02, 1.08)),
            ("PP聚丙烯", "石油化工", (20, 40), (0.89, 0.92)),
            ("PE聚乙烯", "石油化工", (15, 30), (0.92, 0.97)),
            ("PVC聚氯乙烯", "建筑工程", (30, 55), (1.30, 1.45)),
            ("PI聚酰亚胺", "航空航天", (80, 120), (1.35, 1.45)),
            ("UHMWPE超高分子量聚乙烯", "医疗器械", (20, 40), (0.92, 0.95)),
            ("硅橡胶", "医疗器械", (5, 15), (1.10, 1.20)),
            ("氟橡胶", "航空航天", (10, 25), (1.80, 1.90)),
            ("EPDM三元乙丙橡胶", "建筑工程", (5, 15), (1.10, 1.20)),
            ("丁腈橡胶NBR", "石油化工", (8, 20), (1.00, 1.10)),
        ],
    },
    "稀土与功能材料": {
        "materials": [
            ("NdFeB钕铁硼永磁", "电子信息", (250, 400), (7.40, 7.60)),
            ("SmCo钐钴永磁", "航空航天", (200, 350), (8.20, 8.50)),
            ("铝镍钴永磁", "电子信息", (100, 200), (6.80, 7.20)),
            ("软磁铁氧体", "电子信息", (10, 30), (4.80, 5.20)),
            ("坡莫合金", "电子信息", (100, 200), (8.60, 8.80)),
            ("硅钢片", "电力设备", (200, 350), (7.60, 7.80)),
            ("磁致伸缩合金Terfenol-D", "航空航天", (50, 100), (9.00, 9.20)),
            ("形状记忆合金NiTi", "医疗器械", (200, 500), (6.40, 6.60)),
            ("压电陶瓷PZT", "电子信息", (30, 80), (7.50, 7.80)),
            ("热电材料Bi2Te3", "电子信息", (20, 50), (7.70, 8.00)),
        ],
    },
}

# 标准数据
STANDARDS_BASE = [
    ("GB/T", "国标"),
    ("GJB", "国标"),
    ("ASTM", "国际标准"),
    ("AMS", "国际标准"),
    ("ISO", "国际标准"),
    ("EN", "国际标准"),
    ("HB", "国标"),
    ("QJ", "国标"),
    ("TB", "国标"),
    ("YS", "国标"),
]

# 供应商数据
SUPPLIERS_BASE = [
    ("西部超导材料科技股份有限公司", "材料制造"),
    ("中国科学院金属研究所", "材料研发"),
    ("钢铁研究总院", "材料研发"),
    ("宝武钢铁集团", "材料制造"),
    ("鞍钢集团有限公司", "材料制造"),
    ("抚顺特殊钢股份有限公司", "材料制造"),
    ("东北特殊钢集团", "材料制造"),
    ("大冶特殊钢有限公司", "材料制造"),
    ("西宁特殊钢集团", "材料制造"),
    ("长城特殊钢有限公司", "材料制造"),
    ("中铝西南铝业有限公司", "材料制造"),
    ("南山铝业股份有限公司", "材料制造"),
    ("忠旺集团有限公司", "材料制造"),
    ("丛林铝业科技有限公司", "材料制造"),
    ("云海金属股份有限公司", "材料制造"),
    ("宁波韵升股份有限公司", "稀土材料"),
    ("中科三环高技术股份有限公司", "稀土材料"),
    ("正海磁性材料股份有限公司", "稀土材料"),
    ("金力永磁科技股份有限公司", "稀土材料"),
    ("大地熊新材料股份有限公司", "稀土材料"),
    ("中复神鹰碳纤维有限公司", "复合材料"),
    ("光威复材技术股份有限公司", "复合材料"),
    ("恒神股份有限公司", "复合材料"),
    ("江苏恒力化纤股份有限公司", "复合材料"),
    ("泰山玻璃纤维有限公司", "复合材料"),
    ("SGS通标标准技术服务有限公司", "材料检测"),
    ("中国航发北京航空材料研究院", "材料研发"),
    ("北京有色金属研究总院", "材料研发"),
    ("郑州轻金属研究院", "材料研发"),
    ("钢铁研究总院青岛海洋腐蚀研究所", "材料检测"),
    ("中国特种设备检测研究院", "材料检测"),
    ("国家钢铁材料测试中心", "材料检测"),
    ("国家有色金属质量监督检验中心", "材料检测"),
    ("中国商飞上海飞机设计研究院", "材料应用"),
    ("中国航发沈阳黎明航空发动机公司", "材料应用"),
    ("中国航发西安航空发动机公司", "材料应用"),
    ("沈阳飞机工业集团有限公司", "材料应用"),
    ("成都飞机工业集团有限公司", "材料应用"),
    ("哈尔滨飞机工业集团有限公司", "材料应用"),
    ("中国船舶集团第七二五研究所", "材料研发"),
    ("沪东中华造船集团有限公司", "材料应用"),
    ("大连船舶重工集团有限公司", "材料应用"),
    ("中国石化工程建设有限公司", "材料应用"),
    ("中国石油集团工程设计有限公司", "材料应用"),
    ("中广核工程有限公司", "材料应用"),
    ("中国核动力研究设计院", "材料应用"),
    ("华为技术有限公司", "材料应用"),
    ("中芯国际集成电路制造有限公司", "材料应用"),
    ("比亚迪股份有限公司", "材料应用"),
    ("宁德时代新能源科技有限公司", "材料应用"),
]

# 文档类型
DOC_TYPES = ["测试报告", "PDF国标", "研究论文", "工艺规范", "质量标准", "检验规程", "技术条件", "设计手册"]
DOC_SOURCES = ["内部OCR提取", "标准库抓取", "知网导入", "万方导入", "历史项目积累", "供应商提供", "客户委托", "自主编写"]
DOC_MATERIALS_RATIO = [0.3, 0.25, 0.2, 0.15, 0.1]  # 文档偏向哪类材料的比例

def generate_standards():
    """生成100条标准数据"""
    standards = []
    # 国标
    gb_prefixes = ["GB/T", "GB", "GJB", "HB", "QJ", "TB", "YS", "JB/T"]
    gb_categories = [
        "钛及钛合金", "铝及铝合金", "铜及铜合金", "钢", "不锈钢",
        "高温合金", "碳纤维", "玻璃纤维", "焊接材料", "热处理",
        "力学性能", "化学分析", "无损检测", "金相检验", "腐蚀试验",
        "精密铸造", "粉末冶金", "复合材料", "橡胶制品", "塑料制品",
    ]
    for i in range(50):
        prefix = random.choice(gb_prefixes)
        cat = random.choice(gb_categories)
        year = random.choice([2005, 2008, 2010, 2012, 2014, 2016, 2018, 2019, 2020, 2021, 2022, 2023])
        num = random.randint(100, 9999)
        standards.append((f"{prefix} {num}-{year}", "国标"))

    # 国际标准
    intl_prefixes = ["ASTM", "AMS", "ISO", "EN", "SAE", "MIL"]
    intl_categories = [
        "Titanium", "Aluminum", "Steel", "Nickel", "Carbon Fiber",
        "Welding", "Heat Treatment", "Testing", "Corrosion", "Casting",
    ]
    for i in range(50):
        prefix = random.choice(intl_prefixes)
        cat = random.choice(intl_categories)
        num = random.randint(100, 9999)
        suffix = random.choice(["", "M", "R", "A"])
        standards.append((f"{prefix} {num}{suffix}", "国际标准"))

    return standards

def generate_materials():
    """生成500条材料数据"""
    materials = []
    all_materials = []
    for cat, info in CATEGORIES.items():
        for mat in info["materials"]:
            all_materials.append((cat, mat))

    # 先加入所有预定义材料
    for cat, (name, area, (y_min, y_max), (d_min, d_max)) in all_materials:
        y = random.randint(y_min, y_max)
        d = round(random.uniform(d_min, d_max), 2)
        materials.append((name, cat, area, y, d))

    # 补充到500条 - 通过变体生成
    variants = [
        "高强型", "耐热型", "耐蚀型", "细晶型", "锻造型", "铸造型", "轧制型", "挤压型",
        "退火态", "固溶态", "时效态", "淬火态", "调质态", "正火态",
    ]
    areas = ["航空航天", "船舶海工", "石油化工", "机械制造", "电子信息", "医疗器械", "建筑工程", "电力设备", "核工业", "汽车工业"]

    while len(materials) < 500:
        cat, (base_name, base_area, (y_min, y_max), (d_min, d_max)) = random.choice(all_materials)
        variant = random.choice(variants)
        area = random.choice(areas)
        # 变体的性能略有波动
        y = random.randint(max(y_min - 50, 10), y_max + 50)
        d = round(random.uniform(max(d_min - 0.1, 0.5), d_max + 0.1), 2)
        name = f"{base_name}-{variant}"
        materials.append((name, cat, area, y, d))

    random.shuffle(materials)
    return materials[:500]

def generate_suppliers():
    """生成100条供应商数据"""
    suppliers = list(SUPPLIERS_BASE)
    extra_focus = ["材料制造", "材料研发", "材料检测", "材料应用", "稀土材料", "复合材料"]
    extra_locations = [
        "北京", "上海", "天津", "重庆", "沈阳", "大连", "哈尔滨", "长春",
        "济南", "青岛", "南京", "苏州", "杭州", "宁波", "合肥", "福州",
        "厦门", "南昌", "武汉", "长沙", "广州", "深圳", "成都", "西安",
        "兰州", "贵阳", "昆明", "太原", "石家庄", "呼和浩特",
    ]
    extra_types = [
        "科技有限公司", "股份有限公司", "集团有限公司", "研究院", "有限责任公司",
        "技术有限公司", "新材料有限公司", "精密合金有限公司",
    ]
    while len(suppliers) < 100:
        loc = random.choice(extra_locations)
        focus = random.choice(extra_focus)
        typ = random.choice(extra_types)
        name = f"{loc}{random.choice(['鑫达', '华创', '恒远', '博远', '精工', '盛达', '永兴', '中创', '科达', '国盛'])}{typ}"
        suppliers.append((name, focus))
    return suppliers[:100]

def generate_documents(materials):
    """生成200条文档数据"""
    documents = []
    doc_templates = [
        ("{mat}力学性能测试报告", "测试报告"),
        ("{mat}化学成分分析报告", "测试报告"),
        ("{mat}金相组织检验报告", "测试报告"),
        ("{mat}无损检测报告", "测试报告"),
        ("{mat}腐蚀试验报告", "测试报告"),
        ("{mat}高温持久试验报告", "测试报告"),
        ("{mat}疲劳性能测试报告", "测试报告"),
        ("GB/T {num}-{year} {cat}技术条件", "PDF国标"),
        ("GJB {num}-{year} {cat}规范", "PDF国标"),
        ("ASTM {num} {cat}标准", "PDF国标"),
        ("AMS {num} {cat}规范", "PDF国标"),
        ("{mat}制备工艺研究报告", "研究论文"),
        ("{mat}微观组织与性能关系研究", "研究论文"),
        ("{mat}热处理工艺优化研究", "研究论文"),
        ("{mat}焊接工艺评定报告", "工艺规范"),
        ("{mat}铸造工艺规程", "工艺规范"),
        ("{mat}锻造工艺规程", "工艺规范"),
        ("{mat}热处理工艺规程", "工艺规范"),
        ("{mat}入厂检验规程", "检验规程"),
        ("{mat}出厂检验规程", "检验规程"),
        ("{mat}质量一致性检验规定", "质量标准"),
        ("{mat}采购技术条件", "技术条件"),
        ("{mat}设计许用值手册", "设计手册"),
        ("{mat}选材指南", "设计手册"),
    ]

    for i in range(200):
        mat = random.choice(materials)
        mat_name = mat[0]
        cat = mat[1]
        template, doc_type = random.choice(doc_templates)
        title = template.format(
            mat=mat_name, cat=cat,
            num=random.randint(100, 9999),
            year=random.choice([2015, 2018, 2020, 2021, 2022, 2023, 2024]),
        )
        source = random.choice(DOC_SOURCES)
        # related_material_id 对应 materials 列表的索引+1
        mat_id = materials.index(mat) + 1
        documents.append((title[:200], doc_type, source, mat_id))

    return documents

def generate_sql():
    materials = generate_materials()
    suppliers = generate_suppliers()
    standards = generate_standards()
    documents = generate_documents(materials)

    lines = []
    lines.append("-- ==========================================")
    lines.append("-- 材料管理系统数据扩充脚本")
    lines.append("-- 生成时间: 2026-06-10")
    lines.append("-- ==========================================")
    lines.append("")
    lines.append("USE dmma;")
    lines.append("")

    # Step 1: 备份
    lines.append("-- ==========================================")
    lines.append("-- Step 1: 备份原始数据")
    lines.append("-- ==========================================")
    lines.append("CREATE TABLE IF NOT EXISTS dmma_materials_bak AS SELECT * FROM dmma_materials;")
    lines.append("CREATE TABLE IF NOT EXISTS dmma_standards_bak AS SELECT * FROM dmma_standards;")
    lines.append("CREATE TABLE IF NOT EXISTS dmma_suppliers_bak AS SELECT * FROM dmma_suppliers;")
    lines.append("CREATE TABLE IF NOT EXISTS dmma_documents_bak AS SELECT * FROM dmma_documents;")
    lines.append("")
    lines.append("SELECT '备份完成' AS status;")
    lines.append("")

    # Step 2: 清空并重置自增ID
    lines.append("-- ==========================================")
    lines.append("-- Step 2: 清空表并重置自增ID")
    lines.append("-- ==========================================")
    lines.append("TRUNCATE TABLE dmma_documents;")
    lines.append("TRUNCATE TABLE dmma_standards;")
    lines.append("TRUNCATE TABLE dmma_materials;")
    lines.append("TRUNCATE TABLE dmma_suppliers;")
    lines.append("")

    # Step 3: 供应商 (100条)
    lines.append("-- ==========================================")
    lines.append("-- Step 3: 插入供应商 (100条)")
    lines.append("-- ==========================================")
    for i in range(0, len(suppliers), 20):
        batch = suppliers[i:i+20]
        values = ",\n".join(f"('{s[0]}', '{s[1]}')" for s in batch)
        lines.append(f"INSERT INTO dmma_suppliers (supplier_name, main_focus) VALUES\n{values};")
    lines.append("")

    # Step 4: 材料 (500条)
    lines.append("-- ==========================================")
    lines.append("-- Step 4: 插入材料 (500条)")
    lines.append("-- ==========================================")
    for i in range(0, len(materials), 20):
        batch = materials[i:i+20]
        values = ",\n".join(f"('{m[0]}', '{m[1]}', '{m[2]}', {m[3]}, {m[4]})" for m in batch)
        lines.append(f"INSERT INTO dmma_materials (name, category, application_area, yield_strength, density) VALUES\n{values};")
    lines.append("")

    # Step 5: 标准 (100条) - 每条标准关联到随机材料
    lines.append("-- ==========================================")
    lines.append("-- Step 5: 插入标准 (100条)")
    lines.append("-- ==========================================")
    std_values = []
    for s in standards:
        mat_id = random.randint(1, len(materials))
        std_values.append(f"({mat_id}, '{s[0]}', '{s[1]}')")
    for i in range(0, len(std_values), 20):
        batch = std_values[i:i+20]
        values = ",\n".join(batch)
        lines.append(f"INSERT INTO dmma_standards (material_id, standard_code, system_type) VALUES\n{values};")
    lines.append("")

    # Step 6: 文档 (200条)
    lines.append("-- ==========================================")
    lines.append("-- Step 6: 插入文档 (200条)")
    lines.append("-- ==========================================")
    for i in range(0, len(documents), 20):
        batch = documents[i:i+20]
        values = ",\n".join(f"('{d[0]}', '{d[1]}', '{d[2]}', {d[3]})" for d in batch)
        lines.append(f"INSERT INTO dmma_documents (title, document_type, source, related_material_id) VALUES\n{values};")
    lines.append("")

    # 验证
    lines.append("-- ==========================================")
    lines.append("-- Step 7: 验证数据")
    lines.append("-- ==========================================")
    lines.append("SELECT 'dmma_suppliers' AS `表名`, COUNT(*) AS `记录数` FROM dmma_suppliers")
    lines.append("UNION ALL")
    lines.append("SELECT 'dmma_materials', COUNT(*) FROM dmma_materials")
    lines.append("UNION ALL")
    lines.append("SELECT 'dmma_standards', COUNT(*) FROM dmma_standards")
    lines.append("UNION ALL")
    lines.append("SELECT 'dmma_documents', COUNT(*) FROM dmma_documents;")
    lines.append("")
    lines.append("-- 材料分类统计")
    lines.append("SELECT category AS `材料类别`, COUNT(*) AS `数量` FROM dmma_materials GROUP BY category ORDER BY `数量` DESC;")
    lines.append("")
    lines.append("-- 应用领域统计")
    lines.append("SELECT application_area AS `应用领域`, COUNT(*) AS `数量` FROM dmma_materials GROUP BY application_area ORDER BY `数量` DESC;")

    return "\n".join(lines)

if __name__ == "__main__":
    sql = generate_sql()
    with open("D:/vsqt/vscode_files/test3/expand_data.sql", "w", encoding="utf-8") as f:
        f.write(sql)
    print(f"SQL脚本已生成: expand_data.sql")
    print(f"共生成:")
    materials = generate_materials()
    suppliers = generate_suppliers()
    standards = generate_standards()
    documents = generate_documents(materials)
    print(f"  供应商: {len(suppliers)} 条")
    print(f"  材料:   {len(materials)} 条")
    print(f"  标准:   {len(standards)} 条")
    print(f"  文档:   {len(documents)} 条")
