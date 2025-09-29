from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont
import random
import math

def add_parchment_texture_enhanced(width, height):
    """增强的羊皮纸纹理（粗糙、有质感）"""
    base_color = (250, 245, 230)  # 羊皮纸基色
    texture = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(texture)
    
    print("创建羊皮纸纹理...")
    
    # 1. 羊皮纸的粗糙表面（主要特征）
    roughness = Image.new('L', (width, height), 0)
    for _ in range(width * height // 100):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        strength = random.randint(20, 60)
        
        # 创建粗糙点
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    current = roughness.getpixel((nx, ny))
                    roughness.putpixel((nx, ny), max(current, strength))
    
    roughness = roughness.filter(ImageFilter.GaussianBlur(2))
    
    # 2. 羊皮纸的皮革纹理（模仿动物皮肤）
    for _ in range(width * height // 300):
        # 创建不规则的皮革纹理
        start_x = random.randint(0, width)
        start_y = random.randint(0, height)
        
        # 随机曲线路径
        points = []
        current_x, current_y = start_x, start_y
        for _ in range(random.randint(3, 8)):
            current_x += random.randint(-20, 20)
            current_y += random.randint(-10, 10)
            points.append((current_x, current_y))
        
        # 绘制皮革纹理线
        if len(points) > 1:
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                # 绘制带有变化的线条
                steps = max(abs(x2 - x1), abs(y2 - y1))
                if steps > 0:
                    for j in range(steps):
                        t = j / steps
                        x = int(x1 + t * (x2 - x1))
                        y = int(y1 + t * (y2 - y1))
                        
                        if 0 <= x < width and 0 <= y < height:
                            # 皮革纹理颜色
                            leather_color = (
                                max(0, base_color[0] - random.randint(10, 25)),
                                max(0, base_color[1] - random.randint(10, 25)),
                                max(0, base_color[2] - random.randint(8, 20))
                            )
                            
                            for d in range(-1, 2):
                                nx1, ny1 = x + d, y
                                nx2, ny2 = x, y + d

                                if 0 <= nx1 < width and 0 <= ny1 < height:
                                     texture.putpixel((nx1, ny1), leather_color)
                                if 0 <= nx2 < width and 0 <= ny2 < height:
                                        texture.putpixel((nx2, ny2), leather_color)
    
    # 3. 羊皮纸的陈旧效果（斑点、污渍）
    for _ in range(width * height // 800):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        size = random.randint(3, 10)
        
        # 陈旧斑点颜色
        stain_color = (
            max(0, base_color[0] - random.randint(15, 35)),
            max(0, base_color[1] - random.randint(15, 35)),
            max(0, base_color[2] - random.randint(10, 25))
        )
        
        for dx in range(-size, size+1):
            for dy in range(-size, size+1):
                if dx*dx + dy*dy <= size*size:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if random.random() < 0.6:
                            texture.putpixel((nx, ny), stain_color)
    
    # 应用粗糙度效果
    texture = Image.composite(texture, Image.new('RGB', (width, height), (240, 235, 220)), roughness)
    
    return texture
