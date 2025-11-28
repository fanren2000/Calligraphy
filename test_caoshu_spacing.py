

from PIL import Image, ImageDraw, ImageFont
import os

def create_vertical_calligraphy_with_smart_spacing(text_chars, output_path, base_font_size=120):
    """
    根据笔画特征智能调整垂直间距
    """
    # 加载字体
    try:
        font = ImageFont.truetype("FZDaCaoS-R-GB.ttf", base_font_size)
    except:
        font = ImageFont.load_default()
    
    # 笔画数据库（简化版）
    stroke_data = {
        "一": {"strokes": 1, "structure": "simple", "density": "sparse"},
        "马": {"strokes": 3, "structure": "complex", "density": "medium"},
        "当": {"strokes": 6, "structure": "balanced", "density": "dense"},
        "先": {"strokes": 6, "structure": "balanced", "density": "dense"}
    }
    
    temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 计算每个字的尺寸和间距
    char_data = []
    for char in text_chars:
        bbox = temp_draw.textbbox((0, 0), char, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        char_info = stroke_data.get(char, {"strokes": 5, "structure": "balanced", "density": "medium"})
        char_data.append({
            "char": char,
            "width": width,
            "height": height,
            "strokes": char_info["strokes"],
            "density": char_info["density"],
            "structure": char_info["structure"]
        })
    
    # 智能计算间距
    spacings = calculate_smart_spacings(char_data)
    
    # 创建画布
    total_height = sum([data["height"] for data in char_data]) + sum(spacings)
    max_width = max([data["width"] for data in char_data])
    
    margin = 50
    canvas_width = max_width + margin * 2
    canvas_height = total_height + margin * 2
    
    image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 书写文字
    current_y = margin
    x_position = margin + max_width // 2
    
    for i, data in enumerate(char_data):
        char_x = x_position - data["width"] // 2
        
        # 绘制文字
        shadow_color = (0, 0, 0, 80)
        text_color = (0, 0, 0, 255)
        
        draw.text((char_x + 2, current_y + 2), data["char"], font=font, fill=shadow_color)
        draw.text((char_x, current_y), data["char"], font=font, fill=text_color)
        
        # 更新位置（使用智能间距）
        if i < len(char_data) - 1:
            current_y += data["height"] + spacings[i]
    
    image.save(output_path)
    print(f"智能间距书法已创建: {output_path}")
    return image, spacings

def calculate_smart_spacings(char_data):
    """
    根据字的特征智能计算间距
    """
    spacings = []
    
    for i in range(len(char_data) - 1):
        current_char = char_data[i]
        next_char = char_data[i + 1]
        
        # 基础间距
        base_spacing = -20
        
        # 根据笔画密度调整
        density_adjustment = 0
        if current_char["density"] == "sparse" and next_char["density"] == "dense":
            density_adjustment = -8  # 稀疏字接密集字，间距更小
        elif current_char["density"] == "dense" and next_char["density"] == "sparse":
            density_adjustment = 5   # 密集字接稀疏字，间距稍大
        
        # 根据结构特征调整
        structure_adjustment = 0
        if current_char["structure"] == "complex" or next_char["structure"] == "complex":
            structure_adjustment = -5  # 复杂结构字，间距更紧凑
        
        # 最终间距
        final_spacing = base_spacing + density_adjustment + structure_adjustment
        spacings.append(final_spacing)
    
    return spacings

# 针对"一马当先"的专用间距方案
def create_yimadangxian_smart_spacing():
    chars = ["一", "马", "当", "先"]
    
    # 专业书法间距方案
    professional_spacings = {
        "traditional": [-15, -25, -20],  # 传统紧凑型
        "balanced": [-18, -22, -18],     # 平衡型（推荐）
        "expressive": [-12, -28, -15]    # 表现型
    }
    
    for style, spacings in professional_spacings.items():
        create_custom_spacing_version(chars, f"一马当先_间距_{style}.png", spacings)

def create_custom_spacing_version(chars, output_path, custom_spacings):
    """
    创建自定义间距版本
    """
    try:
        font = ImageFont.truetype("FZDaCaoS-R-GB.ttf", 130)
    except:
        font = ImageFont.load_default()
    
    temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 计算字符尺寸
    char_sizes = []
    for char in chars:
        bbox = temp_draw.textbbox((0, 0), char, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        char_sizes.append((width, height))
    
    # 计算总高度
    total_height = sum([size[1] for size in char_sizes]) + sum(custom_spacings)
    max_width = max([size[0] for size in char_sizes])
    
    margin = 50
    image = Image.new('RGBA', (max_width + margin * 2, total_height + margin * 2), 
                     (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 书写
    current_y = margin
    x_position = margin + max_width // 2
    
    for i, (char, (width, height)) in enumerate(zip(chars, char_sizes)):
        char_x = x_position - width // 2
        
        # 绘制
        shadow_color = (0, 0, 0, 80)
        text_color = (0, 0, 0, 255)
        
        draw.text((char_x + 2, current_y + 2), char, font=font, fill=shadow_color)
        draw.text((char_x, current_y), char, font=font, fill=text_color)
        
        # 使用自定义间距
        if i < len(chars) - 1:
            current_y += height + custom_spacings[i]
    
    image.save(output_path)
    print(f"自定义间距版本: {output_path}")
    return image

# 高级版：动态视觉间距
def create_dynamic_visual_spacing(text_chars, output_path):
    """
    基于视觉密度的动态间距调整
    """
    try:
        font = ImageFont.truetype("FZDaCaoS-R-GB.ttf", 125)
    except:
        font = ImageFont.load_default()
    
    # 视觉密度评估（简化）
    visual_density = {
        "一": 0.2,   # 很低
        "马": 0.7,   # 较高
        "当": 0.8,   # 高
        "先": 0.75   # 较高
    }
    
    temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    char_sizes = []
    for char in text_chars:
        bbox = temp_draw.textbbox((0, 0), char, font=font)
        char_sizes.append((bbox[2] - bbox[0], bbox[3] - bbox[1]))
    
    # 动态计算间距
    dynamic_spacings = []
    for i in range(len(text_chars) - 1):
        current_density = visual_density.get(text_chars[i], 0.5)
        next_density = visual_density.get(text_chars[i + 1], 0.5)
        
        # 间距公式：基础值 + 密度差异调整
        density_diff = current_density - next_density
        spacing = -20 + int(density_diff * 15)  # 根据密度差异调整
        
        dynamic_spacings.append(max(-35, min(-5, spacing)))  # 限制范围
    
    return create_custom_spacing_version(text_chars, output_path, dynamic_spacings)

# 使用示例
if __name__ == "__main__":
    chars = ["一", "马", "当", "先"]
    
    # 1. 智能间距版本
    image, spacings = create_vertical_calligraphy_with_smart_spacing(
        chars, "一马当先_智能间距.png"
    )
    print(f"智能计算的间距: {spacings}")
    
    # 2. 专业间距方案
    create_yimadangxian_smart_spacing()
    
    # 3. 动态视觉间距
    create_dynamic_visual_spacing(chars, "一马当先_动态间距.png")
    
    # 4. 特别推荐的平衡版本
    create_custom_spacing_version(
        chars, 
        "一马当先_推荐间距.png", 
        [-18, -22, -18]  # 平衡型间距
    )