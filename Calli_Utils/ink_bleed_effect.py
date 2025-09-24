from PIL import Image, ImageDraw, ImageFilter
import random

def add_ink_bleed_effect(image, intensity=0.3):
    """添加墨迹渗透效果（宣纸特有），使用透明叠加模拟墨迹扩散"""
    width, height = image.size

    # 创建透明渗透层
    bleed_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bleed_layer)

    # 灰度图用于识别文字区域
    gray_image = image.convert('L')

    for x in range(width):
        for y in range(height):
            if gray_image.getpixel((x, y)) < 100:  # 深色区域（文字）
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if random.random() < intensity:
                                radius = random.randint(1, 3)
                                alpha = random.randint(10, 40)
                                draw.ellipse((nx - radius, ny - radius, nx + radius, ny + radius),
                                             fill=(0, 0, 0, alpha))

    # 模糊渗透层
    bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(1.5))

    # 确保原图为 RGBA 模式
    base_rgba = image.convert('RGBA')

    # 应用渗透叠加
    result = Image.alpha_composite(base_rgba, bleed_layer)

    return result.convert('RGB')


    """添加墨迹渗透效果（宣纸特有），使用透明叠加模拟墨迹扩散"""
    width, height = image.size

    # 创建透明渗透层
    bleed_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bleed_layer)

    # 灰度图用于识别文字区域
    gray_image = image.convert('L')

    for x in range(width):
        for y in range(height):
            if gray_image.getpixel((x, y)) < 100:  # 深色区域（文字）
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if random.random() < intensity:
                                radius = random.randint(1, 3)
                                alpha = random.randint(10, 40)
                                draw.ellipse((nx - radius, ny - radius, nx + radius, ny + radius),
                                             fill=(0, 0, 0, alpha))

    # 模糊渗透层
    bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(1.5))

    # 确保原图为 RGBA 模式
    base_rgba = image.convert('RGBA')

    # 应用渗透叠加
    result = Image.alpha_composite(base_rgba, bleed_layer)

    return result.convert('RGB')

    """添加墨迹渗透效果（宣纸特有）"""
    width, height = image.size
    
    # 创建墨迹渗透层
    bleed_layer = overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    # 找到文字区域
    gray_image = image.convert('L')
    
    for x in range(width):
        for y in range(height):
            # 如果是深色区域（文字）
            if gray_image.getpixel((x, y)) < 100:
                # 在文字周围添加渗透效果
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if random.random() < intensity:
                                current = bleed_layer.getpixel((nx, ny))
                                bleed_layer.putpixel((nx, ny), min(255, int(current) + random.randint(10, 40)))
    
    # 模糊渗透效果
    bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(1.5))
    
    # 应用渗透效果
    result = image.copy()
    for x in range(width):
        for y in range(height):
            bleed_value = bleed_layer.getpixel((x, y))
            if bleed_value > 0:
                r, g, b = result.getpixel((x, y))
                # 文字周围稍微变暗模拟渗透
                new_color = (
                    max(0, r - bleed_value // 10),
                    max(0, g - bleed_value // 10),
                    max(0, b - bleed_value // 10)
                )
                result.putpixel((x, y), new_color)
    
    
    return result