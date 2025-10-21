import random
from PIL import Image, ImageDraw, ImageFont
import math
import os

def add_circular_seal_with_border_4char(image, text, position, diameter=150, border_width=4):
    """
    创建带边框的圆形印章，支持四字两两排列
    
    参数:
        image: PIL Image对象
        text: 印章文字（4个字符）
        position: (x, y) 印章中心位置
        diameter: 印章直径
        border_width: 边框宽度
    
    返回:
        PIL Image对象
    """
    if len(text) != 4:
        raise ValueError("印章文字必须是4个字符")
    
    draw = ImageDraw.Draw(image)
    
    # 印章颜色
    seal_color = (180, 30, 30)
    border_color = (150, 20, 20)
    white_color = (255, 255, 255)
    
    x, y = position
    radius = diameter // 2
    center_x, center_y = x, y
    
    # 1. 绘制外边框（稍大的圆）
    outer_radius = radius + border_width
    draw.ellipse([
        center_x - outer_radius, 
        center_y - outer_radius,
        center_x + outer_radius, 
        center_y + outer_radius
    ], outline=border_color, width=border_width)
    
    # 2. 绘制印章主体
    draw.ellipse([
        center_x - radius, 
        center_y - radius,
        center_x + radius, 
        center_y + radius
    ], fill=seal_color)
    
    # 3. 加载字体
    try:
        # 尝试加载篆体字体
        zhuan_font_path = "方圆印章篆体.ttf"  # 请修改为您的实际路径
        if os.path.exists(zhuan_font_path):
            seal_font = ImageFont.truetype(zhuan_font_path, diameter // 5)
            print("使用篆体字体")
        else:
            seal_font = ImageFont.truetype("simkai.ttf", diameter // 5)
            print("使用楷体字体")
    except:
        seal_font = ImageFont.truetype("simkai.ttf", diameter // 5)
    
    # 4. 四字两两排列
    chars = list(text)
    
    # 计算文字位置（2x2网格）
    grid_size = radius * 0.6  # 文字离中心的距离
    cell_size = grid_size * 0.8  # 每个单元格的大小
    
    # 四个字的相对位置（2x2网格）
    positions = [
        (-cell_size, -cell_size),  # 左上：第一个字
        (cell_size, -cell_size),   # 右上：第二个字
        (-cell_size, cell_size),   # 左下：第三个字  
        (cell_size, cell_size)     # 右下：第四个字
    ]
    
    # 绘制四个字
    for i, (rel_x, rel_y) in enumerate(positions):
        char = chars[i]
        
        # 计算绝对位置
        abs_x = center_x + rel_x
        abs_y = center_y + rel_y
        
        # 获取文字尺寸并居中
        bbox = draw.textbbox((0, 0), char, font=seal_font)
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        
        # 调整位置使文字居中在网格点
        char_x = abs_x - char_width // 2
        char_y = abs_y - char_height // 2
        
        draw.text((char_x, char_y), char, font=seal_font, fill=white_color)
    
    # 5. 可选：添加中心装饰（传统印章常有）
    center_decoration_size = diameter // 10
    draw.ellipse([
        center_x - center_decoration_size,
        center_y - center_decoration_size,
        center_x + center_decoration_size,
        center_y + center_decoration_size
    ], fill=border_color)
    
    return image

def add_circular_seal_advanced(image, text, position, diameter=160, border_width=5, compact_ratio=0.55):
    """
    修正版圆形四字印章（篆体文字居中显示）
    """
    draw = ImageDraw.Draw(image)
    
    if len(text) != 4:
        raise ValueError("必须是4个字符")
    
    seal_color = (180, 30, 30)
    border_color = (150, 20, 20)
    white_color = (255, 255, 255)
    
    x, y = position
    radius = diameter // 2
    
    # 绘制边框和主体
    draw.ellipse([x-radius-border_width, y-radius-border_width, 
                 x+radius+border_width, y+radius+border_width], 
                outline=border_color, width=border_width)
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=seal_color)
    
    # 加载字体
    try:
        # 尝试加载篆体，如果失败则使用楷体
        seal_font = ImageFont.truetype("方圆印章篆体.ttf", diameter // 4)
        font_type = "篆体"
    except:
        seal_font = ImageFont.truetype("simkai.ttf", diameter // 4)
        font_type = "楷体"
    
    print(f"使用字体: {font_type}")
    
    chars = list(text)
    
    # 篆体字需要向下偏移（关键修正）
    zhuan_offset = diameter // 5  if font_type == "篆体" else 0
    
    # 更精确的2x2网格布局
    grid_offset = radius * compact_ratio  # 文字离中心距离, compact_ratio越小，字离中心越近
    
    # 四个角的坐标（添加篆体偏移）
    # 修正1：使用统一的基准点，然后应用偏移
    base_y = y + zhuan_offset  # 所有文字共享的基准y坐标
    
    positions = [
        (x - grid_offset, base_y - grid_offset),  # 左上
        (x + grid_offset, base_y - grid_offset),  # 右上
        (x - grid_offset, base_y + grid_offset),  # 左下
        (x + grid_offset, base_y + grid_offset)   # 右下
    ]
    
    # 绘制文字
    for i, (char_x, char_y) in enumerate(positions):
        char = chars[i]
        
        # 获取文字尺寸（精确计算）
        bbox = draw.textbbox((0, 0), char, font=seal_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 调整位置居中
        final_x = char_x - text_width // 2
        final_y = char_y - text_height // 2
        
        draw.text((final_x, final_y), char, font=seal_font, fill=white_color)
    
    return image

def add_circular_seal_with_rotation(image, text, position, diameter=160, compact_ratio=0.6,
                                    rotation_degree=5):
    """
    带轻微旋转的聚集版本（更传统）
    """
    draw = ImageDraw.Draw(image)
    
    if len(text) != 4:
        raise ValueError("必须是4个字符")
    
    x, y = position
    radius = diameter // 2
    
    # 绘制印章
    draw.ellipse([x-radius-4, y-radius-4, x+radius+4, y+radius+4], 
                outline=(150,20,20), width=4)
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=(180,30,30))
    
    try:
        seal_font = ImageFont.truetype("simkai.ttf", diameter // 4)
        vertical_offset = 0
        # seal_font = ImageFont.truetype("方圆印章篆体.ttf", diameter // 4)
        # vertical_offset = diameter // 12
    except (OSError, IOError):
        seal_font = ImageFont.truetype("simkai.ttf", diameter // 4)
        vertical_offset = 0
    
    chars = list(text)
    grid_offset = radius * compact_ratio
    base_y = y + vertical_offset
    
    positions = [
        (x - grid_offset, base_y - grid_offset),  # 左上
        (x + grid_offset, base_y - grid_offset),  # 右上
        (x - grid_offset, base_y + grid_offset),  # 左下
        (x + grid_offset, base_y + grid_offset)   # 右下
    ]
    
    rotations = [-rotation_degree, rotation_degree, -rotation_degree, rotation_degree]
    
    for i, ((char_x, char_y), rotation) in enumerate(zip(positions, rotations)):
        char = chars[i]
        bbox = draw.textbbox((0, 0), char, font=seal_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        temp_img = Image.new('RGBA', (text_width + 15, text_height + 15), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((10, 10), char, font=seal_font, fill=(255, 255, 255, 255))
        
        rotated_temp = temp_img.rotate(rotation, expand=True, resample=Image.BICUBIC)
        
        rot_width, rot_height = rotated_temp.size
        final_x = char_x - rot_width // 2
        final_y = char_y - rot_height // 2
        
        image.paste(rotated_temp, (int(final_x), int(final_y)), rotated_temp)
    
    return image

def add_circular_seal_visual_debug(image, text, position, diameter=160, compact_ratio=0.55):
    """
    可视化调试版（显示参考线，便于调整）
    """
    draw = ImageDraw.Draw(image)
    
    if len(text) != 4:
        raise ValueError("必须是4个字符")
    
    # 印章颜色
    seal_color = (180, 30, 30)
    border_color = (150, 20, 20)
    white_color = (255, 255, 255)
    debug_color = (0, 255, 0)  # 绿色参考线
    
    x, y = position
    radius = diameter // 2
    
    # 绘制印章
    draw.ellipse([x-radius-4, y-radius-4, x+radius+4, y+radius+4], 
                outline=border_color, width=4)
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=seal_color)
    
    # 绘制参考线（中心十字）
    draw.line([x-10, y, x+10, y], fill=debug_color, width=1)
    draw.line([x, y-10, x, y+10], fill=debug_color, width=1)
    
    # 加载字体
    try:
        seal_font = ImageFont.truetype("方圆印章篆体.ttf", diameter // 4)
        zhuan_offset = diameter // 5  # 篆体偏移量
    except:
        seal_font = ImageFont.truetype("simkai.ttf", diameter // 4)
        zhuan_offset = 0
    
    chars = list(text)
    grid_offset = radius * compact_ratio
    
    # 四个文字位置（应用偏移）
    # ==================== 关键修正：正确的偏移应用 ====================
    # 修正1：使用统一的基准点，然后应用偏移
    base_y = y + zhuan_offset  # 所有文字共享的基准y坐标
    
    positions = [
        (x - grid_offset, base_y - grid_offset),  # 左上
        (x + grid_offset, base_y - grid_offset),  # 右上
        (x - grid_offset, base_y + grid_offset),  # 左下
        (x + grid_offset, base_y + grid_offset)   # 右下
    ]
    
    # 绘制文字和调试信息
    for i, (char_x, char_y) in enumerate(positions):
        char = chars[i]
        
        # 绘制位置标记
        draw.ellipse([char_x-2, char_y-2, char_x+2, char_y+2], fill=debug_color)
        
        # 获取文字尺寸
        bbox = draw.textbbox((0, 0), char, font=seal_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 计算居中位置
        final_x = char_x - text_width // 2
        final_y = char_y - text_height // 2
        
        # 绘制文字边界框（调试用）
        draw.rectangle([final_x, final_y, final_x+text_width, final_y+text_height], 
                      outline=debug_color, width=1)
        
        draw.text((final_x, final_y), char, font=seal_font, fill=white_color)
    
    return image

def add_circular_seal_with_traditional_layout(image, text, position, diameter=150):
    """
    传统布局的圆形四字印章（更适合书法作品）
    """
    draw = ImageDraw.Draw(image)
    
    if len(text) != 4:
        raise ValueError("必须是4个字符")
    
    # 传统朱砂色
    seal_color = (170, 40, 40)
    border_color = (130, 25, 25)
    white_color = (255, 240, 240)  # 略带米色的白
    
    x, y = position
    radius = diameter // 2
    
    # 绘制印章（带一点不规则感）
    draw.ellipse([x-radius-3, y-radius-3, x+radius+3, y+radius+3], 
                outline=border_color, width=3)
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=seal_color)
    
    # 使用篆体或楷体
    try:
        seal_font = ImageFont.truetype("方圆印章篆体.ttf", diameter // 4)
    except:
        seal_font = ImageFont.truetype("simkai.ttf", diameter // 4)
    
    chars = list(text)
    
    # 传统2x2排列（稍紧凑）
    offset = radius * 0.5
    
    # 四个字的位置
    positions = [
        (x - offset, y - offset),  # 左上
        (x + offset, y - offset),  # 右上
        (x - offset, y + offset),  # 左下  
        (x + offset, y + offset)   # 右下
    ]
    
    for i, (char_x, char_y) in enumerate(positions):
        char = chars[i]
        bbox = draw.textbbox((0, 0), char, font=seal_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        draw.text((char_x - text_width//2, char_y - text_height//2), 
                 char, font=seal_font, fill=white_color)
    
    # 添加传统印章的纹理效果
    for _ in range(20):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, radius * 0.8)
        dot_x = x + dist * math.cos(angle)
        dot_y = y + dist * math.sin(angle)
        dot_size = random.randint(1, 3)
        draw.ellipse([dot_x-dot_size, dot_y-dot_size, dot_x+dot_size, dot_y+dot_size],
                    fill=(200, 50, 50))
    
    return image

