from PIL import Image, ImageDraw, ImageFilter
import random
import math
import numpy as np

def add_ink_bleed_effect(image, intensity=0.3):
    """添加墨迹渗透效果（宣纸特有），使用透明叠加模拟墨迹扩散"""
    width, height = image.size

    # 创建透明渗透层
    bleed_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bleed_layer)

    # 灰度图用于识别文字区域
    gray_image = image.convert('L')

    for x in range(width):
        for y in range(height):
            if gray_image.getpixel((x, y)) < 100:  # 深色区域（文字）
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if random.random() < intensity:
                                radius = random.randint(1, 3)
                                alpha = random.randint(10, 40)
                                draw.ellipse((nx - radius, ny - radius, nx + radius, ny + radius),
                                             fill=(0, 0, 0, alpha))

    # 模糊渗透层
    bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(1.5))

    # 确保原图为 RGBA 模式
    base_rgba = image.convert('RGBA')

    # 应用渗透叠加
    result = Image.alpha_composite(base_rgba, bleed_layer)

    return result.convert('RGB')

import numpy as np
from PIL import Image, ImageFilter

import numpy as np
from PIL import Image, ImageFilter

def add_ink_bleed_effect_enhanced(image, intensity=1.0, vertical_soak=True, speckle=True, preserve_characters=True):
    """墨迹渗透增强版：方向性渗透 + 笔压模拟 + 噪点 + 保留文字清晰度"""
    width, height = image.size
    img_array = np.array(image)
    gray = np.mean(img_array, axis=2)

    # 创建文字掩码（深色区域）
    char_mask = (gray < 100)
    mask = char_mask.astype(np.uint8) * 255
    mask_img = Image.fromarray(mask)

    # 🧭 方向性渗透（垂直扩散）
    if vertical_soak:
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=0.5))  # horizontal softness
        mask_img = mask_img.filter(ImageFilter.BoxBlur(3))                # vertical soak
    else:
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=3))    # symmetric bleed

    # 🖌️ 笔压模拟：根据灰度深浅调整渗透强度
    blur_mask = np.array(mask_img) / 255.0
    pressure_map = (100 - np.clip(gray, 0, 100)) / 100.0  # 0.0 to 1.0
    bleed_strength = blur_mask * pressure_map * intensity * 80
    darken = bleed_strength.astype(np.uint8)

    # 应用暗化效果
    for c in range(3):
        img_array[..., c] = np.clip(img_array[..., c] - darken, 0, 255)

    # 🌿 随机噪点增强
    if speckle:
        for _ in range(width * height // 50):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            if np.mean(img_array[y, x]) > 180 and np.random.rand() < 0.3:
                img_array[y, x] = np.clip(img_array[y, x] - np.random.randint(10, 40), 0, 255)

    # ✅ 保留文字像素为纯黑
    if preserve_characters:
        img_array[char_mask] = np.array([0, 0, 0])

    return Image.fromarray(img_array)


def add_ink_bleed_effect_enhanced_SLOW(image, intensity=1.0):
    """非常明显的图像处理效果"""
    width, height = image.size
    result = image.copy()
    
    print("应用明显的图像处理效果...")
    
    # 转换为numpy数组进行高效处理
    img_array = np.array(result)
    
    # 找到深色像素（文字）
    dark_pixels = np.where(np.mean(img_array, axis=2) < 100)
    
    if len(dark_pixels[0]) == 0:
        print("警告：未检测到深色文字区域")
        return result
    
    # 创建明显的渗透效果
    for i in range(len(dark_pixels[0])):
        x, y = dark_pixels[1][i], dark_pixels[0][i]
        
        # 在文字周围创建明显的灰色晕染
        for dx in range(-6, 7):
            for dy in range(-6, 7):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= 6:  # 圆形渗透区域
                        # 只处理亮背景区域
                        if np.mean(img_array[ny, nx]) > 200:
                            # 明显的变暗效果
                            darken_amount = int(80 * (1 - distance/6) * intensity)
                            img_array[ny, nx] = np.clip(img_array[ny, nx] - darken_amount, 0, 255)
    
    # 添加一些随机噪点增强效果
    for _ in range(width * height // 50):  # 大量噪点
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        if np.mean(img_array[y, x]) > 180:  # 只在亮区域添加
            if random.random() < 0.3:
                img_array[y, x] = np.clip(img_array[y, x] - random.randint(10, 40), 0, 255)
    
    result = Image.fromarray(img_array)
    return result
