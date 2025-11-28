

from PIL import Image, ImageDraw, ImageFont
import math
import os

# 创建输出目录
os.makedirs('seals', exist_ok=True)

def create_square_seal():
    """创建方形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 红色背景
    draw.rectangle([20, 20, size-20, size-20], fill='red', outline='darkred', width=3)
    
    # 文字
    try:
        font = ImageFont.truetype("simhei.ttf", 60)  # 黑体
    except:
        font = ImageFont.load_default()
    
    text = "方形章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/square_seal.png')
    print("方形印章已生成")

def create_rectangle_seal():
    """创建长方形印章"""
    width, height = 400, 200
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # 红色背景
    draw.rectangle([20, 20, width-20, height-20], fill='red', outline='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "长方形章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((width - text_width) // 2, (height - 40) // 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/rectangle_seal.png')
    print("长方形印章已生成")

def create_circle_seal():
    """创建圆形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 红色圆形
    draw.ellipse([20, 20, size-20, size-20], fill='red', outline='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 50)
    except:
        font = ImageFont.load_default()
    
    text = "圆形章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, size // 2 - 25)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/circle_seal.png')
    print("圆形印章已生成")

def create_oval_seal():
    """创建椭圆形印章"""
    width, height = 350, 250
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # 红色椭圆
    draw.ellipse([20, 20, width-20, height-20], fill='red', outline='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 45)
    except:
        font = ImageFont.load_default()
    
    text = "椭圆章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((width - text_width) // 2, (height - 45) // 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/oval_seal.png')
    print("椭圆形印章已生成")

def create_triangle_seal():
    """创建三角形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 三角形顶点
    points = [
        (size // 2, 30),
        (size - 30, size - 30),
        (30, size - 30)
    ]
    
    draw.polygon(points, fill='red', outline='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "三角章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, size // 2 - 20)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/triangle_seal.png')
    print("三角形印章已生成")

def create_gourd_seal():
    """创建葫芦形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 绘制葫芦形状（两个椭圆组成）
    # 上半部分
    draw.ellipse([100, 50, 200, 150], fill='red', outline='darkred', width=2)
    # 下半部分
    draw.ellipse([80, 120, 220, 250], fill='red', outline='darkred', width=2)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    text = "葫芦章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal.png')
    print("葫芦形印章已生成")

def create_heart_seal():
    """创建心形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 简单的心形绘制
    # 心形可以通过两个圆形和一个三角形组成
    draw.ellipse([80, 70, 150, 140], fill='red')  # 左圆
    draw.ellipse([150, 70, 220, 140], fill='red')  # 右圆
    
    # 下方的三角形部分
    points = [(80, 110), (220, 110), (150, 200)]
    draw.polygon(points, fill='red')
    
    # 描边
    draw.ellipse([80, 70, 150, 140], outline='darkred', width=2)
    draw.ellipse([150, 70, 220, 140], outline='darkred', width=2)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    text = "心形章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 120)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/heart_seal.png')
    print("心形印章已生成")

def create_diamond_seal():
    """创建菱形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 菱形顶点
    points = [
        (size // 2, 30),      # 上
        (size - 30, size // 2),  # 右
        (size // 2, size - 30),  # 下
        (30, size // 2)       # 左
    ]
    
    draw.polygon(points, fill='red', outline='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "菱形章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, size // 2 - 20)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/diamond_seal.png')
    print("菱形印章已生成")

def create_leaf_seal():
    """创建叶形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 简单的叶子形状（椭圆加茎）
    # 叶身
    draw.ellipse([100, 80, 200, 180], fill='red', outline='darkred', width=2)
    
    # 叶茎
    draw.line([(150, 180), (150, 220)], fill='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    text = "叶形章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 120)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/leaf_seal.png')
    print("叶形印章已生成")

from PIL import Image, ImageDraw, ImageFont

def create_gourd_seal_with_stem():
    """创建带蒂的葫芦形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 创建掩模来绘制完整的葫芦形状
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    # 绘制葫芦主体（两个椭圆）
    # 上半部分（较小）
    mask_draw.ellipse([110, 70, 190, 150], fill=255)
    # 下半部分（较大）
    mask_draw.ellipse([90, 130, 210, 250], fill=255)
    
    # 绘制葫芦蒂（细长的椭圆形）
    mask_draw.ellipse([140, 50, 160, 75], fill=255)  # 蒂的主体
    
    # 应用红色填充
    red_img = Image.new('RGB', (size, size), 'red')
    img.paste(red_img, mask=mask)
    
    # 绘制外边框
    draw.ellipse([110, 70, 190, 150], outline='darkred', width=3)  # 上椭圆边框
    draw.ellipse([90, 130, 210, 250], outline='darkred', width=3)  # 下椭圆边框
    draw.ellipse([140, 50, 160, 75], outline='darkred', width=2)   # 蒂的边框
    
    # 在蒂的顶部加一个小圆点，更像真实的葫芦蒂
    draw.ellipse([147, 48, 153, 54], fill='darkred')
    
    try:
        font = ImageFont.truetype("simhei.ttf", 35)
    except:
        font = ImageFont.load_default()
    
    text = "葫芦章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_with_stem.png')
    print("带蒂葫芦形印章已生成")

def create_gourd_seal_detailed():
    """创建更详细的带蒂葫芦形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 使用多边形绘制更自然的葫芦形状
    # 葫芦形状的轮廓点（从蒂开始顺时针绘制）
    points = [
        # 葫芦蒂
        (148, 45), (152, 45),  # 蒂顶部
        
        # 蒂底部连接到葫芦主体
        (154, 55), (158, 60), (165, 65),
        
        # 葫芦上半部分右曲线
        (175, 68), (185, 75), (192, 85), (195, 95),
        (195, 110), (192, 125), (185, 135), (175, 142),
        
        # 葫芦腰部右曲线
        (165, 145), (155, 148),
        
        # 葫芦下半部分右曲线
        (145, 155), (135, 170), (130, 190), (130, 210),
        (135, 230), (145, 245), (160, 255), (175, 258),
        
        # 葫芦下半部分左曲线
        (125, 258), (110, 255), (95, 245), (85, 230),
        (80, 210), (80, 190), (85, 170), (95, 155),
        
        # 葫芦腰部左曲线
        (105, 148), (95, 145),
        
        # 葫芦上半部分左曲线
        (85, 142), (75, 135), (68, 125), (65, 110),
        (65, 95), (68, 85), (75, 75), (85, 68),
        
        # 连接到蒂的左曲线
        (95, 65), (102, 60), (106, 55),
        
        # 回到蒂顶部
        (148, 45)
    ]
    
    # 绘制葫芦主体
    draw.polygon(points, fill='red', outline='darkred', width=2)
    
    # 添加蒂的细节（更自然的蒂形状）
    stem_points = [
        (145, 45), (148, 40), (152, 40), (155, 45),
        (152, 55), (148, 55), (145, 45)
    ]
    draw.polygon(stem_points, fill='red', outline='darkred', width=2)
    
    # 在蒂上添加纹理线条
    draw.line([(148, 42), (148, 52)], fill='darkred', width=1)
    draw.line([(152, 42), (152, 52)], fill='darkred', width=1)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 35)
    except:
        font = ImageFont.load_default()
    
    text = "福禄"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_detailed.png')
    print("详细版带蒂葫芦形印章已生成")

def create_gourd_seal_traditional():
    """创建传统风格的带蒂葫芦印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 使用更简单的方法：两个椭圆+蒂
    # 上半部分椭圆
    draw.ellipse([110, 80, 190, 160], fill='red', outline='darkred', width=3)
    # 下半部分椭圆
    draw.ellipse([95, 150, 205, 260], fill='red', outline='darkred', width=3)
    
    # 绘制葫芦蒂（更自然的弯曲形状）
    # 蒂的主体
    draw.ellipse([140, 60, 160, 85], fill='red', outline='darkred', width=2)
    
    # 蒂的顶部小圆球
    draw.ellipse([145, 55, 155, 65], fill='red', outline='darkred', width=2)
    
    # 蒂的弯曲部分
    draw.arc([135, 70, 165, 90], start=180, end=360, fill='darkred', width=2)
    
    # 在葫芦腰部添加一条装饰线，增强立体感
    draw.arc([100, 140, 200, 170], start=0, end=180, fill='darkred', width=2)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "葫芦"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 170)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_traditional.png')
    print("传统风格带蒂葫芦印章已生成")

from PIL import Image, ImageDraw, ImageFont

def create_gourd_seal_no_intersection():
    """创建无相交边线的葫芦形印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 创建掩模来绘制完整的葫芦形状
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    # 绘制葫芦主体（两个椭圆，重叠部分自然融合）
    # 上半部分椭圆
    mask_draw.ellipse([110, 70, 190, 150], fill=255)
    # 下半部分椭圆
    mask_draw.ellipse([90, 130, 210, 250], fill=255)
    
    # 绘制葫芦蒂
    mask_draw.ellipse([140, 50, 160, 75], fill=255)
    
    # 应用红色填充
    red_img = Image.new('RGB', (size, size), 'red')
    img.paste(red_img, mask=mask)
    
    # 绘制外边框（只绘制外部轮廓，不绘制内部相交线）
    # 计算葫芦的整体轮廓点
    outline_points = [
        # 从蒂开始，顺时针绘制
        (150, 50),  # 蒂顶部中点
        
        # 右上半部分
        (160, 55), (170, 65), (180, 80), (188, 100),
        (190, 120), (190, 140),  # 上半部分右下方
        
        # 右下半部分（直接连接到下半部分）
        (200, 150), (205, 170), (205, 200), (200, 230),
        (190, 250), (170, 260),  # 下半部分右下方
        
        # 左下半部分
        (130, 260), (110, 250), (100, 230), (95, 200),
        (95, 170), (100, 150),  # 下半部分左下方
        
        # 左上半部分（直接连接到上半部分）
        (110, 140), (110, 120), (112, 100), (120, 80),
        (130, 65), (140, 55),  # 回到蒂部
        
        (150, 50)  # 闭合
    ]
    
    # 绘制平滑的葫芦外边框
    draw.line(outline_points, fill='darkred', width=3, joint='curve')
    
    # 绘制闭合的蒂部
    draw.ellipse([140, 50, 160, 75], outline='darkred', width=2)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 35)
    except:
        font = ImageFont.load_default()
    
    text = "葫芦章"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_no_intersection.png')
    print("无相交边线葫芦印章已生成")

def create_gourd_seal_single_outline():
    """创建单一边框的葫芦印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 创建掩模
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    # 绘制完整的葫芦形状
    # 上半部分
    mask_draw.ellipse([110, 70, 190, 150], fill=255)
    # 下半部分
    mask_draw.ellipse([90, 130, 210, 250], fill=255)
    # 蒂
    mask_draw.ellipse([140, 50, 160, 75], fill=255)
    
    # 填充红色
    red_img = Image.new('RGB', (size, size), 'red')
    img.paste(red_img, mask=mask)
    
    # 方法二：使用贝塞尔曲线绘制单一外边框
    # 定义葫芦的关键控制点
    start_x, start_y = 150, 50  # 蒂顶部
    
    # 绘制右半部分轮廓
    right_points = [
        (150, 50), (160, 55), (175, 70), (185, 90),
        (190, 110), (192, 130), (195, 150), (200, 170),
        (200, 200), (195, 230), (185, 250), (170, 260),
        (150, 262)  # 底部中点
    ]
    
    # 绘制左半部分轮廓
    left_points = [
        (150, 262), (130, 260), (115, 250), (105, 230),
        (100, 200), (100, 170), (105, 150), (110, 130),
        (110, 110), (115, 90), (125, 70), (140, 55),
        (150, 50)
    ]
    
    # 绘制完整轮廓
    all_points = right_points + left_points
    for i in range(len(all_points) - 1):
        draw.line([all_points[i], all_points[i+1]], fill='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 35)
    except:
        font = ImageFont.load_default()
    
    text = "福禄"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_single_outline.png')
    print("单一边框葫芦印章已生成")

def create_gourd_seal_clean():
    """创建干净无相交线的葫芦印章（最佳版本）"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 直接绘制一个完整的葫芦形状多边形
    points = [
        # 葫芦蒂（从顶部开始）
        (148, 45), (152, 45),
        
        # 右上半部分
        (160, 55), (170, 65), (180, 80), (188, 100),
        (190, 120), (190, 140),
        
        # 右下半部分（平滑过渡）
        (195, 150), (200, 170), (200, 200),
        (195, 225), (185, 245), (170, 255),
        
        # 左下半部分
        (130, 255), (115, 245), (105, 225),
        (100, 200), (100, 170), (105, 150),
        
        # 左上半部分（平滑过渡）
        (110, 140), (110, 120), (112, 100),
        (120, 80), (130, 65), (140, 55),
        
        # 回到蒂部
        (148, 45)
    ]
    
    # 填充葫芦主体
    draw.polygon(points, fill='red')
    
    # 绘制单一外边框
    draw.line(points, fill='darkred', width=3, joint='curve')
    
    # 闭合图形
    draw.line([points[-1], points[0]], fill='darkred', width=3)
    
    # 添加蒂的细节
    draw.ellipse([145, 43, 155, 53], fill='red', outline='darkred', width=2)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "葫芦"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_clean.png')
    print("干净无相交线葫芦印章已生成")

def create_gourd_seal_simple_fix():
    """最简单的修复版本 - 使用单一形状"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 定义一个完整的葫芦形状（贝塞尔曲线控制点）
    # 这种方法确保只有一个连续的边框
    
    # 葫芦形状的多边形点
    gourd_points = [
        (150, 40),  # 蒂顶
        
        # 右上曲线
        (165, 45), (180, 60), (190, 80), (195, 105),
        (195, 130), (192, 155), (185, 175),
        
        # 右下曲线
        (195, 190), (200, 210), (200, 235), (195, 255),
        (185, 270), (170, 280),
        
        # 左下曲线
        (130, 280), (115, 270), (105, 255), (100, 235),
        (100, 210), (105, 190),
        
        # 左上曲线
        (115, 175), (108, 155), (105, 130), (105, 105),
        (110, 80), (120, 60), (135, 45),
        
        (150, 40)  # 闭合
    ]
    
    # 绘制填充
    draw.polygon(gourd_points, fill='red')
    
    # 绘制边框 - 只有一个连续的边框
    for i in range(len(gourd_points) - 1):
        draw.line([gourd_points[i], gourd_points[i+1]], 
                 fill='darkred', width=3)
    # 闭合最后一段
    draw.line([gourd_points[-1], gourd_points[0]], 
             fill='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 45)
    except:
        font = ImageFont.load_default()
    
    text = "葫"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_simple_fix.png')
    print("简单修复版葫芦印章已生成")

from PIL import Image, ImageDraw, ImageFont

def create_gourd_seal_single_outline_fixed():
    """修复边框脱离问题的葫芦印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 定义葫芦的轮廓点（与填充使用相同的点集）
    points = [
        # 葫芦蒂（从顶部开始）
        (148, 45), (152, 45),
        
        # 右上半部分
        (160, 55), (170, 65), (180, 80), (188, 100),
        (190, 120), (190, 140),
        
        # 右下半部分（平滑过渡）
        (195, 150), (200, 170), (200, 200),
        (195, 225), (185, 245), (170, 255),
        
        # 左下半部分
        (130, 255), (115, 245), (105, 225),
        (100, 200), (100, 170), (105, 150),
        
        # 左上半部分（平滑过渡）
        (110, 140), (110, 120), (112, 100),
        (120, 80), (130, 65), (140, 55),
        
        # 回到蒂部
        (148, 45)
    ]
    
    # 先绘制填充
    draw.polygon(points, fill='red')
    
    # 再绘制边框 - 使用相同的点集
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill='darkred', width=3)
    # 闭合最后一段
    draw.line([points[-1], points[0]], fill='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "葫芦"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_single_outline_fixed.png')
    print("修复边框脱离的葫芦印章已生成")

def create_gourd_seal_perfect():
    """创建完美的葫芦印章（推荐使用）"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 精心调整的葫芦轮廓点
    points = [
        # 蒂顶部
        (149, 42), (151, 42),
        
        # 右上半部分（平滑曲线）
        (158, 48), (168, 58), (178, 73), (185, 93),
        (188, 113), (188, 133), (185, 148),
        
        # 右下半部分（自然过渡）
        (192, 158), (196, 173), (196, 198),
        (192, 223), (184, 243), (172, 257),
        
        # 左下半部分
        (128, 257), (116, 243), (108, 223),
        (104, 198), (104, 173), (108, 158),
        
        # 左上半部分
        (115, 148), (112, 133), (112, 113),
        (115, 93), (122, 73), (132, 58),
        (142, 48),
        
        # 回到蒂部
        (149, 42)
    ]
    
    # 绘制填充和边框
    draw.polygon(points, fill='red', outline='darkred', width=3)
    
    # 添加蒂的细节
    draw.ellipse([146, 38, 154, 46], fill='red', outline='darkred', width=2)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 45)
    except:
        font = ImageFont.load_default()
    
    text = "葫"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2 - 10)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_perfect.png')
    print("完美版葫芦印章已生成")

def create_gourd_seal_smooth():
    """创建平滑边框的葫芦印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 更密集的点集以获得更平滑的曲线
    points = [
        (150, 40),  # 0: 蒂顶
        
        # 右上曲线 - 更密集的点
        (155, 42), (160, 45), (165, 49), (170, 54),  # 1-4
        (175, 60), (178, 65), (182, 72), (185, 78),  # 5-8
        (187, 85), (189, 92), (190, 100), (190, 108), # 9-12
        (190, 116), (189, 124), (187, 132), (184, 139), # 13-16
        (181, 146), (178, 152), (175, 158),          # 17-19
        
        # 右下曲线
        (178, 163), (182, 170), (185, 178), (187, 186), # 20-23
        (188, 194), (188, 202), (187, 210), (185, 218), # 24-27
        (182, 225), (178, 232), (173, 238), (168, 243), # 28-31
        (162, 248), (156, 252), (150, 255),            # 32-34
        
        # 左下曲线
        (144, 252), (138, 248), (132, 243), (127, 238), # 35-38
        (122, 232), (118, 225), (115, 218), (113, 210), # 39-42
        (112, 202), (112, 194), (113, 186), (115, 178), # 43-46
        (118, 170), (122, 163), (125, 158),            # 47-49
        
        # 左上曲线
        (122, 152), (119, 146), (116, 139), (113, 132), # 50-53
        (111, 124), (110, 116), (110, 108), (110, 100), # 54-57
        (111, 92), (113, 85), (115, 78), (118, 72),    # 58-61
        (122, 65), (125, 60), (130, 54), (135, 49),    # 62-65
        (140, 45), (145, 42),                          # 66-67
        
        (150, 40)  # 68: 闭合
    ]
    
    # 使用polygon的outline参数确保边框与填充完美匹配
    draw.polygon(points, fill='red', outline='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 50)
    except:
        font = ImageFont.load_default()
    
    text = "福"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_smooth.png')
    print("平滑边框葫芦印章已生成")

from PIL import Image, ImageDraw, ImageFont

def create_gourd_seal_single_outline_fixed_v2():
    """修复边框脱离问题，同时保持精致蒂部"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 定义葫芦主体轮廓点
    body_points = [
        # 从蒂底部开始
        (142, 55), (145, 58),
        
        # 右上半部分
        (155, 60), (165, 68), (175, 80), (182, 95),
        (185, 110), (185, 130), (182, 145),
        
        # 右下半部分（平滑过渡）
        (188, 155), (192, 170), (192, 195),
        (188, 220), (180, 240), (168, 255),
        
        # 左下半部分
        (132, 255), (120, 240), (112, 220),
        (108, 195), (108, 170), (112, 155),
        
        # 左上半部分
        (118, 145), (115, 130), (115, 110),
        (118, 95), (125, 80), (135, 68),
        (142, 58),
        
        # 回到蒂底部
        (142, 55)
    ]
    
    # 定义精致蒂部轮廓点
    stem_points = [
        # 蒂的精致形状
        (146, 42), (148, 40), (152, 40), (154, 42),
        (152, 50), (148, 50), (146, 42)
    ]
    
    # 绘制葫芦主体填充和边框
    draw.polygon(body_points, fill='red', outline='darkred', width=3)
    
    # 绘制精致蒂部填充和边框
    draw.polygon(stem_points, fill='red', outline='darkred', width=2)
    
    # 在蒂上添加精致的纹理线条
    draw.line([(148, 42), (148, 48)], fill='darkred', width=1)
    draw.line([(152, 42), (152, 48)], fill='darkred', width=1)
    
    # 蒂顶部的小圆球装饰
    draw.ellipse([149, 39, 151, 41], fill='darkred')
    
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "葫芦"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_single_outline_fixed_v2.png')
    print("修复边框且保持精致蒂部的葫芦印章已生成")

def create_gourd_seal_elegant():
    """创建优雅版的葫芦印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 完整的葫芦轮廓点（包含精致蒂部）
    points = [
        # 蒂顶部（精致弯曲）
        (147, 38), (149, 36), (151, 36), (153, 38),
        
        # 蒂底部到葫芦主体
        (152, 42), (155, 45), (158, 48),
        
        # 右上半部分
        (165, 52), (172, 60), (178, 70), (183, 82),
        (186, 95), (186, 110), (185, 125), (182, 138),
        
        # 右下半部分
        (185, 148), (188, 160), (188, 180), (186, 200),
        (182, 218), (176, 235), (168, 248), (158, 258),
        
        # 左下半部分
        (142, 258), (132, 248), (124, 235), (118, 218),
        (114, 200), (112, 180), (112, 160), (115, 148),
        
        # 左上半部分
        (118, 138), (115, 125), (114, 110), (114, 95),
        (117, 82), (122, 70), (128, 60), (135, 52),
        
        # 回到蒂部
        (142, 48), (145, 45), (148, 42),
        (147, 38)  # 闭合
    ]
    
    # 一次性绘制完整的葫芦（包含精致蒂部）
    draw.polygon(points, fill='red', outline='darkred', width=3)
    
    # 添加蒂部的精致细节
    draw.ellipse([148, 35, 152, 39], fill='red', outline='darkred', width=1)
    draw.line([(149, 37), (149, 43)], fill='darkred', width=1)
    draw.line([(151, 37), (151, 43)], fill='darkred', width=1)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 45)
    except:
        font = ImageFont.load_default()
    
    text = "福禄"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_elegant.png')
    print("优雅版葫芦印章已生成")

def create_gourd_seal_traditional_refined():
    """传统精致版葫芦印章"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 使用更精细的点集定义葫芦形状
    points = [
        # 精致蒂部 - 弯曲的葫芦蒂
        (148, 35), (149, 34), (151, 34), (152, 35),
        (153, 37), (153, 40), (152, 42), (150, 43),
        (148, 43), (146, 42), (145, 40), (145, 37),
        (146, 35), (148, 35),
        
        # 从蒂底部平滑过渡到葫芦主体
        (148, 43), (150, 44), (152, 45),
        
        # 右上半部分（密集点集确保平滑）
        (155, 47), (158, 50), (162, 54), (166, 59),
        (170, 65), (173, 72), (176, 79), (178, 87),
        (180, 95), (180, 105), (180, 115), (178, 125),
        (176, 134), (173, 142), (170, 149),
        
        # 右下半部分
        (172, 155), (175, 162), (177, 170), (178, 178),
        (179, 187), (179, 196), (178, 205), (176, 214),
        (173, 222), (169, 230), (164, 237), (158, 243),
        (152, 248), (146, 252),
        
        # 左下半部分
        (140, 252), (134, 248), (128, 243), (122, 237),
        (117, 230), (113, 222), (110, 214), (108, 205),
        (107, 196), (107, 187), (108, 178), (110, 170),
        (112, 162), (115, 155), (117, 149),
        
        # 左上半部分
        (114, 142), (111, 134), (109, 125), (108, 115),
        (108, 105), (108, 95), (110, 87), (112, 79),
        (115, 72), (118, 65), (122, 59), (126, 54),
        (130, 50), (134, 47), (138, 45),
        
        # 回到蒂底部
        (142, 44), (145, 43), (148, 43)
    ]
    
    # 绘制完整的精致葫芦
    draw.polygon(points, fill='red', outline='darkred', width=3)
    
    # 在葫芦腰部添加传统装饰线
    draw.arc([120, 140, 180, 160], start=0, end=180, fill='darkred', width=2)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 42)
    except:
        font = ImageFont.load_default()
    
    text = "吉祥"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_traditional_refined.png')
    print("传统精致版葫芦印章已生成")

from PIL import Image, ImageDraw, ImageFont

def create_gourd_seal_simple_fixed():
    """简洁修复版 - 回到基础设计"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 简单的葫芦形状：两个椭圆 + 蒂
    # 上半部分椭圆
    draw.ellipse([110, 80, 190, 160], fill='red')
    # 下半部分椭圆  
    draw.ellipse([95, 150, 205, 260], fill='red')
    # 蒂
    draw.ellipse([145, 65, 155, 80], fill='red')
    
    # 单一外边框 - 手动绘制葫芦轮廓
    outline_points = [
        # 从蒂开始
        (150, 65),
        # 右上轮廓
        (160, 70), (170, 80), (180, 95), (185, 110),
        (188, 125), (188, 140), (190, 150),
        # 右下轮廓
        (195, 160), (200, 175), (200, 200), (195, 225),
        (185, 245), (170, 255),
        # 左下轮廓
        (130, 255), (115, 245), (105, 225), (100, 200),
        (100, 175), (105, 160), (110, 150),
        # 左上轮廓
        (112, 140), (112, 125), (115, 110), (120, 95),
        (130, 80), (140, 70),
        # 回到蒂
        (150, 65)
    ]
    
    # 绘制外边框
    for i in range(len(outline_points) - 1):
        draw.line([outline_points[i], outline_points[i+1]], 
                 fill='darkred', width=3)
    draw.line([outline_points[-1], outline_points[0]], 
             fill='darkred', width=3)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 45)
    except:
        font = ImageFont.load_default()
    
    text = "葫芦"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    position = ((size - text_width) // 2, 160)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_simple_fixed.png')
    print("简洁修复版葫芦印章已生成")

def create_gourd_seal_clean_final():
    """最终清洁版 - 最简单的解决方案"""
    size = 300
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)
    
    # 方法：先绘制完整填充，再绘制单一外边框
    # 1. 绘制填充
    draw.ellipse([110, 80, 190, 160], fill='red')  # 上椭圆
    draw.ellipse([95, 150, 205, 260], fill='red')  # 下椭圆  
    draw.ellipse([145, 65, 155, 80], fill='red')   # 蒂
    
    # 2. 绘制单一外边框（避开内部相交线）
    # 只绘制外部可见的边框部分
    # 上椭圆的上半部分边框
    draw.arc([110, 80, 190, 160], start=0, end=180, fill='darkred', width=3)
    # 下椭圆的下半部分边框
    draw.arc([95, 150, 205, 260], start=180, end=360, fill='darkred', width=3)
    # 左右两侧的直线边框
    draw.line([(110, 120), (95, 180)], fill='darkred', width=3)  # 左上
    draw.line([(110, 120), (95, 180)], fill='darkred', width=3)  # 左下
    draw.line([(190, 120), (205, 180)], fill='darkred', width=3)  # 右上
    draw.line([(190, 120), (205, 180)], fill='darkred', width=3)  # 右下
    # 蒂的边框
    draw.ellipse([145, 65, 155, 80], outline='darkred', width=2)
    
    try:
        font = ImageFont.truetype("simhei.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "葫"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save('seals/gourd_seal_clean_final.png')
    print("最终清洁版葫芦印章已生成")

# def create_gourd_seal_best(seal_text="福禄", size=300):
#     """最佳版本 - 使用相对坐标，支持任意尺寸"""
#     img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(img)
    
#     # 计算比例因子（基于原始300x300尺寸）
#     scale = size / 300.0
    
#     # 定义相对坐标点（基于比例）
#     points = [
#         (0.5, 70/300),    # 蒂底 (150, 70) -> (0.5, 0.233)
        
#         # 右上
#         (160/300, 75/300), (170/300, 85/300), (180/300, 100/300), (185/300, 120/300),
#         (185/300, 140/300), (190/300, 155/300),
        
#         # 右下  
#         (195/300, 170/300), (200/300, 190/300), (200/300, 220/300), (195/300, 245/300),
#         (185/300, 260/300), (170/300, 270/300),
        
#         # 左下
#         (130/300, 270/300), (115/300, 260/300), (105/300, 245/300), (100/300, 220/300), 
#         (100/300, 190/300), (105/300, 170/300), (110/300, 155/300),
        
#         # 左上
#         (115/300, 140/300), (115/300, 120/300), (120/300, 100/300), (130/300, 85/300),
#         (140/300, 75/300),
        
#         (0.5, 70/300)     # 闭合 (150, 70) -> (0.5, 0.233)
#     ]
    
#     # 将相对坐标转换为实际坐标
#     actual_points = [(x * size, y * size) for x, y in points]
    
#     # 一次绘制完成
#     draw.polygon(actual_points, fill='red', outline='darkred', width=int(3 * scale))
    
#     # 添加简单蒂部（使用相对坐标）
#     ellipse_x1 = 147/300 * size
#     ellipse_y1 = 60/300 * size
#     ellipse_x2 = 153/300 * size
#     ellipse_y2 = 70/300 * size
#     draw.ellipse([ellipse_x1, ellipse_y1, ellipse_x2, ellipse_y2], 
#                 fill='red', outline='darkred', width=int(2 * scale))
    
#     # 计算葫芦内部可用空间
#     # 葫芦的大致内部尺寸（相对坐标）
#     inner_width = 0.4 * size   # 内部宽度
#     inner_height = 0.6 * size  # 内部高度
    
#     # 自适应文字大小
#     text_length = len(seal_text)
    
#     # 根据文字长度和可用空间计算最大字体大小
#     max_char_height = inner_height / text_length * 0.8  # 每个字符最大高度
#     max_char_width = inner_width * 0.9  # 每个字符最大宽度
    
#     # 初始字体大小
#     font_size = int(min(max_char_height, max_char_width))
#     font_size = max(10, min(font_size, 300))  # 限制在10-40之间
    
#     # 文字大小也按比例缩放
#     try:
#         # font_size = int(50 * scale)
#         font = ImageFont.truetype("simhei.ttf", font_size)
#     except:
#         try:
#             font_size = int(50 * scale)
#             font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
#         except:
#             font_size = int(50 * scale)
#             font = ImageFont.load_default()
    
#     # 计算总高度（包括间距）
#     spacing = font_size * 0.1  # 较小的间距
#     total_text_height = sum(char_heights) + (text_length - 1) * spacing
    
#     # **关键修正：使用葫芦内部空间的中心，而不是整个图片的中心**
#     text_center_x = (inner_left + inner_right) // 2
#     text_center_y = (inner_top + inner_bottom) // 2
    
#     # **修正起始位置：从中心向上偏移一半文字高度**
#     start_y = text_center_y - total_text_height // 2
    
#     print(f"文字总高度: {total_text_height:.1f}")
#     print(f"内部空间中心Y: {text_center_y:.1f}")
#     print(f"文字起始Y: {start_y:.1f}")
    
#     # 绘制文字
#     current_y = start_y
#     for i, char in enumerate(seal_text):
#         char_width = char_widths[i]
#         x = text_center_x - char_width // 2
#         draw.text((x, current_y), char, fill='white', font=font)
#         current_y += char_heights[i] + spacing
    
#     return img

def create_gourd_seal_best(seal_text="福禄", size=300):
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

def create_gourd_seal_with_text():
    """创建带有'薯丝卅三'文字的葫芦印章"""
    size = 300
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))  # 透明背景
    draw = ImageDraw.Draw(img)
    
    # 葫芦形状
    points = [
        (size//2, size//8),  # 蒂底
        
        # 右上
        (size//2 + size//10, size//6), 
        (size//2 + size//5, size//4), 
        (size//2 + size//3, size//3),
        (size//2 + size//3, size//2),
        
        # 右下  
        (size//2 + size//3, size//2 + size//4),
        (size//2 + size//4, size - size//8),
        (size//2, size - size//10),
        
        # 左下
        (size//2 - size//4, size - size//8),
        (size//2 - size//3, size//2 + size//4),
        (size//2 - size//3, size//2),
        
        # 左上
        (size//2 - size//3, size//3),
        (size//2 - size//5, size//4),
        (size//2 - size//10, size//6),
        
        (size//2, size//8)  # 闭合
    ]
    
    # 绘制红色葫芦
    draw.polygon(points, fill=(255, 0, 0, 220), outline=(180, 0, 0, 255), width=3)
    
    # 添加蒂
    draw.ellipse([size//2 - size//20, size//16, size//2 + size//20, size//8], 
                fill=(255, 0, 0, 220), outline=(180, 0, 0, 255), width=2)
    
    # 添加文字"薯丝卅三"
    try:
        # 尝试使用系统中文字体
        font = ImageFont.truetype("simhei.ttf", 36)  # 黑体
        # 或者使用其他中文字体：
        # font = ImageFont.truetype("msyh.ttc", 36)  # 微软雅黑
        # font = ImageFont.truetype("simsun.ttc", 36)  # 宋体
    except:
        try:
            # macOS 系统字体
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
        except:
            try:
                # Linux 系统字体
                font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 36)
            except:
                # 如果都找不到，使用默认字体（可能显示不全）
                font = ImageFont.load_default()
                print("警告：未找到中文字体，文字可能无法正常显示")
    
    text = "薯丝卅三"
    
    # 计算文字位置（垂直排列）
    char_height = 40  # 每个字符的高度
    total_text_height = char_height * len(text)
    start_y = (size - total_text_height) // 2
    
    # 逐个绘制字符（从上到下）
    for i, char in enumerate(text):
        bbox = draw.textbbox((0, 0), char, font=font)
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        
        x = (size - char_width) // 2
        y = start_y + i * char_height
        
        # 绘制白色文字，带一点黑色描边效果
        draw.text((x, y), char, fill=(255, 255, 255, 255), font=font)
    
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

def add_seal_to_image_with_text(image_path, start_x, start_y, seal_size=150, text_style="vertical"):
    """将带文字的葫芦印章添加到图片"""
    # 打开目标图片
    target_img = Image.open(image_path).convert('RGBA')
    
    # 根据文字样式选择印章
    if text_style == "horizontal":
        seal = create_gourd_seal_horizontal_text()
    elif text_style == "circular":
        seal = create_gourd_seal_circular_text()
    else:  # vertical
        # seal_size = 300
        seal = create_gourd_seal_best("薯丝卅三", seal_size)        # create_gourd_seal_with_text()
    
    # 调整印章大小
    seal = seal.resize((seal_size, seal_size), Image.Resampling.LANCZOS)
    
    # 合并图片
    result = target_img.copy()
    result.paste(seal, (start_x, start_y), seal)
    
    return result

# 生成所有版本
if __name__ == "__main__":
    # 生成三种文字排列方式的印章
    seal1 = create_gourd_seal_with_text()  # 垂直排列
    seal1.save('gourd_seal_vertical.png')
    
    seal2 = create_gourd_seal_horizontal_text()  # 水平排列
    seal2.save('gourd_seal_horizontal.png')
    
    seal3 = create_gourd_seal_circular_text()  # 环绕排列
    seal3.save('gourd_seal_circular.png')
    
    print("带有'薯丝卅三'文字的葫芦印章已生成！")
    print("文件：gourd_seal_vertical.png（垂直排列）")
    print("文件：gourd_seal_horizontal.png（水平排列）")
    print("文件：gourd_seal_circular.png（环绕排列）")  

    # 首先确保你有目标图片
    target_image_path = "banner_vertical_complete.png"  # 替换为你的图片路径

    # 如果还没有图片，可以先创建一个示例图片
    if not os.path.exists(target_image_path):
        # 创建示例图片
        sample_img = Image.new('RGB', (800, 600), 'white')
        draw = ImageDraw.Draw(sample_img)
        try:
            font = ImageFont.truetype("simhei.ttf", 60)
        except:
            font = ImageFont.load_default()
        draw.text((200, 250), "书法作品示例", fill='black', font=font)
        sample_img.save(target_image_path)
        print("已创建示例图片")

    # 调用函数添加印章
    result = add_seal_to_image_with_text(
        image_path=target_image_path,
        start_x=300,      # 印章左上角x坐标
        start_y=750,      # 印章左上角y坐标
        seal_size=200,    # 印章大小
        text_style="vertical"  # 文字排列方式
    )

    # 保存结果
    result.save("result_with_seal.png")
    print("印章添加完成！")  

# 运行简洁版本
if __name__ == "__main__":
    create_gourd_seal_simple_fixed()
    create_gourd_seal_clean_final()
    create_gourd_seal_best()
    print("所有简洁修复版葫芦印章已生成！")    

# 运行修复版本
if __name__ == "__main__":
    create_gourd_seal_single_outline_fixed_v2()
    create_gourd_seal_elegant()
    create_gourd_seal_traditional_refined()
    print("所有精致蒂部修复版葫芦印章已生成！")    

# 运行修复版本
if __name__ == "__main__":
    create_gourd_seal_single_outline_fixed()
    create_gourd_seal_perfect()
    create_gourd_seal_smooth()
    print("所有修复版葫芦印章已生成！")    

# 运行所有版本
if __name__ == "__main__":
    create_gourd_seal_no_intersection()
    create_gourd_seal_single_outline()
    create_gourd_seal_clean()
    create_gourd_seal_simple_fix()
    print("所有无相交边线的葫芦印章已生成！")

# 生成所有印章
if __name__ == "__main__":
    create_square_seal()
    create_rectangle_seal()
    create_circle_seal()
    create_oval_seal()
    create_triangle_seal()
    create_gourd_seal()
    create_gourd_seal_with_stem()
    create_gourd_seal_detailed()
    create_gourd_seal_traditional()
    create_heart_seal()
    create_diamond_seal()
    create_leaf_seal()
    
    print("\n所有印章已生成在 'seals' 文件夹中！")