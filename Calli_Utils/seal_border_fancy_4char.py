import cv2
from PIL import Image, ImageFilter
from PIL import Image, ImageDraw, ImageFont
from Utils import safe_get_font
from config import PAPER_COLORS
import random
import os
import numpy as np


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

def add_seal_transparent(image, text, position, size=120):
    """最简单的半透明印章"""
    
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # 创建印章图层
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal_layer)
    
    x, y = position
    square_size = size

    # 🎯 完全不透明的边框和文字，半透明的背景
    seal_bg_color = (180, 30, 30, 120)    # 半透明背景
    border_color = (150, 20, 20, 255)     # 不透明边框
    text_color = (255, 255, 255, 255)     # 不透明文字

    # 绘制半透明背景
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_bg_color)
    
    # 绘制不透明边框
    draw.rectangle([x, y, x + square_size, y + square_size], outline=border_color, width=3)
    
    # 绘制不透明文字
    try:
        font = safe_get_font("方圆印章篆体.ttf", square_size // 3)        # 方圆印章篆体
        # font = ImageFont.truetype("simkai.ttf", square_size // 3)
    except:
        font = ImageFont.load_default()
    
    if len(text) == 4:
        chars = list(text)
        cell_size = square_size // 2
        
        positions = [
            (x + 10, y + 10),
            (x + cell_size + 10, y + 10),
            (x + 10, y + cell_size + 10),
            (x + cell_size + 10, y + cell_size + 10)
        ]
        
        for i, (char_x, char_y) in enumerate(positions):
            draw.text((char_x, char_y), chars[i], fill=text_color, font=font)
    
    # 合成
    result = Image.alpha_composite(image, seal_layer)
    print(f"✅ 简单半透明印章完成")
    return result

def add_seal_with_text_penetration(image, text, position, size=120, opacity=0.7, style="aged", intensity=0.6):
    """在工作函数基础上添加透明度参数"""
    
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    pixels = image.load()    
    
    # 创建印章图层
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal_layer)
    
    x, y = position
    square_size = size
    border_width = 3

    # 🎯 将硬编码透明度改为基于参数
    base_alpha = 255  # 原来的硬编码值
    dynamic_alpha = int(base_alpha * opacity)
    
    seal_bg_color = (200, 50, 50, dynamic_alpha)    # 动态透明度背景
    border_color = (150, 20, 20, dynamic_alpha)               # 不透明边框
    text_color = PAPER_COLORS.get("xuan") + (dynamic_alpha,)     # 透明文字

    print(f"🎯 动态透明度: opacity={opacity} * {base_alpha} = {dynamic_alpha}")

    # 绘制外边框
    draw.rectangle([
        x - 4, y - 4,
        x + square_size + 4, y + square_size + 4
    ], outline=border_color, width=3)

    # 绘制半透明背景
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_bg_color)
    
    # 绘制不透明边框
    # draw.rectangle([x, y, x + square_size, y + square_size], outline=border_color, width=border_width)

    # 在背景内部绘制边框
    # internal_border = border_width
    # draw.rectangle([x + internal_border, y + internal_border, 
    #                x + size - internal_border, y + size - internal_border], 
    #               outline=border_color, width=border_width)
    
    # 绘制不透明文字
    try:
        font = safe_get_font("方圆印章篆体.ttf", square_size // 3)
    except:
        font = ImageFont.load_default()
    
    if len(text) == 4:
        chars = list(text)
        cell_size = square_size // 2
        font_offset = square_size // 4
        positions = [
            (x + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size // 2, y + cell_size + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size + cell_size // 2 + font_offset)
        ]
        
        # 微调篆体字水平位置(测试经验值）：
        char_zhuanti_x_offside = 5
        for i, (pos_x, pos_y) in enumerate(positions):
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            char_x = pos_x - font_offset // 2 - char_zhuanti_x_offside       # - text_width // 2
            char_y = pos_y - text_height // 2 
            draw.text((char_x, char_y), chars[i], fill=text_color, font=font)

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
        
    
    # 合成
    result = Image.alpha_composite(image, seal_layer)
    print(f"✅ 增强版半透明印章完成 - 透明度: {opacity}")

    return result

def calculate_font_offset(font, sample_char, square_size, font_name):
    # 篆体通常需要向下偏移
    if "篆" in font_name or "印" in font_name:
        return square_size // 4  # 篆体向下偏移25%
    else:
        return 0

