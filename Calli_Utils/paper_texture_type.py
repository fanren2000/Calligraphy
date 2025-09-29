from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random
import math

def add_realistic_paper_texture(width, height, paper_type="xuan"):
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
