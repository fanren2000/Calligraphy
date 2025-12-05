
import cv2
import numpy as np

import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_scroll_middle_by_color(image_path):
    """
    通过颜色分析找到卷轴中间区域
    """
    # 读取图像
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 方法1: 基于亮度（卷轴中间通常较亮）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 沿水平方向分析亮度变化
    height, width = gray.shape
    column_means = np.mean(gray, axis=0)
    
    # 平滑处理
    column_means_smooth = cv2.GaussianBlur(column_means.astype(np.float32), (15, 15), 5)
    
    # 找到最亮的区域
    max_brightness = np.max(column_means_smooth)
    threshold = max_brightness * 0.8
    
    # 找到超过阈值的区域
    bright_regions = column_means_smooth > threshold
    
    # 找到连续的最亮区域
    bright_indices = np.where(bright_regions)[0]
    if len(bright_indices) > 0:
        left_boundary = bright_indices[0]
        right_boundary = bright_indices[-1]
    else:
        # 如果没有明显亮区，使用中间区域
        left_boundary = int(width * 0.4)
        right_boundary = int(width * 0.6)
    
    return left_boundary, right_boundary, column_means_smooth

def find_scroll_middle_by_edges(image_path):
    """
    通过边缘检测找到卷轴边界
    """
    # 读取图像
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 预处理：降噪
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 边缘检测
    edges = cv2.Canny(gray, 180, 200)
    
    # 形态学操作增强边缘
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # 找到轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # 找到最大的轮廓（假设是卷轴）
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 获取轮廓的边界框
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # 计算中间区域（假设卷轴中间在轮廓内）
        # 可以基于轮廓形状进一步优化
        middle_width = w * 0.6  # 中间占60%
        left_boundary = x + int((w - middle_width) / 2)
        right_boundary = left_boundary + int(middle_width)
        
        return left_boundary, right_boundary, edges
    else:
        return int(gray.shape[1] * 0.4), int(gray.shape[1] * 0.6), edges
    
def find_scroll_middle_by_hough_lines(image_path):
    """
    使用Hough变换检测卷轴的直线边界
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 边缘检测
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # 使用Hough变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100,
                            minLineLength=gray.shape[0]*0.3, maxLineGap=10)
    
    vertical_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # 筛选接近垂直的线（角度在80-100度之间）
            if abs(x2 - x1) < 10:  # 垂直度检查
                vertical_lines.append((x1, x2))
    
    if vertical_lines:
        # 找到最左侧和最右侧的垂直线
        vertical_lines = np.array(vertical_lines)
        left_boundaries = vertical_lines.min(axis=0)
        right_boundaries = vertical_lines.max(axis=0)
        
        left_boundary = np.min(left_boundaries)
        right_boundary = np.max(right_boundaries)
    else:
        # 如果没有检测到垂直线，使用默认值
        left_boundary = int(gray.shape[1] * 0.3)
        right_boundary = int(gray.shape[1] * 0.7)
    
    return left_boundary, right_boundary, edges

def find_scroll_middle_by_texture(image_path):
    """
    通过纹理分析区分卷轴纸张和装裱部分
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    height, width = gray.shape
    
    # 将图像分成若干列进行分析
    num_sections = 20
    section_width = width // num_sections
    
    texture_scores = []
    
    for i in range(num_sections):
        start_x = i * section_width
        end_x = min((i + 1) * section_width, width)
        
        section = gray[:, start_x:end_x]
        
        # 计算纹理特征（使用局部二值模式LBP的简化版本）
        # 1. 计算梯度幅度
        sobelx = cv2.Sobel(section, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(section, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        # 2. 纹理评分（纸张区域通常纹理更复杂）
        texture_score = np.mean(gradient_magnitude)
        texture_scores.append(texture_score)
    
    # 平滑纹理评分
    texture_scores = np.array(texture_scores)
    texture_scores_smooth = cv2.GaussianBlur(texture_scores.astype(np.float32), (3, 3), 1)
    
    # 找到纹理最复杂的区域（假设是纸张区域）
    max_texture = np.max(texture_scores_smooth)
    threshold = max_texture * 0.7
    
    # 找到高纹理区域
    high_texture_indices = np.where(texture_scores_smooth > threshold)[0]
    
    if len(high_texture_indices) > 0:
        left_section = high_texture_indices[0]
        right_section = high_texture_indices[-1]
        
        left_boundary = left_section * section_width
        right_boundary = right_section * section_width + section_width
    else:
        left_boundary = int(width * 0.4)
        right_boundary = int(width * 0.6)
    
    return left_boundary, right_boundary, texture_scores_smooth    

def smart_find_scroll_middle(image_path, output_path=None, visualize=False):
    """
    智能检测卷轴中间区域并使其透明
    """
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print("无法读取图像")
        return None
    
    height, width = img.shape[:2]
    
    # 尝试多种方法
    methods = [
        # find_scroll_middle_by_color,
        find_scroll_middle_by_edges,
        # find_scroll_middle_by_hough_lines,
        # find_scroll_middle_by_texture
    ]
    
    boundaries = []
    for method in methods:
        try:
            left, right, _ = method(image_path)
            boundaries.append((left, right))
        except:
            continue
    
    # 选择最合理的边界（取中间值）
    if boundaries:
        left_boundaries = [b[0] for b in boundaries]
        right_boundaries = [b[1] for b in boundaries]
        
        # 去除异常值
        left_boundaries = sorted(left_boundaries)
        right_boundaries = sorted(right_boundaries)
        
        left_boundary = left_boundaries[len(left_boundaries)//2]  # 中位数
        right_boundary = right_boundaries[len(right_boundaries)//2]
        
        # 确保边界合理
        min_width = width * 0.1
        if (right_boundary - left_boundary) < min_width:
            # 如果检测区域太小，扩展它
            center = (left_boundary + right_boundary) // 2
            left_boundary = max(0, center - int(min_width/2))
            right_boundary = min(width, center + int(min_width/2))
    else:
        # 默认值
        left_boundary = int(width * 0.4)
        right_boundary = int(width * 0.6)
    
    # 转换为RGBA
    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    
    # 创建渐变透明效果
    transparent_width = right_boundary - left_boundary
    gradient_width = min(100, transparent_width // 3)
    
    # 设置透明度
    for x in range(left_boundary, right_boundary):
        if x < left_boundary + gradient_width:
            # 左侧渐变
            alpha_value = int(255 * (x - left_boundary) / gradient_width)
        elif x > right_boundary - gradient_width:
            # 右侧渐变
            alpha_value = int(255 * (right_boundary - x) / gradient_width)
        else:
            # 中间完全透明
            alpha_value = 0
        
        img_rgba[:, x, 3] = alpha_value
    
    # 可视化（可选）
    if visualize:
        # 创建可视化图像
        viz_img = img.copy()
        cv2.line(viz_img, (left_boundary, 0), (left_boundary, height), (0, 255, 0), 3)
        cv2.line(viz_img, (right_boundary, 0), (right_boundary, height), (0, 255, 0), 3)
        
        # 显示结果
        plt.figure(figsize=(15, 5))
        plt.subplot(131)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title('原始图像')
        
        plt.subplot(132)
        plt.imshow(cv2.cvtColor(viz_img, cv2.COLOR_BGR2RGB))
        plt.title('检测到的边界')
        
        plt.subplot(133)
        plt.imshow(cv2.cvtColor(img_rgba, cv2.COLOR_BGRA2RGBA))
        plt.title('透明化结果')
        
        plt.tight_layout()
        plt.show()
    
    # 保存结果
    if output_path:
        cv2.imwrite(output_path, img_rgba)
        print(f"结果已保存至: {output_path}")
        print(f"检测到的边界: {left_boundary} - {right_boundary} (宽度: {transparent_width}px)")
    
    return left_boundary, right_boundary, img_rgba

# 使用示例
if __name__ == "__main__":
    scroll_image = "Source/scroll_horizontal_brown_basic.png"
    # 简单使用
    left, right, result = smart_find_scroll_middle(
        scroll_image, 
        "output_smart.png",
        visualize=True
    )
    
    print(f"卷轴中间区域边界: 左={left}, 右={right}")