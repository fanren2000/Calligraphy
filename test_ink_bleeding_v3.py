from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import random
import math
import numpy as np

def create_high_contrast_test_image():
    """创建高对比度的测试图像"""
    image = Image.new('RGB', (400, 300), (250, 245, 240))  # 很亮的背景
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("simkai.ttf", 60)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
    
    # 使用非常深的颜色
    draw.text((50, 50), "墨迹测试", font=font, fill=(10, 10, 10))  # 接近黑色
    draw.text((50, 150), "效果对比", font=font, fill=(15, 15, 15))
    
    return image

def add_very_visible_bleed_effect_v3(image, intensity=1.0):
    """版本3重写：非常明显的图像处理效果"""
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

def add_colorful_ink_effect_v4(image, intensity=0.9):
    """版本4重写：明显的彩色墨迹效果"""
    width, height = image.size
    result = image.copy()
    
    print("应用彩色墨迹效果...")
    
    # 创建明显的蓝色墨迹效果
    for x in range(width):
        for y in range(height):
            r, g, b = result.getpixel((x, y))
            brightness = (r + g + b) // 3
            
            # 如果是亮背景区域
            if brightness > 200:
                # 检查周围是否有深色文字
                has_dark = False
                min_distance = 10
                
                for dx in range(-5, 6):
                    for dy in range(-5, 6):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            nr, ng, nb = result.getpixel((nx, ny))
                            nbrightness = (nr + ng + nb) // 3
                            if nbrightness < 100:
                                distance = abs(dx) + abs(dy)
                                if distance < min_distance:
                                    min_distance = distance
                                    has_dark = True
                
                # 如果在文字附近，添加明显的蓝灰色
                if has_dark and random.random() < intensity:
                    # 明显的颜色偏移：减少红色和绿色，保持蓝色
                    new_r = max(0, r - 30)
                    new_g = max(0, g - 20)
                    new_b = b  # 蓝色保持不变或轻微增加
                    
                    # 进一步变暗
                    darken = min(40, (10 - min_distance) * 5)
                    new_r = max(0, new_r - darken)
                    new_g = max(0, new_g - darken)
                    
                    result.putpixel((x, y), (new_r, new_g, new_b))
    
    return result

def add_dramatic_bleed_effect(image, strength=1.0):
    """戏剧性的墨迹渗透效果（保证可见）"""
    width, height = image.size
    result = image.copy()
    
    # 首先找到所有文字像素
    text_pixels = []
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if (r + g + b) // 3 < 120:
                text_pixels.append((x, y))
    
    print(f"找到 {len(text_pixels)} 个文字像素")
    
    # 为每个文字像素创建明显的渗透
    for x, y in text_pixels:
        # 创建明显的圆形渗透区域
        for radius in [8, 6, 4, 2]:  # 多个半径层次
            for angle in range(0, 360, 10):  # 圆形采样
                rad = math.radians(angle)
                nx = int(x + radius * math.cos(rad))
                ny = int(y + radius * math.sin(rad))
                
                if 0 <= nx < width and 0 <= ny < height:
                    r, g, b = result.getpixel((nx, ny))
                    brightness = (r + g + b) // 3
                    
                    # 只在亮背景上添加效果
                    if brightness > 180:
                        # 根据距离计算效果强度
                        distance_effect = 1 - (radius / 10)
                        darken_amount = int(60 * distance_effect * strength)
                        
                        new_color = (
                            max(0, r - darken_amount),
                            max(0, g - darken_amount),
                            max(0, b - darken_amount)
                        )
                        result.putpixel((nx, ny), new_color)
    
    return result

def create_truly_visible_comparison_v2():
    """创建真正可见的效果对比版本2"""
    
    # 创建高对比度测试图像
    base_image = create_high_contrast_test_image()
    base_image.save("0_原图.png", quality=95)
    
    # 应用不同的效果（使用更强的参数）
    effects = [
        ("1. 原图", base_image),
        ("2. 明显渗透效果", add_very_visible_bleed_effect_v3(base_image.copy(), 1.0)),
        ("3. 图像处理效果", add_dramatic_bleed_effect(base_image.copy(), 1.0)),
        ("4. 彩色墨迹效果", add_colorful_ink_effect_v4(base_image.copy(), 0.8)),
        ("5. 戏剧性效果", add_dramatic_bleed_effect(base_image.copy(), 1.5))
    ]
    
    # 创建大尺寸对比图
    comparison = Image.new('RGB', (1000, 1500), (255, 255, 255))
    
    # 加载字体
    try:
        title_font = ImageFont.truetype("simkai.ttf", 28)
        label_font = ImageFont.truetype("simkai.ttf", 20)
    except:
        try:
            title_font = ImageFont.truetype("arial.ttf", 28)
            label_font = ImageFont.truetype("arial.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
    
    draw = ImageDraw.Draw(comparison)
    draw.text((350, 20), "墨迹效果明显对比（增强版）", font=title_font, fill=(0, 0, 0))
    
    # 排列对比图像
    for i, (name, effect_image) in enumerate(effects):
        # 保存单个效果图
        effect_image.save(f"{i}_{name.split('.')[1]}.png", quality=95)
        
        row = i
        x = 50
        y = 80 + row * 280
        
        # 粘贴效果图
        comparison.paste(effect_image, (x, y))
        
        # 绘制标签
        draw.text((x, y + 250), name, font=label_font, fill=(0, 0, 0))
        
        # 在图像上添加明显的标记
        draw.rectangle([x+10, y+10, x+25, y+25], fill=(255, 0, 0), outline=(0, 0, 0), width=2)
    
    # 添加说明文字
    draw.text((50, 1450), "红色方块是参考点，观察文字周围的灰色晕染效果", fill=(100, 100, 100))
    
    comparison.save("明显效果对比增强版.png", quality=95)
    print("生成完成：明显效果对比增强版.png")
    
    # 打印调试信息
    print("\n📊 效果强度报告：")
    for i, (name, img) in enumerate(effects):
        if i > 0:  # 跳过原图
            diff = ImageChops.difference(effects[0][1], img)
            diff_value = np.mean(np.array(diff))
            print(f"{name}: 差异强度 = {diff_value:.1f}")
    
    return comparison

def debug_pixel_values():
    """调试像素值，确保有足够的对比度"""
    
    test_img = create_high_contrast_test_image()
    width, height = test_img.size
    
    print("📋 像素值调试信息：")
    print("=" * 50)
    
    # 检查文字区域
    text_region = []
    for x in range(50, 300, 20):
        for y in range(50, 200, 20):
            r, g, b = test_img.getpixel((x, y))
            brightness = (r + g + b) // 3
            text_region.append(brightness)
            status = "文字" if brightness < 100 else "背景"
            print(f"({x:3d},{y:3d}): RGB({r:3d},{g:3d},{b:3d}) 亮度:{brightness:3d} [{status}]")
    
    avg_text_brightness = np.mean([b for b in text_region if b < 100])
    avg_bg_brightness = np.mean([b for b in text_region if b > 200])
    
    print(f"\n文字区域平均亮度: {avg_text_brightness:.1f}")
    print(f"背景区域平均亮度: {avg_bg_brightness:.1f}")
    print(f"对比度: {avg_bg_brightness - avg_text_brightness:.1f}")
    
    return test_img

if __name__ == "__main__":
    print("开始增强版效果测试...")
    
    # 先调试像素值
    print("调试像素对比度...")
    debug_img = debug_pixel_values()
    
    print("\n生成明显效果对比...")
    create_truly_visible_comparison_v2()
    
    print("\n🎯 如果效果仍然不明显，可能是以下原因：")
    print("1. 字体渲染问题：文字可能不是纯黑色")
    print("2. 图像尺寸问题：效果在缩略图中不明显")
    print("3. 显示设备问题：屏幕对比度设置")
    print("4. 建议直接查看保存的单个PNG文件进行对比")