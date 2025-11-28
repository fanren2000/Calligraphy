from PIL import Image, ImageDraw, ImageFont
import math
import os

def add_leisure_oval_seal(image, text, position, width=120, height=30, border_width=4):
    draw = ImageDraw.Draw(image)
    
    """添加闲章（在右上角）"""
    seal_text = text
    seal_size = max(width, height)
    seal_color = "#8B0000"
    
    # 位置：右上角
    seal_x, seal_y = position
    
    # 绘制椭圆形闲章
    seal_width = width
    seal_height = height
    
    # 绘制椭圆（简化为圆角矩形）
    draw.rounded_rectangle([
        seal_x, seal_y,
        seal_x + seal_width, 
        seal_y + seal_height
    ], radius=20, outline=seal_color, width=border_width)

    # 计算葫芦内部实际可用空间
    inner_top = 0.35 * seal_size    # 顶部边界
    inner_bottom = 0.85 * seal_size # 底部边界  
    inner_left = 0.38 * seal_size   # 左侧边界
    inner_right = 0.62 * seal_size  # 右侧边界
    
    inner_height = inner_bottom - inner_top
    inner_width = inner_right - inner_left

    # 字体大小计算
    text_length = len(seal_text)
    
    # 强制使用小字体
    if text_length == 2:
        font_size = int(seal_size * 0.45)
    elif text_length == 3:
        font_size = int(seal_size * 0.30)
    elif text_length == 4:
        font_size = int(seal_size * 0.23)
    else:
        font_size = int(seal_size * 0.10)
    
    font_size = max(12, font_size)

    # 绘制文字
    try:
        seal_font = ImageFont.truetype("HanYiWaWaZhuanJian-1.ttf", font_size)
    except:
        seal_font = ImageFont.load_default()
    
    # text_bbox = draw.textbbox((0, 0), seal_content, font=seal_font)
    # text_width = text_bbox[2] - text_bbox[0]
    # text_height = text_bbox[3] - text_bbox[1]
    # text_x = seal_x + (seal_width - text_width) // 2
    # text_y = seal_y + (seal_height - (seal_size - 5)) // 2

    # 计算每个字符的实际尺寸
    char_heights = []
    char_widths = []
    
    for char in seal_text:
        bbox = draw.textbbox((0, 0), char, font=seal_font)
        char_heights.append(bbox[3] - bbox[1])
        char_widths.append(bbox[2] - bbox[0])
    
    # 计算总高度（包括间距）
    spacing = font_size * 0.1  # 较小的间距
    total_text_width = sum(char_widths) + (text_length - 1) * spacing
    total_text_height = sum(char_heights) + (text_length - 1) * spacing
    
    # **关键修正：使用葫芦内部空间的中心，而不是整个图片的中心**
    text_center_x = (inner_left + inner_right) // 2
    text_center_y = (inner_top + inner_bottom) // 2
    
    # **修正起始位置：从中心向上偏移一半文字高度**
    start_y = text_center_y - total_text_height // 2
    
    print(f"文字总高度: {total_text_height:.1f}")
    print(f"内部空间中心Y: {text_center_y:.1f}")
    print(f"文字起始Y: {start_y:.1f}")
    
    # 绘制文字
    seal_x += 3
    seal_y += 5
    
    if seal_width > seal_height:
        text_x = seal_x
        text_y = seal_y
        draw.text((text, text_y), seal_text, fill=seal_color, font=seal_font)
    else:
        current_y = seal_y
        current_x = seal_x
        for i, char in enumerate(seal_text):
            char_width = char_widths[i]
            # x = text_center_x - char_width // 2
            draw.text((current_x, current_y), char, fill=seal_color, font=seal_font)
            current_y += char_heights[i] + spacing
    
    
    print(f"🎨 闲章位置: ({seal_x}, {seal_y})")

    return image