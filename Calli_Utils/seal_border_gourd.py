from PIL import Image, ImageDraw, ImageFont

def create_gourd_seal_vertical_text(seal_text="福禄", size=300):
    """修正文字位置 - 更好的垂直居中"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 定义相对坐标
    relative_points = [
        (0.50, 0.233), (0.533, 0.250), (0.567, 0.283), (0.600, 0.333), 
        (0.617, 0.400), (0.617, 0.467), (0.633, 0.517), (0.650, 0.567), 
        (0.667, 0.633), (0.667, 0.733), (0.650, 0.817), (0.617, 0.867), 
        (0.567, 0.900), (0.433, 0.900), (0.383, 0.867), (0.350, 0.817), 
        (0.333, 0.733), (0.333, 0.633), (0.350, 0.567), (0.367, 0.517),
        (0.383, 0.467), (0.383, 0.400), (0.400, 0.333), (0.433, 0.283),
        (0.467, 0.250), (0.50, 0.233)
    ]
    
    actual_points = [(x * size, y * size) for x, y in relative_points]
    line_width = max(2, int(3 * size / 300))
    draw.polygon(actual_points, fill='red', outline='darkred', width=line_width)
    
    # 蒂部
    draw.ellipse([0.49 * size, 0.20 * size, 0.51 * size, 0.233 * size], 
                fill='red', outline='darkred', width=line_width-1)
    
    # 计算葫芦内部实际可用空间
    inner_top = 0.35 * size    # 顶部边界
    inner_bottom = 0.85 * size # 底部边界  
    inner_left = 0.38 * size   # 左侧边界
    inner_right = 0.62 * size  # 右侧边界
    
    inner_height = inner_bottom - inner_top
    inner_width = inner_right - inner_left
    
    # 字体大小计算
    text_length = len(seal_text)
    
    # 强制使用小字体
    if text_length == 2:
        font_size = int(size * 0.12)
    elif text_length == 3:
        font_size = int(size * 0.10)
    elif text_length == 4:
        font_size = int(size * 0.06)
    else:
        font_size = int(size * 0.06)
    
    font_size = max(12, font_size)
    
    try:
        font = ImageFont.truetype("ZC0009-Regular-2.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # 计算每个字符的实际尺寸
    char_heights = []
    char_widths = []
    
    for char in seal_text:
        bbox = draw.textbbox((0, 0), char, font=font)
        char_heights.append(bbox[3] - bbox[1])
        char_widths.append(bbox[2] - bbox[0])
    
    # 计算总高度（包括间距）
    spacing = font_size * 0.1  # 较小的间距
    total_text_height = sum(char_heights) + (text_length - 1) * spacing
    
    # **关键修正：使用葫芦内部空间的中心，而不是整个图片的中心**
    text_center_x = (inner_left + inner_right) // 2
    text_center_y = (inner_top + inner_bottom) // 2
    
    # **修正起始位置：从中心向上偏移一半文字高度**
    start_y = text_center_y - total_text_height // 2
    
    print(f"文字总高度: {total_text_height:.1f}")
    print(f"内部空间中心Y: {text_center_y:.1f}")
    print(f"文字起始Y: {start_y:.1f}")
    
    # 绘制文字
    current_y = start_y
    for i, char in enumerate(seal_text):
        char_width = char_widths[i]
        x = text_center_x - char_width // 2
        draw.text((x, current_y), char, fill='white', font=font)
        current_y += char_heights[i] + spacing
    
    return img

def create_gourd_seal_horizontal_text():
    """创建水平排列文字的葫芦印章"""
    size = 300
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # 葫芦形状（同上）
    points = [
        (size//2, size//8),
        (size//2 + size//10, size//6), 
        (size//2 + size//5, size//4), 
        (size//2 + size//3, size//3),
        (size//2 + size//3, size//2),
        (size//2 + size//3, size//2 + size//4),
        (size//2 + size//4, size - size//8),
        (size//2, size - size//10),
        (size//2 - size//4, size - size//8),
        (size//2 - size//3, size//2 + size//4),
        (size//2 - size//3, size//2),
        (size//2 - size//3, size//3),
        (size//2 - size//5, size//4),
        (size//2 - size//10, size//6),
        (size//2, size//8)
    ]
    
    draw.polygon(points, fill=(255, 0, 0, 220), outline=(180, 0, 0, 255), width=3)
    draw.ellipse([size//2 - size//20, size//16, size//2 + size//20, size//8], 
                fill=(255, 0, 0, 220), outline=(180, 0, 0, 255), width=2)
    
    # 添加水平排列的文字
    try:
        font = ImageFont.truetype("simhei.ttf", 32)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 32)
        except:
            font = ImageFont.load_default()
    
    text = "薯丝卅三"
    
    # 计算整个文字的宽度和高度
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 居中位置
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    return img

def create_gourd_seal_circular_text():
    """创建圆形排列文字的葫芦印章"""
    size = 300
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # 葫芦形状
    points = [
        (size//2, size//8),
        (size//2 + size//10, size//6), 
        (size//2 + size//5, size//4), 
        (size//2 + size//3, size//3),
        (size//2 + size//3, size//2),
        (size//2 + size//3, size//2 + size//4),
        (size//2 + size//4, size - size//8),
        (size//2, size - size//10),
        (size//2 - size//4, size - size//8),
        (size//2 - size//3, size//2 + size//4),
        (size//2 - size//3, size//2),
        (size//2 - size//3, size//3),
        (size//2 - size//5, size//4),
        (size//2 - size//10, size//6),
        (size//2, size//8)
    ]
    
    draw.polygon(points, fill=(255, 0, 0, 220), outline=(180, 0, 0, 255), width=3)
    draw.ellipse([size//2 - size//20, size//16, size//2 + size//20, size//8], 
                fill=(255, 0, 0, 220), outline=(180, 0, 0, 255), width=2)
    
    # 添加环绕文字（简化版）
    try:
        font = ImageFont.truetype("simhei.ttf", 28)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
        except:
            font = ImageFont.load_default()
    
    text = "薯丝卅三"
    
    # 在葫芦内部四个方向放置文字
    radius = size // 4
    center_x, center_y = size // 2, size // 2
    
    positions = [
        (center_x - 15, center_y - radius + 20),  # 上
        (center_x + radius - 60, center_y - 10),  # 右
        (center_x - 15, center_y + radius - 50),  # 下
        (center_x - radius + 20, center_y - 10),  # 左
    ]
    
    for i, char in enumerate(text):
        if i < len(positions):
            x, y = positions[i]
            draw.text((x, y), char, fill=(255, 255, 255, 255), font=font)
    
    return img
