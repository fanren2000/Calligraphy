from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
from .seal_texture_type import add_texture_and_aging

def apply_seal_safely(paper, seal, position):
    """安全地应用印章到撕边纸张"""
    
    # 确保都是RGBA模式
    if paper.mode != 'RGBA':
        paper = paper.convert('RGBA')
    if seal.mode != 'RGBA':
        seal = seal.convert('RGBA')
    
    # 方法：使用透明图层合成
    seal_layer = Image.new('RGBA', paper.size, (0, 0, 0, 0))
    seal_layer.paste(seal, position, seal)
    
    # 使用alpha合成，这会保留底层图像的alpha通道
    result = Image.alpha_composite(paper, seal_layer)
    
    return result

def create_basic_seal(text, size=400, border_width=10):
    # 创建红色背景
    img = Image.new('RGBA', (size, size), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制方形边框
    margin = 20
    draw.rectangle([margin, margin, size-margin, size-margin], 
                   outline=(200, 0, 0, 255), width=border_width)
    
    # 添加文字（这里需要中文字体）
    try:
        font = ImageFont.truetype("simsun.ttc", size//4)
    except:
        font = ImageFont.load_default()
    
    # 在印章中心添加文字
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill=(200, 0, 0, 255), font=font)
    
    return img

def create_circular_seal(text, size=400):
    """创建圆形闲章"""
    img = Image.new('RGBA', (size, size), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制圆形边框
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 outline=(200, 0, 0, 255), width=10)
    
    # 添加弧形文字
    try:
        font = ImageFont.truetype("simsun.ttc", size//6)
    except:
        font = ImageFont.load_default()
    
    # 将文字沿圆形排列（简化版）
    chars = list(text)
    char_count = len(chars)
    radius = size // 2 - 40
    
    for i, char in enumerate(chars):
        angle = 2 * math.pi * i / char_count - math.pi/2
        x = size // 2 + radius * math.cos(angle) - 10
        y = size // 2 + radius * math.sin(angle) - 10
        
        # 旋转文字以适应圆形
        char_img = Image.new('RGBA', (30, 30), (255, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        char_draw.text((0, 0), char, fill=(200, 0, 0, 255), font=font)
        
        rotated_char = char_img.rotate(math.degrees(angle) + 90, expand=True)
        img.paste(rotated_char, (int(x), int(y)), rotated_char)
    
    return img


def create_realistic_seal(text, seal_type="square", size=400):
    """创建具有质感的印章"""
    
    if seal_type == "square":
        img = create_basic_seal(text, size)
    else:  # circular
        img = create_circular_seal(text, size)
    
    # 添加纹理
    img = add_texture_and_aging(img)
    
    # 添加模糊效果模拟墨水扩散
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # 增强对比度
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    return img  