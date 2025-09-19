from PIL import Image, ImageDraw, ImageFont
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Calli_Utils import (
    add_seal_with_border,
    add_circular_seal_with_border,
    add_fancy_seal_with_border,
    add_antique_seal_with_border
)

def create_example_image():
    image = Image.new('RGB', (800, 600), color=(245, 235, 215))
    draw = ImageDraw.Draw(image)
    
    try:
        font_path = "C:/Windows/Fonts/simkai.ttf"
        if not os.path.exists(font_path): font_path = "simkai.ttf"
        title_font = ImageFont.truetype(font_path, 30)
        text_font = ImageFont.truetype(font_path, 20)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    draw.text((300, 30), "印章效果示例", font=title_font, fill=(0, 0, 0))
    
    image = add_seal_with_border(image, "印", (100, 100), 80)
    draw.text((100, 190), "简单边框", font=text_font, fill=(0, 0, 0))
    
    image = add_circular_seal_with_border(image, "印", (250, 100), 80)
    draw.text((250, 190), "圆形边框", font=text_font, fill=(0, 0, 0))
    
    image = add_fancy_seal_with_border(image, "印", (400, 100), 80)
    draw.text((400, 190), "装饰边框", font=text_font, fill=(0, 0, 0))
    
    image = add_antique_seal_with_border(image, "印", (550, 100), 80)
    draw.text((550, 190), "仿古边框", font=text_font, fill=(0, 0, 0))
    
    image.save("seal_examples.png")
    print("✅ 印章示例图像已保存: seal_examples.png")

if __name__ == "__main__": create_example_image()