from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont
import random
import math
import numpy as np


from Calli_Utils import add_ink_bleed_effect_enhanced, add_subtle_ink_effect, add_ink_bleed_effect_parchment
from Calli_Utils import add_xuan_paper_texture_enhanced, add_rice_paper_texture_enhanced, add_parchment_texture_enhanced

def add_material_specific_ink_effect(image, paper_type):
    """根据纸张类型添加特定的墨迹效果"""
    
    if paper_type == "xuan":
        # 宣纸：明显的渗透和扩散
        return add_ink_bleed_effect_enhanced(image, 0.8)
    
    elif paper_type == "rice":
        # 米纸：轻微渗透，边缘清晰
        return add_subtle_ink_effect(image, 0.3)
    
    elif paper_type == "parchment":
        # 羊皮纸：不均匀吸收，有纹理感
        return add_ink_bleed_effect_parchment(image)
    
    else:
        return image

def create_material_comparison():
    """创建三种纸张材质的对比图"""
    
    width, height = 400, 300
    comparison = Image.new('RGB', (1200, 900), (255, 255, 255))
    draw = ImageDraw.Draw(comparison)
    
    # 加载字体
    try:
        title_font = ImageFont.truetype("simkai.ttf", 24)
        label_font = ImageFont.truetype("simkai.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    draw.text((500, 20), "三种纸张材质对比", font=title_font, fill=(0, 0, 0))
    
    materials = [
        ("宣纸", add_xuan_paper_texture_enhanced(width, height), "xuan"),
        ("米纸", add_rice_paper_texture_enhanced(width, height), "rice"),
        ("羊皮纸", add_parchment_texture_enhanced(width, height), "parchment")
    ]
    
    # 为每种材质添加测试文字
    for i, (name, texture, paper_type) in enumerate(materials):
        # 创建带文字的测试图
        test_image = texture.copy()
        test_draw = ImageDraw.Draw(test_image)
        
        try:
            font = ImageFont.truetype("simkai.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        test_draw.text((50, 50), name, font=font, fill=(0, 0, 0))
        test_draw.text((50, 120), "材质测试", font=font, fill=(0, 0, 0))
        
        # 应用材质特定的墨迹效果
        test_image = add_material_specific_ink_effect(test_image, paper_type)
        
        # 粘贴到对比图
        x = 50 + i * 400
        y = 100
        comparison.paste(test_image, (x, y))
        
        # 添加标签和说明
        draw.text((x, y + 250), name, font=label_font, fill=(0, 0, 0))
        
        # 材质特性说明
        characteristics = {
            "宣纸": "纤维明显、渗透性强、有云状纹理",
            "米纸": "表面光滑、纹理细腻、均匀性好", 
            "羊皮纸": "粗糙质感、皮革纹理、有陈旧感"
        }
        
        draw.text((x, y + 280), characteristics[name], font=label_font, fill=(100, 100, 100))
    
    comparison.save("纸张材质对比增强版.png", quality=95)
    print("生成完成：纸张材质对比增强版.png")
    return comparison

if __name__ == "__main__":
    print("创建增强版纸张材质效果...")
    create_material_comparison()