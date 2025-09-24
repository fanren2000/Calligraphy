from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from datetime import datetime
from zhdate import ZhDate
import random

from Calli_Utils import (
    add_circular_seal_with_rotation,
    add_circular_seal_visual_debug,
    add_four_character_seal,
    add_xuan_paper_texture,
    add_ink_bleed_effect
)

def create_correct_vertical_poem():
    """修正后的竖排书法：正确尺寸 + 农历日期 + 传统落款顺序"""
    
    # 正确尺寸：高 > 宽（立轴式）
    # image = Image.new('RGB', (1400, 700), (245, 235, 215))  # 宽700, 高1400
    # create an image and defer color decisions
    width, height = 1400, 700
    image = Image.new('RGB', (width, height), (245, 235, 215))
    
    # 使用宣纸
    texture_intensity=0.85
    image = add_xuan_paper_texture(image, texture_intensity, False)

    image.save("debug_xuan_image.png")

    draw = ImageDraw.Draw(image)

    
    
    # 加载字体
    try:
        poem_font = ImageFont.truetype("simkai.ttf", 55)
        title_font = ImageFont.truetype("simkai.ttf", 75)
        note_font = ImageFont.truetype("simkai.ttf", 28)
    except:
        poem_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        note_font = ImageFont.load_default()
    
    # 《彩书怨》全文
    poem_chars = [
        "叶", "下", "洞", "庭", "初",
        "思", "君", "万", "里", "余",
        "露", "浓", "香", "被", "冷", 
        "月", "落", "锦", "屏", "虚",
        "欲", "奏", "江", "南", "曲",
        "贪", "封", "蓟", "北", "书",
        "书", "中", "无", "别", "意",
        "惟", "怅", "久", "离", "居"
    ]
    
    # 竖排布局参数
    poem_start_x = 1100  # 诗文起始位置
    poem_start_y = 200  # 诗文顶部位置
    char_spacing = 60   # 字间距
    line_spacing = 60   # 行间距
    
    # 绘制竖排诗文
    for col in range(8):
        for row in range(5):
            char_index = col * 5 + row
            if char_index < len(poem_chars):
                char_x = poem_start_x - col * line_spacing
                char_y = poem_start_y + row * char_spacing
                draw.text((char_x, char_y), poem_chars[char_index], font=poem_font, fill=(0, 0, 0))
    
    # 添加标题（诗文右侧）
    title_chars = ["彩", "书", "怨"]
    title_x = poem_start_x + 80
    for i, char in enumerate(title_chars):
        draw.text((title_x, poem_start_y + i * char_spacing), char, font=title_font, fill=(0, 0, 0))
    
    # ==================== 传统落款区域 ====================
    author_column_x = 300  # 作者名列
    date_column_x = author_column_x - 50    # 日期列（作者名左侧）
    base_y = 300           # 基准高度
    
    # 1. 作者名（左列）
    author_chars = list("玻璃耗子")
    for i, char in enumerate(author_chars):
        draw.text((author_column_x, base_y + i * 35), char, font=note_font, fill=(0, 0, 0))
    
    # 2. 日期（右列，与作者名纵向对齐）
    lunar_date_chars = get_correct_vertical_lunar_date()
    date_start_y = base_y  # 与作者名顶部对齐
    
    for row_index, column_chars in enumerate(lunar_date_chars):
        for col_index, char in enumerate(column_chars):
            if char:
                draw.text((date_column_x + col_index * 35, date_start_y + row_index * 35), 
                         char, font=note_font, fill=(80, 80, 80))

    date_end_y = date_start_y + (row_index + 1) * 35    # 计算日期底部变量以使闲章与它对其           
    
    # 3. 印章（在作者名左侧上方）
    seal_x = author_column_x - 200
    seal_y = base_y - 30  # 略高于作者名
    image = add_four_character_seal(image, "玻璃耗子", (seal_x, seal_y), 100)
    
    # 4. 添加闲章或题跋（底部）
    # 4. 闲章（左下角）
    # note_chars = ["唐", "宫", "遗", "韵"]
    note_diameter = 100
    note_center_ratio = 0.3
    note_char_rotation_degree = 25
    note_text = "耗气长存"
    note_x = seal_x + note_diameter // 2    # 圆形的半径
    note_y = date_end_y - note_diameter // 2    # 圆形的半径
    image = add_circular_seal_with_rotation(image, note_text, (note_x, note_y), note_diameter, note_center_ratio, note_char_rotation_degree)

    
    
    # 增加墨迹渗透效果
    bleed_intensity=0.15
    image = add_ink_bleed_effect(image, bleed_intensity)

    

    
    image.save("传统竖排书法_宣纸_测试.png", quality=95)
    print("生成完成：传统竖排书法.png")
    print("包含：正确尺寸 + 农历日期 + 传统落款顺序")
    
    return image

def get_lunar_date():
    """获取传统农历日期"""
    today = datetime.now()
    lunar = ZhDate.from_datetime(today)
    
    # 天干地支纪年
    heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    year_index = (lunar.lunar_year - 4) % 60  # 从甲子年开始
    stem_index = year_index % 10
    branch_index = year_index % 12
    
    year_name = f"{heavenly_stems[stem_index]}{earthly_branches[branch_index]}"
    
    # 农历月份
    lunar_months = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
    month_name = lunar_months[lunar.lunar_month - 1]
    
    
    # 农历日期
    lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                 "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                 "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    
    day_name = lunar_days[lunar.lunar_day - 1]
    
    return [
        f"岁次{year_name}年",
        f"{month_name}{day_name}"
    ]

def get_vertical_lunar_date():
    """获取竖排农历日期（每个字单独一行）"""
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
    lunar_days = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
                 "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                 "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    
    day_char = lunar_days[lunar.lunar_day - 1]
    
    # 竖排格式：每列一个字
    return [
        ["岁"],  # 第一列
        ["次"],  # 第二列  
        [stem_char],  # 天干
        [branch_char],  # 地支
        ["年"],  # 年
        [month_char],  # 月
        [day_char]   # 日
    ]

def get_correct_vertical_lunar_date():
    """获取正确的竖排农历日期（数字保持完整竖排）"""
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
    
    # 农历日期（保持完整数字）
    lunar_days = {
        1: "初一", 2: "初二", 3: "初三", 4: "初四", 5: "初五", 6: "初六", 7: "初七", 8: "初八", 9: "初九", 10: "初十",
        11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五", 16: "十六", 17: "十七", 18: "十八", 19: "十九", 20: "二十",
        21: "廿一", 22: "廿二", 23: "廿三", 24: "廿四", 25: "廿五", 26: "廿六", 27: "廿七", 28: "廿八", 29: "廿九", 30: "三十"
    }
    
    day_text = lunar_days.get(lunar.lunar_day, "初一")
    
    # 正确的竖排格式：每列包含完整的文字
    # 例如："三十"应该在一列中竖排显示，而不是拆成"三"和"十"两列
    # 正确的竖排格式：月份永远包含"月"字
    return [
        ["岁"],          # 第一列
        ["次"],          # 第二列
        [stem_char],     # 第三列：天干
        [branch_char],   # 第四列：地支
        ["年"],          # 第五列
        [month_char],    # 第六列：月份数字
        ["月"],          # 第七列："月"字（永远显示）
        [day_text[0]],   # 第八列：日期第一部分
        [day_text[1]] if len(day_text) > 1 else [""]  # 第九列：日期第二部分
    ]

# 传统落款顺序示例函数
def show_traditional_order():
    """展示传统落款顺序"""
    print("传统书法落款顺序：")
    print("1. 📝 先写作者姓名（右下角或左下角）")
    print("2. 📅 再写创作时间（作者下方）")
    print("3. 🔴 最后盖章（落款左侧或上方）")
    print("4. 🎨 闲章（作品起首或右下角）")
    print("")
    print("现代常见格式：")
    print("作者名 + 时间 → 盖章在上方")
    print("或：时间 + 作者名 → 盖章在左侧")

if __name__ == "__main__":
    # 显示落款顺序说明
    show_traditional_order()
    print("")
    
    # 生成作品
    create_correct_vertical_poem()