import cv2
from PIL import Image, ImageFilter
from PIL import Image, ImageDraw, ImageFont
from Utils import safe_get_font
import random
import os


def add_four_character_seal(image, text, position, size=120, intensity=0.3, style='aged'):
    """创建四字方形印章（2x2排列，文字居中），支持 aged 或 clean 风格"""
    #image = image.convert("RGBA")
    draw = ImageDraw.Draw(image)
    pixels = image.load()

    seal_color = (180, 30, 30)
    border_color = (150, 20, 20)
    white_color = (255, 255, 255)

    x, y = position
    square_size = size

    # 绘制外边框
    draw.rectangle([
        x - 4, y - 4,
        x + square_size + 4, y + square_size + 4
    ], outline=border_color, width=3)

    # 绘制印章主体
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_color)

    # 加载字体
    try:
        seal_font = safe_get_font("方圆印章篆体.ttf", square_size // 3)
    except:
        seal_font = ImageFont.load_default()

    # 2x2排列四个字
    if len(text) == 4:
        chars = list(text)
        cell_size = square_size // 2
        font_offset = calculate_font_offset(seal_font, chars[0], square_size, "印章篆体")

        centers = [
            (x + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size // 2, y + cell_size + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size + cell_size // 2 + font_offset)
        ]

        for i, (center_x, center_y) in enumerate(centers):
            char_bbox = draw.textbbox((0, 0), chars[i], font=seal_font)
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3] - char_bbox[1]
            char_x = center_x - char_width // 2
            char_y = center_y - char_height // 2
            draw.text((char_x, char_y), chars[i], font=seal_font, fill=white_color)

    # 🎨 添加印章区域的老化纹理
    if style == 'aged':
        for i in range(x, x + square_size):
            for j in range(y, y + square_size):
                r, g, b, a = pixels[i, j]

                # 添加随机噪点模拟纹理
                if random.random() < intensity:
                    variation = random.randint(-20, 20)
                    r = max(0, min(255, r + variation))
                    g = max(0, min(255, g + variation))
                    b = max(0, min(255, b + variation))

                # 模拟墨水不均匀
                if random.random() < intensity / 2:
                    a = max(0, min(255, a - random.randint(0, 30)))

                pixels[i, j] = (r, g, b, a)

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

