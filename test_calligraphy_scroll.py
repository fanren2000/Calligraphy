from PIL import Image, ImageDraw, ImageFont
import os

def create_calligraphy_scroll(text, output_path="calligraphy_scroll.png"):
    # 创建卷轴背景
    width, height = 800, 400
    scroll_color = (240, 220, 180)  # 羊皮纸色
    
    # 创建图像
    image = Image.new("RGB", (width, height), color=scroll_color)
    draw = ImageDraw.Draw(image)
    
    # 添加卷轴边框装饰
    border_color = (139, 69, 19)  # 深棕色
    border_width = 20
    draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                   outline=border_color, width=3)
    
    # 添加卷轴轴
    scroll_axis_color = (101, 67, 33)  # 木色
    axis_height = 40
    draw.rectangle([0, height//2-axis_height//2, border_width, height//2+axis_height//2], 
                   fill=scroll_axis_color)
    draw.rectangle([width-border_width, height//2-axis_height//2, width, height//2+axis_height//2], 
                   fill=scroll_axis_color)
    
    # 尝试加载中文字体，如果没有则使用默认字体
    try:
        # 你可以替换为系统中的中文字体路径
        font_path = "simkai.ttf"  # 楷体
        font = ImageFont.truetype(font_path, 60)
    except:
        # 如果找不到指定字体，使用默认字体
        font = ImageFont.load_default()
        print("警告：未找到指定字体，使用默认字体")
    
    # 计算文字位置（居中）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # 绘制文字阴影（增加立体感）
    shadow_color = (100, 100, 100, 128)
    draw.text((x+2, y+2), text, font=font, fill=shadow_color)
    
    # 绘制主文字
    text_color = (0, 0, 0)  # 黑色
    draw.text((x, y), text, font=font, fill=text_color)
    
    # 添加印章
    seal_size = 60
    seal_x = x + text_width - seal_size // 2
    seal_y = y + text_height + 10
    draw.rectangle([seal_x, seal_y, seal_x+seal_size, seal_y+seal_size], 
                   outline=(255, 0, 0), width=2)
    
    # 保存图像
    image.save(output_path)
    print(f"书法卷轴已保存为: {output_path}")
    
    return image

# 使用示例
if __name__ == "__main__":
    text = "宁静致远"  # 要书写的文字
    create_calligraphy_scroll(text)