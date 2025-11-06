from PIL import Image, ImageDraw, ImageFont
import os
from Utils import safe_get_font

def create_calligraphy_with_seal():
    """创建书法作品，印章盖在文字上"""
    
    # 查找中文字体
    def find_chinese_font():
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc", 
            "C:/Windows/Fonts/simkai.ttf",
            "C:/Windows/Fonts/msyh.ttc",
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
        return None
    
    font_path = "C:/Windows/Fonts/方圆印章篆体.ttf"
    
    # 创建画布
    width, height = 800, 400
    image = Image.new('RGB', (width, height), 'lightyellow')
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    try:
        if font_path:
            calligraphy_font = safe_get_font(font_path, 120)
            seal_font = safe_get_font(font_path, 35)
        else:
            raise Exception("No Chinese font found")
    except:
        # 使用默认字体作为后备
        calligraphy_font = ImageFont.load_default()
        seal_font = ImageFont.load_default()
    
    # 书法文字
    text = "大道至简"
    
    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), text, font=calligraphy_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2 - 20
    
    # 绘制书法文字
    draw.text((text_x, text_y), text, fill='darkred', font=calligraphy_font)
    
    # 印章文字
    seal_text = "玻璃耗子"
    
    # 计算印章位置 - 盖在文字的右下角
    seal_bbox = draw.textbbox((0, 0), seal_text, font=seal_font)
    seal_width = seal_bbox[2] - seal_bbox[0] + 20  # 加边距
    seal_height = seal_bbox[3] - seal_bbox[1] + 20
    
    # 印章位置：文字区域的右下角，稍微重叠
    seal_x = text_x + text_width - seal_width + 30  # 向右移动
    seal_y = text_y + text_height - seal_height + 10  # 向下移动
    
    # 绘制印章背景（浅红色半透明）
    seal_bg = Image.new('RGBA', (seal_width, seal_height), (255, 200, 200, 150))
    image.paste(seal_bg, (seal_x, seal_y), seal_bg)
    
    # 绘制印章边框
    draw.rectangle([seal_x, seal_y, seal_x + seal_width, seal_y + seal_height], 
                  outline='red', width=2)
    
    # 绘制印章文字（居中在印章内）
    seal_text_x = seal_x + (seal_width - (seal_bbox[2] - seal_bbox[0])) // 2 - seal_bbox[0]
    seal_text_y = seal_y + (seal_height - (seal_bbox[3] - seal_bbox[1])) // 2 - seal_bbox[1]
    draw.text((seal_text_x, seal_text_y), seal_text, fill='darkred', font=seal_font)
    
    return image

def create_transparent_seal_version():
    """创建带透明效果的印章版本"""
    
    # 查找字体
    font_path = "C:/Windows/Fonts/simhei.ttf"
    if not os.path.exists(font_path):
        font_path = None
    
    # 创建主画布
    width, height = 800, 400
    background = Image.new('RGB', (width, height), 'lightyellow')
    
    # 加载字体
    try:
        if font_path:
            calligraphy_font = ImageFont.truetype(font_path, 120)
            seal_font = ImageFont.truetype(font_path, 35)
        else:
            raise Exception("No font")
    except:
        calligraphy_font = ImageFont.load_default()
        seal_font = ImageFont.load_default()
    
    draw = ImageDraw.Draw(background)
    
    # 书法文字
    text = "大道至简"
    bbox = draw.textbbox((0, 0), text, font=calligraphy_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2 - 20
    
    draw.text((text_x, text_y), text, fill='darkred', font=calligraphy_font)
    
    # 创建独立的印章图层
    seal_text = "玻璃耗子"
    seal_bbox = draw.textbbox((0, 0), seal_text, font=seal_font)
    seal_width = seal_bbox[2] - seal_bbox[0] + 40
    seal_height = seal_bbox[3] - seal_bbox[1] + 30
    
    # 创建透明印章
    seal_layer = Image.new('RGBA', (seal_width, seal_height), (0, 0, 0, 0))
    seal_draw = ImageDraw.Draw(seal_layer)
    
    # 绘制印章红色背景（半透明）
    seal_draw.rectangle([0, 0, seal_width, seal_height], 
                       fill=(255, 0, 0, 80))  # 半透明红色
    
    # 绘制印章边框
    seal_draw.rectangle([0, 0, seal_width-1, seal_height-1], 
                       outline=(255, 0, 0, 255), width=3)
    
    # 绘制印章文字
    seal_text_x = (seal_width - (seal_bbox[2] - seal_bbox[0])) // 2 - seal_bbox[0]
    seal_text_y = (seal_height - (seal_bbox[3] - seal_bbox[1])) // 2 - seal_bbox[1]
    seal_draw.text((seal_text_x, seal_text_y), seal_text, 
                  fill=(255, 0, 0, 255), font=seal_font)
    
    # 将印章盖在书法文字上（重叠位置）
    seal_x = text_x + text_width - seal_width + 20
    seal_y = text_y + text_height - seal_height - 10
    
    # 合并图层
    background.paste(seal_layer, (seal_x, seal_y), seal_layer)
    
    return background

def create_multiple_seals_version():
    """创建多个印章版本的书法作品"""
    
    font_path = "C:/Windows/Fonts/方圆印章篆体.ttf"
    if not os.path.exists(font_path):
        font_path = None
    
    width, height = 900, 500
    image = Image.new('RGB', (width, height), 'lightyellow')
    draw = ImageDraw.Draw(image)
    
    try:
        if font_path:
            calligraphy_font = safe_get_font(font_path, 140)
            seal_font = safe_get_font(font_path, 30)
            small_seal_font = safe_get_font(font_path, 25)
        else:
            raise Exception("No font")
    except:
        calligraphy_font = ImageFont.load_default()
        seal_font = ImageFont.load_default()
        small_seal_font = ImageFont.load_default()
    
    # 书法文字
    text = "大道至简"
    bbox = draw.textbbox((0, 0), text, font=calligraphy_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2 - 30
    
    draw.text((text_x, text_y), text, fill='darkred', font=calligraphy_font)
    
    # 主印章（右下角）
    main_seal_text = "玻璃耗子"
    main_bbox = draw.textbbox((0, 0), main_seal_text, font=seal_font)
    main_seal_width = main_bbox[2] - main_bbox[0] + 30
    main_seal_height = main_bbox[3] - main_bbox[1] + 25
    
    main_seal_x = text_x + text_width - main_seal_width - 10
    main_seal_y = text_y + text_height - main_seal_height - 5
    
    # 绘制主印章
    draw.rectangle([main_seal_x, main_seal_y, 
                   main_seal_x + main_seal_width, 
                   main_seal_y + main_seal_height], 
                  outline='red', width=3, fill=(255, 200, 200, 128))
    
    main_text_x = main_seal_x + (main_seal_width - (main_bbox[2] - main_bbox[0])) // 2 - main_bbox[0]
    main_text_y = main_seal_y + (main_seal_height - (main_bbox[3] - main_bbox[1])) // 2 - main_bbox[1]
    draw.text((main_text_x, main_text_y), main_seal_text, fill='darkred', font=seal_font)
    
    # 小印章（左下角）
    small_seal_text = "鉴赏"
    small_bbox = draw.textbbox((0, 0), small_seal_text, font=small_seal_font)
    small_seal_size = 80
    
    small_seal_x = text_x + 20
    small_seal_y = text_y + text_height - small_seal_size + 10
    
    # 绘制圆形小印章
    draw.ellipse([small_seal_x, small_seal_y, 
                  small_seal_x + small_seal_size, 
                  small_seal_y + small_seal_size], 
                 outline='red', width=2)
    
    small_text_x = small_seal_x + (small_seal_size - (small_bbox[2] - small_bbox[0])) // 2 - small_bbox[0]
    small_text_y = small_seal_y + (small_seal_size - (small_bbox[3] - small_bbox[1])) // 2 - small_bbox[1]
    draw.text((small_text_x, small_text_y), small_seal_text, fill='red', font=small_seal_font)
    
    return image

# 生成三个版本
print("生成书法作品...")

# 版本1：基础版本
result1 = create_calligraphy_with_seal()
result1.save("calligraphy_seal_v1.jpg")
print("✅ 版本1已保存: calligraphy_seal_v1.jpg")

# 版本2：透明印章版本
result2 = create_transparent_seal_version()
result2.save("calligraphy_seal_v2.jpg")
print("✅ 版本2已保存: calligraphy_seal_v2.jpg")

# 版本3：多个印章版本
result3 = create_multiple_seals_version()
result3.save("calligraphy_seal_v3.jpg")
print("✅ 版本3已保存: calligraphy_seal_v3.jpg")

print("\n🎨 三个版本都已生成完成！")
print("   版本1: 基础红色印章")
print("   版本2: 透明效果印章") 
print("   版本3: 多个印章（主印章+鉴赏章）")

# 显示其中一个版本
result1.show()