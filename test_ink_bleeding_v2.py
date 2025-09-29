from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

def create_test_image_with_visible_text():
    """创建有明显文字的测试图像"""
    image = Image.new('RGB', (400, 300), (245, 235, 215))
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("simkai.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # 绘制明显的黑色文字
    draw.text((50, 50), "墨迹测试", font=font, fill=(20, 20, 20))  # 深黑色
    draw.text((50, 150), "效果对比", font=font, fill=(30, 30, 30))
    
    return image

def add_visible_ink_bleed_effect_v1(image, intensity=0.5):
    """版本1：明显的墨迹渗透效果"""
    width, height = image.size
    result = image.copy()
    
    # 创建明显的渗透掩膜
    bleed_mask = Image.new('L', (width, height), 0)
    
    # 找到深色区域（文字）
    for x in range(0, width, 2):  # 跳着采样提高性能
        for y in range(0, height, 2):
            r, g, b = image.getpixel((x, y))
            brightness = (r + g + b) // 3
            
            if brightness < 100:  # 深色区域
                # 在文字周围创建明显的渗透
                for dx in range(-4, 5):
                    for dy in range(-4, 5):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            distance = math.sqrt(dx*dx + dy*dy)
                            if distance <= 4:  # 圆形区域
                                bleed_value = min(255, int(200 * (1 - distance/4) * intensity))
                                current = bleed_mask.getpixel((nx, ny))
                                bleed_mask.putpixel((nx, ny), max(current, bleed_value))
    
    bleed_mask = bleed_mask.filter(ImageFilter.GaussianBlur(2))
    
    # 应用明显的变暗效果
    for x in range(width):
        for y in range(height):
            bleed_value = bleed_mask.getpixel((x, y))
            if bleed_value > 10:
                r, g, b = result.getpixel((x, y))
                # 明显变暗
                darken = bleed_value // 3
                result.putpixel((x, y), (
                    max(0, r - darken),
                    max(0, g - darken),
                    max(0, b - darken)
                ))
    
    return result

def add_visible_ink_bleed_effect_v2(image, intensity=0.8):
    """版本2：使用图像处理技术的渗透效果"""
    width, height = image.size
    result = image.copy()
    
    # 转换为灰度并二值化找到文字区域
    gray = image.convert('L')
    binary = gray.point(lambda x: 0 if x < 128 else 255)  # 二值化
    
    # 扩张文字区域
    dilated = binary.filter(ImageFilter.MaxFilter(5))
    
    # 创建渗透区域（扩张区域减去原始文字区域）
    bleed_region = Image.new('L', (width, height), 0)
    for x in range(width):
        for y in range(height):
            if dilated.getpixel((x, y)) == 0 and binary.getpixel((x, y)) == 255:
                bleed_region.putpixel((x, y), int(255 * intensity))
    
    # 模糊渗透区域
    bleed_region = bleed_region.filter(ImageFilter.GaussianBlur(3))
    
    # 应用效果
    for x in range(width):
        for y in range(height):
            bleed_value = bleed_region.getpixel((x, y))
            if bleed_value > 0:
                r, g, b = result.getpixel((x, y))
                # 根据背景亮度决定变暗程度
                brightness = (r + g + b) // 3
                if brightness > 200:  # 只处理亮背景
                    darken = min(50, bleed_value // 5)
                    result.putpixel((x, y), (
                        max(0, r - darken),
                        max(0, g - darken),
                        max(0, b - darken)
                    ))
    
    return result

def add_ink_bleed_with_colored_effect(image, intensity=0.6):
    """版本3：带颜色的墨迹效果"""
    width, height = image.size
    result = image.copy()
    
    # 创建蓝色调的墨迹效果
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            brightness = (r + g + b) // 3
            
            # 检查周围是否有深色文字
            has_dark_neighbor = False
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        nr, ng, nb = image.getpixel((nx, ny))
                        nbrightness = (nr + ng + nb) // 3
                        if nbrightness < 100:
                            has_dark_neighbor = True
                            break
                if has_dark_neighbor:
                    break
            
            # 如果在文字附近，添加蓝灰色调
            if has_dark_neighbor and brightness > 180:
                if random.random() < intensity:
                    # 向蓝灰色偏移
                    result.putpixel((x, y), (
                        max(0, r - 10),
                        max(0, g - 5),
                        max(0, b)  # 蓝色通道保持不变或增加
                    ))
    
    return result

def add_simple_but_visible_bleed(image, strength=0.7):
    """版本4：简单但明显的效果"""
    width, height = image.size
    result = image.copy()
    
    # 直接在每个文字像素周围添加效果
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            brightness = (r + g + b) // 3
            
            # 如果是文字区域
            if brightness < 120:
                # 在周围添加效果
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            nr, ng, nb = result.getpixel((nx, ny))
                            nbrightness = (nr + ng + nb) // 3
                            
                            # 如果是背景区域
                            if nbrightness > 180:
                                distance = abs(dx) + abs(dy)
                                if random.random() < strength * (1 - distance/4):
                                    # 明显变暗
                                    result.putpixel((nx, ny), (
                                        max(0, nr - 20),
                                        max(0, ng - 20),
                                        max(0, nb - 20)
                                    ))
    
    return result

def create_truly_visible_comparison():
    """创建真正可见的效果对比"""
    
    # 创建基础测试图像
    base_image = create_test_image_with_visible_text()
    
    # 应用不同的效果（使用更明显的参数）
    effects = [
        ("1. 原图", base_image),
        ("2. 明显渗透效果", add_visible_ink_bleed_effect_v1(base_image.copy(), 0.8)),
        ("3. 图像处理效果", add_visible_ink_bleed_effect_v2(base_image.copy(), 0.9)),
        ("4. 彩色墨迹效果", add_ink_bleed_with_colored_effect(base_image.copy(), 0.7)),
        ("5. 简单明显效果", add_simple_but_visible_bleed(base_image.copy(), 0.8))
    ]
    
    # 创建大尺寸对比图
    comparison = Image.new('RGB', (800, 1200), (255, 255, 255))
    draw = ImageDraw.Draw(comparison)
    
    draw.text((300, 20), "墨迹效果明显对比", fill=(0, 0, 0), 
              font=ImageFont.truetype("simkai.ttf", 30) if hasattr(ImageFont, 'truetype') else None)
    
    # 排列对比图像
    for i, (name, effect_image) in enumerate(effects):
        row = i
        x = 50
        y = 80 + row * 220
        
        # 粘贴效果图
        comparison.paste(effect_image, (x, y))
        
        # 添加标签
        font = ImageFont.truetype("simkai.ttf", 24)  # 字体文件, 字体大小
        draw.text((x, y + 180), name, font=font, fill=(0, 0, 0))
        
        # 在图像上添加参考点
        draw.rectangle([x+10, y+10, x+20, y+20], fill=(255, 0, 0))  # 红色参考点
    
    # 添加说明文字
    draw.text((50, 1150), "注意观察文字周围的灰色晕染效果", fill=(100, 100, 100))
    
    comparison.save("明显效果对比.png", quality=95)
    print("生成完成：明显效果对比.png")
    
    # 同时保存单个效果图用于详细比较
    for i, (name, effect_image) in enumerate(effects):
        effect_image.save(f"效果{i+1}_{name.split('.')[1]}.png", quality=95)
    
    return comparison

def debug_effect_application():
    """调试效果应用过程"""
    
    test_img = create_test_image_with_visible_text()
    width, height = test_img.size
    
    print("调试信息：")
    print(f"图像尺寸: {width}x{height}")
    print(f"图像模式: {test_img.mode}")
    
    # 检查文字区域像素值
    text_pixels = 0
    for x in range(50, 250, 10):  # 采样文字区域
        for y in range(50, 150, 10):
            r, g, b = test_img.getpixel((x, y))
            brightness = (r + g + b) // 3
            if brightness < 100:
                text_pixels += 1
            print(f"像素({x},{y}): RGB({r},{g},{b}) 亮度: {brightness}")
    
    print(f"检测到的文字像素数: {text_pixels}")
    
    return test_img

if __name__ == "__main__":
    print("开始调试效果应用...")
    
    # 先调试基础图像
    debug_image = debug_effect_application()
    
    print("\n生成明显效果对比图...")
    create_truly_visible_comparison()
    
    print("\n如果效果仍然不明显，请检查：")
    print("1. 文字颜色是否足够深（RGB值应该小于100）")
    print("2. 背景颜色是否足够亮（RGB值应该大于200）")
    print("3. 效果强度参数是否足够大")