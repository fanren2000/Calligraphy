from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont
import random
import math

def add_rice_paper_texture_enhanced(width, height):
    """增强的米纸纹理（光滑细腻的特性）"""
    base_color = (248, 240, 225)  # 米纸基色（更白更亮）
    texture = Image.new('RGB', (width, height), base_color)
    
    print("创建米纸纹理...")
    
    # 1. 米纸的细腻纹理（比宣纸更细腻）
    for _ in range(width * height // 400):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        
        # 米纸纹理更细更短
        length = random.randint(10, 60)
        angle = random.uniform(0, 2 * math.pi)
        
        fiber_color = (
            max(0, base_color[0] - random.randint(5, 12)),
            max(0, base_color[1] - random.randint(5, 12)),
            max(0, base_color[2] - random.randint(5, 12))
        )
        
        for i in range(length):
            px = int(x + i * math.cos(angle))
            py = int(y + i * math.sin(angle))
            if 0 <= px < width and 0 <= py < height:
                texture.putpixel((px, py), fiber_color)
    
    # 2. 米纸的光滑表面（轻微光泽）
    smoothness = Image.new('L', (width, height), 255)
    for x in range(0, width, 2):
        for y in range(0, height, 2):
            # 创建轻微的光滑变化
            variation = random.randint(-3, 3)
            for dx in range(2):
                for dy in range(2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        current = smoothness.getpixel((nx, ny))
                        smoothness.putpixel((nx, ny), max(0, min(255, current + variation)))
    
    smoothness = smoothness.filter(ImageFilter.GaussianBlur(1))
    texture = Image.composite(texture, Image.new('RGB', (width, height), (255, 255, 255)), smoothness)
    
    # 3. 米纸的均匀性（比宣纸更均匀）
    uniformity = Image.new('L', (width, height), 0)
    for _ in range(width * height // 10000):  # 很少的不均匀点
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        radius = random.randint(5, 15)
        
        for r in range(radius, 0, -1):
            for angle in range(0, 360, 20):
                rad = math.radians(angle)
                ux = int(x + r * math.cos(rad))
                uy = int(y + r * math.sin(rad))
                if 0 <= ux < width and 0 <= uy < height:
                    current = uniformity.getpixel((ux, uy))
                    uniformity.putpixel((ux, uy), max(current, int(50 * (1 - r/radius))))
    
    uniformity = uniformity.filter(ImageFilter.GaussianBlur(3))
    texture = Image.composite(texture, Image.new('RGB', (width, height), (253, 248, 238)), uniformity)
    
    return texture
