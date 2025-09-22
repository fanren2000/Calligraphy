from PIL import Image, ImageDraw, ImageFont
from Utils.font_tools import safe_get_font
from Calli_Utils.seal_border_fancy_4char import add_four_character_seal
import random
import os


def create_real_vertical_poem():
    """生成真正的竖排《彩书怨》"""
    
    image = Image.new('RGB', (1600, 800), (245, 235, 215))
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    try:
        font = ImageFont.truetype("simkai.ttf", 50)
        small_font = ImageFont.truetype("simkai.ttf", 30)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 《彩书怨》全文（每个字单独）
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
    
    # 竖排参数：从右向左，从上到下
    start_x = 1200  # 从右侧开始
    start_y = 200  # 从顶部开始
    char_spacing = 60  # 字间距（垂直）
    line_spacing = 60  # 行间距（水平）
    
    # 绘制竖排诗文（8列，每列5个字）
    for col in range(8):  # 8句诗
        for row in range(5):  # 每句5个字
            char_index = col * 5 + row
            if char_index < len(poem_chars):
                char = poem_chars[char_index]
                char_x = start_x - col * line_spacing
                char_y = start_y + row * char_spacing
                draw.text((char_x, char_y), char, font=font, fill=(0, 0, 0))
    
    # 添加标题"彩书怨"（竖排在右侧）
    title_chars = ["彩", "书", "怨"]
    title_x = start_x + 80  # 诗句右侧
    for i, char in enumerate(title_chars):
        draw.text((title_x, start_y + i * char_spacing), char, font=font, fill=(0, 0, 0))
    
    # 添加作者"上官婉儿"（竖排在标题右侧）
    author_chars = ["上", "官", "婉", "儿"]
    author_x = title_x + 60
    author_y = 600
    for i, char in enumerate(author_chars):
        draw.text((author_x, start_y + i * char_spacing), char, font=small_font, fill=(0, 0, 0))
    
    # 添加印章（在作者旁边）
    # 使用修正后的印章函数
    seal_x = author_x - 120
    seal_y = author_y - 15
    image = add_four_character_seal(image, "玻璃耗子", (seal_x, seal_y), 100)
    
    image.save("真正竖排格式.png", quality=95)
    print("生成完成：真正竖排格式.png")
    print("布局：传统竖排，从右向左，从上到下")
    
    return image

if __name__ == "__main__":
    create_real_vertical_poem()