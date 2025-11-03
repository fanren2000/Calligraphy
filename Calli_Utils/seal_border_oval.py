from PIL import Image, ImageDraw, ImageFont
import math
import os

def add_leisure_oval_seal(image, text, position, width=120, height=30, border_width=4):
    draw = ImageDraw.Draw(image)
    
    """添加闲章（在右上角）"""
    seal_content = text
    seal_size = 25
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
    # 绘制文字
    try:
        seal_font = ImageFont.truetype("HanYiWaWaZhuanJian-1.ttf", seal_size - 5)
    except:
        seal_font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), seal_content, font=seal_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = seal_x + (seal_width - text_width) // 2
    text_y = seal_y + (seal_height - (seal_size - 5)) // 2
    
    draw.text((text_x, text_y), seal_content, fill=seal_color, font=seal_font)
    
    print(f"🎨 闲章位置: ({seal_x}, {seal_y})")

    return image