from PIL import Image, ImageDraw, ImageFont
from Utils.font_tools import safe_get_font
import random
import os

def add_four_character_seal(image, text, position, size=120):
    """创建四字方形印章（2x2排列，文字居中）"""
    draw = ImageDraw.Draw(image)
    
    # 印章颜色
    seal_color = (180, 30, 30)
    border_color = (150, 20, 20)
    white_color = (255, 255, 255)
    
    x, y = position
    
    # 确保是正方形
    square_size = size
    
    # 绘制外边框
    draw.rectangle([
        x - 4, y - 4,
        x + square_size + 4, y + square_size + 4
    ], outline=border_color, width=3)
    
    # 绘制印章主体（正方形）
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_color)
    
    # 加载字体
    try:
        seal_font = safe_get_font("方圆印章篆体.ttf", square_size // 3)
    except:
        seal_font = ImageFont.load_default()
    
    # 2x2排列四个字，确保居中
    if len(text) == 4:
        chars = list(text)
        cell_size = square_size // 2
        
         # 测试字体偏移量（针对篆体特殊调整）
        font_offset = calculate_font_offset(seal_font, chars[0], square_size, "印章篆体")
        
        centers = [
            (x + cell_size // 2, y + cell_size // 2 + font_offset),      # 上
            (x + cell_size + cell_size // 2, y + cell_size // 2 + font_offset),  # 官
            (x + cell_size // 2, y + cell_size + cell_size // 2 + font_offset),  # 婉
            (x + cell_size + cell_size // 2, y + cell_size + cell_size // 2 + font_offset)  # 儿
        ]
        
        for i, (center_x, center_y) in enumerate(centers):
            char_bbox = draw.textbbox((0, 0), chars[i], font=seal_font)
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3] - char_bbox[1]
            
            char_x = center_x - char_width // 2
            char_y = center_y - char_height // 2
            
            draw.text((char_x, char_y), chars[i], font=seal_font, fill=white_color)
    
    return image


def calculate_font_offset(font, sample_char, square_size, font_name):
    """计算字体特定的垂直偏移量"""
    # 创建测试图像来计算字体偏移
    test_img = Image.new('RGB', (100, 100), (255, 255, 255))
    test_draw = ImageDraw.Draw(test_img)
    
    bbox = test_draw.textbbox((0, 0), sample_char, font=font)
    char_height = bbox[3] - bbox[1]
    
    # 篆体通常需要向下偏移
    if "篆" in font_name or "印" in font_name:
        return square_size // 4  # 篆体向下偏移25%
    else:
        return 0

