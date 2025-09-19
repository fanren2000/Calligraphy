from PIL import Image, ImageDraw, ImageFont

from Calli_Utils.seal_border_fancy_4char import add_four_character_seal

def create_cai_shu_yuan():
    """生成上官婉儿的《彩书怨》带四字方形印章"""
    
    # 创建宣纸背景
    image = Image.new('RGB', (1000, 1400), (245, 235, 215))
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    font = ImageFont.truetype("simkai.ttf", 60)
    title_font = ImageFont.truetype("simkai.ttf", 70)
    author_font = ImageFont.truetype("simkai.ttf", 35)
    
    # 上官婉儿的《彩书怨》
    poem = """彩书怨
叶下洞庭初，思君万里余。
露浓香被冷，月落锦屏虚。
欲奏江南曲，贪封蓟北书。
书中无别意，惟怅久离居。"""
    
    # 绘制诗词
    lines = poem.split('\n')
    y_position = 150
    
    # 标题
    title_bbox = draw.textbbox((0, 0), lines[0], font=title_font)
    title_x = (1000 - (title_bbox[2] - title_bbox[0])) // 2
    draw.text((title_x, y_position), lines[0], font=title_font, fill=(0, 0, 0))
    y_position += 100
    
    # 诗句
    for line in lines[1:]:
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_x = (1000 - (line_bbox[2] - line_bbox[0])) // 2
        draw.text((line_x, y_position), line, font=font, fill=(0, 0, 0))
        y_position += 80
    
    # 添加作者落款
    author_text = "上官婉儿"
    author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
    author_x = 1000 - (author_bbox[2] - author_bbox[0]) - 150
    author_y = y_position + 80
    
    draw.text((author_x, author_y), author_text, font=author_font, fill=(0, 0, 0))
    
    # 添加四字方形印章
    seal_x = author_x - 120
    seal_y = author_y - 25
    
    # 使用修正后的印章函数
    image = add_four_character_seal(image, "玻璃耗子", (seal_x, seal_y), 100)
    
    # 保存作品
    image.save("上官婉儿_彩书怨_方形印章.png", quality=95)
    print("生成完成：上官婉儿_彩书怨_方形印章.png")
    print("印章：正方形，四字居中排列")
    
    return image

if __name__ == "__main__":
    create_cai_shu_yuan()