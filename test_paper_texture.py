from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random
import math

from Utils import safe_get_font
from Calli_Utils import add_xuan_paper_texture, add_xuan_paper_texture_enhanced, add_ink_bleed_effect, add_ink_bleed_effect_enhanced, add_realistic_paper_texture, apply_paper_texture

def create_authentic_calligraphy(poem_text, author, output_path):
    """创建具有真实纸张质感的书法作品"""
    
    # 创建基础图像
    width, height = 1400, 800
    
    
    print("添加纸张质感...")
    
    # 1. 首先添加宣纸纹理
    # image = add_xuan_paper_texture(width, height) 

    image = add_xuan_paper_texture_enhanced(width, height) 
  
    draw = ImageDraw.Draw(image)
    
    # 绘制书法内容（省略具体绘制代码）
    poem_font = safe_get_font("方正行楷_GBK.ttf", 300)
    draw.text((100, 100), "乾坤正气", font=poem_font, fill=(0, 0, 0))

    # 2. 添加墨迹渗透效果
    image = add_ink_bleed_effect_enhanced(image, 0.2)
    # image = add_ink_bleed_effect(image, 0.2)
    
    # 3. 最终微调
    image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # 保存结果
    image.save(output_path, quality=95, dpi=(300, 300))
    print(f"真实质感书法作品已保存: {output_path}")
    
    return image

def create_texture_preview():
    """创建纸张质感预览"""
    
    textures = [
        ("宣纸质感", "xuan"),
        ("米纸质感", "rice"), 
        ("羊皮纸质感", "parchment")
    ]
    
    preview = Image.new('RGB', (1000, 600), (255, 255, 255))
    draw = ImageDraw.Draw(preview)
    
    draw.text((400, 20), "不同纸张质感效果对比", fill=(0, 0, 0))
    
    for i, (name, paper_type) in enumerate(textures):
        # 创建样本
        sample = Image.new('RGB', (300, 200), (245, 235, 215))
        sample_texture = add_realistic_paper_texture(300, 200, paper_type)
        
        # 添加文字说明
        sample_draw = ImageDraw.Draw(sample_texture)
        sample_draw.text((20, 20), f"这是{name}", fill=(100, 100, 100))
        
        # 粘贴到预览图
        x = 50 + i * 320
        y = 100
        preview.paste(sample_texture, (x, y))
        draw.text((x, y + 220), name, fill=(0, 0, 0))
    
    preview.save("纸张质感预览.png", quality=95)
    return preview

if __name__ == "__main__":
    # 生成质感预览
    #create_texture_preview()
    #print("生成完成：纸张质感预览.png")
    
    # 创建真实质感书法作品
    create_authentic_calligraphy("静夜思", "李白", "真实质感书法_宣纸.png")