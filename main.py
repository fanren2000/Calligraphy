# Entry point

from PIL import Image, ImageDraw, ImageFont
from Calli_Utils.seal_border_fancy import add_fancy_seal_with_border

def create_jing_ye_si():
    """生成李白的《静夜思》带装饰边框印章"""
    
    # 创建宣纸背景
    image = Image.new('RGB', (900, 1200), (245, 235, 215))
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    font = ImageFont.truetype("simkai.ttf", 65)
    author_font = ImageFont.truetype("simkai.ttf", 35)
    
    # 李白的《静夜思》
    poem = """静夜思
床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。"""
    
    # 绘制诗词
    lines = poem.split('\n')
    y_position = 180
    
    # 标题
    title_bbox = draw.textbbox((0, 0), lines[0], font=font)
    title_x = (900 - (title_bbox[2] - title_bbox[0])) // 2
    draw.text((title_x, y_position), lines[0], font=font, fill=(0, 0, 0))
    y_position += 120
    
    # 诗句
    for line in lines[1:]:
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_x = (900 - (line_bbox[2] - line_bbox[0])) // 2
        draw.text((line_x, y_position), line, font=font, fill=(0, 0, 0))
        y_position += 85
    
    # 添加作者和印章
    author_bbox = draw.textbbox((0, 0), "李白", font=author_font)
    author_x = 900 - (author_bbox[2] - author_bbox[0]) - 100
    author_y = y_position + 70
    
    draw.text((author_x, author_y), "李白", font=author_font, fill=(0, 0, 0))
    
    # 添加装饰边框印章
    image = add_fancy_seal_with_border(image, "玻璃耗子", (author_x - 90, author_y - 15), 75)
    
    # 保存作品
    image.save("李白_静夜思.png")
    print("生成完成：李白_静夜思.png")

if __name__ == "__main__":
    create_jing_ye_si()