from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math
import re
import numpy as np

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

def add_organic_torn_mask(width, height, roughness=0.5):
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

def safe_apply_mask(paper_img, mask):
    """安全地应用蒙版"""
    paper_rgba = paper_img.convert('RGBA')
    
    # 确保蒙版尺寸匹配
    if mask.size != paper_rgba.size:
        mask = mask.resize(paper_rgba.size)
    
    # 应用蒙版
    paper_rgba.putalpha(mask)
    return paper_rgba
