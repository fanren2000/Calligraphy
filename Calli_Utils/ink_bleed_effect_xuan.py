from PIL import Image, ImageDraw, ImageFilter
import random
import math
import numpy as np


def add_ink_bleed_effect(image, intensity=0.3, imageMode="RGBA"):
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

def add_ink_bleed_effect_optimized(image, intensity=0.5, image_mode="RGBA"):
    """修复版优化墨迹渗透效果 - 强度差异明显"""
    width, height = image.size

    # 使用numpy提高性能
    base_array = np.array(image.convert('RGBA'))
    
    # 创建渗透层
    bleed_array = np.zeros((height, width, 4), dtype=np.uint8)
    
    # 识别文字区域（灰度值<100）
    gray_array = np.array(image.convert('L'))
    text_mask = gray_array < 100
    
    # 🔧 修复1: 增强参数映射
    intensity_clamped = max(0.1, min(10.0, intensity))  # 限制范围但允许较大值
    
    # 🔧 修复2: 重新设计参数计算
    max_distance = int(2 + 8 * intensity_clamped)       # 大幅增加距离范围
    base_alpha = int(20 + 80 * intensity_clamped)       # 增强Alpha基准值
    density = min(1.0, intensity_clamped * 0.5)         # 密度合理映射
    penetration_power = int(3 + 7 * intensity_clamped)  # 渗透力度
    
    print(f"[优化修复版] 强度:{intensity} -> 映射后:{intensity_clamped:.1f}")
    print(f"  参数: 距离={max_distance}, Alpha基准={base_alpha}, 密度={density:.2f}, 力度={penetration_power}")
    
    # 找到所有文字像素的坐标
    text_coords = np.argwhere(text_mask)
    
    # 🔧 修复3: 增加采样密度
    sample_rate = max(1, int(10 / intensity_clamped)) if intensity_clamped > 0.5 else 1
    sampled_coords = text_coords[::sample_rate] if sample_rate > 1 else text_coords
    
    print(f"  采样率: {sample_rate}, 处理像素: {len(sampled_coords)}/{len(text_coords)}")
    
    for coord in sampled_coords:
        y, x = coord
        
        # 🔧 修复4: 基于密度的跳过逻辑
        if random.random() > density:
            continue
            
        # 🔧 修复5: 增强渗透生成
        for _ in range(penetration_power):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.randint(1, max_distance)
            
            ny = int(y + distance * math.sin(angle))
            nx = int(x + distance * math.cos(angle))
            
            if 0 <= ny < height and 0 <= nx < width:
                # 🔧 修复6: 改进的Alpha计算
                distance_factor = 1.0 - (distance / max_distance)
                # 添加随机扰动
                random_factor = 0.7 + 0.6 * random.random()
                alpha = int(base_alpha * distance_factor * random_factor)
                alpha = max(10, min(255, alpha))  # 扩展范围到255
                
                # 🔧 修复7: 动态半径
                radius = max(1, int(1 + 3 * intensity_clamped * random.random()))
                
                # 在渗透层绘制圆点
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        cy, ny_val = y + dy, ny + dy  # 修复变量名冲突
                        cx, nx_val = x + dx, nx + dx
                        
                        if 0 <= cy < height and 0 <= cx < width:
                            if dx*dx + dy*dy <= radius*radius:
                                # 累积Alpha值，而不是取最大值
                                current_alpha = bleed_array[cy, cx, 3]
                                new_alpha = min(255, int(current_alpha) + alpha // 3)
                                bleed_array[cy, cx, 3] = new_alpha
    
    # 🔧 修复8: 动态模糊
    blur_radius = 0.5 + intensity_clamped * 2.0
    bleed_layer = Image.fromarray(bleed_array, 'RGBA')
    bleed_layer = bleed_layer.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # 合成结果
    base_rgba = image.convert('RGBA')
    result = Image.alpha_composite(base_rgba, bleed_layer)
    
    if image_mode == "RGB":
        return result.convert('RGB')
    else:
        return result
    
def add_ink_bleed_effect_enhanced(image, intensity=0.5, 
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
