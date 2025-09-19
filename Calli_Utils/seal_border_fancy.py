from PIL import Image, ImageDraw, ImageFont
import random
import os

def add_fancy_seal_with_border(image, text, position, size=120):
    """
    添加带装饰边框的复杂印章
    """
    draw = ImageDraw.Draw(image)
    
    seal_color = (180, 30, 30)
    border_color = (120, 20, 20)
    highlight_color = (200, 50, 50)
    white_color = (255, 255, 255)
    
    x, y = position
    
    draw.rectangle([x-4, y-4, x+size+4, y+size+4], outline=border_color, width=2)
    draw.rectangle([x-2, y-2, x+size+2, y+size+2], outline=highlight_color, width=1)
    draw.rectangle([x, y, x+size, y+size], outline=border_color, width=1)
    draw.rectangle([x, y, x+size, y+size], fill=seal_color)
    
    for i in range(10):
        pattern_x = x + random.randint(10, size-10)
        pattern_y = y + random.randint(10, size-10)
        pattern_size = random.randint(5, 15)
        draw.ellipse([pattern_x, pattern_y, pattern_x+pattern_size, pattern_y+pattern_size], fill=highlight_color)
    
    try:
        font_path = "C:/Windows/Fonts/simkai.ttf"
        if not os.path.exists(font_path): font_path = "simkai.ttf"
        seal_font = ImageFont.truetype(font_path, size//2)
    except: seal_font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=seal_font)
    text_x = x + (size - (text_bbox[2] - text_bbox[0])) // 2
    text_y = y + (size - (text_bbox[3] - text_bbox[1])) // 2
    
    draw.text((text_x+1, text_y+1), text, font=seal_font, fill=(100, 10, 10))
    draw.text((text_x, text_y), text, font=seal_font, fill=white_color)
    return image