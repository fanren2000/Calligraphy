import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random
import math

def add_ink_bleed_effect_enhanced(image, intensity=1.0, vertical_soak=True, speckle=True, preserve_characters=True):
    """墨迹渗透增强版：方向性渗透 + 笔压模拟 + 噪点 + 保留文字清晰度"""
    width, height = image.size
    img_array = np.array(image)
    gray = np.mean(img_array, axis=2)

    # 创建文字掩码（深色区域）
    char_mask = (gray < 100)
    mask = char_mask.astype(np.uint8) * 255
    mask_img = Image.fromarray(mask)

    # 🧭 方向性渗透（垂直扩散）
    if vertical_soak:
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=0.5))  # horizontal softness
        mask_img = mask_img.filter(ImageFilter.BoxBlur(3))                # vertical soak
    else:
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=3))    # symmetric bleed

    # 🖌️ 笔压模拟：根据灰度深浅调整渗透强度
    blur_mask = np.array(mask_img) / 255.0
    pressure_map = (100 - np.clip(gray, 0, 100)) / 100.0  # 0.0 to 1.0
    bleed_strength = blur_mask * pressure_map * intensity * 80
    darken = bleed_strength.astype(np.uint8)

    # 应用暗化效果
    for c in range(3):
        img_array[..., c] = np.clip(img_array[..., c] - darken, 0, 255)

    # 🌿 随机噪点增强
    if speckle:
        for _ in range(width * height // 50):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            if np.mean(img_array[y, x]) > 180 and np.random.rand() < 0.3:
                img_array[y, x] = np.clip(img_array[y, x] - np.random.randint(10, 40), 0, 255)

    # ✅ 保留文字像素为纯黑
    if preserve_characters:
        img_array[char_mask] = np.array([0, 0, 0])

    return Image.fromarray(img_array)


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


def add_ink_bleed_effect_fusion(image, intensity=0.5, 
                               vertical_soak=True, 
                               pressure_sensitive=True,
                               preserve_characters=True,
                               speckle_density=0.3,
                               natural_randomness=0.7,
                               multi_layer=True,
                               image_mode="RGBA"):
    """
    融合版墨迹渗透效果 - 结合自然随机性与物理参数控制
    
    Args:
        image: 输入图像
        intensity: 渗透强度 (0.1-1.0)
        vertical_soak: 是否垂直方向渗透 (模拟重力)
        pressure_sensitive: 是否启用笔压感应
        preserve_characters: 是否保护文字清晰度
        speckle_density: 噪点密度 (0-1)
        natural_randomness: 自然随机度 (0-1)
        multi_layer: 是否使用多层渗透
        image_mode: 输出图像模式
    """
    
    # 参数验证和调整
    intensity = max(0.1, min(1.0, intensity))
    natural_randomness = max(0.1, min(1.0, natural_randomness))
    speckle_density = max(0, min(1.0, speckle_density))
    
    width, height = image.size
    
    # 转换为RGBA进行处理
    if image.mode != 'RGBA':
        base_rgba = image.convert('RGBA')
    else:
        base_rgba = image.copy()
    
    # 创建渗透图层
    bleed_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bleed_layer)
    
    # 获取灰度图像用于文字检测和笔压计算
    gray_image = image.convert('L')
    gray_array = np.array(gray_image)
    
    # 文字掩码（您的版本技术）
    char_mask = gray_array < 100
    
    # 笔压映射（您的版本技术）
    if pressure_sensitive:
        pressure_map = (100 - np.clip(gray_array, 0, 100)) / 100.0
    else:
        pressure_map = np.ones_like(gray_array, dtype=float)
    
    print(f"[融合版] 强度:{intensity}, 垂直渗透:{vertical_soak}, 笔压感应:{pressure_sensitive}")
    
    # 多层渗透机制（我的版本技术）
    if multi_layer:
        layer_count = max(1, int(3 * intensity))
    else:
        layer_count = 1
    
    # 方向性参数（您的版本技术）
    if vertical_soak:
        # 垂直渗透：y方向距离更大
        vertical_bias = 1.5
        horizontal_bias = 0.7
    else:
        # 各向同性渗透
        vertical_bias = 1.0
        horizontal_bias = 1.0
    
    # 逐层渗透（我的版本技术增强）
    for layer in range(layer_count):
        layer_intensity = intensity * (layer + 1) / layer_count
        
        # 动态参数计算（结合两个版本的优点）
        base_range = max(1, int(3 * layer_intensity))
        max_alpha = int(40 + 60 * layer_intensity * natural_randomness)
        min_alpha = int(10 + 20 * layer_intensity * natural_randomness)
        
        # 找到文字像素坐标
        text_coords = np.argwhere(char_mask)
        
        # 对每个文字像素应用渗透
        for coord in text_coords:
            y, x = coord
            
            # 基于笔压调整渗透强度（您的版本技术）
            pixel_pressure = pressure_map[y, x]
            if pixel_pressure < 0.3 and random.random() > 0.5:
                continue  # 低笔压区域减少渗透
            
            # 渗透次数基于强度和笔压
            bleed_count = max(1, int(3 * layer_intensity * pixel_pressure * natural_randomness))
            
            for _ in range(bleed_count):
                # 随机角度（我的版本技术）
                angle = random.uniform(0, 2 * math.pi)
                
                # 方向性距离调整（您的版本技术 + 我的随机性）
                base_distance = random.randint(1, base_range)
                
                # 应用方向偏差
                dx = base_distance * math.cos(angle) * horizontal_bias
                dy = base_distance * math.sin(angle) * vertical_bias
                
                # 最终位置
                nx = int(x + dx * (0.8 + 0.4 * random.random()))
                ny = int(y + dy * (0.8 + 0.4 * random.random()))
                
                if 0 <= nx < width and 0 <= ny < height:
                    # Alpha值计算（结合笔压和随机性）
                    base_alpha = random.randint(min_alpha, max_alpha)
                    distance_factor = 1.0 - (abs(dx) + abs(dy)) / (base_range * 2)
                    pressure_factor = 0.5 + 0.5 * pixel_pressure
                    final_alpha = int(base_alpha * distance_factor * pressure_factor)
                    
                    # 半径基于强度和随机性
                    radius = max(1, int(1 + 2 * layer_intensity * random.random()))
                    
                    # 绘制渗透点
                    draw.ellipse((nx - radius, ny - radius, nx + radius, ny + radius),
                                fill=(0, 0, 0, final_alpha))
    
    # 方向性模糊（您的版本技术增强）
    if vertical_soak:
        # 垂直渗透：水平模糊小，垂直模糊大
        bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(radius=0.3))
        bleed_layer = bleed_layer.filter(ImageFilter.BoxBlur(2))
    else:
        # 各向同性模糊
        blur_radius = 0.5 + intensity * 1.0
        bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    # 合成渗透效果
    result = Image.alpha_composite(base_rgba, bleed_layer)
    
    # 噪点效果（您的版本技术增强）
    if speckle_density > 0:
        result = add_speckle_effect(result, speckle_density, intensity)
    
    # 文字保护（您的版本技术）
    if preserve_characters:
        result = preserve_text_clarity(result, char_mask)
    
    # 输出模式转换
    if image_mode == "RGB":
        return result.convert('RGB')
    else:
        return result

def add_speckle_effect(image, density, intensity):
    """添加噪点效果（增强版）"""
    width, height = image.size
    img_array = np.array(image)
    
    # 噪点数量基于密度和图像大小
    speckle_count = int(width * height * density * 0.01)
    
    for _ in range(speckle_count):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        
        # 只在较亮区域添加噪点
        if np.mean(img_array[y, x]) > 180:
            if random.random() < 0.3:
                # 噪点强度基于主强度
                darken_amount = random.randint(5, int(25 * intensity))
                img_array[y, x] = np.clip(img_array[y, x] - darken_amount, 0, 255)
    
    return Image.fromarray(img_array)

def preserve_text_clarity(image, char_mask):
    """保护文字清晰度"""
    img_array = np.array(image)
    
    # 将文字区域恢复为纯黑色
    img_array[char_mask] = [0, 0, 0, 255]
    
    return Image.fromarray(img_array)

def create_ink_bleed_presets():
    """创建常用的预设配置"""
    
    presets = {
        "traditional": {
            "description": "传统书法效果 - 轻微垂直渗透",
            "params": {
                "intensity": 0.3,
                "vertical_soak": True,
                "pressure_sensitive": True,
                "preserve_characters": True,
                "speckle_density": 0.2,
                "natural_randomness": 0.6,
                "multi_layer": True
            }
        },
        "artistic": {
            "description": "艺术水墨效果 - 强烈随机渗透",
            "params": {
                "intensity": 0.7,
                "vertical_soak": False,
                "pressure_sensitive": False,
                "preserve_characters": False,
                "speckle_density": 0.5,
                "natural_randomness": 0.9,
                "multi_layer": True
            }
        },
        "realistic": {
            "description": "真实物理效果 - 精确的笔压和方向",
            "params": {
                "intensity": 0.5,
                "vertical_soak": True,
                "pressure_sensitive": True,
                "preserve_characters": True,
                "speckle_density": 0.3,
                "natural_randomness": 0.4,
                "multi_layer": True
            }
        },
        "subtle": {
            "description": "轻微渗透效果 - 保持文字清晰",
            "params": {
                "intensity": 0.2,
                "vertical_soak": True,
                "pressure_sensitive": True,
                "preserve_characters": True,
                "speckle_density": 0.1,
                "natural_randomness": 0.5,
                "multi_layer": False
            }
        }
    }
    
    return presets

def apply_ink_bleed_preset(image, preset_name="traditional"):
    """应用预设配置"""
    presets = create_ink_bleed_presets()
    
    if preset_name not in presets:
        print(f"预设 '{preset_name}' 不存在，使用传统预设")
        preset_name = "traditional"
    
    preset = presets[preset_name]
    print(f"应用预设: {preset_name} - {preset['description']}")
    
    return add_ink_bleed_effect_fusion(image, **preset['params'])

def demo_fusion_version():
    """演示融合版本的效果"""
    
    print("=== 融合版墨迹渗透效果演示 ===\n")
    
    # 创建测试图像
    test_image = create_test_image()
    test_image.save("fusion_test_original.png")
    
    # 测试不同预设
    presets = create_ink_bleed_presets()
    
    for preset_name, preset_info in presets.items():
        print(f"🎨 测试预设: {preset_name}")
        print(f"   描述: {preset_info['description']}")
        
        result = apply_ink_bleed_preset(test_image, preset_name)
        result.save(f"fusion_preset_{preset_name}.png")
        print(f"   ✅ 保存: fusion_preset_{preset_name}.png\n")
    
    # 测试自定义参数
    print("🔧 测试自定义参数组合:")
    
    custom_params = [
        {"intensity": 0.8, "vertical_soak": True, "preserve_characters": False},
        {"intensity": 0.4, "vertical_soak": False, "natural_randomness": 0.9},
        {"intensity": 0.6, "pressure_sensitive": False, "speckle_density": 0.8}
    ]
    
    for i, params in enumerate(custom_params):
        result = add_ink_bleed_effect_fusion(test_image, **params)
        result.save(f"fusion_custom_{i+1}.png")
        print(f"   ✅ 自定义组合 {i+1}: fusion_custom_{i+1}.png")

def compare_fusion_with_originals():
    """对比融合版与原始版本"""
    
    print("=== 版本对比测试 ===\n")
    
    test_image = create_test_image()
    
    # 您的原始版本（简化调用）
    # your_original = your_enhanced_function(test_image, intensity=0.5)
    # your_original.save("comparison_your_original.png")
    
    # 我的原始版本
    my_original = add_ink_bleed_effect_enhanced(test_image, intensity=0.5)
    my_original.save("comparison_my_original.png")
    
    # 融合版本
    fusion_result = add_ink_bleed_effect_fusion(test_image, intensity=0.5)
    fusion_result.save("comparison_fusion.png")
    
    print("对比文件已生成:")
    # print("  - comparison_your_original.png (您的原始版本)")
    print("  - comparison_my_original.png (我的原始版本)")
    print("  - comparison_fusion.png (融合版本)")

def create_test_image():
    """创建测试书法图像"""
    paper = Image.new('RGB', (400, 200), (248, 240, 228))
    draw = ImageDraw.Draw(paper)
    
    try:
        font = ImageFont.truetype("simkai.ttf", 48)
    except:
        try:
            font = ImageFont.truetype("simsun.ttc", 48)
        except:
            font = ImageFont.load_default()
    
    draw.text((120, 70), "水墨融合", fill=(30, 30, 30), font=font)
    return paper

def fusion_features_summary():
    """融合特点总结"""
    
    print("=== 融合版核心特点 ===\n")
    
    features = [
        "🎯 参数丰富性: 继承您的完整参数体系",
        "🎨 自然随机性: 融合我的多层随机算法", 
        "📐 物理真实性: 保留您的方向性和笔压模拟",
        "🔒 文字保护: 完善的文字清晰度保护",
        "⚡ 性能平衡: NumPy + PIL 混合优化",
        "🎪 艺术可控: 从真实到艺术的连续调节",
        "🔧 易用性: 预设配置 + 精细调节"
    ]
    
    print("融合版结合了两个版本的精华:")
    for feature in features:
        print(f"  {feature}")
    
    print("\n💡 推荐使用场景:")
    scenarios = [
        "传统书法数字化 - 使用 'traditional' 预设",
        "艺术创作 - 使用 'artistic' 预设或调节 natural_randomness",
        "物理模拟 - 开启 vertical_soak 和 pressure_sensitive",
        "文字清晰优先 - 开启 preserve_characters",
        "性能要求高 - 关闭 multi_layer"
    ]
    
    for scenario in scenarios:
        print(f"  • {scenario}")

# 运行演示
if __name__ == "__main__":
    fusion_features_summary()
    demo_fusion_version()
    compare_fusion_with_originals()
    
    print("\n🎉 融合版函数创建完成！")
    print("这个版本既保持了您参数的丰富性，又融入了我的自然随机算法")