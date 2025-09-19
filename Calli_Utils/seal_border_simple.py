from PIL import Image, ImageDraw, ImageFont
import os

def add_seal_with_border(image, text, position, size=100, border_width=3):
    """
    添加简单的矩形边框印章效果
    """
    draw = ImageDraw.Draw(image)
    
    seal_color = (180, 30, 30)
    border_color = (150, 20, 20)
    
    x, y = position
    
    draw.rectangle([
        x - border_width, y - border_width,
        x + size + border_width, y + size + border_width
    ], outline=border_color, width=border_width)
    
    draw.rectangle([x, y, x + size, y + size], fill=seal_color)
    
    try:
        font_path = "C:/Windows/Fonts/simkai.ttf"
        if not os.path.exists(font_path): font_path = "simkai.ttf"
        seal_font = ImageFont.truetype(font_path, size//3)
    except: seal_font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=seal_font)
    text_x = x + (size - (text_bbox[2] - text_bbox[0])) // 2
    text_y = y + (size - (text_bbox[3] - text_bbox[1])) // 2
    
    draw.text((text_x, text_y), text, font=seal_font, fill=(255, 255, 255))
    return image