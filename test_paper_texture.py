from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random
import math

from Calli_Utils import add_ink_bleed_effect

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
    paper_texture = create_realistic_paper_texture(width, height, paper_type)
    
    # 将原图与纸张纹理混合
    result = Image.blend(image, paper_texture, alpha=0.3)
    
    # 增强对比度模拟墨水渗透
    result = ImageOps.autocontrast(result, cutoff=2)
    
    return result

def create_authentic_calligraphy(poem_text, author, output_path):
    """创建具有真实纸张质感的书法作品"""
    
    # 创建基础图像
    image = Image.new('RGB', (1000, 1400), (245, 235, 215))
    draw = ImageDraw.Draw(image)
    
    # 绘制书法内容（省略具体绘制代码）
    # ...
    
    print("添加纸张质感...")
    
    # 1. 首先添加宣纸纹理
    image = apply_paper_texture(image, "xuan")
    
    # 2. 添加墨迹渗透效果
    image = add_ink_bleed_effect(image, 0.2)
    
    # 3. 最终微调
    image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # 保存结果
    image.save(output_path, quality=95, dpi=(300, 300))
    print(f"真实质感书法作品已保存: {output_path}")
    
    return image

def create_texture_preview():
    """创建纸张质感预览"""
    
    textures = [
        ("宣纸质感", "xuan"),
        ("米纸质感", "rice"), 
        ("羊皮纸质感", "parchment")
    ]
    
    preview = Image.new('RGB', (1000, 600), (255, 255, 255))
    draw = ImageDraw.Draw(preview)
    
    draw.text((400, 20), "不同纸张质感效果对比", fill=(0, 0, 0))
    
    for i, (name, paper_type) in enumerate(textures):
        # 创建样本
        sample = Image.new('RGB', (300, 200), (245, 235, 215))
        sample_texture = create_realistic_paper_texture(300, 200, paper_type)
        
        # 添加文字说明
        sample_draw = ImageDraw.Draw(sample_texture)
        sample_draw.text((20, 20), f"这是{name}", fill=(100, 100, 100))
        
        # 粘贴到预览图
        x = 50 + i * 320
        y = 100
        preview.paste(sample_texture, (x, y))
        draw.text((x, y + 220), name, fill=(0, 0, 0))
    
    preview.save("纸张质感预览.png", quality=95)
    return preview

if __name__ == "__main__":
    # 生成质感预览
    create_texture_preview()
    print("生成完成：纸张质感预览.png")
    
    # 创建真实质感书法作品
    # create_authentic_calligraphy("静夜思", "李白", "真实质感书法.png")