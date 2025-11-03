import cv2
from PIL import Image, ImageFilter
from PIL import Image, ImageDraw, ImageFont
from Utils import safe_get_font
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

def add_seal_with_text_penetration_wrong(image, text, position, size=120, opacity=0.7):
    """真实的压款印效果 - 文字穿透，可调节透明度"""
    
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # 🎯 步骤1: 先保存下款文字区域
    x, y = position
    square_size = size

     # 🎯 修复1: 先保存原文字区域（在添加印章之前）
    original_region = image.crop((x, y, x + square_size, y + square_size))
    original_array = np.array(original_region)
    
    # 提取印章区域的文字内容
    seal_region = image.crop((x, y, x + square_size, y + square_size))
    
    # 🎯 步骤2: 创建印章图层
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal_layer)
    
    # 🎯 使用 opacity 参数控制透明度
    bg_alpha = int(255 * opacity)  # 背景透明度
    border_alpha = int(255 * min(1.0, opacity + 0.3))  # 边框稍深
    text_alpha = 255  # 印章文字不透明
    
    # 绘制半透明印章背景
    seal_bg_color = (180, 30, 30, bg_alpha)
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_bg_color)
    
    # 绘制印章边框
    border_color = (150, 20, 20, border_alpha)
    draw.rectangle([x, y, x + square_size, y + square_size], 
                  outline=border_color, width=3)
    
    # 🎯 步骤3: 添加印章文字（不透明）
    try:
        font = safe_get_font("simkai.ttf", square_size // 3)        # 方圆印章篆体
    except:
        font = ImageFont.load_default()
    
    if len(text) == 4:
        chars = list(text)
        cell_size = square_size // 2
        font_offset = calculate_font_offset(font, chars[0], square_size, "印章篆体")
        
        positions = [
            (x + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size // 2, y + cell_size + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size + cell_size // 2 + font_offset)
        ]
        
        for i, (center_x, center_y) in enumerate(positions):
            char_bbox = draw.textbbox((0, 0), chars[i], font=font)
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3] - char_bbox[1]
            char_x = center_x - char_width // 2
            char_y = center_y - char_height // 2
            draw.text((char_x, char_y), chars[i], font=font, fill=(255, 255, 255, text_alpha))
    
    # 🎯 步骤4: 合成 - 先印章后恢复部分文字
    result = Image.alpha_composite(image, seal_layer)
    
    # 🎯 步骤5: 让部分文字穿透显示（根据透明度调整穿透程度）
    result_array = np.array(result)
    seal_region_array = np.array(seal_region)
    
    # 🎯 根据 opacity 调整文字穿透强度
    # opacity 越高，文字穿透越弱；opacity 越低，文字穿透越强
    text_penetration_strength = 1.0 - opacity  # 反向关系
    
     # 在印章区域内应用文字穿透
    for i in range(square_size):
        for j in range(square_size):
            px, py = x + i, y + j
            if 0 <= px < result_array.shape[1] and 0 <= py < result_array.shape[0]:
                # 获取原图的文字颜色
                original_r, original_g, original_b, original_a = original_array[j, i]
                
                # 🎯 修复3: 更精确的文字检测
                # 检测深色文字（黑色或深灰色）
                is_dark_text = (original_r < 80 and original_g < 80 and original_b < 80)
                
                if is_dark_text:
                    # 🎯 修复4: 更自然的混合算法
                    blend_ratio = 0.6 * text_penetration_strength
                    
                    # 当前合成后的颜色
                    current_r, current_g, current_b, current_a = result_array[py, px]
                    
                    # 混合原文字颜色和当前颜色
                    # 让原文字部分穿透印章红色背景
                    final_r = int(current_r * (1 - blend_ratio) + original_r * blend_ratio)
                    final_g = int(current_g * (1 - blend_ratio) + original_g * blend_ratio)
                    final_b = int(current_b * (1 - blend_ratio) + original_b * blend_ratio)
                    
                    result_array[py, px] = (final_r, final_g, final_b, 255)
    
    result = Image.fromarray(result_array)
    print(f"✅ 修复版压款印完成 - 透明度: {opacity}")
    return result

def add_seal_with_text_penetration_fixed(image, text, position, size=120, opacity=0.7):
    """修复透明度问题的真实压款印效果"""
    
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    x, y = position
    square_size = size
    
    # 🎯 修复1: 先保存原文字区域（在添加印章之前）
    original_region = image.crop((x, y, x + square_size, y + square_size))
    original_array = np.array(original_region)
    
    # 🎯 步骤2: 创建印章图层
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal_layer)
    
    # 🎯 关键修复：使用与工作函数相同的透明度基准
    base_alpha = 120  # 与工作函数相同的基准值
    bg_alpha = int(base_alpha * opacity)
    border_alpha = 255  # 边框固定不透明，与工作函数一致
    text_alpha = 255

    print(f"🎯 透明度计算: base_alpha={base_alpha}, opacity={opacity} -> bg_alpha={bg_alpha}")

    # 绘制半透明印章背景
    seal_bg_color = (180, 30, 30, bg_alpha)
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_bg_color)
    
    # 绘制印章边框（固定不透明）
    border_color = (150, 20, 20, border_alpha)
    draw.rectangle([x, y, x + square_size, y + square_size], 
                  outline=border_color, width=3)
    
    # 添加印章文字
    try:
        font = safe_get_font("方圆印章篆体.ttf", square_size // 3)
    except:
        font = ImageFont.load_default()
    
    if len(text) == 4:
        chars = list(text)
        cell_size = square_size // 2
        font_offset = calculate_font_offset(font, chars[0], square_size, "印章篆体")
        
        positions = [
            (x + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size // 2, y + cell_size + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size + cell_size // 2 + font_offset)
        ]
        
        for i, (center_x, center_y) in enumerate(positions):
            # char_bbox = draw.textbbox((0, 0), chars[i], font=font)
            # char_width = char_bbox[2] - char_bbox[0]
            # char_height = char_bbox[3] - char_bbox[1]
            char_x = center_x - 2 // 2
            char_y = center_y - 8 // 2
            draw.text((char_x, char_y), chars[i], font=font, fill=(255, 255, 255, text_alpha))
    
    # 🎯 步骤4: 合成印章到原图
    result = Image.alpha_composite(image, seal_layer)
    result_array = np.array(result)
    
    # 🎯 修复2: 改进的文字穿透逻辑
    text_penetration_strength = 1.0 - opacity
    
    # 在印章区域内应用文字穿透
    for i in range(square_size):
        for j in range(square_size):
            px, py = x + i, y + j
            if 0 <= px < result_array.shape[1] and 0 <= py < result_array.shape[0]:
                # 获取原图的文字颜色
                original_r, original_g, original_b, original_a = original_array[j, i]
                
                # 🎯 修复3: 更精确的文字检测
                # 检测深色文字（黑色或深灰色）
                is_dark_text = (original_r < 80 and original_g < 80 and original_b < 80)
                
                if is_dark_text:
                    # 🎯 修复4: 更自然的混合算法
                    blend_ratio = 0.6 * text_penetration_strength
                    
                    # 当前合成后的颜色
                    current_r, current_g, current_b, current_a = result_array[py, px]
                    
                    # 混合原文字颜色和当前颜色
                    # 让原文字部分穿透印章红色背景
                    final_r = int(current_r * (1 - blend_ratio) + original_r * blend_ratio)
                    final_g = int(current_g * (1 - blend_ratio) + original_g * blend_ratio)
                    final_b = int(current_b * (1 - blend_ratio) + original_b * blend_ratio)
                    
                    result_array[py, px] = (final_r, final_g, final_b, 255)
    
    result = Image.fromarray(result_array)
    print(f"✅ 修复版压款印完成 - 透明度: {opacity}")
    return result

def add_seal_with_text_penetration(image, text, position, size=120, opacity=0.7):
    """在工作函数基础上添加透明度参数"""
    
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # 创建印章图层
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal_layer)
    
    x, y = position
    square_size = size

    # 🎯 将硬编码透明度改为基于参数
    base_alpha = 200  # 原来的硬编码值
    dynamic_alpha = int(base_alpha * opacity)
    
    seal_bg_color = (200, 50, 50, dynamic_alpha)    # 动态透明度背景
    border_color = (150, 20, 20, 255)               # 不透明边框
    text_color = (255, 255, 255, 255)               # 不透明文字

    print(f"🎯 动态透明度: opacity={opacity} * {base_alpha} = {dynamic_alpha}")

    # 绘制半透明背景
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_bg_color)
    
    # 绘制不透明边框
    draw.rectangle([x, y, x + square_size, y + square_size], outline=border_color, width=3)
    
    # 绘制不透明文字
    try:
        font = safe_get_font("方圆印章篆体.ttf", square_size // 3)
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
            char_x = char_x - 2 // 2
            char_y = char_y + 60 // 2
            draw.text((char_x, char_y), chars[i], fill=text_color, font=font)
    
    # 合成
    result = Image.alpha_composite(image, seal_layer)
    print(f"✅ 增强版半透明印章完成 - 透明度: {opacity}")
    return result

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

