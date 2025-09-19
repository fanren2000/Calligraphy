from PIL import Image, ImageDraw, ImageFont
import math
import os

def add_circular_seal_with_border(image, text, position, diameter=120, border_width=4):
    """
    添加传统圆形印章带边框
    """
    draw = ImageDraw.Draw(image)
    
    seal_color = (180, 30, 30)
    border_color = (150, 20, 20)
    white_color = (255, 255, 255)
    
    x, y = position
    radius = diameter // 2
    center_x, center_y = x + radius, y + radius
    
    outer_radius = radius + border_width
    draw.ellipse([
        center_x - outer_radius, center_y - outer_radius,
        center_x + outer_radius, center_y + outer_radius
    ], outline=border_color, width=border_width)
    
    draw.ellipse([
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius
    ], fill=seal_color)
    
    try:
        font_path = "C:/Windows/Fonts/simkai.ttf"
        if not os.path.exists(font_path): font_path = "simkai.ttf"
        seal_font = ImageFont.truetype(font_path, diameter//6)
    except: seal_font = ImageFont.load_default()
    
    if len(text) <= 2:
        text_bbox = draw.textbbox((0, 0), text, font=seal_font)
        text_x = center_x - (text_bbox[2] - text_bbox[0]) // 2
        text_y = center_y - (text_bbox[3] - text_bbox[1]) // 2
        draw.text((text_x, text_y), text, font=seal_font, fill=white_color)
    else:
        char_count = len(text)
        for i, char in enumerate(text):
            angle = 2 * math.pi * i / char_count - math.pi/2
            char_radius = radius * 0.7
            char_x = center_x + char_radius * math.cos(angle)
            char_y = center_y + char_radius * math.sin(angle)
            draw.text((char_x, char_y), char, font=seal_font, fill=white_color, anchor="mm")
    
    return image