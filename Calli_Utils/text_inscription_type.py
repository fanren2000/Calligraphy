from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

from Utils.date_format_tools import get_vertical_lunar_date

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
        upper_font = ImageFont.truetype("华文行楷.ttf", 24)
    except:
        upper_font = ImageFont.load_default()
    
    # 竖排绘制
    for i, char in enumerate(upper_text):
        draw.text((upper_x, upper_y + i * 30), char, 
                 fill=(60, 60, 60, 220), font=upper_font)
    
    result = Image.alpha_composite(image.convert('RGBA'), upper_layer)
    return result

def add_special_upper_inscription(image, inscription_text, layout="traditional"):
    # """竖排上款 - 上款由参数输入"""
   
    print(f"🎁 添加竖排上款 ({layout}布局): {inscription_text}")
    
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
        upper_font = ImageFont.truetype("华文行楷.ttf", 24)
    except:
        upper_font = ImageFont.load_default()
    
    # 竖排绘制
    for i, char in enumerate(inscription_text):
        draw.text((upper_x, upper_y + i * 30), char, 
                 fill=(60, 60, 60, 220), font=upper_font)
    
    result = Image.alpha_composite(image.convert('RGBA'), upper_layer)
    return result

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
                                       include_date=True, layout="traditional", bottom_margin = 140):
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
    # purpose_short = shorten_purpose_text(purpose_text)
    purpose_short = purpose_text
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
        start_x = 80   # 左侧
    else:
        start_x = width - 80 - (len(columns) * 35)  # 右侧
    
    inscription_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(inscription_layer)
    
    try:
        font = ImageFont.truetype("华文行楷.ttf", 22)
    except:
        font = ImageFont.load_default()
    
    # 分列绘制
    column_spacing = 35
    
    for col_index, column_text in enumerate(columns):
        current_x = start_x + col_index * column_spacing
        column_height = len(column_text) * 30
        current_y = height - bottom_margin - column_height
        
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



