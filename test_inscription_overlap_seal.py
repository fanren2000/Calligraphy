


from PIL import Image, ImageDraw, ImageFont
import random

def create_simple_calligraphy_with_seal():
    """简单的书法作品，包含压款印"""
    
    # 1. 创建宣纸背景
    width, height = 800, 600
    paper = Image.new('RGB', (width, height), color='#F5F0E6')
    draw = ImageDraw.Draw(paper)
    
    # 2. 添加主体文字
    try:
        main_font = ImageFont.truetype("simkai.ttf", 120)
    except:
        main_font = ImageFont.load_default()
    
    # 横排文字（从右到左）
    text = "气势如虹"
    char_width = 120
    spacing = 30
    total_width = len(text) * (char_width + spacing) - spacing
    start_x = (width - total_width) // 2
    start_y = height // 3
    
    # 绘制主体文字（从右到左）
    for i, char in enumerate(text):
        x = start_x + (len(text) - 1 - i) * (char_width + spacing)
        draw.text((x, start_y), char, fill=(30, 30, 30), font=main_font)
    
    # 3. 添加下款文字
    try:
        inscription_font = ImageFont.truetype("simkai.ttf", 20)
    except:
        inscription_font = ImageFont.load_default()
    
    lower_text = "某某书于甲辰年仲秋"
    lower_x = 100  # 左下角
    lower_y = height - 150
    
    # 竖排绘制下款
    for i, char in enumerate(lower_text):
        draw.text((lower_x, lower_y + i * 25), char, fill=(60, 60, 60), font=inscription_font)
    
    # 4. 🎯 在落款文字上盖收藏章
    add_collection_seal_on_inscription(draw, lower_x, lower_y, len(lower_text))
    
    return paper

def add_collection_seal_on_inscription(draw, lower_x, lower_y, text_length):
    """在落款文字上添加收藏章"""
    
    # 印章参数
    seal_content = "珍藏"
    seal_size = 28  # 印章大小
    seal_color = "#8B0000"  # 朱红色
    
    # 🎯 计算印章位置（盖在第一个字上）
    # 第一个字的位置：lower_x, lower_y
    seal_x = lower_x - seal_size - 5  # 在文字左侧
    seal_y = lower_y + 5  # 稍微向下偏移，盖在文字上
    
    # 绘制印章边框
    seal_width = seal_size * 2
    seal_height = seal_size * 2
    
    # 方形印章
    draw.rectangle([
        seal_x, seal_y, 
        seal_x + seal_width, 
        seal_y + seal_height
    ], outline=seal_color, width=2)
    
    # 绘制印章文字
    try:
        # 使用篆书字体，如果没有就用默认字体
        seal_font = ImageFont.truetype("simkai.ttf", seal_size)
    except:
        seal_font = ImageFont.load_default()
    
    # 计算文字位置（居中）
    text_bbox = draw.textbbox((0, 0), seal_content, font=seal_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = seal_x + (seal_width - text_width) // 2
    text_y = seal_y + (seal_height - text_height) // 2
    
    draw.text((text_x, text_y), seal_content, fill=seal_color, font=seal_font)
    
    print(f"🎨 压款印位置: ({seal_x}, {seal_y})")
    print(f"   盖在落款文字上，内容: '{seal_content}'")

def create_artwork_with_multiple_seals():
    """包含多个印章的例子"""
    
    # 创建基础作品
    artwork = create_simple_calligraphy_with_seal()
    draw = ImageDraw.Draw(artwork)
    width, height = artwork.size
    
    # 添加姓名印（不重叠）
    add_name_seal(draw, width, height)
    
    # 添加闲章
    add_leisure_seal(draw, width)
    
    return artwork

def add_name_seal(draw, width, height):
    """添加姓名印（在左下角，不重叠）"""
    seal_content = "某某之印"
    seal_size = 22
    seal_color = "#8B0000"
    
    # 位置：左下角，在下款右侧
    seal_x = 180  # 在下款文字右侧
    seal_y = height - 120  # 与下款对齐
    
    seal_width = seal_size * 2
    seal_height = seal_size * 2
    
    # 绘制方形印章
    draw.rectangle([
        seal_x, seal_y,
        seal_x + seal_width, 
        seal_y + seal_height
    ], outline=seal_color, width=2)
    
    # 绘制文字
    try:
        seal_font = ImageFont.truetype("simkai.ttf", seal_size)
    except:
        seal_font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), seal_content, font=seal_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = seal_x + (seal_width - text_width) // 2
    text_y = seal_y + (seal_height - seal_size) // 2
    
    draw.text((text_x, text_y), seal_content, fill=seal_color, font=seal_font)
    
    print(f"🖋️ 姓名印位置: ({seal_x}, {seal_y})")

def add_leisure_seal(draw, width):
    """添加闲章（在右上角）"""
    seal_content = "心画"
    seal_size = 25
    seal_color = "#8B0000"
    
    # 位置：右上角
    seal_x = width - 120
    seal_y = 80
    
    # 绘制椭圆形闲章
    seal_width = seal_size * 2
    seal_height = seal_size
    
    # 绘制椭圆（简化为圆角矩形）
    draw.rounded_rectangle([
        seal_x, seal_y,
        seal_x + seal_width, 
        seal_y + seal_height
    ], radius=20, outline=seal_color, width=2)
    
    # 绘制文字
    try:
        seal_font = ImageFont.truetype("simkai.ttf", seal_size - 5)
    except:
        seal_font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), seal_content, font=seal_font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = seal_x + (seal_width - text_width) // 2
    text_y = seal_y + (seal_height - (seal_size - 5)) // 2
    
    draw.text((text_x, text_y), seal_content, fill=seal_color, font=seal_font)
    
    print(f"🎨 闲章位置: ({seal_x}, {seal_y})")

def create_advanced_seal_example():
    """更复杂的压款印例子"""
    
    artwork = create_simple_calligraphy_with_seal()
    draw = ImageDraw.Draw(artwork)
    width, height = artwork.size
    
    # 下款位置
    lower_x = 100
    lower_y = height - 150
    lower_text = "某某书于甲辰年仲秋"
    
    # 🎯 添加多个压款印在不同位置
    seal_positions = [
        ("珍藏", lower_x - 40, lower_y + 10),      # 第一个字上方
        ("神品", lower_x - 40, lower_y + 100),     # 中间位置
        ("真迹", lower_x + 200, lower_y + 10),     # 右侧
    ]
    
    for content, x, y in seal_positions:
        # 绘制印章
        seal_size = 22
        seal_width = seal_size * 2
        seal_height = seal_size * 2
        
        # 方形印章
        draw.rectangle([x, y, x + seal_width, y + seal_height], 
                      outline="#8B0000", width=2)
        
        # 印章文字
        try:
            seal_font = ImageFont.truetype("simkai.ttf", seal_size)
        except:
            seal_font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), content, font=seal_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = x + (seal_width - text_width) // 2
        text_y = y + (seal_height - seal_size) // 2
        
        draw.text((text_x, text_y), content, fill="#8B0000", font=seal_font)
        
        print(f"📌 压款印 '{content}' 位置: ({x}, {y})")
    
    return artwork

# 使用示例
if __name__ == "__main__":
    print("=== 简单压款印例子 ===")
    simple_artwork = create_simple_calligraphy_with_seal()
    simple_artwork.save("simple_seal.png")
    
    print("\n=== 多印章例子 ===")
    multi_seal_artwork = create_artwork_with_multiple_seals()
    multi_seal_artwork.save("multi_seal.png")
    
    print("\n=== 复杂压款印例子 ===")
    advanced_artwork = create_advanced_seal_example()
    advanced_artwork.save("advanced_seal.png")
    
    print("\n✅ 所有作品已保存!")