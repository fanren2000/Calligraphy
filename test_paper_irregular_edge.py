import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import random
import math

def create_paper_texture(width, height, paper_type="xuan"):
    """创建基础纸张纹理"""
    # 创建基础画布
    if paper_type == "xuan":
        # 宣纸：偏黄白色，轻微纹理
        base_color = (245, 240, 230)
    else:  # parchment
        # 羊皮纸：更黄的色调
        base_color = (250, 235, 215)
    
    img = Image.new('RGB', (width, height), base_color)
    pixels = img.load()
    
    # 添加细微的纤维纹理
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            # 添加随机纹理变化
            variation = random.randint(-3, 3)
            pixels[i, j] = (
                max(0, min(255, r + variation)),
                max(0, min(255, g + variation)),
                max(0, min(255, b + variation))
            )
    
    return img

def generate_organic_edge(width, height, roughness=0.5):
    """生成有机不规则边缘"""
    # 创建边缘控制点
    num_points = 50
    points = []
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        # 基础圆形
        base_radius = min(width, height) * 0.45
        
        # 添加不规则性
        irregularity = random.uniform(0.7, 1.3) * roughness
        radius = base_radius * irregularity
        
        x = width // 2 + radius * math.cos(angle)
        y = height // 2 + radius * math.sin(angle)
        points.append((x, y))
    
    return points

def create_irregular_mask(width, height, roughness=0.5):
    """创建不规则形状蒙版"""
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    points = generate_organic_edge(width, height, roughness)
    
    # 绘制多边形
    draw.polygon(points, fill=255)
    
    # 添加更细的不规则性
    mask_array = np.array(mask)
    
    # 使用距离变换创建更自然的边缘
    from scipy import ndimage
    
    # 添加随机侵蚀和膨胀
    for _ in range(3):
        if random.random() > 0.5:
            # 随机侵蚀
            structure = np.ones((3, 3))
            mask_array = ndimage.binary_erosion(mask_array, structure=structure).astype(mask_array.dtype) * 255
        else:
            # 随机膨胀
            structure = np.ones((2, 2))
            mask_array = ndimage.binary_dilation(mask_array, structure=structure).astype(mask_array.dtype) * 255
    
    return Image.fromarray(mask_array)

def add_fiber_edges(mask, fiber_density=0.3):
    """添加纤维状边缘效果"""
    width, height = mask.size
    mask_array = np.array(mask)
    
    # 找到边缘像素
    edges = np.zeros((height, width), dtype=bool)
    for i in range(1, height-1):
        for j in range(1, width-1):
            if mask_array[i, j] > 128:  # 内部点
                # 检查是否是边缘
                if (mask_array[i-1, j] < 128 or mask_array[i+1, j] < 128 or 
                    mask_array[i, j-1] < 128 or mask_array[i, j+1] < 128):
                    edges[i, j] = True
    
    # 在边缘添加纤维
    for i in range(height):
        for j in range(width):
            if edges[i, j] and random.random() < fiber_density:
                # 创建纤维延伸
                fiber_length = random.randint(1, 5)
                direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                
                for k in range(fiber_length):
                    ni, nj = i + direction[0] * k, j + direction[1] * k
                    if 0 <= ni < height and 0 <= nj < width:
                        # 逐渐减弱纤维
                        fiber_strength = 255 - k * 50
                        if fiber_strength > 0:
                            mask_array[ni, nj] = max(mask_array[ni, nj], fiber_strength)
    
    return Image.fromarray(mask_array)

def add_aging_effects(paper_img, intensity=0.3):
    """添加老化效果：水渍、色斑等"""
    width, height = paper_img.size
    aged_img = paper_img.copy()
    pixels = aged_img.load()
    
    # 添加随机水渍
    for _ in range(int(50 * intensity)):
        # 随机水渍位置和大小
        center_x = random.randint(0, width)
        center_y = random.randint(0, height)
        radius = random.randint(10, 50)
        
        for i in range(max(0, center_x - radius), min(width, center_x + radius)):
            for j in range(max(0, center_y - radius), min(height, center_y + radius)):
                dist = math.sqrt((i - center_x)**2 + (j - center_y)**2)
                if dist < radius:
                    # 水渍效果：颜色变深
                    r, g, b = pixels[i, j]
                    fade = 1 - (dist / radius) * 0.3  # 中心更明显
                    pixels[i, j] = (
                        int(r * fade),
                        int(g * fade),
                        int(b * fade)
                    )
    
    # 添加随机色斑
    for _ in range(int(20 * intensity)):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        spot_size = random.randint(2, 8)
        
        for i in range(max(0, x-spot_size), min(width, x+spot_size)):
            for j in range(max(0, y-spot_size), min(height, y+spot_size)):
                if random.random() < 0.7:
                    r, g, b = pixels[i, j]
                    # 黄色或棕色斑点
                    pixels[i, j] = (
                        min(255, int(r * 1.1)),
                        min(255, int(g * 0.9)),
                        min(255, int(b * 0.8))
                    )
    
    return aged_img

def create_realistic_paper(width, height, paper_type="xuan", roughness=0.5):
    """创建逼真的纸张效果"""
    # 1. 创建基础纹理
    paper = create_paper_texture(width, height, paper_type)
    
    # 2. 创建不规则边缘蒙版
    mask = create_irregular_mask(width, height, roughness)
    
    # 3. 添加纤维边缘
    mask = add_fiber_edges(mask)
    
    # 4. 应用蒙版
    paper.putalpha(mask)
    
    # 5. 添加老化效果
    paper_rgb = paper.convert('RGB')
    aged_paper = add_aging_effects(paper_rgb)
    
    # 重新添加alpha通道
    final_paper = aged_paper.copy()
    final_paper.putalpha(mask)
    
    return final_paper

def create_torn_edge_effect(width, height, tear_intensity=0.7):
    """创建撕边效果"""
    # 创建渐变蒙版
    mask = Image.new('L', (width, height), 255)
    
    # 在边缘创建撕边效果
    edge_width = int(min(width, height) * 0.1)
    
    for i in range(width):
        for j in range(height):
            # 计算到最近边缘的距离
            dist_to_edge = min(i, j, width-i, height-j)
            
            if dist_to_edge < edge_width:
                # 在边缘区域创建不规则透明度
                progress = dist_to_edge / edge_width
                # 添加随机性模拟撕边
                randomness = random.uniform(0.8, 1.2) * tear_intensity
                alpha = int(255 * progress * randomness)
                mask.putpixel((i, j), max(0, min(255, alpha)))
    
    return mask


    """创建撕边效果"""
    # 创建渐变蒙版
    mask = Image.new('L', (width, height), 255)
    
    # 在边缘创建撕边效果
    edge_width = int(min(width, height) * 0.1)
    
    for i in range(width):
        for j in range(height):
            # 计算到最近边缘的距离
            dist_to_edge = min(i, j, width-i, height-j)
            
            if dist_to_edge < edge_width:
                # 在边缘区域创建不规则透明度
                progress = dist_to_edge / edge_width
                # 添加随机性模拟撕边
                randomness = random.uniform(0.8, 1.2) * tear_intensity
                alpha = int(255 * progress * randomness)
                mask.putpixel((i, j), max(0, min(255, alpha)))
    
    return mask

def create_premium_paper(width, height, paper_type="xuan"):
    """创建高级纸张效果，结合多种技术"""
    # 基础纸张
    paper = create_realistic_paper(width, height, paper_type)
    
    # 撕边效果
    tear_mask = create_torn_edge_effect(width, height)
    
    # 组合蒙版
    existing_alpha = paper.getchannel('A')
    combined_alpha = ImageChops.multiply(existing_alpha, tear_mask)
    paper.putalpha(combined_alpha)
    
    # 添加轻微阴影效果
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    
    # 在纸张下方绘制阴影
    points = generate_organic_edge(width, height, 0.3)
    draw.polygon(points, fill=(0, 0, 0, 30))
    
    # 模糊阴影
    shadow = shadow.filter(ImageFilter.GaussianBlur(5))
    
    # 合并阴影
    final_result = Image.alpha_composite(shadow, paper)
    
    return final_result

# 使用示例
if __name__ == "__main__":
    # 创建宣纸
    xuan_paper = create_premium_paper(800, 600, "xuan")
    xuan_paper.save("realistic_xuan_paper.png")
    
    # 创建羊皮纸
    parchment = create_premium_paper(800, 600, "parchment")
    parchment.save("realistic_parchment.png")