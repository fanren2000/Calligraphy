from PIL import Image, ImageDraw, ImageFont, ImageFilter
from Utils.font_tools import safe_get_font
from Calli_Utils.seal_border_fancy_4char import add_four_character_seal
from Calli_Utils import convert_poem_to_char_matrix
import os
import numpy as np
import random
import math
import re

def generate_natural_torn_edge(width, height, roughness=0.5):
    """生成自然的撕边效果 - 结合平滑和粗糙元素"""
    margin = min(width, height) * 0.03
    
    points = []
    
    # 生成四边的控制点
    edges = [
        # 上边
        [(margin, margin), (width - margin, margin)],
        # 右边  
        [(width - margin, margin), (width - margin, height - margin)],
        # 下边
        [(width - margin, height - margin), (margin, height - margin)],
        # 左边
        [(margin, height - margin), (margin, margin)]
    ]
    
    for edge_start, edge_end in edges:
        edge_length = math.sqrt((edge_end[0]-edge_start[0])**2 + (edge_end[1]-edge_start[1])**2)
        segments = max(20, int(edge_length / 15))  # 动态分段
        
        for i in range(segments + 1):
            # 线性插值
            t = i / segments
            base_x = edge_start[0] + t * (edge_end[0] - edge_start[0])
            base_y = edge_start[1] + t * (edge_end[1] - edge_start[1])
            
            # 多频率噪声组合
            noise = 0
            
            # 1. 低频大波浪（整体形状）
            freq1 = 0.02
            amp1 = roughness * 8
            noise += math.sin(t * segments * freq1) * amp1
            
            # 2. 中频细节（主要撕边感）
            freq2 = 0.1
            amp2 = roughness * 4
            noise += math.sin(t * segments * freq2 + 1) * amp2
            
            # 3. 高频细节（纤维感）
            freq3 = 0.5
            amp3 = roughness * 2
            noise += math.sin(t * segments * freq3 + 2) * amp3
            
            # 4. 随机扰动（自然感）
            random_noise = random.uniform(-1, 1) * roughness * 3
            
            # 计算垂直方向
            if edge_start[0] == edge_end[0]:  # 垂直边
                x = base_x + noise + random_noise
                y = base_y
            else:  # 水平边
                x = base_x
                y = base_y + noise + random_noise
            
            # 确保坐标在图像范围内
            x = max(0, min(width - 1, x))
            y = max(0, min(height - 1, y))
            
            points.append((x, y))
    
    return points

def add_micro_fibers_to_mask(mask, fiber_intensity=0.3):
    """在边缘添加微观纤维效果"""
    width, height = mask.size
    mask_array = np.array(mask)
    
    # 找到边缘像素
    edge_pixels = []
    for i in range(1, height-1):
        for j in range(1, width-1):
            if mask_array[i, j] > 128:  # 内部点
                # 检查是否有外部邻居
                neighbors = [
                    mask_array[i-1, j], mask_array[i+1, j],
                    mask_array[i, j-1], mask_array[i, j+1]
                ]
                if any(n < 128 for n in neighbors):
                    edge_pixels.append((i, j))
    
    # 添加纤维
    for y, x in edge_pixels:
        if random.random() < fiber_intensity:
            # 纤维方向（主要向外）
            angle = random.uniform(0, 2 * math.pi)
            fiber_length = random.randint(1, 6)
            
            for step in range(fiber_length):
                fiber_y = int(y + step * math.sin(angle))
                fiber_x = int(x + step * math.cos(angle))
                
                # 确保坐标在范围内
                if 0 <= fiber_x < width and 0 <= fiber_y < height:
                    # 纤维逐渐变细
                    alpha = 255 - (step * 40)
                    if alpha > 0:
                        current_alpha = mask_array[fiber_y, fiber_x]
                        mask_array[fiber_y, fiber_x] = min(current_alpha, alpha)
    
    return Image.fromarray(mask_array)

def create_organic_torn_mask(width, height, roughness=0.5):
    """创建有机的撕边蒙版"""
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # 生成自然撕边点
    points = generate_natural_torn_edge(width, height, roughness)
    
    if points:
        # 绘制撕边形状
        draw.polygon(points, fill=255)
    
    # 添加微观纤维
    mask = add_micro_fibers_to_mask(mask, fiber_intensity=0.2)
    
    # 轻微模糊使边缘更自然
    mask = mask.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return mask

def create_authentic_paper_texture(width, height, paper_type="xuan"):
    """创建真实的纸张纹理"""
    if paper_type == "xuan":
        base_color = (251, 245, 235)
    else:
        base_color = (252, 243, 229)
    
    img = Image.new('RGB', (width, height), base_color)
    pixels = img.load()  # 使用load()方法提高性能
    
    # 添加细微的颜色变化
    for i in range(width):
        for j in range(height):
            r, g, b = base_color
            # 非常细微的颜色变化
            variation = random.randint(-2, 2)
            pixels[i, j] = (
                max(0, min(255, r + variation)),
                max(0, min(255, g + variation)),
                max(0, min(255, b + variation))
            )
    
    # 添加纤维纹理
    draw = ImageDraw.Draw(img)
    for _ in range(width * height // 500):  # 适量的纤维
        x1 = random.randint(0, width-1)
        y1 = random.randint(0, height-1)
        length = random.randint(15, 40)
        angle = random.uniform(0, math.pi)
        
        x2 = min(width-1, max(0, int(x1 + length * math.cos(angle))))
        y2 = min(height-1, max(0, int(y1 + length * math.sin(angle))))
        
        # 确保坐标有效
        if 0 <= x1 < width and 0 <= y1 < height and 0 <= x2 < width and 0 <= y2 < height:
            # 非常细微的颜色变化
            darken = random.uniform(0.97, 0.995)
            r, g, b = pixels[x1, y1]
            fiber_color = (
                int(r * darken),
                int(g * darken), 
                int(b * darken)
            )
            
            draw.line([(x1, y1), (x2, y2)], fill=fiber_color, width=1)
    
    return img

def add_realistic_aging(paper_img, intensity=0.2):
    """添加真实的老化效果"""
    width, height = paper_img.size
    aged_img = paper_img.copy()
    pixels = aged_img.load()  # 使用load()方法
    
    # 1. 细微的色斑
    for _ in range(int(25 * intensity)):
        center_x = random.randint(0, width-1)
        center_y = random.randint(0, height-1)
        radius = random.randint(2, 8)  # 小斑点
        
        for i in range(max(0, center_x-radius), min(width, center_x+radius)):
            for j in range(max(0, center_y-radius), min(height, center_y+radius)):
                # 确保坐标有效
                if 0 <= i < width and 0 <= j < height:
                    dist = math.sqrt((i-center_x)**2 + (j-center_y)**2)
                    if dist < radius:
                        r, g, b = pixels[i, j]
                        # 轻微变黄
                        fade = 1.0 - (dist / radius) * 0.1
                        pixels[i, j] = (
                            int(r * fade),
                            int(g * fade * 0.98),
                            int(b * fade * 0.95)
                        )
    
    return aged_img

def safe_apply_mask(paper_img, mask):
    """安全地应用蒙版"""
    paper_rgba = paper_img.convert('RGBA')
    
    # 确保蒙版尺寸匹配
    if mask.size != paper_rgba.size:
        mask = mask.resize(paper_rgba.size)
    
    # 应用蒙版
    paper_rgba.putalpha(mask)
    return paper_rgba

def create_authentic_torn_paper(paper_size="small_xuan", paper_type="xuan", tear_intensity=0.4):
    """创建真实的撕边纸张"""
    PAPER_SIZES = {
        "small_xuan": (400, 600),  # 减小尺寸便于测试
        "medium_xuan": (600, 800),
        "large_xuan": (1600, 800),
        "handscroll": (800, 200),
        "album_leaf": (400, 500),
    }
    
    width, height = PAPER_SIZES.get(paper_size, (400, 600))
    
    print(f"创建真实撕边纸张: {width} × {height}, 撕边强度: {tear_intensity}")
    
    try:
        # 1. 创建基础纹理
        paper = create_authentic_paper_texture(width, height, paper_type)
        
        # 2. 创建有机撕边蒙版
        mask = create_organic_torn_mask(width, height, tear_intensity)
        
        # 3. 安全应用蒙版
        final_paper = safe_apply_mask(paper, mask)
        
        # 4. 添加老化效果
        aged_paper = add_realistic_aging(paper, intensity=0.15)
        final_paper_aged = safe_apply_mask(aged_paper, mask)
        
        return final_paper_aged
        
    except Exception as e:
        print(f"创建纸张时出错: {e}")
        # 返回一个简单的备用图像
        return Image.new('RGBA', (width, height), (255, 255, 255, 255))

def create_simple_test():
    """创建简单的测试图像"""
    print("创建简单测试图像...")
    
    # 先创建一个非常简单的版本测试
    width, height = 400, 300
    
    # 创建基础纸张
    paper = Image.new('RGB', (width, height), (250, 245, 235))
    
    # 创建简单的撕边蒙版
    mask = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(mask)
    
    # 简单的矩形带圆角
    margin = 20
    points = [
        (margin, margin),
        (width - margin, margin), 
        (width - margin, height - margin),
        (margin, height - margin)
    ]
    draw.polygon(points, fill=255)
    
    # 应用蒙版
    paper.putalpha(mask)
    paper.save("simple_test.png")
    print("简单测试图像保存成功！")

def poem_to_flat_char_list(poem_text):
    """
    将诗歌转换为扁平的字列表
    返回: ["字1", "字2", "字3", ...]
    """
    # 提取所有汉字，去除标点和空白
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', poem_text)
    return chinese_chars

def flat_list_to_matrix(char_list, cols=5):
    """
    将扁平字列表转换为二维矩阵
    Args:
        char_list: 扁平的字列表
        cols: 每行的列数
    """
    matrix = []
    for i in range(0, len(char_list), cols):
        row = char_list[i:i + cols]
        matrix.append(row)
    return matrix

def create_real_vertical_poem(image, poem_text):
    """生成真正的竖排《彩书怨》"""
    
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    try:
        font = safe_get_font("方正行楷_GBK.ttf", 75)
        small_font = ImageFont.truetype("simkai.ttf", 30)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 《彩书怨》全文（每个字单独）
    poem_chars = poem_to_flat_char_list(poem_text)
    poem_matrix = flat_list_to_matrix(poem_chars, cols=5)
    
    print("转换完成的字列：")
    print(poem_chars)
    print("转换完成的字矩阵：")
    print(poem_matrix)

    # 竖排参数：从右向左，从上到下
    start_x = 1200  # 从右侧开始
    start_y = 200  # 从顶部开始
    char_spacing = 90  # 字间距（垂直）
    line_spacing = 90  # 行间距（水平）
    
    # 绘制竖排诗文（8列，每列5个字）
    for col in range(8):  # 8句诗
        for row in range(5):  # 每句5个字
            char_index = col * 5 + row
            if char_index < len(poem_chars):
                char = poem_chars[char_index]
                char_x = start_x - col * line_spacing
                char_y = start_y + row * char_spacing
                draw.text((char_x, char_y), char, font=font, fill=(0, 0, 0))
    
    # 添加标题"彩书怨"（竖排在右侧）
    title_chars = ["彩", "书", "怨"]
    title_x = start_x + 80  # 诗句右侧
    for i, char in enumerate(title_chars):
        draw.text((title_x, start_y + i * char_spacing), char, font=font, fill=(0, 0, 0))
    
    # 添加作者"上官婉儿"（竖排在标题右侧）
    author_chars = ["上", "官", "婉", "儿"]
    author_x = title_x + 90
    author_y = 600
    for i, char in enumerate(author_chars):
        draw.text((author_x, start_y + i * char_spacing), char, font=small_font, fill=(0, 0, 0))
    
    # 添加印章（在作者旁边）
    # 使用修正后的印章函数
    seal_x = author_x - 120
    seal_y = author_y - 15

    # 创建透明图层用于绘制印章
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    
    seal_layer = add_four_character_seal(seal_layer, "玻璃耗子", (seal_x, seal_y), 100)
    
    result = Image.alpha_composite(image, seal_layer)

    result.save("真正竖排格式_透明图层.png", quality=95)
    print("生成完成：真正竖排格式.png")
    print("布局：传统竖排，从右向左，从上到下")
    
    return image
    

# 主要执行函数
def main():
    print("开始创建真实撕边纸张...")
    
    # 先创建简单测试确保基础功能正常
    create_simple_test()
    
    try:
        # 测试不同撕边强度
        intensities = [0.35]    #, 0.40, 0.45]
        
        for intensity in intensities:
            print(f"创建撕边强度 {intensity}...")
            
            # 创建宣纸
            paper = create_authentic_torn_paper("large_xuan", "xuan", intensity)
            
            if paper.mode != 'RGBA':
                paper = paper.convert('RGBA')
                
            poem_example = """
                            叶下洞庭初，思君万里余。
                            露浓香被冷，月落锦屏虚。
                            欲奏江南曲，贪封蓟北书。
                            书中无别意，惟怅久离居。
                            """
            paper = create_real_vertical_poem(paper, poem_example)
            if paper:
                paper.save(f"torn_paper_{intensity}.png")
                print(f"撕边强度 {intensity} 创建成功")
            else:
                print(f"撕边强度 {intensity} 创建失败")
                
    except Exception as e:
        print(f"主程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    print("程序执行完成！")