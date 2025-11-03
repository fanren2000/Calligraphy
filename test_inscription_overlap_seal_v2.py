from PIL import Image, ImageDraw, ImageFont, ImageFilter
from Utils.font_tools import safe_get_font
from Utils.date_format_tools import get_vertical_lunar_date
from Calli_Utils.seal_border_fancy_4char import add_four_character_seal, calculate_font_offset

def add_four_character_seal_transparent_fixed(image, text, position, size=120, opacity=0.7):
    """完全修复的透明印章函数"""
    
    # 🎯 关键修复1: 确保输入输出都是RGBA
    original_mode = image.mode
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
        print(f"🔄 图像模式转换: {original_mode} -> RGBA")
    
    # 🎯 关键修复2: 创建完全透明的图层
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal_layer)
    
    x, y = position
    square_size = size

    # 🎯 关键修复3: 正确的透明度计算
    bg_alpha = int(255 * opacity)  # 背景透明度
    border_alpha = int(255 * min(1.0, opacity + 0.2))  # 边框稍深
    
    print(f"🎯 透明度参数: opacity={opacity}, bg_alpha={bg_alpha}, border_alpha={border_alpha}")

    # 绘制半透明印章背景
    seal_bg_color = (180, 30, 30, bg_alpha)
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_bg_color)
    
    # 绘制印章边框
    border_color = (150, 20, 20, border_alpha)
    draw.rectangle([x, y, x + square_size, y + square_size], 
                  outline=border_color, width=3)

    # 加载字体
    try:
        seal_font = safe_get_font("方圆印章篆体.ttf", square_size // 3)
    except:
        seal_font = ImageFont.load_default()

    # 🎯 关键修复4: 确保文字不透明
    text_color = (255, 255, 255, 255)  # 文字完全不透明

    if len(text) == 4:
        chars = list(text)
        cell_size = square_size // 2
        font_offset = calculate_font_offset(seal_font, chars[0], square_size, "印章篆体")

        centers = [
            (x + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size // 2 + font_offset),
            (x + cell_size // 2, y + cell_size + cell_size // 2 + font_offset),
            (x + cell_size + cell_size // 2, y + cell_size + cell_size // 2 + font_offset)
        ]

        for i, (center_x, center_y) in enumerate(centers):
            char_bbox = draw.textbbox((0, 0), chars[i], font=seal_font)
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3] - char_bbox[1]
            char_x = center_x - char_width // 2
            char_y = center_y - char_height // 2
            
            # 🎯 使用正确的文字颜色
            draw.text((char_x, char_y), chars[i], font=seal_font, fill=text_color)

    # 🎯 关键修复5: 使用alpha_composite确保透明度
    result = Image.alpha_composite(image, seal_layer)
    
    # 🎯 关键修复6: 恢复原始模式（如果需要）
    if original_mode == "RGB":
        result = result.convert('RGB')
        print("🔄 图像模式恢复: RGBA -> RGB")
    
    print(f"✅ 透明印章完成 - 实际透明度: {opacity}")
    return result

def add_seal_with_debug_transparency(image, text, position, size=120, opacity=0.7):
    """带调试信息的透明印章"""
    
    print(f"🔧 透明度调试开始: opacity={opacity}")
    
    original_mode = image.mode
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
        print(f"   模式转换: {original_mode} -> RGBA")
    
    # 创建印章图层
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal_layer)
    
    x, y = position
    square_size = size
    
    # 计算alpha值
    bg_alpha = int(255 * opacity)
    border_alpha = int(255 * min(1.0, opacity + 0.2))
    
    print(f"   计算Alpha值: bg_alpha={bg_alpha}, border_alpha={border_alpha}")
    
    # 测试绘制不同透明度的区域
    test_colors = [
        ((255, 0, 0, bg_alpha), "印章背景"),
        ((0, 255, 0, border_alpha), "印章边框"), 
        ((0, 0, 255, 255), "测试文字")
    ]
    
    # 绘制测试区域
    for i, (color, desc) in enumerate(test_colors):
        test_x = x + i * 30
        draw.rectangle([test_x, y-30, test_x+20, y-10], fill=color)
        draw.text((test_x, y-25), desc, fill=(0, 0, 0, 255))
        print(f"   绘制{desc}: {color}")
    
    # 绘制实际印章
    seal_bg_color = (180, 30, 30, bg_alpha)
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_bg_color)
    
    border_color = (150, 20, 20, border_alpha)
    draw.rectangle([x, y, x + square_size, y + square_size], 
                  outline=border_color, width=3)
    
    # 添加文字
    try:
        font = safe_get_font("方圆印章篆体.ttf", square_size // 3)
    except:
        font = ImageFont.load_default()
    
    if len(text) == 4:
        chars = list(text)
        cell_size = square_size // 2
        
        for i, char in enumerate(chars):
            row = i // 2
            col = i % 2
            char_x = x + col * cell_size + 15
            char_y = y + row * cell_size + 15
            draw.text((char_x, char_y), char, fill=(255, 255, 255, 255), font=font)
    
    # 合成
    result = Image.alpha_composite(image, seal_layer)
    
    if original_mode == "RGB":
        result = result.convert('RGB')
    
    print(f"✅ 透明度调试完成")
    return result

def test_minimal_transparency():
    """最小化透明度测试"""
    
    print("\n🎯 最小化透明度测试:")

    # 添加文字
    try:
        font = safe_get_font("方圆印章篆体.ttf", 120 // 3)
    except:
        font = ImageFont.load_default()
    
    # 创建最简单的测试
    base = Image.new('RGB', (200, 200), 'white')
    draw = ImageDraw.Draw(base)
    draw.text((80, 80), "文字", fill='black', font=font)
    base.save("minimal_base.png")
    
    # 转换为RGBA
    base_rgba = base.convert('RGBA')
    
    # 创建完全透明的图层
    layer = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    layer_draw = ImageDraw.Draw(layer)
    
    # 直接绘制半透明矩形
    test_opacity = 0.3
    test_alpha = int(255 * test_opacity)
    layer_draw.rectangle([50, 50, 150, 150], fill=(255, 0, 0, test_alpha))
    
    print(f"   测试透明度: {test_opacity} -> Alpha: {test_alpha}")
    print(f"   使用颜色: (255, 0, 0, {test_alpha})")
    
    # 保存图层本身
    layer.save("minimal_layer.png")
    
    # 合成
    result = Image.alpha_composite(base_rgba, layer)
    result.save("minimal_result.png")
    
    print("   ✅ 保存 minimal_*.png 文件")
    print("   请检查 minimal_layer.png - 应该看到半透明红色")
    print("   请检查 minimal_result.png - 应该看到文字透过红色")

# test_minimal_transparency()

# # 方法1: 使用完全修复版本
author_name = "玻璃耗子"
# 添加文字
try:
    font = safe_get_font("方圆印章篆体.ttf", 120 // 3)
except:
    font = ImageFont.load_default()

# 创建最简单的测试
image = Image.new('RGB', (600, 600), 'white')
draw = ImageDraw.Draw(image)
draw.text((80, 80), "文字", fill='black', font=font)

image = add_four_character_seal_transparent_fixed(
    image, author_name, (20, 20), 
    opacity=0.6  # 60%透明度
)

# # 方法2: 使用调试版本查看问题
# image = add_seal_with_debug_transparency(
#     image, author_name, (120, 400),
#     opacity=0.6
# )

# # 方法3: 测试不同透明度
for opacity in [0.3, 0.5, 0.8]:
    test_img = add_four_character_seal_transparent_fixed(
        image.copy(), author_name, (100, 150), 
        opacity=opacity
    )
    test_img.save(f"test_opacity_{opacity}.png")