import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math
import time
from datetime import datetime
from zhdate import ZhDate

# ==================== 基础工具函数 ====================

def create_authentic_torn_paper(paper_size="small_xuan", paper_type="xuan", tear_intensity=0.4):
    """创建撕边宣纸背景（简化版）"""
    width, height = (800, 300) if paper_size == "small_xuan" else (1000, 400)
    
    # 创建基础纸张
    if paper_type == "xuan":
        base_color = (248, 240, 228)
    else:
        base_color = (250, 235, 215)
    
    paper = Image.new('RGB', (width, height), base_color)
    return paper

def create_test_image():
    """创建测试书法图像"""
    paper = Image.new('RGB', (400, 200), (248, 240, 228))
    draw = ImageDraw.Draw(paper)
    
    try:
        font = ImageFont.truetype("simkai.ttf", 48)
    except:
        try:
            font = ImageFont.truetype("simsun.ttc", 48)
        except:
            font = ImageFont.load_default()
    
    draw.text((120, 70), "测试文字", fill=(30, 30, 30), font=font)
    return paper

# ==================== 横幅创建函数 ====================

def create_traditional_banner(text_chars, paper_size=(1000, 300)):
    """创建传统从右到左的横幅"""
    if len(text_chars) != 4:
        raise ValueError("横幅应为四个汉字")
    
    # 创建宣纸背景
    paper = create_authentic_torn_paper("handscroll", "xuan", 0.2)
    paper = paper.resize(paper_size)
    
    draw = ImageDraw.Draw(paper)
    
    try:
        # 尝试加载书法字体
        font = ImageFont.truetype("simkai.ttf", 120)
    except:
        try:
            font = ImageFont.truetype("simsun.ttc", 120)
        except:
            font = ImageFont.load_default()
    
    width, height = paper_size
    
    # 传统从右到左布局
    char_width = width // 5
    start_x = width - char_width
    
    print("📜 传统横幅布局（从右到左）:")
    
    for i, char in enumerate(text_chars):
        x_pos = start_x - i * char_width
        y_pos = height // 2 - 60
        
        print(f"  位置 {i+1}: '{char}' at ({x_pos}, {y_pos})")
        draw.text((x_pos, y_pos), char, fill=(30, 30, 30), font=font)
    
    return paper

def create_modern_banner(text_chars, paper_size=(1000, 300)):
    """创建现代从左到右的横幅"""
    paper = create_authentic_torn_paper("handscroll", "xuan", 0.2)
    paper = paper.resize(paper_size)
    
    draw = ImageDraw.Draw(paper)
    
    try:
        font = ImageFont.truetype("simkai.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    width, height = paper_size
    
    # 现代从左到右布局
    char_width = width // 5
    start_x = char_width
    
    print("🏙️ 现代横幅布局（从左到右）:")
    
    for i, char in enumerate(text_chars):
        x_pos = start_x + i * char_width
        y_pos = height // 2 - 60
        
        print(f"  位置 {i+1}: '{char}' at ({x_pos}, {y_pos})")
        draw.text((x_pos, y_pos), char, fill=(30, 30, 30), font=font)
    
    return paper

# ==================== 落款系统 ====================

def add_upper_inscription(image, recipient_name, honorific="先生", humble_word="雅正"):
    """为书法作品添加上款"""
    upper_text = f"{recipient_name}{honorific}{humble_word}"
    
    print(f"🎁 添加上款: {upper_text}")
    
    width, height = image.size
    upper_x = width - 200
    upper_y = 80
    
    upper_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(upper_layer)
    
    try:
        upper_font = ImageFont.truetype("simkai.ttf", 28)
    except:
        upper_font = ImageFont.load_default()
    
    draw.text((upper_x, upper_y), upper_text, fill=(60, 60, 60, 220), font=upper_font)
    result = Image.alpha_composite(image.convert('RGBA'), upper_layer)
    
    return result

def add_banner_signature(banner, layout="traditional", author_name="某某"):
    """添加横幅下款"""
    width, height = banner.size
    draw = ImageDraw.Draw(banner)
    
    try:
        small_font = ImageFont.truetype("simkai.ttf", 24)
    except:
        small_font = ImageFont.load_default()
    
    # 根据布局决定落款位置
    if layout == "traditional":
        signature_x = width // 10
        signature_y = height - 60
        signature_text = f"{author_name}书"
    else:
        signature_x = width - 150
        signature_y = height - 60
        signature_text = f"{author_name}书"
    
    draw.text((signature_x, signature_y), signature_text, 
              fill=(80, 80, 80), font=small_font)
    
    print(f"  下款位置: ({signature_x}, {signature_y}) - '{signature_text}'")
    
    return banner

def get_vertical_lunar_date(include_shu=True, include_author=None, include_season=False):
    """获取竖排农历日期 - 修正季节逻辑"""
    today = datetime.now()
    lunar = ZhDate.from_datetime(today)
    
    # 天干地支
    heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    year_index = (lunar.lunar_year - 4) % 60
    stem_char = heavenly_stems[year_index % 10]
    branch_char = earthly_branches[year_index % 12]
    
    # 农历月份
    lunar_months = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
    month_char = lunar_months[lunar.lunar_month - 1]
    
    # 农历日期
    lunar_days = {
        1: "初一", 2: "初二", 3: "初三", 4: "初四", 5: "初五", 6: "初六", 7: "初七", 8: "初八", 9: "初九", 10: "初十",
        11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五", 16: "十六", 17: "十七", 18: "十八", 19: "十九", 20: "二十",
        21: "廿一", 22: "廿二", 23: "廿三", 24: "廿四", 25: "廿五", 26: "廿六", 27: "廿七", 28: "廿八", 29: "廿九", 30: "三十"
    }
    
    day_text = lunar_days.get(lunar.lunar_day, "初一")
    
    # 季节映射（基于农历月份）
    def get_season_by_lunar_month(lunar_month):
        season_mapping = {
            1: "孟春",  2: "仲春",  3: "季春",
            4: "孟夏",  5: "仲夏",  6: "季夏", 
            7: "孟秋",  8: "仲秋",  9: "季秋",
            10: "孟冬", 11: "仲冬", 12: "季冬"
        }
        return season_mapping.get(lunar_month, "")
    
    # 构建基础部分
    date_parts = [
        ["岁"], ["次"], [stem_char], [branch_char], ["年"]
    ]
    
    # 🎯 修正：确保季节功能正常工作
    if include_season:
        # 使用季节模式：只显示季节
        season_text = get_season_by_lunar_month(lunar.lunar_month)
        print(f"🔍 调试信息: lunar_month={lunar.lunar_month}, season_text='{season_text}'")
        
        if season_text and len(season_text) == 2:
            date_parts.append([season_text[0]])  # 孟/仲/季
            date_parts.append([season_text[1]])  # 春/夏/秋/冬
            print(f"✅ 成功添加季节: {season_text}")
        else:
            print(f"❌ 季节获取失败，回退到传统模式")
            # 回退到传统模式
            date_parts.extend([
                [month_char], ["月"], [day_text[0]]
            ])
            if len(day_text) > 1 and day_text[1].strip():
                date_parts.append([day_text[1]])
    else:
        # 传统模式：显示具体月份和日期
        date_parts.extend([
            [month_char], ["月"], [day_text[0]]
        ])
        if len(day_text) > 1 and day_text[1].strip():
            date_parts.append([day_text[1]])
    
    # 添加作者（如果提供）
    if include_author:
        for char in include_author:
            date_parts.append([char])
    
    # 添加"书"字
    if include_shu:
        date_parts.append(["书"])
    
    # 打印最终结果
    final_text = "".join([part[0] for part in date_parts])
    print(f"📅 最终输出: {final_text}")
    
    return date_parts


# 修改后的落款函数
def add_vertical_lower_inscription(image, author_name="某某", include_date=True, 
                                  layout="traditional", columns=2, location=None,
                                  include_season=False):
    """修正版竖排下款 - 正确的季节逻辑"""
    
    # 生成下款内容
    inscription_parts = []
    
    # 🎯 根据列数组织内容
    if columns == 1:
        # 单列：作者 + 书
        inscription_parts.append([author_name, "书"])
        
    elif columns == 2:
        # 双列：时间 + 作者+书
        if include_date:
            date_data = get_vertical_lunar_date(include_shu=False, include_author=None, include_season=include_season)
            date_text = [part[0] for part in date_data if part[0].strip()]
            inscription_parts.append(date_text)
        
        # 修正：将作者名字拆分为单个字符
        author_chars = list(author_name) + ["书"]
        inscription_parts.append(author_chars)
        
    elif columns >= 3:
        # 三列：时间 + 地点 + 作者+书
        if include_date:
            date_data = get_vertical_lunar_date(include_shu=False, include_author=None, include_season=include_season)
            date_text = [part[0] for part in date_data if part[0].strip()]
            inscription_parts.append(date_text)
        
        if location:
            location_chars = ["于"] + list(location)
            inscription_parts.append(location_chars)
        else:
            inscription_parts.append(["记"])
        
        author_chars = list(author_name) + ["书"]
        inscription_parts.append(author_chars)
    
    print(f"📝 添加竖排下款 ({columns}列):")
    for i, column in enumerate(inscription_parts):
        print(f"   第{i+1}列: {''.join(column)}")
    
    width, height = image.size
    
    # 🎯 根据布局决定起始位置
    if layout == "traditional":
        start_x = 60
    else:
        start_x = width - 80
    
    lower_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(lower_layer)
    
    try:
        lower_font = ImageFont.truetype("simkai.ttf", 22)
    except:
        lower_font = ImageFont.load_default()
    
    column_spacing = 35
    start_y = height - 250
    
    for col_index, column_text in enumerate(inscription_parts):
        current_x = start_x + col_index * column_spacing
        
        for row_index, char in enumerate(column_text):
            draw.text((current_x, start_y + row_index * 30), char, 
                     fill=(60, 60, 60, 220), font=lower_font)
    
    result = Image.alpha_composite(image.convert('RGBA'), lower_layer)
    return result

def add_special_lower_inscription(image, author_name, purpose_text, 
                                       include_date=True, layout="traditional"):
    """
    专门为您的需求定制的三列下款
    """
    
    # 🎯 组织三列内容
    columns = []
    
    # 第一列：日期
    if include_date:
        date_data = get_vertical_lunar_date(include_shu=False)
        date_text = [part[0] for part in date_data if part[0].strip()]
        columns.append(date_text)
    else:
        # 如果没有日期，第一列可以为空或简单标记
        columns.append(["记"])
    
    # 第二列：书写目的（精简处理）
    purpose_short = shorten_purpose_text(purpose_text)
    purpose_columns = split_purpose_text(purpose_short, max_chars_per_column=10)
    
    # 如果目的文本不长，放在一列
    if len(purpose_columns) == 1:
        columns.append(purpose_columns[0])
    else:
        # 如果目的文本较长，分成两列
        columns.extend(purpose_columns)
        # 调整作者列为第四列
        author_text = list(author_name) + ["书"]
        columns.append(author_text)
    
    # 第三列：作者+书（如果目的只有一列）
    if len(columns) == 2:
        author_chars = list(author_name) + ["书"]
        columns.append(author_chars)
    
    print(f"📝 定制三列下款:")
    for i, column in enumerate(columns):
        print(f"   第{i+1}列: {''.join(column)}")
    
    width, height = image.size
    
    # 根据布局决定位置
    if layout == "traditional":
        start_x = 60   # 左侧
    else:
        start_x = width - 80 - (len(columns) * 35)  # 右侧
    
    inscription_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(inscription_layer)
    
    try:
        font = ImageFont.truetype("simkai.ttf", 22)
    except:
        font = ImageFont.load_default()
    
    # 分列绘制
    column_spacing = 35
    
    for col_index, column_text in enumerate(columns):
        current_x = start_x + col_index * column_spacing
        column_height = len(column_text) * 30
        current_y = height - 40 - column_height
        
        for row_index, char in enumerate(column_text):
            draw.text((current_x, current_y + row_index * 30), char, 
                     fill=(60, 60, 60, 220), font=font)
    
    result = Image.alpha_composite(image.convert('RGBA'), inscription_layer)
    return result

def shorten_purpose_text(purpose_text):
    """精简书写目的文本"""
    
    # 常见精简规则
    shortening_rules = {
        "为清华大学校庆120年": "贺清华百廿华诞",
        "为清华大学120周年校庆": "贺清华双甲子", 
        "庆祝清华大学建校120年": "庆清华百廿庆典",
        "为清华百廿年校庆": "贺清华百廿",
        "清华大学120年校庆": "清华百廿庆"
    }
    
    # 直接匹配
    if purpose_text in shortening_rules:
        return shortening_rules[purpose_text]
    
    # 智能精简
    short_text = purpose_text
    short_text = short_text.replace("清华大学", "清华")
    short_text = short_text.replace("校庆", "庆")
    short_text = short_text.replace("120", "百廿")
    short_text = short_text.replace("120周年", "百廿")
    short_text = short_text.replace("为", "贺")
    short_text = short_text.replace("庆祝", "庆")
    
    # 确保以贺/庆/祝开头
    if not any(short_text.startswith(prefix) for prefix in ["贺", "庆", "祝", "颂"]):
        short_text = "贺" + short_text
    
    return short_text

def split_purpose_text(purpose_text, max_chars_per_column=4):
    """分割目的文本到多列"""
    
    if len(purpose_text) <= max_chars_per_column:
        return [list(purpose_text)]
    
    # 智能分割：尽量在语义边界分割
    text = purpose_text
    
    # 尝试在常见字后分割
    split_positions = []
    for split_char in ["贺", "庆", "祝", "于", "为"]:
        if split_char in text[1:]:  # 不在第一个字
            pos = text.index(split_char, 1)
            split_positions.append(pos)
    
    if split_positions:
        split_pos = min(split_positions)
        return [list(text[:split_pos]), list(text[split_pos:])]
    else:
        # 平均分割
        mid_point = len(text) // 2
        return [list(text[:mid_point]), list(text[mid_point:])]

def add_vertical_upper_inscription(image, recipient_name, honorific="先生", humble_word="雅正", layout="traditional"):
    """修正版竖排上款 - 支持不同布局"""
    upper_text = f"{recipient_name}{honorific}{humble_word}"
    
    print(f"🎁 添加竖排上款 ({layout}布局): {upper_text}")
    
    width, height = image.size
    
    # 🎯 根据布局微调位置
    if layout == "traditional":
        # 传统布局：右侧上方
        upper_x = width - 80
        upper_y = 60
        position_desc = "右侧上方"
    else:
        # 现代布局：左侧上方
        upper_x = 60
        upper_y = 60  
        position_desc = "左侧上方"
    
    print(f"   位置: {position_desc} ({upper_x}, {upper_y})")
    
    upper_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(upper_layer)
    
    try:
        upper_font = ImageFont.truetype("simkai.ttf", 24)
    except:
        upper_font = ImageFont.load_default()
    
    # 竖排绘制
    for i, char in enumerate(upper_text):
        draw.text((upper_x, upper_y + i * 30), char, 
                 fill=(60, 60, 60, 220), font=upper_font)
    
    result = Image.alpha_composite(image.convert('RGBA'), upper_layer)
    return result

def explain_lower_inscription_columns():
    """解释下款分列规则"""
    
    print("=== 下款分列规则 ===\n")
    
    column_rules = {
        "单列下款": {
            "内容": "作者名 + 书",
            "字数": "2-4字",
            "适用": "极简风格、空间有限",
            "示例": "张书法"
        },
        "双列下款": {
            "内容": "时间 + 作者 + 书",
            "字数": "5-8字", 
            "适用": "标准格式、最常见",
            "示例": "甲辰年仲春\n张书法书"
        },
        "三列下款": {
            "内容": "时间 + 地点 + 作者 + 书",
            "字数": "8-12字",
            "适用": "详细记录、重要作品",
            "示例": "岁次甲辰\n于北京\n张书法书"
        },
        "分列原则": {
            "内容分组": "时间、地点、作者信息分开",
            "字数均衡": "每列2-4字，避免过长",
            "阅读顺序": "从右到左，从上到下",
            "视觉平衡": "各列长度相近"
        }
    }
    
    for category, info in column_rules.items():
        print(f"📝 {category}:")
        if isinstance(info, dict):
            for key, value in info.items():
                print(f"   {key}: {value}")
        else:
            print(f"   {info}")
        print()



def create_correct_traditional_banner(text_chars, paper_size=(1000, 300)):
    """正确的传统横幅 - 横排但从右到左"""
    
    if len(text_chars) != 4:
        raise ValueError("横幅应为四个汉字")
    
    # 创建宣纸背景
    paper = create_authentic_torn_paper("handscroll", "xuan", 0.2)
    paper = paper.resize(paper_size)
    
    draw = ImageDraw.Draw(paper)
    
    try:
        # 主体文字用较大字体
        main_font = ImageFont.truetype("simkai.ttf", 120)
    except:
        main_font = ImageFont.load_default()
    
    width, height = paper_size
    
    # 🎯 正确的从右到左排列逻辑
    total_chars = len(text_chars)
    char_width = width // (total_chars + 2)  # 留出边距
    total_text_width = char_width * total_chars
    
    # 起始位置：从右侧开始，但要居中
    start_x = (width - total_text_width) // 2 + total_text_width - char_width
    
    print("📜 传统横幅正确格式:")
    print(f"   文字顺序: {' → '.join(text_chars[::-1])} (从右到左阅读)")
    print(f"   布局参数: 总宽={width}, 字宽={char_width}, 起始X={start_x}")
    
    # 🎯 正确的传统排列：从右到左
    for i, char in enumerate(text_chars):
        # 从右向左递减
        x_pos = start_x - (i * char_width)
        y_pos = height // 2 - 60
        
        print(f"   第{i}字 '{char}': x={x_pos}")
        draw.text((x_pos, y_pos), char, fill=(30, 30, 30), font=main_font)
    
    return paper

def get_precise_font_metrics(font, test_char="汉"):
    """获取精确的字体度量"""
    try:
        # 方法1：使用getbbox（包含边距）
        bbox = font.getbbox(test_char)
        full_width = bbox[2] - bbox[0]
        full_height = bbox[3] - bbox[1]
        
        # 方法2：使用getmetrics获取基线信息
        ascent, descent = font.getmetrics()
        actual_height = ascent + descent
        
        print(f"📐 字体度量信息:")
        print(f"   getbbox 尺寸: {full_width} x {full_height}")
        print(f"   getmetrics 高度: {actual_height} (ascent={ascent}, descent={descent})")
        
        return {
            'full_width': full_width,
            'full_height': full_height,
            'actual_height': actual_height,
            'ascent': ascent,
            'descent': descent
        }
    except:
        # 备用方案
        bbox = font.getbbox(test_char)
        return {
            'full_width': bbox[2] - bbox[0],
            'full_height': bbox[3] - bbox[1],
            'actual_height': bbox[3] - bbox[1],
            'ascent': (bbox[3] - bbox[1]) * 0.8,  # 估算
            'descent': (bbox[3] - bbox[1]) * 0.2
        }

# 在您的代码中使用
main_font = ImageFont.truetype("ShanHaiBoYaGuLiW-2.ttf", 240)
metrics = get_precise_font_metrics(main_font, "汉")

char_width = metrics['full_width']
char_height = metrics['actual_height']  # 使用实际高度，而不是包含边距的高度

def create_perfectly_centered_banner(text_chars, paper_size=(1000, 300)):
    """修正垂直居中的横幅"""
    
    paper = create_authentic_torn_paper("handscroll", "xuan", 0.2)
    paper = paper.resize(paper_size)
    draw = ImageDraw.Draw(paper)
    
    width, height = paper_size
    
    main_font = ImageFont.truetype("ShanHaiBoYaGuLiW-2.ttf", 280)
    
    # 获取精确的字体度量
    metrics = get_precise_font_metrics(main_font, "汉")
    char_width = metrics['full_width']
    actual_char_height = metrics['actual_height']
    ascent = metrics['ascent']
    
    # 🎯 关键修正：正确的垂直居中
    total_chars = len(text_chars)
    # 计算隶属的字间距
    spacing = get_lishu_spacing(char_width, "traditional")
    total_width = (char_width * total_chars) + (spacing * (total_chars - 1))
    
    # 水平居中
    start_x = (width - total_width) / 2
    
    # 🎯 垂直居中修正：考虑基线位置
    # 传统方法：start_y = (height - char_height) / 2  ← 这是错误的！
    # 正确方法：
    start_y = (height - actual_char_height) / 2 - metrics['descent'] * 0.5
    
    print(f"🎯 修正后的布局参数:")
    print(f"   字体实际高度: {actual_char_height}")
    print(f"   字体总高度: {metrics['full_height']}")
    print(f"   上边距(ascent): {ascent}")
    print(f"   下边距(descent): {metrics['descent']}")
    print(f"   起始Y坐标: {start_y}")
    
    # 绘制文字（从右到左）
    for i, char in enumerate(text_chars):
        traditional_index = total_chars - 1 - i
        x_pos = start_x + traditional_index * (char_width + spacing)
        
        draw.text((x_pos, start_y), char, fill=(30, 30, 30), font=main_font)
        print(f"   '{char}' 位置: ({x_pos:.1f}, {start_y:.1f})")
    
    return paper

def get_lishu_spacing(char_width, style="traditional"):
    """获取隶书专用字间距"""
    
    if style == "traditional":
        # 传统隶书：非常紧凑，字距约为字宽的10-15%
        return char_width * 0.12
    elif style == "modern":
        # 现代隶书：稍宽松，字距约为字宽的15-20%
        return char_width * 0.18
    elif style == "decorative":
        # 装饰性隶书：更宽松，字距约为字宽的20-25%
        return char_width * 0.22
    else:
        # 默认：适中
        return char_width * 0.15



# ==================== 墨迹渗透效果 ====================

def add_ink_bleed_effect_fixed(image, intensity=0.3, image_mode="RGBA"):
    """修复版墨迹渗透效果"""
    width, height = image.size

    bleed_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bleed_layer)

    gray_image = image.convert('L')

    # 根据强度调整参数
    bleed_range = max(1, int(3 * intensity))
    max_alpha = int(80 * intensity)
    min_alpha = int(20 * intensity)
    
    print(f"[墨迹渗透] 强度:{intensity}, 范围:{bleed_range}, Alpha:{min_alpha}-{max_alpha}")

    for x in range(0, width, 2):
        for y in range(0, height, 2):
            if gray_image.getpixel((x, y)) < 100:
                bleed_count = max(1, int(5 * intensity))
                
                for _ in range(bleed_count):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.randint(1, bleed_range)
                    
                    nx = int(x + distance * math.cos(angle))
                    ny = int(y + distance * math.sin(angle))
                    
                    if 0 <= nx < width and 0 <= ny < height:
                        alpha = random.randint(min_alpha, max_alpha)
                        radius = random.randint(1, 2)
                        
                        draw.ellipse((nx - radius, ny - radius, nx + radius, ny + radius),
                                    fill=(0, 0, 0, alpha))

    # 根据强度调整模糊程度
    blur_radius = 0.5 + intensity * 1.0
    bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(blur_radius))

    base_rgba = image.convert('RGBA')
    result = Image.alpha_composite(base_rgba, bleed_layer)

    if image_mode == "RGB":
        return result.convert('RGB')
    else:
        return result

# ==================== 完整作品创建函数 ====================

def create_complete_banner(text, layout="traditional", 
                          paper_size=(1500, 500),  # 🆕 纸张尺寸参数
                          add_upper=False, recipient_info=None,
                          add_ink_bleed=False, ink_intensity=0.3,
                          author_name="某某", include_date=True):
    """
    完整书法横幅创建函数 - 支持自定义纸张尺寸
    
    Args:
        text: 四个汉字
        layout: "traditional" 或 "modern"
        paper_size: (width, height) 元组，纸张尺寸 🆕
        add_upper: 是否添加上款
        recipient_info: 受赠人信息
        add_ink_bleed: 是否添加墨迹渗透
        ink_intensity: 墨迹强度
        author_name: 作者姓名
        include_date: 是否包含日期
    """
    
    if len(text) != 4:
        raise ValueError("请提供四个汉字")
    
    text_chars = list(text)
    width, height = paper_size
    
    print(f"=== 创建{layout}风格横幅: {text} ===")
    print(f"📐 纸张尺寸: {width} × {height} 像素 (比例: {width/height:.1f}:1)")
    
    # 创建基础横幅
    if layout == "traditional":
        banner = create_perfectly_centered_banner(text_chars, paper_size)
        print("🎋 传统布局: 横排主体 + 竖排落款")
    else:
        banner = create_modern_banner(text_chars, paper_size)
        print("🏙️ 现代布局: 横排主体 + 竖排落款")
    
    # 添加竖排上款
    if add_upper and recipient_info:
        banner = add_vertical_upper_inscription(
            banner, 
            recipient_info['name'],
            recipient_info.get('honorific', '先生'),
            recipient_info.get('humble_word', '雅正'),
            layout=layout
        )
    
    # 添加竖排下款
    banner = add_special_lower_inscription(
        banner, 
        author_name, 
        "颂舞者健美肱肌",
        include_date,
        layout=layout,
        
    )
    
    # 添加墨迹渗透效果
    if add_ink_bleed:
        banner = add_ink_bleed_effect_fixed(banner, ink_intensity)
        print(f"🎨 添加墨迹渗透效果，强度: {ink_intensity}")
    
    return banner
# ==================== 预设配置 ====================

def create_banner_presets():
    """创建横幅预设配置"""
    
    presets = {
        "traditional_formal": {
            "description": "传统正式横幅",
            "params": {
                "layout": "traditional",
                "add_upper": True,
                "add_ink_bleed": True,
                "ink_intensity": 0.2
            }
        },
        "modern_artistic": {
            "description": "现代艺术横幅", 
            "params": {
                "layout": "modern",
                "add_upper": False,
                "add_ink_bleed": True,
                "ink_intensity": 0.5
            }
        },
        "minimalist": {
            "description": "极简风格横幅",
            "params": {
                "layout": "traditional", 
                "add_upper": False,
                "add_ink_bleed": False
            }
        }
    }
    
    return presets

def apply_banner_preset(text, preset_name="traditional_formal", **kwargs):
    """应用横幅预设"""
    presets = create_banner_presets()
    
    if preset_name not in presets:
        print(f"预设 '{preset_name}' 不存在，使用传统预设")
        preset_name = "traditional_formal"
    
    preset = presets[preset_name]
    print(f"应用预设: {preset_name} - {preset['description']}")
    
    # 合并参数
    params = {**preset['params'], **kwargs}
    
    return create_complete_banner(text, **params)

def usage_guide():
    """使用指南"""
    
    print("=== 四字横幅系统使用指南 ===\n")
    
    guide = {
        "基础使用": [
            "create_complete_banner('厚德载物') - 最简单用法",
            "create_complete_banner('宁静致远', layout='modern') - 现代布局",
            "create_complete_banner('天道酬勤', add_ink_bleed=True) - 带墨迹效果"
        ],
        "高级功能": [
            "添加上款: add_upper=True + recipient_info参数",
            "墨迹渗透: add_ink_bleed=True + ink_intensity控制强度", 
            "作者署名: author_name参数设置下款",
            "预设系统: apply_banner_preset()快速应用配置"
        ],
        "参数说明": {
            "text": "四个汉字，如'厚德载物'",
            "layout": "'traditional'传统或'modern'现代",
            "add_upper": "是否添加上款",
            "recipient_info": "受赠人信息字典",
            "add_ink_bleed": "是否添加墨迹渗透", 
            "ink_intensity": "墨迹强度0.1-1.0",
            "author_name": "下款作者姓名"
        }
    }
    
    for category, content in guide.items():
        print(f"📖 {category}:")
        if isinstance(content, list):
            for item in content:
                print(f"   • {item}")
        else:
            for key, value in content.items():
                print(f"   {key}: {value}")
        print()

# 运行指南
# usage_guide()

def demo_all_banner_types():
    """演示所有横幅类型"""
    
    print("=== 四字横幅完整演示 ===\n")
    
    # 示例1: 传统正式横幅
    print("1. 🎋 传统正式横幅")
    traditional_banner = create_complete_banner(
        text="厚德载物",
        layout="traditional",
        add_upper=True,
        recipient_info={"name": "王明", "honorific": "先生", "humble_word": "雅正"},
        add_ink_bleed=True,
        ink_intensity=0.3,
        author_name="张书法"
    )
    traditional_banner.save("banner_traditional_formal.png")
    print("   ✅ 保存: banner_traditional_formal.png\n")
    
    # 示例2: 现代艺术横幅
    print("2. 🏙️ 现代艺术横幅")
    modern_banner = create_complete_banner(
        text="宁静致远", 
        layout="modern",
        add_upper=False,
        add_ink_bleed=True,
        ink_intensity=0.6,
        author_name="李艺术"
    )
    modern_banner.save("banner_modern_artistic.png")
    print("   ✅ 保存: banner_modern_artistic.png\n")
    
    # 示例3: 极简风格
    print("3. ⚪ 极简风格横幅")
    minimal_banner = create_complete_banner(
        text="天道酬勤",
        layout="traditional",
        add_upper=False,
        add_ink_bleed=False,
        author_name="简书"
    )
    minimal_banner.save("banner_minimalist.png")
    print("   ✅ 保存: banner_minimalist.png\n")
    
    # 示例4: 使用预设
    print("4. 🎯 使用预设配置")
    preset_banner = apply_banner_preset(
        "海纳百川",
        "traditional_formal",
        recipient_info={"name": "李老师", "honorific": "老师", "humble_word": "教正"},
        author_name="王学生"
    )
    preset_banner.save("banner_preset.png")
    print("   ✅ 保存: banner_preset.png\n")

def demo_ink_bleed_effects():
    """演示不同墨迹渗透效果"""
    
    print("=== 墨迹渗透效果演示 ===\n")
    
    test_text = "水墨丹青"
    
    intensities = [0.1, 0.3, 0.6, 0.9]
    
    for intensity in intensities:
        print(f"🎨 墨迹强度: {intensity}")
        banner = create_complete_banner(
            text=test_text,
            layout="traditional",
            add_ink_bleed=True,
            ink_intensity=intensity,
            author_name="墨客"
        )
        banner.save(f"ink_bleed_{intensity}.png")
        print(f"   ✅ 保存: ink_bleed_{intensity}.png")
    
    print()

def demo_different_layouts():
    """演示不同布局"""
    
    print("=== 布局风格演示 ===\n")
    
    test_text = "风华正茂"
    
    # 传统布局
    traditional = create_complete_banner(
        text=test_text,
        layout="traditional", 
        add_upper=True,
        recipient_info={"name": "老王", "honorific": "教授", "humble_word": "指正"},
        author_name="传统书家"
    )
    traditional.save("layout_traditional.png")
    print("🎋 传统布局: layout_traditional.png")
    
    # 现代布局
    modern = create_complete_banner(
        text=test_text,
        layout="modern",
        author_name="现代书家"  
    )
    modern.save("layout_modern.png")
    print("🏙️ 现代布局: layout_modern.png")

def quick_start_example():
    """快速开始示例"""
    
    print("=== 快速开始示例 ===\n")
    
    # 最简单的使用方式
    # print("🚀 最简单用法:")
    # simple_banner = create_complete_banner("吉祥如意")
    # simple_banner.save("banner_simple.png")
    # print("   创建: banner_simple.png")
    
    # # 带效果的用法
    # print("\n🎨 带效果用法:")
    # effect_banner = create_complete_banner(
    #     "福寿安康",
    #     add_ink_bleed=True,
    #     ink_intensity=0.4
    # )
    # effect_banner.save("banner_with_effects.png")
    # print("   创建: banner_with_effects.png")
    
    # 完整用法的用法
    print("\n💎 完整用法:")
    complete_banner = create_complete_banner(
        "氣勢如肱",         # "气势如肱",
        layout="traditional",
        add_upper=True, 
        recipient_info={"name": "任真儿", "honorific": "主播", "humble_word": "雅正"},
        add_ink_bleed=True,
        ink_intensity=0.3,
        author_name="玻璃耗子"
    )
    complete_banner.save("banner_complete.png")
    print("   创建: banner_complete.png")

# ==================== 主函数 ====================

if __name__ == "__main__":
    print("四字横幅创作系统")
    print("=" * 50)
    
    # 演示所有功能
    # demo_all_banner_types()
    # demo_ink_bleed_effects() 
    # demo_different_layouts()
    quick_start_example()
    
    print("\n🎉 所有演示完成！")
    print("生成的PNG文件包含:")
    print("  • 不同风格的横幅布局")
    print("  • 不同强度的墨迹效果") 
    print("  • 完整的上下款系统")
    print("  • 预设配置应用")