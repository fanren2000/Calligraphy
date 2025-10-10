from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random
import math

def create_realistic_paper_texture(width, height, paper_type="xuan"):
    """创建真实的纸张纹理"""
    
    # 根据纸张类型设置参数
    if paper_type == "xuan":
        base_color = (242, 232, 212)  # 宣纸色
        fiber_density = width * height // 400
        spot_density = width * height // 800
    elif paper_type == "rice":
        base_color = (248, 240, 225)  # 米纸色
        fiber_density = width * height // 300
        spot_density = width * height // 600
    else:  # parchment
        base_color = (250, 245, 230)  # 羊皮纸色
        fiber_density = width * height // 200
        spot_density = width * height // 400
    
    # 创建基础纹理
    texture = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(texture)
    
    # 添加纤维纹理
    for _ in range(fiber_density):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        length = random.randint(30, 150)
        angle = random.uniform(0, 2 * math.pi)
        
        # 纤维颜色（稍暗）
        fiber_color = (
            max(0, base_color[0] - random.randint(5, 15)),
            max(0, base_color[1] - random.randint(5, 15)),
            max(0, base_color[2] - random.randint(5, 15))
        )
        
        # 绘制纤维
        for i in range(0, length, 2):
            px = int(x1 + i * math.cos(angle))
            py = int(y1 + i * math.sin(angle))
            if 0 <= px < width and 0 <= py < height:
                size = random.randint(1, 2)
                draw.ellipse([px-size, py-size, px+size, py+size], fill=fiber_color)
    
    # 添加纸张斑点
    for _ in range(spot_density):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        size = random.randint(1, 4)
        
        spot_color = (
            max(0, base_color[0] - random.randint(10, 25)),
            max(0, base_color[1] - random.randint(10, 25)),
            max(0, base_color[2] - random.randint(10, 25))
        )
        
        draw.ellipse([x-size, y-size, x+size, y+size], fill=spot_color)
    
    # 添加光照效果（模拟纸张起伏）
    gradient = Image.new('L', (width, height), 255)
    g_draw = ImageDraw.Draw(gradient)
    
    for _ in range(width // 10):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(50, 200)
        
        for r in range(radius, 0, -5):
            alpha = int(255 * (1 - r/radius))
            g_draw.ellipse([x-r, y-r, x+r, y+r], fill=alpha)
    
    gradient = gradient.filter(ImageFilter.GaussianBlur(20))
    
    # 应用光照效果
    texture = Image.composite(
        texture,
        Image.new('RGB', (width, height), (
            max(0, base_color[0] - 10),
            max(0, base_color[1] - 10),
            max(0, base_color[2] - 10)
        )),
        gradient
    )
    
    return texture

def apply_paper_texture(image, paper_type="xuan"):
    """将纸张纹理应用到图像"""
    width, height = image.size
    
    # 创建纸张纹理
    paper_texture = add_realistic_paper_texture(width, height, paper_type)
    
    # 将原图与纸张纹理混合
    result = Image.blend(image, paper_texture, alpha=0.3)
    
    # 增强对比度模拟墨水渗透
    result = ImageOps.autocontrast(result, cutoff=2)
    
    return result

def create_authentic_paper_texture(width, height, paper_type="xuan"):
    """创建真实的纸张纹理"""
    if paper_type == "xuan":
        base_color = (251, 245, 235)
    else:
        base_color = (252, 243, 229)
    
    img = Image.new('RGB', (width, height), base_color)
    pixels = img.load()  # 使用load()方法提高性能
    
    # 添加细微的颜色变化
    for i in range(width):
        for j in range(height):
            r, g, b = base_color
            # 非常细微的颜色变化
            variation = random.randint(-2, 2)
            pixels[i, j] = (
                max(0, min(255, r + variation)),
                max(0, min(255, g + variation)),
                max(0, min(255, b + variation))
            )
    
    # 添加纤维纹理
    draw = ImageDraw.Draw(img)
    for _ in range(width * height // 500):  # 适量的纤维
        x1 = random.randint(0, width-1)
        y1 = random.randint(0, height-1)
        length = random.randint(15, 40)
        angle = random.uniform(0, math.pi)
        
        x2 = min(width-1, max(0, int(x1 + length * math.cos(angle))))
        y2 = min(height-1, max(0, int(y1 + length * math.sin(angle))))
        
        # 确保坐标有效
        if 0 <= x1 < width and 0 <= y1 < height and 0 <= x2 < width and 0 <= y2 < height:
            # 非常细微的颜色变化
            darken = random.uniform(0.97, 0.995)
            r, g, b = pixels[x1, y1]
            fiber_color = (
                int(r * darken),
                int(g * darken), 
                int(b * darken)
            )
            
            draw.line([(x1, y1), (x2, y2)], fill=fiber_color, width=1)
    
    return img

def add_realistic_aging(paper_img, intensity=0.2):
    """添加真实的老化效果"""
    width, height = paper_img.size
    aged_img = paper_img.copy()
    pixels = aged_img.load()  # 使用load()方法
    
    # 1. 细微的色斑
    for _ in range(int(25 * intensity)):
        center_x = random.randint(0, width-1)
        center_y = random.randint(0, height-1)
        radius = random.randint(2, 8)  # 小斑点
        
        for i in range(max(0, center_x-radius), min(width, center_x+radius)):
            for j in range(max(0, center_y-radius), min(height, center_y+radius)):
                # 确保坐标有效
                if 0 <= i < width and 0 <= j < height:
                    dist = math.sqrt((i-center_x)**2 + (j-center_y)**2)
                    if dist < radius:
                        r, g, b = pixels[i, j]
                        # 轻微变黄
                        fade = 1.0 - (dist / radius) * 0.1
                        pixels[i, j] = (
                            int(r * fade),
                            int(g * fade * 0.98),
                            int(b * fade * 0.95)
                        )
    
    return aged_img

