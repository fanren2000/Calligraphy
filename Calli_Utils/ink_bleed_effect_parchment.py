from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont
import random
import math
import numpy as np

def add_ink_bleed_effect_parchment(image):
    """羊皮纸特有的纹理墨迹效果"""
    width, height = image.size
    result = image.copy()
    
    # 找到文字区域
    gray = image.convert('L')
    
    for x in range(width):
        for y in range(height):
            if gray.getpixel((x, y)) < 100:  # 文字区域
                # 在羊皮纸上墨迹会不均匀
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            # 羊皮纸上的墨迹会有纹理感
                            if random.random() < 0.4:  # 不均匀分布
                                r, g, b = result.getpixel((nx, ny))
                                brightness = (r + g + b) // 3
                                
                                if brightness > 180:  # 背景区域
                                    # 根据距离和随机因素变暗
                                    distance = abs(dx) + abs(dy)
                                    random_factor = random.uniform(0.5, 1.5)
                                    darken = int(25 * (1 - distance/6) * random_factor)
                                    
                                    result.putpixel((nx, ny), (
                                        max(0, r - darken),
                                        max(0, g - darken),
                                        max(0, b - darken)
                                    ))
    
    return result
