from PIL import Image, ImageDraw, ImageFilter, ImageOps
import random
import math

def add_paper_texture_basic(image, intensity=0.1):
    """添加基础纸张纹理"""
    width, height = image.size
    
    # 创建纹理层
    texture = Image.new('L', (width, height), 255)  # 灰度图像
    
    # 添加随机噪声模拟纸张纤维
    for x in range(width):
        for y in range(height):
            if random.random() < intensity:
                # 随机变暗像素模拟纸张纹理
                current = texture.getpixel((x, y))
                new_value = max(0, current - random.randint(10, 40))
                texture.putpixel((x, y), new_value)
    
    # 轻微模糊使纹理更自然
    texture = texture.filter(ImageFilter.GaussianBlur(0.5))
    
    # 将纹理应用到原图
    result = Image.composite(
        image, 
        Image.new('RGB', (width, height), (230, 220, 200)),  # 稍暗的纸张底色
        texture
    )
    
    return result