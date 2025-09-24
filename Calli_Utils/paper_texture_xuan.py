from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
import random
import math

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
import random, math

def add_xuan_paper_texture(image, texture_intensity=0.25, invert_mask=True):
    """添加宣纸质感到图像上，支持纹理强度和可选反转"""
    width, height = image.size

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
    result = ImageChops.multiply(image, fiber_rgb)

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