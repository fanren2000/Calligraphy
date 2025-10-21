
import random
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def add_ink_bleed_effect_original(image, intensity=0.3, imageMode="RGBA"):
    """原始版本墨迹渗透效果"""
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

    if imageMode == "RGB":
        return result.convert('RGB')
    else:
        return result

def add_ink_bleed_effect_fixed(image, intensity=0.3, imageMode="RGBA"):
    """修复版墨迹渗透效果 - 强度差异明显"""
    width, height = image.size

    # 创建透明渗透层
    bleed_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bleed_layer)

    # 灰度图用于识别文字区域
    gray_image = image.convert('L')

    # 根据强度调整参数
    bleed_range = max(1, int(3 * intensity))  # 渗透范围随强度变化
    max_alpha = int(80 * intensity)           # 最大透明度随强度变化
    min_alpha = int(20 * intensity)           # 最小透明度随强度变化
    
    print(f"[修复版] 强度 {intensity}: 范围={bleed_range}, Alpha={min_alpha}-{max_alpha}")

    for x in range(0, width, 2):  # 跳采样提高性能
        for y in range(0, height, 2):
            if gray_image.getpixel((x, y)) < 100:  # 深色区域（文字）
                # 根据强度决定渗透次数
                bleed_count = max(1, int(5 * intensity))
                
                for _ in range(bleed_count):
                    # 渗透方向和距离
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.randint(1, bleed_range)
                    
                    nx = int(x + distance * math.cos(angle))
                    ny = int(y + distance * math.sin(angle))
                    
                    if 0 <= nx < width and 0 <= ny < height:
                        # Alpha值基于强度
                        alpha = random.randint(min_alpha, max_alpha)
                        radius = random.randint(1, 2)
                        
                        draw.ellipse((nx - radius, ny - radius, nx + radius, ny + radius),
                                    fill=(0, 0, 0, alpha))

    # 根据强度调整模糊程度
    blur_radius = 0.5 + intensity * 1.0
    bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(blur_radius))

    # 确保原图为 RGBA 模式
    base_rgba = image.convert('RGBA')

    # 应用渗透叠加
    result = Image.alpha_composite(base_rgba, bleed_layer)

    if imageMode == "RGB":
        return result.convert('RGB')
    else:
        return result

def add_ink_bleed_effect_enhanced(image, intensity=0.3, imageMode="RGBA"):
    """增强版墨迹渗透效果 - 强度差异非常明显"""
    width, height = image.size

    # 创建多个渗透层来增强效果
    bleed_layers = []
    
    # 根据强度创建不同层数
    layer_count = max(1, int(3 * intensity))
    
    for layer in range(layer_count):
        bleed_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bleed_layer)
        
        gray_image = image.convert('L')
        
        # 每层的参数基于强度
        layer_intensity = intensity * (layer + 1) / layer_count
        
        for x in range(0, width, 2):
            for y in range(0, height, 2):
                if gray_image.getpixel((x, y)) < 100:
                    # 渗透概率基于强度
                    if random.random() < layer_intensity:
                        # 距离和大小基于强度
                        max_distance = int(2 + 3 * layer_intensity)
                        distance = random.randint(1, max_distance)
                        angle = random.uniform(0, 2 * math.pi)
                        
                        nx = int(x + distance * math.cos(angle))
                        ny = int(y + distance * math.sin(angle))
                        
                        if 0 <= nx < width and 0 <= ny < height:
                            # Alpha值明显基于强度
                            alpha = int(30 + 70 * layer_intensity)
                            radius = random.randint(1, int(1 + 2 * layer_intensity))
                            
                            draw.ellipse((nx - radius, ny - radius, nx + radius, ny + radius),
                                        fill=(0, 0, 0, alpha))
        
        # 每层单独模糊
        blur_radius = 0.3 + layer_intensity * 1.2
        bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(blur_radius))
        bleed_layers.append(bleed_layer)
    
    # 合并所有渗透层
    base_rgba = image.convert('RGBA')
    result = base_rgba.copy()
    
    for layer in bleed_layers:
        result = Image.alpha_composite(result, layer)
    
    if imageMode == "RGB":
        return result.convert('RGB')
    else:
        return result

def add_ink_bleed_effect_optimized(image, intensity=0.3, imageMode="RGBA"):
    """优化版墨迹渗透效果 - 性能更好，效果明显"""
    width, height = image.size

    # 使用numpy提高性能
    base_array = np.array(image.convert('RGBA'))
    
    # 创建渗透层
    bleed_array = np.zeros((height, width, 4), dtype=np.uint8)
    
    # 识别文字区域（灰度值<100）
    gray_array = np.array(image.convert('L'))
    text_mask = gray_array < 100
    
    # 根据强度调整参数
    max_distance = int(2 + 3 * intensity)
    base_alpha = int(30 * intensity)
    density = intensity  # 渗透密度
    
    print(f"[优化版] 强度 {intensity}: 距离={max_distance}, Alpha基准={base_alpha}")
    
    # 找到所有文字像素的坐标
    text_coords = np.argwhere(text_mask)
    
    for coord in text_coords:
        y, x = coord
        
        # 根据密度跳过一些像素
        if random.random() > density:
            continue
            
        # 生成渗透点
        for _ in range(int(3 * intensity)):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.randint(1, max_distance)
            
            ny = int(y + distance * math.sin(angle))
            nx = int(x + distance * math.cos(angle))
            
            if 0 <= ny < height and 0 <= nx < width:
                # 计算alpha值（距离越远越淡）
                distance_factor = 1 - (distance / max_distance)
                alpha = int(base_alpha * distance_factor * random.uniform(0.8, 1.2))
                alpha = max(10, min(100, alpha))
                
                radius = max(1, int(1 * intensity))
                
                # 在渗透层绘制圆点
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        cy, cx = ny + dy, nx + dx
                        if 0 <= cy < height and 0 <= cx < width:
                            if dx*dx + dy*dy <= radius*radius:
                                bleed_array[cy, cx, 3] = max(bleed_array[cy, cx, 3], alpha)
    
    # 转换为PIL图像并模糊
    bleed_layer = Image.fromarray(bleed_array, 'RGBA')
    bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(0.5 + intensity))
    
    # 合成结果
    base_rgba = image.convert('RGBA')
    result = Image.alpha_composite(base_rgba, bleed_layer)
    
    if imageMode == "RGB":
        return result.convert('RGB')
    else:
        return result

def create_test_image():
    """创建测试用的书法图像"""
    # 创建宣纸背景
    paper = Image.new('RGB', (400, 200), (248, 240, 228))
    draw = ImageDraw.Draw(paper)
    
    # 绘制书法文字
    try:
        # 尝试加载中文字体
        font = ImageFont.truetype("simkai.ttf", 48)  # 楷体
    except:
        try:
            font = ImageFont.truetype("simsun.ttc", 48)  # 宋体
        except:
            font = ImageFont.load_default()
    
    draw.text((120, 70), "水墨书法", fill=(30, 30, 30), font=font)
    
    return paper

def demo_all_ink_bleed_effects():
    """演示所有墨迹渗透效果"""
    
    print("=== 墨迹渗透效果演示 ===")
    
    # 创建测试图像
    test_image = create_test_image()
    test_image.save("00_original_test_image.png")
    print("✓ 创建测试图像: 00_original_test_image.png")
    
    # 测试不同强度
    intensities = [0.1, 0.3, 0.5, 0.8]
    
    # 1. 原始版本演示
    print("\n1. 原始版本演示:")
    for intensity in intensities:
        result = add_ink_bleed_effect_original(test_image.copy(), intensity)
        result.save(f"01_original_intensity_{intensity}.png")
        print(f"  ✓ 强度 {intensity}: 01_original_intensity_{intensity}.png")
    
    # 2. 修复版本演示
    print("\n2. 修复版本演示:")
    for intensity in intensities:
        result = add_ink_bleed_effect_fixed(test_image.copy(), intensity)
        result.save(f"02_fixed_intensity_{intensity}.png")
        print(f"  ✓ 强度 {intensity}: 02_fixed_intensity_{intensity}.png")
    
    # 3. 增强版本演示
    print("\n3. 增强版本演示:")
    for intensity in intensities:
        result = add_ink_bleed_effect_enhanced(test_image.copy(), intensity)
        result.save(f"03_enhanced_intensity_{intensity}.png")
        print(f"  ✓ 强度 {intensity}: 03_enhanced_intensity_{intensity}.png")
    
    # 4. 优化版本演示
    print("\n4. 优化版本演示:")
    for intensity in intensities:
        result = add_ink_bleed_effect_optimized(test_image.copy(), intensity)
        result.save(f"04_optimized_intensity_{intensity}.png")
        print(f"  ✓ 强度 {intensity}: 04_optimized_intensity_{intensity}.png")

def compare_specific_intensity():
    """对比特定强度下的不同版本效果"""
    
    test_image = create_test_image()
    target_intensity = 0.5
    
    print(f"\n=== 强度 {target_intensity} 的版本对比 ===")
    
    versions = {
        "original": add_ink_bleed_effect_original,
        "fixed": add_ink_bleed_effect_fixed,
        "enhanced": add_ink_bleed_effect_enhanced,
        "optimized": add_ink_bleed_effect_optimized
    }
    
    for name, function in versions.items():
        result = function(test_image.copy(), target_intensity)
        result.save(f"compare_{name}_intensity_{target_intensity}.png")
        print(f"✓ {name}版本: compare_{name}_intensity_{target_intensity}.png")

def practical_usage_example():
    """实际使用示例"""
    
    print("\n=== 实际使用示例 ===")
    
    # 场景1: 轻微渗透效果（传统书法）
    print("场景1: 传统书法 - 轻微渗透")
    calligraphy_image = create_test_image()
    subtle_effect = add_ink_bleed_effect_fixed(calligraphy_image, intensity=0.2)
    subtle_effect.save("practical_subtle_effect.png")
    print("✓ 传统书法轻微渗透: practical_subtle_effect.png")
    
    # 场景2: 明显渗透效果（水墨画风格）
    print("场景2: 水墨画风格 - 明显渗透")
    strong_effect = add_ink_bleed_effect_enhanced(calligraphy_image, intensity=0.6)
    strong_effect.save("practical_strong_effect.png")
    print("✓ 水墨画明显渗透: practical_strong_effect.png")
    
    # 场景3: 重度渗透效果（古画仿制）
    print("场景3: 古画仿制 - 重度渗透")
    heavy_effect = add_ink_bleed_effect_optimized(calligraphy_image, intensity=0.9)
    heavy_effect.save("practical_heavy_effect.png")
    print("✓ 古画重度渗透: practical_heavy_effect.png")

def performance_test():
    """性能测试"""
    
    import time
    
    print("\n=== 性能测试 ===")
    
    test_image = create_test_image()
    test_intensity = 0.5
    
    versions = {
        "原始版本": add_ink_bleed_effect_original,
        "修复版本": add_ink_bleed_effect_fixed,
        "增强版本": add_ink_bleed_effect_enhanced,
        "优化版本": add_ink_bleed_effect_optimized
    }
    
    for name, function in versions.items():
        start_time = time.time()
        result = function(test_image.copy(), test_intensity)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"{name}: {execution_time:.3f} 秒")
        
        # 保存结果
        result.save(f"performance_{name}.png")

# 主函数
if __name__ == "__main__":
    print("墨迹渗透效果测试开始...")
    
    # 演示所有效果
    demo_all_ink_bleed_effects()
    
    # 对比特定强度
    compare_specific_intensity()
    
    # 实际使用示例
    practical_usage_example()
    
    # 性能测试（可选）
    # performance_test()
    
    print("\n🎉 所有测试完成！")
    print("请查看生成的PNG文件来比较不同版本和强度的效果。")
    print("\n推荐使用:")
    print("  - 修复版本 (add_ink_bleed_effect_fixed): 平衡效果和性能")
    print("  - 优化版本 (add_ink_bleed_effect_optimized): 高性能需求")
    print("  - 增强版本 (add_ink_bleed_effect_enhanced): 追求最佳效果")