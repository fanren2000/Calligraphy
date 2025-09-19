from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

def add_antique_seal_with_border(image, text, position, size=100):
    """
    添加仿古印章效果带边框
    """
    draw = ImageDraw.Draw(image)
    
    seal_color = (170, 40, 40)
    border_color = (130, 25, 25)
    antique_color = (190, 60, 60)
    
    x, y = position
    center_x, center_y = x + size//2, y + size//2
    
    border_points = []
    for i in range(0, 360, 10):
        angle = math.radians(i)
        variation = size * 0.05 * (0.5 + 0.5 * math.sin(angle * 3))
        radius = size//2 + variation + 6
        bx = center_x + radius * math.cos(angle)
        by = center_y + radius * math.sin(angle)
        border_points.append((bx, by))
    
    draw.polygon(border_points, outline=border_color, width=3)
    
    seal_points = []
    for i in range(0, 360, 15):
        angle = math.radians(i)
        variation = size * 0.03 * (0.5 + 0.5 * math.cos(angle * 4))
        radius = size//2 + variation
        sx = center_x + radius * math.cos(angle)
        sy = center_y + radius * math.sin(angle)
        seal_points.append((sx, sy))
    
    draw.polygon(seal_points, fill=seal_color)
    
    try:
        font_path = "C:/Windows/Fonts/simkai.ttf"
        if not os.path.exists(font_path): font_path = "simkai.ttf"
        seal_font = ImageFont.truetype(font_path, size//2)
    except: seal_font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=seal_font)
    text_x = center_x - (text_bbox[2] - text_bbox[0]) // 2 + random.randint(-2, 2)
    text_y = center_y - (text_bbox[3] - text_bbox[1]) // 2 + random.randint(-2, 2)
    
    draw.text((text_x, text_y), text, font=seal_font, fill=(255, 235, 235))
    
    for _ in range(20):
        ox = random.randint(x, x + size)
        oy = random.randint(y, y + size)
        if random.random() > 0.5: draw.point((ox, oy), fill=antique_color)
        else: draw.point((ox, oy), fill=(255, 255, 255, 100))
    
    return image