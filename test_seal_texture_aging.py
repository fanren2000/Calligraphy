import cv2
import numpy as np
from PIL import Image, ImageFilter
from PIL import Image, ImageDraw, ImageFont
from Utils import safe_get_font
import random
import math

from Calli_Utils import add_four_character_seal

def create_basic_seal(text, size=400, border_width=10):
    # 创建红色背景
    img = Image.new('RGBA', (size, size), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制方形边框
    margin = 20
    draw.rectangle([margin, margin, size-margin, size-margin], 
                   outline=(200, 0, 0, 255), width=border_width)
    
    # 添加文字（这里需要中文字体）
    try:
        font = ImageFont.truetype("simsun.ttc", size//4)
    except:
        font = ImageFont.load_default()
    
    # 在印章中心添加文字
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill=(200, 0, 0, 255), font=font)
    
    return img

# 创建基础印章
seal = create_basic_seal("印")
seal.save("basic_seal.png")

def add_texture_and_aging(img, intensity=0.3):
    """添加纹理和老化效果"""
    width, height = img.size
    pixels = img.load()
    
    for i in range(width):
        for j in range(height):
            r, g, b, a = pixels[i, j]
            
            # 只处理非透明像素
            if a > 0:
                # 添加随机噪点模拟纹理
                if random.random() < intensity:
                    variation = random.randint(-20, 20)
                    r = max(0, min(255, r + variation))
                
                # 模拟墨水不均匀
                if random.random() < intensity/2:
                    a = max(0, min(255, a - random.randint(0, 30)))
                
                pixels[i, j] = (r, g, b, a)
    
    return img

# 应用质感效果
textured_seal = add_texture_and_aging(seal)
textured_seal.save("textured_seal.png")

def create_circular_seal(text, size=400):
    """创建圆形闲章"""
    img = Image.new('RGBA', (size, size), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制圆形边框
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 outline=(200, 0, 0, 255), width=10)
    
    # 添加弧形文字
    try:
        font = ImageFont.truetype("simsun.ttc", size//6)
    except:
        font = ImageFont.load_default()
    
    # 将文字沿圆形排列（简化版）
    chars = list(text)
    char_count = len(chars)
    radius = size // 2 - 40
    
    for i, char in enumerate(chars):
        angle = 2 * math.pi * i / char_count - math.pi/2
        x = size // 2 + radius * math.cos(angle) - 10
        y = size // 2 + radius * math.sin(angle) - 10
        
        # 旋转文字以适应圆形
        char_img = Image.new('RGBA', (30, 30), (255, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((0, 0), char, fill=(200, 0, 0, 255), font=font)
        
        rotated_char = char_img.rotate(math.degrees(angle) + 90, expand=True)
        img.paste(rotated_char, (int(x), int(y)), rotated_char)
    
    return img

# 创建圆形闲章
circular_seal = create_circular_seal("闲情逸致")
circular_seal.save("circular_seal.png")

def enhance_with_opencv(pil_img):
    """使用OpenCV增强质感"""
    # 转换为OpenCV格式
    cv_img = np.array(pil_img)
    
    # 添加高斯模糊模拟墨水扩散
    blurred = cv2.GaussianBlur(cv_img, (3, 3), 0)
    
    # 添加噪声
    noise = np.random.randint(-10, 10, cv_img.shape, dtype=np.int16)
    noisy_img = np.clip(cv_img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # 混合原图和噪声图
    alpha = 0.7
    enhanced = cv2.addWeighted(blurred, alpha, noisy_img, 1-alpha, 0)
    
    return Image.fromarray(enhanced)

# 应用OpenCV增强
enhanced_seal = enhance_with_opencv(textured_seal)
enhanced_seal.save("enhanced_seal.png")

def create_realistic_seal(text, seal_type="square", size=400):
    """创建具有质感的印章"""
    
    if seal_type == "square":
        img = create_basic_seal(text, size)
    else:  # circular
        img = create_circular_seal(text, size)
    
    # 添加纹理
    img = add_texture_and_aging(img)
    
    # 添加模糊效果模拟墨水扩散
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # 增强对比度
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    return img

# 创建最终效果的印章
image = Image.new('RGB', (1000, 600), (255, 255, 255))
draw = ImageDraw.Draw(image)

# realistic_seal = create_realistic_seal("金石之章", "circle")    # "square")
realistic_seal = add_four_character_seal(image, "它山之玉", (10, 10))
realistic_seal.save("realistic_seal.png")