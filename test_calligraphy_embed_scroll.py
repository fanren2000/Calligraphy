
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def embed_calligraphy_in_scroll(scroll_path, calligraphy_path, output_path, target_region=None):
    """
    将书法图片精确嵌入卷轴的空白区域
    
    参数:
    - scroll_path: 卷轴图片路径
    - calligraphy_path: 书法文字图片路径（建议透明背景）
    - output_path: 输出图片路径
    - target_region: 目标区域 (x1, y1, x2, y2)，如果为None则自动检测
    """
    
    # 打开图片
    scroll = Image.open(scroll_path).convert('RGBA')
    calligraphy = Image.open(calligraphy_path).convert('RGBA')
    
    print(f"卷轴尺寸: {scroll.size}")
    print(f"书法尺寸: {calligraphy.size}")
    
    # 如果没有指定目标区域，自动检测或使用默认位置
    if target_region is None:
        target_region = auto_detect_blank_region(scroll, calligraphy.size)
    
    # 调整书法文字尺寸以适应目标区域
    calligraphy_resized = resize_to_fit_region(calligraphy, target_region)
    
    # 创建结果图片
    result = scroll.copy()
    
    # 计算放置位置（居中于目标区域）
    region_width = target_region[2] - target_region[0]
    region_height = target_region[3] - target_region[1]
    
    x_offset = target_region[0] + (region_width - calligraphy_resized.width) // 2
    y_offset = target_region[1] + (region_height - calligraphy_resized.height) // 2
    
    # 使用透明度混合嵌入书法文字
    result = blend_images(result, calligraphy_resized, (x_offset, y_offset))
    
    result.save(output_path)
    print(f"书法已嵌入卷轴: {output_path}")
    return result

def auto_detect_blank_region(scroll, calligraphy_size):
    """
    自动检测卷轴中的空白区域
    """
    width, height = scroll.size
    
    # 方法1: 基于卷轴结构的经验位置
    # 通常卷轴空白区域在中心偏上位置
    region_width = width * 0.7  # 空白区域宽度为卷轴的70%
    region_height = height * 0.4  # 高度为卷轴的40%
    
    x1 = int((width - region_width) // 2)
    y1 = int(height * 0.2)  # 从顶部20%开始
    x2 = int(x1 + region_width)
    y2 = int(y1 + region_height)
    
    print(f"自动检测的空白区域: ({x1}, {y1}, {x2}, {y2})")
    return (x1, y1, x2, y2)

def resize_to_fit_region(calligraphy, target_region):
    """
    调整书法图片尺寸以适应目标区域，保持比例
    """
    region_width = target_region[2] - target_region[0]
    region_height = target_region[3] - target_region[1]
    
    orig_width, orig_height = calligraphy.size
    
    # 计算保持比例的缩放尺寸
    width_ratio = region_width / orig_width
    height_ratio = region_height / orig_height
    scale_ratio = min(width_ratio, height_ratio) * 0.9  # 留出10%边距
    
    new_width = int(orig_width * scale_ratio)
    new_height = int(orig_height * scale_ratio)
    
    return calligraphy.resize((new_width, new_height), Image.Resampling.LANCZOS)

def blend_images(background, foreground, position):
    """
    将前景图混合到背景图的指定位置，保持透明度
    """
    bg = background.copy()
    fg = foreground.copy()
    
    x, y = position
    
    # 创建一个与背景相同尺寸的透明图层
    overlay = Image.new('RGBA', bg.size, (0, 0, 0, 0))
    
    # 将书法文字放置到透明图层的正确位置
    overlay.paste(fg, (x, y), fg)
    
    # 使用alpha_composite进行混合
    result = Image.alpha_composite(bg, overlay)
    return result

def create_calligraphy_with_transparent_bg(text, output_path, font_size=120):
    """
    创建透明背景的书法文字图片（如果还没有书法图片）
    """
    # 尝试加载书法字体
    try:
        font_paths = [
            "simkai.ttf",  # 楷体
            "simhei.ttf",  # 黑体
            "STKAITI.TTF", # 楷体
            "/System/Library/Fonts/PingFang.ttc"  # macOS
        ]
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # 计算文字尺寸
    temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 创建透明背景图片（留出边距）
    margin = 20
    img_width = text_width + margin * 2
    img_height = text_height + margin * 2
    image = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制文字
    x = margin - bbox[0]
    y = margin - bbox[1]
    
    # 添加文字阴影（可选）
    shadow_color = (0, 0, 0, 100)
    draw.text((x+2, y+2), text, font=font, fill=shadow_color)
    
    # 绘制主文字
    text_color = (0, 0, 0, 255)  # 黑色，不透明
    draw.text((x, y), text, font=font, fill=text_color)
    
    image.save(output_path)
    print(f"书法文字已创建: {output_path}")
    return image

def manual_region_selection(scroll_path, calligraphy_path, output_path, region_ratio=(0.7, 0.4), position_ratio=(0.5, 0.3)):
    """
    手动指定区域参数的方法
    """
    scroll = Image.open(scroll_path).convert('RGBA')
    width, height = scroll.size
    
    # 根据比例计算目标区域
    region_width = int(width * region_ratio[0])
    region_height = int(height * region_ratio[1])
    
    x1 = int((width - region_width) * position_ratio[0])
    y1 = int((height - region_height) * position_ratio[1])
    x2 = x1 + region_width
    y2 = y1 + region_height
    
    target_region = (x1, y1, x2, y2)
    print(f"手动设定区域: {target_region}")
    
    return embed_calligraphy_in_scroll(scroll_path, calligraphy_path, output_path, target_region)


def interactive_placement(scroll_path, calligraphy_path, output_path, x_ratio=0.5, y_ratio=0.3, width_ratio=0.6, height_ratio=0.3):
    """
    交互式调整书法位置
    """
    scroll = Image.open(scroll_path).convert('RGBA')
    width, height = scroll.size
    
    # 根据参数计算目标区域
    region_width = int(width * width_ratio)
    region_height = int(height * height_ratio)
    x1 = int((width - region_width) * x_ratio)
    y1 = int((height - region_height) * y_ratio)
    x2 = x1 + region_width
    y2 = y1 + region_height
    
    target_region = (x1, y1, x2, y2)
    
    print(f"当前参数: x_ratio={x_ratio}, y_ratio={y_ratio}")
    print(f"目标区域: {target_region}")
    
    return embed_calligraphy_in_scroll(scroll_path, calligraphy_path, output_path, target_region)


# 使用示例
if __name__ == "__main__":
    scroll_bg_img = "Frames/scroll_horizontal_brown_basic.png"
    # 方法1: 自动检测空白区域
    # embed_calligraphy_in_scroll(
    #     scroll_path=scroll_bg_img,
    #     calligraphy_path="calligraphy_text.png",  # 透明背景的书法图片
    #     output_path="result_auto.png"
    # )
    
    # # 方法2: 手动指定区域参数
    # manual_region_selection(
    #     scroll_path=scroll_bg_img,
    #     calligraphy_path="calligraphy_text.png",
    #     output_path="result_manual.png",
    #     region_ratio=(0.6, 0.35),  # 区域大小比例
    #     position_ratio=(0.5, 0.25)  # 区域位置比例
    # )
    
    # 方法3: 如果没有书法图片，先创建
    # create_calligraphy_with_transparent_bg(
    #     text="宁静致远",
    #     output_path="my_calligraphy.png",
    #     font_size=150
    # )
    
    # # 然后嵌入
    # embed_calligraphy_in_scroll(
    #     scroll_path=scroll_bg_img,
    #     calligraphy_path="my_calligraphy.png",
    #     output_path="final_result.png"
    # )

    # 调整参数直到满意
    interactive_placement("scroll.png", "calligraphy.png", "test1.png", x_ratio=0.5, y_ratio=0.25)
    interactive_placement("scroll.png", "calligraphy.png", "test2.png", x_ratio=0.5, y_ratio=0.3)
    interactive_placement("scroll.png", "calligraphy.png", "test3.png", width_ratio=0.7, height_ratio=0.4)