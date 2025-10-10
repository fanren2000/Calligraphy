from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random

def safe_get_font(font_path, size):
    """加载字体，失败则使用默认字体"""
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

def calculate_font_offset(font, char, seal_size, context=""):
    """根据字体和字符估算垂直偏移量"""
    # 可根据篆体特性微调
    return -seal_size // 20

def create_seal_layer(text, position, size=120, intensity=0.3, style='aged'):
    """生成单个印章图层，带老化效果"""
    canvas_size = (1400, 700)
    seal_layer = Image.new('RGBA', canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(seal_layer)

    seal_color = (180, 30, 30)
    border_color = (150, 20, 20)
    white_color = (255, 255, 255)

    x, y = position
    square_size = size

    # 绘制边框
    draw.rectangle([
        x - 4, y - 4,
        x + square_size + 4, y + square_size + 4
    ], outline=border_color, width=3)

    # 绘制印章主体
    draw.rectangle([x, y, x + square_size, y + square_size], fill=seal_color)

    # 加载字体
    seal_font = safe_get_font("方圆印章篆体.ttf", square_size // 3)

    # 绘制四字排列
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
            draw.text((char_x, char_y), chars[i], font=seal_font, fill=white_color)

    # 🎨 添加老化纹理
    if style == 'aged':
        pixels = seal_layer.load()
        for i in range(x, x + square_size):
            for j in range(y, y + square_size):
                r, g, b, a = pixels[i, j]
                if a > 0:
                    if random.random() < intensity:
                        variation = random.randint(-20, 20)
                        r = max(0, min(255, r + variation))
                        g = max(0, min(255, g + variation))
                        b = max(0, min(255, b + variation))
                    if random.random() < intensity / 2:
                        a = max(0, min(255, a - random.randint(0, 30)))
                    pixels[i, j] = (r, g, b, a)

    return seal_layer

def apply_seals(base_image, seals):
    """将多个印章图层依次叠加到基础图像"""
    base = base_image.convert('RGBA')
    for seal in seals:
        base = Image.alpha_composite(base, seal)
    return base.convert('RGB')




base = Image.new('RGB', (1400, 700), (242, 232, 212))

seal1 = create_seal_layer("乾坤正气", position=(180, 170), size=100, intensity=0.4, style='aged')
seal2 = create_seal_layer("官婉乾儿", position=(230, 120), size=100, intensity=0.3, style='clean')

final = apply_seals(base, [seal1, seal2])
final.save("layered_seals.png")
