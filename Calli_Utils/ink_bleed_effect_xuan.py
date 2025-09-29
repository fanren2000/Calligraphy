from PIL import Image, ImageDraw, ImageFilter
import random
import math
import numpy as np

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

def add_ink_bleed_effect_enhanced(image, intensity=1.0):
    """非常明显的图像处理效果"""
    width, height = image.size
    result = image.copy()
    
    print("应用明显的图像处理效果...")
    
    # 转换为numpy数组进行高效处理
    img_array = np.array(result)
    
    # 找到深色像素（文字）
    dark_pixels = np.where(np.mean(img_array, axis=2) < 100)
    
    if len(dark_pixels[0]) == 0:
        print("警告：未检测到深色文字区域")
        return result
    
    # 创建明显的渗透效果
    for i in range(len(dark_pixels[0])):
        x, y = dark_pixels[1][i], dark_pixels[0][i]
        
        # 在文字周围创建明显的灰色晕染
        for dx in range(-6, 7):
            for dy in range(-6, 7):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= 6:  # 圆形渗透区域
                        # 只处理亮背景区域
                        if np.mean(img_array[ny, nx]) > 200:
                            # 明显的变暗效果
                            darken_amount = int(80 * (1 - distance/6) * intensity)
                            img_array[ny, nx] = np.clip(img_array[ny, nx] - darken_amount, 0, 255)
    
    # 添加一些随机噪点增强效果
    for _ in range(width * height // 50):  # 大量噪点
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        if np.mean(img_array[y, x]) > 180:  # 只在亮区域添加
            if random.random() < 0.3:
                img_array[y, x] = np.clip(img_array[y, x] - random.randint(10, 40), 0, 255)
    
    result = Image.fromarray(img_array)
    return result
