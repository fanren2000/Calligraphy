from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont
import random, math

from Calli_Utils import add_ink_bleed_effect

def enrich_paper_texture(paper_base, grain_intensity=0.2, bleed_intensity=0.3, crosshatch=False):
    """叠加宣纸纹理与笔触渗化效果，增强纸张质感"""
    width, height = paper_base.size

    # 🌾 Rice paper grain (random speckles)
    grain = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(grain)
    for _ in range(width * height // 800):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        radius = random.randint(1, 2)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=random.randint(180, 230))

    grain = grain.filter(ImageFilter.GaussianBlur(0.5))
    grain = ImageChops.multiply(grain, Image.new('L', (width, height), int(255 * grain_intensity)))
    grain_rgb = Image.merge('RGB', (grain, grain, grain))
    paper_base = ImageChops.multiply(paper_base, grain_rgb)

    # 🖌️ Brush bleed (soft radial ink diffusion)
    bleed = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(bleed)
    for _ in range(10):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(30, 80)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=random.randint(100, 180))

    bleed = bleed.filter(ImageFilter.GaussianBlur(3.0))
    bleed = ImageChops.multiply(bleed, Image.new('L', (width, height), int(255 * bleed_intensity)))

    # debug
    bleed.save("debug_bleed.png")
    
    bleed_rgb = Image.merge('RGB', (bleed, bleed, bleed))
    paper_base = ImageChops.blend(paper_base, bleed_rgb)

    # 🧵 Optional crosshatch fibers
    if crosshatch:
        hatch = Image.new('L', (width, height), 255)
        draw = ImageDraw.Draw(hatch)
        for _ in range(width * height // 1000):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            length = random.randint(30, 100)
            angle = random.choice([0, math.pi / 2])  # horizontal or vertical
            for i in range(length):
                px = int(x1 + i * math.cos(angle))
                py = int(y1 + i * math.sin(angle))
                if 0 <= px < width and 0 <= py < height:
                    hatch.putpixel((px, py), random.randint(150, 200))
        hatch = hatch.filter(ImageFilter.GaussianBlur(1.0))
        hatch_rgb = Image.merge('RGB', (hatch, hatch, hatch))
        paper_base = ImageChops.multiply(paper_base, hatch_rgb)

    return paper_base

def apply_brush_bleed_overlay(base_image, bleed_intensity=0.3, num_bleeds=10):
    """在图像上叠加笔触渗化效果，使用透明层模拟墨迹扩散"""
    from PIL import Image, ImageDraw, ImageFilter

    width, height = base_image.size
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for _ in range(num_bleeds):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(30, 80)
        alpha = int(255 * bleed_intensity)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(0, 0, 0, alpha))

    overlay = overlay.filter(ImageFilter.GaussianBlur(3.0))

    # Convert base to RGBA if needed
    if base_image.mode != 'RGBA':
        base_image = base_image.convert('RGBA')

    result = Image.alpha_composite(base_image, overlay)
    return result.convert('RGB')


def add_correct_ink_bleed_effect(image, intensity=0.2, bleed_radius=3):
    """
    修正的墨迹渗透效果（只影响文字周围）
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    width, height = image.size
    
    # 创建原图的副本
    result = image.copy()
    
    # 转换为灰度图来检测文字区域
    gray_image = image.convert('L')
    
    # 创建渗透掩膜（只标记需要渗透的区域）
    bleed_mask = Image.new('L', (width, height), 0)
    
    print("正在计算墨迹渗透区域...")
    
    # 只处理深色区域（文字）
    for x in range(width):
        for y in range(height):
            pixel_value = gray_image.getpixel((x, y))
            
            # 如果是文字区域（深色）
            if pixel_value < 100:  # 阈值可根据需要调整
                # 在文字周围创建渗透效果
                for dx in range(-bleed_radius, bleed_radius + 1):
                    for dy in range(-bleed_radius, bleed_radius + 1):
                        nx, ny = x + dx, y + dy
                        
                        # 确保在图像范围内
                        if 0 <= nx < width and 0 <= ny < height:
                            # 只处理背景区域（避免文字本身过暗）
                            if gray_image.getpixel((nx, ny)) > 150:  # 背景区域
                                distance = abs(dx) + abs(dy)
                                probability = intensity * (1 - distance / (bleed_radius * 2))
                                
                                if random.random() < probability:
                                    current = bleed_mask.getpixel((nx, ny))
                                    bleed_mask.putpixel((nx, ny), min(255, current + 30))
    
    # 模糊渗透掩膜使效果更自然
    bleed_mask = bleed_mask.filter(ImageFilter.GaussianBlur(1.2))
    
    print("应用墨迹渗透效果...")
    
    # 只对渗透区域应用变暗效果
    for x in range(width):
        for y in range(height):
            bleed_value = bleed_mask.getpixel((x, y))
            if bleed_value > 0:
                r, g, b = result.getpixel((x, y))
                
                # 轻微变暗，模拟墨水渗透
                darken_amount = bleed_value // 20  # 控制变暗程度
                new_color = (
                    max(0, r - darken_amount),
                    max(0, g - darken_amount),
                    max(0, b - darken_amount)
                )
                result.putpixel((x, y), new_color)
    
    return result

def add_selective_ink_bleed(image, intensity=0.3):
    """
    选择性墨迹渗透效果（更精确的控制）
    """
    width, height = image.size
    result = image.copy()
    
    # 检测文字区域
    gray = image.convert('L')
    
    # 创建文字区域掩膜
    text_mask = Image.new('L', (width, height), 0)
    for x in range(width):
        for y in range(height):
            if gray.getpixel((x, y)) < 120:  # 文字区域
                text_mask.putpixel((x, y), 255)
    
    # 扩展文字区域（模拟渗透）
    expanded_mask = text_mask.filter(ImageFilter.MaxFilter(3))  # 扩张3像素
    
    # 只对扩张区域应用效果（排除原始文字区域）
    bleed_region = Image.new('L', (width, height), 0)
    for x in range(width):
        for y in range(height):
            if expanded_mask.getpixel((x, y)) == 255 and text_mask.getpixel((x, y)) == 0:
                bleed_region.putpixel((x, y), int(255 * intensity))
    
    bleed_region = bleed_region.filter(ImageFilter.GaussianBlur(1.5))
    
    # 应用渗透效果
    for x in range(width):
        for y in range(height):
            bleed_value = bleed_region.getpixel((x, y))
            if bleed_value > 0:
                r, g, b = result.getpixel((x, y))
                # 轻微变暗
                darken = bleed_value // 15
                result.putpixel((x, y), (
                    max(0, r - darken),
                    max(0, g - darken),
                    max(0, b - darken)
                ))
    
    return result

def add_subtle_ink_effect(image, strength=0.1):
    """
     subtle墨迹效果（最保守的版本）
    """
    width, height = image.size
    result = image.copy()
    gray = image.convert('L')
    
    # 只处理文字边缘
    for x in range(width):
        for y in range(height):
            # 如果是背景区域
            if gray.getpixel((x, y)) > 180:
                # 检查周围是否有文字
                has_nearby_text = False
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if gray.getpixel((nx, ny)) < 100:
                                has_nearby_text = True
                                break
                    if has_nearby_text:
                        break
                
                # 如果在文字附近，轻微变暗
                if has_nearby_text and random.random() < strength:
                    r, g, b = result.getpixel((x, y))
                    result.putpixel((x, y), (
                        max(0, r - 5),
                        max(0, g - 5),
                        max(0, b - 5)
                    ))
    
    return result

def test_bleed_effects():
    """测试不同的渗透效果"""
    
    # 创建测试图像
    image = Image.new('RGB', (400, 200), (245, 235, 215))
    draw = ImageDraw.Draw(image)
    
    # 绘制测试文字
    try:
        font = ImageFont.truetype("simkai.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 50), "墨迹渗透测试", font=font, fill=(0, 0, 0))
    draw.text((50, 100), "乾坤正气", font=font, fill=(0, 0, 0))
    
    # 测试不同效果
    effects = [
        ("原图", image),
        ("轻微效果", add_subtle_ink_effect(image.copy(), 0.1)),
        ("标准效果", add_correct_ink_bleed_effect(image.copy(), 0.2)),
        ("明显效果", add_selective_ink_bleed(image.copy(), 0.4))
    ]
    
    # 创建对比图
    comparison = Image.new('RGB', (900, 500), (255, 255, 255))
    draw_comp = ImageDraw.Draw(comparison)
    
    draw_comp.text((350, 20), "墨迹渗透效果对比", fill=(0, 0, 0))
    
    for i, (name, effect_image) in enumerate(effects):
        x = 50 + (i % 2) * 450
        y = 80 + (i // 2) * 220
        
        comparison.paste(effect_image, (x, y))
        draw_comp.text((x, y + 180), name, fill=(0, 0, 0))
    
    comparison.save("墨迹效果对比.png", quality=95)
    print("生成完成：墨迹效果对比.png")
    
    return comparison

def create_better_paper_texture(image):
    """
    改进的纸张质感（不依赖墨迹渗透）
    """
    width, height = image.size
    
    # 创建纸张纹理（不改变整体亮度）
    texture = Image.new('L', (width, height), 255)
    
    # 添加细微的纸张纹理
    for _ in range(width * height // 1000):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        brightness = random.randint(240, 255)  # 保持高亮度
        texture.putpixel((x, y), brightness)
    
    texture = texture.filter(ImageFilter.GaussianBlur(0.3))
    
    # 应用纹理（保持原图亮度）
    result = Image.composite(image, image, texture)  # 使用原图作为both参数
    
    return result

if __name__ == "__main__":
    print("测试墨迹渗透效果...")
    test_bleed_effects()
    
    print("\n使用建议：")
    print("1. add_subtle_ink_effect - 最轻微的效果")
    print("2. add_correct_ink_bleed_effect - 标准效果") 
    print("3. add_selective_ink_bleed - 更明显的效果")
    print("4. create_better_paper_texture - 只添加纸张纹理，不改变亮度")
else:
    # Step 1: Create base
    paper_base = Image.new('RGB', (1400, 700), (242, 232, 212))

    # Step 2: Draw text or seal
    draw = ImageDraw.Draw(paper_base)
    poem_font = ImageFont.truetype("simkai.ttf", 320)
    draw.text((100, 100), "乾坤正气", font=poem_font, fill=(0, 0, 0))

    # Step 3: Apply texture overlays
    # paper_base = apply_brush_bleed_overlay(paper_base, bleed_intensity=0.15)
    paper_base = add_ink_bleed_effect(paper_base, intensity=0.3)
    paper_base.save("墨迹渗透效果.png")

