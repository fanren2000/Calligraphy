from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
import random
import math

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
import random, math

def add_xuan_paper_texture(width, height, texture_intensity=0.25, invert_mask=True):
    """添加宣纸质感到图像上，支持纹理强度和可选反转"""
    
    # 创建宣纸底色（米黄色）
    paper_base = Image.new('RGB', (width, height), (242, 232, 212))

    # 创建纤维纹理层（灰度）
    fiber_texture = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(fiber_texture)

    # 模拟宣纸纤维（长条状纹理）
    for _ in range(width * height // 500):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        length = random.randint(20, 100)
        angle = random.uniform(0, 2 * math.pi)

        for i in range(length):
            px = int(x1 + i * math.cos(angle))
            py = int(y1 + i * math.sin(angle))
            if 0 <= px < width and 0 <= py < height:
                current = fiber_texture.getpixel((px, py))
                fiber_texture.putpixel((px, py), max(100, current - random.randint(5, 15)))

    # 添加随机斑点
    for _ in range(width * height // 1000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        size = random.randint(1, 3)
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    current = fiber_texture.getpixel((nx, ny))
                    fiber_texture.putpixel((nx, ny), max(150, current - random.randint(10, 30)))

    # 模糊纹理
    fiber_texture = fiber_texture.filter(ImageFilter.GaussianBlur(0.8))

    # 应用强度缩放
    enhancer = ImageEnhance.Brightness(fiber_texture)
    fiber_texture = enhancer.enhance(texture_intensity)

    # 转换为 RGB 纹理层
    fiber_rgb = Image.merge('RGB', (fiber_texture, fiber_texture, fiber_texture))

    # 使用 multiply 模式叠加纹理
    result = ImageChops.multiply(paper_base, fiber_rgb)

    return result

    """添加宣纸质感"""
    width, height = image.size
    
    # 创建宣纸底色（米黄色）
    paper_base = Image.new('RGB', (width, height), (242, 232, 212))
    
    # 创建纤维纹理层
    fiber_texture = Image.new('L', (width, height), 255)

     # Apply intensity scaling to fiber_texture
    enhancer = ImageEnhance.Brightness(fiber_texture)
    fiber_texture = enhancer.enhance(texture_intensity)
    
    draw = ImageDraw.Draw(fiber_texture)
    
    # 模拟宣纸纤维（长条状纹理）
    for _ in range(width * height // 500):  # 控制纤维密度
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        length = random.randint(20, 100)
        angle = random.uniform(0, 2 * math.pi)
        
        x2 = x1 + length * math.cos(angle)
        y2 = y1 + length * math.sin(angle)
        
        # 绘制纤维线条
        for i in range(length):
            px = int(x1 + i * math.cos(angle))
            py = int(y1 + i * math.sin(angle))
            if 0 <= px < width and 0 <= py < height:
                current = fiber_texture.getpixel((px, py))
                fiber_texture.putpixel((px, py), max(100, current - random.randint(5, 15)))
    
    # 添加随机斑点
    for _ in range(width * height // 1000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        size = random.randint(1, 3)
        for dx in range(-size, size+1):
            for dy in range(-size, size+1):
                nx, ny = x+dx, y+dy
                if 0 <= nx < width and 0 <= ny < height:
                    current = fiber_texture.getpixel((nx, ny))
                    fiber_texture.putpixel((nx, ny), max(150, current - random.randint(10, 30)))
    
    # 模糊纹理
    fiber_texture = fiber_texture.filter(ImageFilter.GaussianBlur(0.8))

    # debug the texture
    fiber_texture.save("debug_texture.png")

    fiber_texture = ImageOps.invert(fiber_texture)
    
    # 合并纹理和原图
    result = Image.composite(paper_base, image, fiber_texture)
    
    return result

def add_xuan_paper_texture_enhanced(width, height):
    """增强的宣纸纹理（模仿真实的宣纸特性）"""
    base_color = (242, 232, 212)  # 宣纸基色
    texture = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(texture)
    
    print("创建宣纸纹理...")
    
    # 1. 宣纸纤维纹理（主要特征）
    for _ in range(width * height // 200):  # 密集的纤维
        # 长条状纤维（宣纸特点）
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        length = random.randint(50, 200)  # 较长的纤维
        angle = random.uniform(0, math.pi)  # 主要是水平方向
        
        # 纤维颜色（比基色稍深）
        fiber_color = (
            max(0, base_color[0] - random.randint(8, 15)),
            max(0, base_color[1] - random.randint(8, 15)),
            max(0, base_color[2] - random.randint(8, 15))
        )
        
        # 绘制纤维（带有不规则边缘）
        for i in range(0, length, 3):
            px = int(x1 + i * math.cos(angle))
            py = int(y1 + i * math.sin(angle))
            if 0 <= px < width and 0 <= py < height:
                # 纤维宽度变化
                fiber_width = random.randint(1, 3)
                for w in range(-fiber_width, fiber_width + 1):
                    for h in range(-fiber_width, fiber_width + 1):
                        nx, ny = px + w, py + h
                        if 0 <= nx < width and 0 <= ny < height:
                            if random.random() < 0.7:  # 不规则分布
                                texture.putpixel((nx, ny), fiber_color)
    
    # 2. 宣纸的云状纹理（手工造纸特征）
    for _ in range(width * height // 500):
        center_x = random.randint(0, width)
        center_y = random.randint(0, height)
        radius = random.randint(30, 100)
        
        for r in range(radius, 0, -5):
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                x = int(center_x + r * math.cos(rad))
                y = int(center_y + r * math.sin(rad))
                
                if 0 <= x < width and 0 <= y < height:
                    # 云状渐变
                    intensity = 1 - (r / radius)
                    darken = int(15 * intensity * random.uniform(0.5, 1.0))
                    
                    r_current, g_current, b_current = texture.getpixel((x, y))
                    new_color = (
                        max(0, r_current - darken),
                        max(0, g_current - darken),
                        max(0, b_current - darken)
                    )
                    texture.putpixel((x, y), new_color)
    
    # 3. 添加宣纸特有的斑点（材料杂质）
    for _ in range(width * height // 1000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        size = random.randint(2, 6)
        
        # 斑点颜色（类似树皮或草纤维）
        spot_color = (
            max(0, base_color[0] - random.randint(20, 40)),
            max(0, base_color[1] - random.randint(15, 30)),
            max(0, base_color[2] - random.randint(10, 25))
        )
        
        for dx in range(-size, size+1):
            for dy in range(-size, size+1):
                if dx*dx + dy*dy <= size*size:  # 圆形斑点
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if random.random() < 0.8:
                            texture.putpixel((nx, ny), spot_color)
    
    # 4. 宣纸的光泽效果（表面轻微反光）
    highlight = Image.new('L', (width, height), 0)
    for _ in range(width // 20):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(50, 150)
        
        for r in range(radius, 0, -10):
            brightness = int(255 * (1 - r/radius) * 0.3)  # 柔和的高光
            for angle in range(0, 360, 10):
                rad = math.radians(angle)
                hx = int(x + r * math.cos(rad))
                hy = int(y + r * math.sin(rad))
                if 0 <= hx < width and 0 <= hy < height:
                    current = highlight.getpixel((hx, hy))
                    highlight.putpixel((hx, hy), max(current, brightness))
    
    highlight = highlight.filter(ImageFilter.GaussianBlur(15))
    texture = Image.composite(texture, Image.new('RGB', (width, height), (255, 255, 255)), highlight)
    
    return texture
