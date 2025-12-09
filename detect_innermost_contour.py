

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import ndimage
from sklearn.cluster import KMeans
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

def find_inner_region_and_make_transparent(scroll_template_path, output_template_path, debug=False):
    """
    找到卷轴模板的内部空白区域并使其透明
    
    参数:
    - scroll_template_path: 空白卷轴模板图像路径
    - output_template_path: 输出的透明模板路径
    - debug: 是否显示调试信息
    """
    print("=" * 60)
    print("步骤1: 处理卷轴模板")
    print("=" * 60)
    
    # 1. 读取卷轴模板
    scroll_img = cv2.imread(scroll_template_path)
    if scroll_img is None:
        print("❌ 无法读取卷轴模板")
        return None
    
    height, width = scroll_img.shape[:2]
    print(f"📏 模板尺寸: {width}x{height}")
    
    # 2. 转换为灰度图
    gray = cv2.cvtColor(scroll_img, cv2.COLOR_BGR2GRAY)
    
    # 3. 找到内部空白区域（基于亮度）
    print("🔍 寻找内部空白区域...")
    
    # 方法A: 使用自适应阈值找到空白区域
    # 空白区域通常比周围亮
    thresh = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 15, 5)
    
    # 反转，使空白区域为白色
    thresh_inv = cv2.bitwise_not(thresh)
    
    # 形态学操作填充小孔洞
    kernel = np.ones((3, 3), np.uint8)
    filled = cv2.morphologyEx(thresh_inv, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # 4. 找到轮廓
    contours, hierarchy = cv2.findContours(filled, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if hierarchy is None:
        print("⚠️  未找到层级信息，尝试其他方法...")
        # 使用简单方法：找最大的矩形区域
        inner_region = find_inner_region_simple(scroll_img)
    else:
        # 5. 找到最内部的轮廓
        inner_region = find_innermost_contour(contours, hierarchy, width, height)
    
    if inner_region is None:
        print("❌ 无法找到内部区域")
        return None
    
    # 6. 创建透明模板
    print("🎨 创建透明模板...")
    
    # 转换为RGBA
    scroll_rgba = cv2.cvtColor(scroll_img, cv2.COLOR_BGR2RGBA)
    
    # 创建遮罩：内部区域透明，外部不透明
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # 填充内部区域为白色（将变成透明）
    if len(inner_region.shape) == 3:  # 轮廓点
        cv2.drawContours(mask, [inner_region], -1, 255, -1)
    else:  # 矩形坐标
        x, y, w, h = inner_region
        cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)
    
    # 应用遮罩：遮罩区域透明（alpha=0），其他区域不透明（alpha=255）
    for y in range(height):
        for x in range(width):
            if mask[y, x] > 0:
                scroll_rgba[y, x, 3] = 0  # 完全透明
    
    # 7. 保存透明模板
    cv2.imwrite(output_template_path, scroll_rgba)
    print(f"💾 透明模板已保存: {output_template_path}")
    
    # 8. 调试显示
    if debug:
        show_debug_info(scroll_img, gray, thresh_inv, mask, scroll_rgba)
    
    return scroll_rgba, mask

def find_innermost_contour(contours, hierarchy, image_width, image_height):
    """
    从轮廓层级中找到最内部的轮廓
    """
    # hierarchy结构: [Next, Previous, First_Child, Parent]
    innermost_contours = []
    
    for i, contour in enumerate(contours):
        # 检查是否是最内部轮廓（没有子轮廓）
        if hierarchy[0][i][2] == -1:  # 没有子轮廓
            area = cv2.contourArea(contour)
            
            # 过滤太小或太大的区域
            min_area = image_width * image_height * 0.1  # 最小10%的面积
            max_area = image_width * image_height * 0.8  # 最大80%的面积
            
            if min_area < area < max_area:
                # 计算轮廓的紧凑度
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    compactness = 4 * np.pi * area / (perimeter * perimeter)
                    
                    # 矩形度
                    x, y, w, h = cv2.boundingRect(contour)
                    rect_area = w * h
                    rectangularity = area / rect_area if rect_area > 0 else 0
                    
                    # 选择紧凑且接近矩形的轮廓（可能是文字区域）
                    if compactness > 0.3 and rectangularity > 0.6:
                        innermost_contours.append({
                            'contour': contour,
                            'area': area,
                            'compactness': compactness,
                            'rectangularity': rectangularity
                        })
    
    if innermost_contours:
        # 选择面积最大的内部轮廓
        innermost_contours.sort(key=lambda x: x['area'], reverse=True)
        print(f"✅ 找到 {len(innermost_contours)} 个内部区域")
        print(f"   最大区域面积: {innermost_contours[0]['area']:.0f} pixels")
        return innermost_contours[0]['contour']
    
    return None

def find_inner_region_simple(scroll_img):
    """
    简单方法：寻找最大的连续亮色区域
    """
    gray = cv2.cvtColor(scroll_img, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    
    # 使用Otsu阈值
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 反转，使亮色区域为白色
    thresh_inv = cv2.bitwise_not(thresh)
    
    # 寻找轮廓
    contours, _ = cv2.findContours(thresh_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # 找到最大的轮廓
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 获取边界框
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        print(f"📐 简单方法找到的区域: ({x}, {y}, {w}, {h})")
        
        # 稍微缩小边界框，确保在卷轴内部
        padding = 10
        x += padding
        y += padding
        w = max(0, w - 2*padding)
        h = max(0, h - 2*padding)
        
        return (x, y, w, h)
    
    return None

def show_debug_info(original, gray, threshold, mask, result):
    """
    显示调试信息
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 原始图像
    axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('原始卷轴模板')
    axes[0, 0].axis('off')
    
    # 灰度图像
    axes[0, 1].imshow(gray, cmap='gray')
    axes[0, 1].set_title('灰度图像')
    axes[0, 1].axis('off')
    
    # 阈值图像
    axes[0, 2].imshow(threshold, cmap='gray')
    axes[0, 2].set_title('阈值分割')
    axes[0, 2].axis('off')
    
    # 检测到的区域
    contour_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    if mask is not None:
        # 找到mask的轮廓
        mask_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if mask_contours:
            cv2.drawContours(contour_img, mask_contours, -1, (0, 255, 0), 3)
    
    axes[1, 0].imshow(contour_img)
    axes[1, 0].set_title('检测到的内部区域')
    axes[1, 0].axis('off')
    
    # Alpha遮罩
    axes[1, 1].imshow(mask, cmap='gray')
    axes[1, 1].set_title('透明区域遮罩\n(白色=透明区域)')
    axes[1, 1].axis('off')
    
    # 最终结果
    axes[1, 2].imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    axes[1, 2].set_title('透明模板结果')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.show()

def insert_calligraphy_into_scroll(scroll_template_path, calligraphy_path, output_path, debug=False):
    """
    将书法作品嵌入到卷轴模板中
    
    参数:
    - scroll_template_path: 透明卷轴模板路径
    - calligraphy_path: 书法作品图像路径
    - output_path: 输出合成图像路径
    """
    print("\n" + "=" * 60)
    print("步骤2: 合成书法作品")
    print("=" * 60)
    
    # 1. 读取透明卷轴模板
    scroll = cv2.imread(scroll_template_path, cv2.IMREAD_UNCHANGED)  # 保持alpha通道
    if scroll is None:
        print("❌ 无法读取透明卷轴模板")
        return None
    
    # 2. 读取书法作品
    calligraphy = cv2.imread(calligraphy_path)
    if calligraphy is None:
        print("❌ 无法读取书法作品")
        return None
    
    print(f"📏 卷轴尺寸: {scroll.shape[1]}x{scroll.shape[0]}")
    print(f"📏 书法尺寸: {calligraphy.shape[1]}x{calligraphy.shape[0]}")
    
    # 3. 找到透明区域的位置和大小
    if scroll.shape[2] == 4:  # 有alpha通道
        alpha_channel = scroll[:, :, 3]
        
        # 找到透明区域的边界
        transparent_pixels = np.where(alpha_channel == 0)
        
        if len(transparent_pixels[0]) == 0:
            print("⚠️  没有找到透明区域")
            return None
        
        y_indices = transparent_pixels[0]
        x_indices = transparent_pixels[1]
        
        # 计算透明区域的边界框
        x_min, x_max = np.min(x_indices), np.max(x_indices)
        y_min, y_max = np.min(y_indices), np.max(y_indices)
        
        region_width = x_max - x_min
        region_height = y_max - y_min
        
        print(f"📐 透明区域: 位置({x_min}, {y_min}), 大小{region_width}x{region_height}")
    else:
        print("❌ 卷轴模板没有透明通道")
        return None
    
    # 4. 调整书法作品大小以适应透明区域
    calligraphy_resized = cv2.resize(calligraphy, (region_width, region_height))
    
    # 5. 创建合成图像
    # 先创建一个卷轴的副本
    composite = scroll.copy()
    
    # 将书法作品放入透明区域
    # 注意：这里假设书法作品是BGR格式
    if calligraphy_resized.shape[2] == 3:  # BGR
        # 将书法作品放入透明区域
        composite[y_min:y_min+region_height, x_min:x_max, :3] = calligraphy_resized
        
        # 设置该区域为不透明
        composite[y_min:y_min+region_height, x_min:x_max, 3] = 255
    elif calligraphy_resized.shape[2] == 4:  # BGRA
        # 如果有alpha通道，需要混合
        for y in range(region_height):
            for x in range(region_width):
                calligraphy_pixel = calligraphy_resized[y, x]
                scroll_pixel = composite[y_min+y, x_min+x]
                
                # 如果书法像素是透明的，使用卷轴像素
                if calligraphy_pixel[3] == 0:
                    continue
                
                # 否则使用书法像素
                composite[y_min+y, x_min+x] = calligraphy_pixel
    
    # 6. 保存合成结果
    cv2.imwrite(output_path, composite)
    print(f"✅ 合成作品已保存: {output_path}")
    
    # 7. 调试显示
    if debug:
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # 透明卷轴模板
        axes[0, 0].imshow(cv2.cvtColor(composite[:, :, :3], cv2.COLOR_BGR2RGB))
        axes[0, 0].set_title('卷轴模板（合成前）')
        axes[0, 0].axis('off')
        
        # 书法作品
        axes[0, 1].imshow(cv2.cvtColor(calligraphy, cv2.COLOR_BGR2RGB))
        axes[0, 1].set_title('原始书法作品')
        axes[0, 1].axis('off')
        
        # 调整大小的书法作品
        axes[0, 2].imshow(cv2.cvtColor(calligraphy_resized, cv2.COLOR_BGR2RGB))
        axes[0, 2].set_title(f'调整大小: {region_width}x{region_height}')
        axes[0, 2].axis('off')
        
        # Alpha通道
        axes[1, 0].imshow(alpha_channel, cmap='gray')
        axes[1, 0].set_title('透明区域Alpha通道')
        axes[1, 0].axis('off')
        
        # 透明区域边界
        boundary_img = cv2.cvtColor(scroll[:, :, :3], cv2.COLOR_BGR2RGB)
        cv2.rectangle(boundary_img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)
        axes[1, 1].imshow(boundary_img)
        axes[1, 1].set_title('透明区域边界')
        axes[1, 1].axis('off')
        
        # 最终合成结果
        axes[1, 2].imshow(cv2.cvtColor(composite[:, :, :3], cv2.COLOR_BGR2RGB))
        axes[1, 2].set_title('最终合成作品')
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    return composite

def complete_workflow(scroll_template_path, calligraphy_path, 
                      output_template_path, output_final_path,
                      debug=True):
    """
    完整的工作流程：创建透明模板并合成书法作品
    """
    print("🚀 开始完整工作流程")
    print("=" * 60)
    
    # 步骤1: 创建透明卷轴模板
    transparent_template, mask = find_inner_region_and_make_transparent(
        scroll_template_path,
        output_template_path,
        debug=debug
    )
    
    if transparent_template is None:
        print("❌ 无法创建透明模板")
        return None
    
    print("\n✅ 步骤1完成：透明模板已创建")
    
    # 步骤2: 合成书法作品
    final_result = insert_calligraphy_into_scroll(
        output_template_path,
        calligraphy_path,
        output_final_path,
        debug=debug
    )
    
    if final_result is None:
        print("❌ 无法合成书法作品")
        return None
    
    print("\n✅ 步骤2完成：书法作品已合成")
    print("=" * 60)
    print("🎉 全部完成！")
    print(f"📁 透明模板: {output_template_path}")
    print(f"📁 最终作品: {output_final_path}")
    
    return final_result

# 简单版函数（如果上面的太复杂）
def simple_scroll_insertion(scroll_path, calligraphy_path, output_path):
    """
    简单版本：手动指定透明区域
    """
    # 1. 读取卷轴
    scroll = cv2.imread(scroll_path)
    h, w = scroll.shape[:2]
    
    # 2. 手动指定透明区域（根据你的卷轴调整这些值）
    # 这些是百分比，需要根据你的卷轴调整
    left_percent = 35
    right_percent = 65
    top_percent = 25
    bottom_percent = 75
    
    # 转换为像素
    left = int(w * left_percent / 100)
    right = int(w * right_percent / 100)
    top = int(h * top_percent / 100)
    bottom = int(h * bottom_percent / 100)
    
    print(f"透明区域: 左{left_percent}% 右{right_percent}% 上{top_percent}% 下{bottom_percent}%")
    print(f"像素区域: ({left}, {top}) 到 ({right}, {bottom})")
    
    # 3. 创建透明模板
    scroll_rgba = cv2.cvtColor(scroll, cv2.COLOR_BGR2RGBA)
    scroll_rgba[top:bottom, left:right, 3] = 0  # 设置为透明
    
    # 4. 读取并调整书法作品
    calligraphy = cv2.imread(calligraphy_path)
    calligraphy_resized = cv2.resize(calligraphy, (right-left, bottom-top))
    
    # 5. 合成
    scroll_rgba[top:bottom, left:right, :3] = calligraphy_resized
    scroll_rgba[top:bottom, left:right, 3] = 255  # 设置为不透明
    
    # 6. 保存
    cv2.imwrite(output_path, scroll_rgba)
    print(f"已保存: {output_path}")
    
    return scroll_rgba

# ==============================================


def insert_calligraphy_with_proportion(scroll_template_path, calligraphy_path, output_path, 
                                      padding=20, bg_color=(255, 255, 255), debug=False):
    """
    将书法作品嵌入到卷轴模板中，保持书法原始比例
    
    参数:
    - scroll_template_path: 透明卷轴模板路径
    - calligraphy_path: 书法作品图像路径
    - output_path: 输出合成图像路径
    - padding: 书法作品与透明区域边缘的间距（像素）
    - bg_color: 书法作品背景颜色（如果需要填充）
    """
    print("\n" + "=" * 60)
    print("步骤2: 合成书法作品（保持比例）")
    print("=" * 60)
    
    # 1. 读取透明卷轴模板
    scroll = cv2.imread(scroll_template_path, cv2.IMREAD_UNCHANGED)  # 保持alpha通道
    if scroll is None:
        print("❌ 无法读取透明卷轴模板")
        return None
    
    # 2. 读取书法作品
    calligraphy = cv2.imread(calligraphy_path)
    if calligraphy is None:
        print("❌ 无法读取书法作品")
        return None
    
    scroll_height, scroll_width = scroll.shape[:2]
    calligraphy_height, calligraphy_width = calligraphy.shape[:2]
    
    print(f"📏 卷轴尺寸: {scroll_width}x{scroll_height}")
    print(f"📏 书法尺寸: {calligraphy_width}x{calligraphy_height}")
    print(f"📐 书法宽高比: {calligraphy_width/calligraphy_height:.3f}")
    
    # 3. 找到透明区域的位置和大小
    if scroll.shape[2] == 4:  # 有alpha通道
        alpha_channel = scroll[:, :, 3]
        
        # 找到透明区域的边界
        transparent_pixels = np.where(alpha_channel == 0)
        
        if len(transparent_pixels[0]) == 0:
            print("⚠️  没有找到透明区域")
            return None
        
        y_indices = transparent_pixels[0]
        x_indices = transparent_pixels[1]
        
        # 计算透明区域的边界框
        x_min, x_max = np.min(x_indices), np.max(x_indices)
        y_min, y_max = np.min(y_indices), np.max(y_indices)
        
        region_width = x_max - x_min
        region_height = y_max - y_min
        
        print(f"📐 透明区域: 位置({x_min}, {y_min}), 大小{region_width}x{region_height}")
        print(f"📐 透明区域宽高比: {region_width/region_height:.3f}")
    else:
        print("❌ 卷轴模板没有透明通道")
        return None
    
    # 4. 计算书法作品的最佳适配尺寸（保持比例）
    print("\n📏 计算适配尺寸...")
    
    # 考虑padding
    available_width = region_width - 2 * padding
    available_height = region_height - 2 * padding
    
    if available_width <= 0 or available_height <= 0:
        print("⚠️  透明区域太小，减少padding值")
        padding = min(region_width, region_height) // 10
        available_width = region_width - 2 * padding
        available_height = region_height - 2 * padding
    
    # 计算缩放比例（保持原始比例）
    width_ratio = available_width / calligraphy_width
    height_ratio = available_height / calligraphy_height
    
    # 选择较小的缩放比例，确保书法完全在区域内
    scale_ratio = min(width_ratio, height_ratio)
    
    # 计算新的尺寸
    new_width = int(calligraphy_width * scale_ratio)
    new_height = int(calligraphy_height * scale_ratio)
    
    print(f"📐 可用空间: {available_width}x{available_height}")
    print(f"📐 缩放比例: {scale_ratio:.3f}")
    print(f"📐 新书法尺寸: {new_width}x{new_height} (保持比例)")
    print(f"📐 新书法宽高比: {new_width/new_height:.3f} (与原图相同)")
    
    # 5. 调整书法作品大小（保持比例）
    if scale_ratio != 1.0:
        print(f"🔄 缩放书法作品: {scale_ratio:.2f}x")
        calligraphy_resized = cv2.resize(calligraphy, (new_width, new_height), 
                                        interpolation=cv2.INTER_AREA)
    else:
        print("✅ 书法作品无需缩放")
        calligraphy_resized = calligraphy.copy()
    
    # 6. 创建带背景的书法图像（可选）
    # 计算居中位置
    x_offset = padding + (available_width - new_width) // 2
    y_offset = padding + (available_height - new_height) // 2
    
    # 创建与透明区域相同大小的背景
    calligraphy_with_bg = np.ones((region_height, region_width, 3), dtype=np.uint8) * 255
    calligraphy_with_bg[:] = bg_color  # 这里设置背景颜色
    
    # 将书法作品放置在背景中心
    calligraphy_with_bg[y_offset:y_offset+new_height, 
                       x_offset:x_offset+new_width] = calligraphy_resized
    
    # 7. 创建合成图像
    composite = scroll.copy()
    
    # 将书法作品放入透明区域
    composite[y_min:y_min+region_height, x_min:x_max, :3] = calligraphy_with_bg
    
    # 设置书法区域为不透明
    composite[y_min:y_min+region_height, x_min:x_max, 3] = 255
    
    # 8. 保存合成结果
    cv2.imwrite(output_path, composite)
    print(f"✅ 合成作品已保存: {output_path}")
    
    # 9. 调试显示
    if debug:
        show_composition_with_proportion(scroll, calligraphy, calligraphy_resized, 
                                       calligraphy_with_bg, alpha_channel, 
                                       x_min, y_min, region_width, region_height,
                                       composite)
    
    return composite

def show_composition_with_proportion(scroll, calligraphy, calligraphy_resized, 
                                   calligraphy_with_bg, alpha_channel,
                                   x_min, y_min, region_width, region_height,
                                   composite):
    """显示合成过程的详细信息"""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 卷轴模板
    axes[0, 0].imshow(cv2.cvtColor(scroll[:, :, :3], cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('卷轴模板')
    axes[0, 0].axis('off')
    
    # 原始书法作品
    axes[0, 1].imshow(cv2.cvtColor(calligraphy, cv2.COLOR_BGR2RGB))
    original_ratio = calligraphy.shape[1] / calligraphy.shape[0]
    axes[0, 1].set_title(f'原始书法\n{calligraphy.shape[1]}x{calligraphy.shape[0]}\n宽高比: {original_ratio:.3f}')
    axes[0, 1].axis('off')
    
    # 调整后的书法作品
    axes[0, 2].imshow(cv2.cvtColor(calligraphy_resized, cv2.COLOR_BGR2RGB))
    resized_ratio = calligraphy_resized.shape[1] / calligraphy_resized.shape[0]
    axes[0, 2].set_title(f'调整后书法\n{calligraphy_resized.shape[1]}x{calligraphy_resized.shape[0]}\n宽高比: {resized_ratio:.3f}')
    axes[0, 2].axis('off')
    
    # Alpha通道（透明区域）
    axes[1, 0].imshow(alpha_channel, cmap='gray')
    axes[1, 0].set_title('透明区域Alpha通道')
    axes[1, 0].axis('off')
    
    # 带背景的书法作品
    axes[1, 1].imshow(cv2.cvtColor(calligraphy_with_bg, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f'带背景的书法\n{region_width}x{region_height}')
    axes[1, 1].axis('off')
    
    # 最终合成结果
    axes[1, 2].imshow(cv2.cvtColor(composite[:, :, :3], cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('最终合成作品')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # 显示比例对比
    print("\n📊 比例对比:")
    print(f"  原始书法宽高比: {original_ratio:.3f}")
    print(f"  调整后书法宽高比: {resized_ratio:.3f}")
    print(f"  透明区域宽高比: {region_width/region_height:.3f}")
    
    if abs(original_ratio - resized_ratio) < 0.001:
        print("✅ 书法比例保持不变！")
    else:
        print("⚠️  书法比例有变化！")

# 增强版：多种适配选项
def insert_calligraphy_advanced(scroll_template_path, calligraphy_path, output_path,
                               fit_mode='fit_center', bg_color=(255, 255, 255),
                               padding=20, debug=False):
    """
    高级书法合成，提供多种适配模式
    
    参数:
    - fit_mode: 适配模式
        'fit_center': 居中适配，保持比例，可能有留白
        'stretch': 拉伸填满，会变形
        'crop': 裁剪适配，保持比例，裁剪多余部分
        'fit_width': 适配宽度，高度自动
        'fit_height': 适配高度，宽度自动
    - bg_color: 背景颜色 (B, G, R)
    - padding: 边距
    """
    
    print("\n" + "=" * 60)
    print(f"高级合成 - 模式: {fit_mode}")
    print("=" * 60)
    
    # 读取图像
    scroll = cv2.imread(scroll_template_path, cv2.IMREAD_UNCHANGED)
    calligraphy = cv2.imread(calligraphy_path)
    
    if scroll is None or calligraphy is None:
        print("❌ 无法读取图像")
        return None
    
    # 获取透明区域
    if scroll.shape[2] != 4:
        print("❌ 卷轴模板没有透明通道")
        return None
    
    alpha_channel = scroll[:, :, 3]
    transparent_pixels = np.where(alpha_channel == 0)
    
    if len(transparent_pixels[0]) == 0:
        print("⚠️  没有找到透明区域")
        return None
    
    y_min, y_max = np.min(transparent_pixels[0]), np.max(transparent_pixels[0])
    x_min, x_max = np.min(transparent_pixels[1]), np.max(transparent_pixels[1])
    region_width, region_height = x_max - x_min, y_max - y_min
    
    # 书法原始尺寸
    calligraphy_h, calligraphy_w = calligraphy.shape[:2]
    calligraphy_ratio = calligraphy_w / calligraphy_h
    
    # 可用区域（考虑padding）
    avail_w = region_width - 2 * padding
    avail_h = region_height - 2 * padding
    
    print(f"📏 透明区域: {region_width}x{region_height}")
    print(f"📏 书法原始: {calligraphy_w}x{calligraphy_h} (比例: {calligraphy_ratio:.3f})")
    print(f"📏 可用区域: {avail_w}x{avail_h}")
    
    # 根据模式计算新尺寸
    new_w, new_h = avail_w, avail_h  # 默认
    
    if fit_mode == 'fit_center':
        # 居中适配，保持比例
        width_ratio = avail_w / calligraphy_w
        height_ratio = avail_h / calligraphy_h
        scale = min(width_ratio, height_ratio)
        new_w = int(calligraphy_w * scale)
        new_h = int(calligraphy_h * scale)
        
    elif fit_mode == 'stretch':
        # 拉伸填满（会变形）
        new_w = avail_w
        new_h = avail_h
        
    elif fit_mode == 'crop':
        # 裁剪适配，保持比例
        width_ratio = avail_w / calligraphy_w
        height_ratio = avail_h / calligraphy_h
        scale = max(width_ratio, height_ratio)
        new_w = int(calligraphy_w * scale)
        new_h = int(calligraphy_h * scale)
        
    elif fit_mode == 'fit_width':
        # 适配宽度，高度按比例
        scale = avail_w / calligraphy_w
        new_w = avail_w
        new_h = int(calligraphy_h * scale)
        
    elif fit_mode == 'fit_height':
        # 适配高度，宽度按比例
        scale = avail_h / calligraphy_h
        new_w = int(calligraphy_w * scale)
        new_h = avail_h
        
    print(f"📐 新尺寸: {new_w}x{new_h} (比例: {new_w/new_h:.3f})")
    
    # 调整书法大小
    if (new_w, new_h) != (calligraphy_w, calligraphy_h):
        calligraphy_resized = cv2.resize(calligraphy, (new_w, new_h), 
                                        interpolation=cv2.INTER_AREA)
    else:
        calligraphy_resized = calligraphy.copy()
    
    # 创建背景
    calligraphy_with_bg = np.ones((avail_h, avail_w, 3), dtype=np.uint8)
    calligraphy_with_bg[:] = bg_color
    
    # 计算放置位置
    if fit_mode == 'crop':
        # 裁剪模式：居中裁剪
        crop_x = max(0, (new_w - avail_w) // 2)
        crop_y = max(0, (new_h - avail_h) // 2)
        cropped = calligraphy_resized[crop_y:crop_y+avail_h, crop_x:crop_x+avail_w]
        calligraphy_with_bg = cropped
        x_offset, y_offset = 0, 0
    else:
        # 其他模式：居中放置
        x_offset = (avail_w - new_w) // 2
        y_offset = (avail_h - new_h) // 2
        calligraphy_with_bg[y_offset:y_offset+new_h, 
                          x_offset:x_offset+new_w] = calligraphy_resized
    
    # 合成
    composite = scroll.copy()
    composite[y_min+padding:y_min+padding+avail_h, 
             x_min+padding:x_min+padding+avail_w, :3] = calligraphy_with_bg
    composite[y_min:y_min+region_height, x_min:x_max, 3] = 255
    
    # 保存
    cv2.imwrite(output_path, composite)
    print(f"✅ 已保存: {output_path}")
    
    if debug:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        axes[0].imshow(cv2.cvtColor(calligraphy, cv2.COLOR_BGR2RGB))
        axes[0].set_title(f'原始\n{calligraphy_w}x{calligraphy_h}')
        axes[0].axis('off')
        
        axes[1].imshow(cv2.cvtColor(calligraphy_resized, cv2.COLOR_BGR2RGB))
        axes[1].set_title(f'调整后\n{new_w}x{new_h}\n模式: {fit_mode}')
        axes[1].axis('off')
        
        axes[2].imshow(cv2.cvtColor(composite[:, :, :3], cv2.COLOR_BGR2RGB))
        axes[2].set_title('合成结果')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    return composite

# 完整工作流程
def complete_workflow_with_proportion(scroll_template_path, calligraphy_path,
                                     output_template_path, output_final_path,
                                     padding=30, bg_color=(255, 255, 255), debug=True):
    """
    完整工作流程：保持书法比例
    """
    
    # 先创建透明模板（使用之前的函数）
    # from your_previous_code import find_inner_region_and_make_transparent
    
    print("🚀 开始完整工作流程（保持书法比例）")
    print("=" * 60)
    
    # 步骤1: 创建透明模板
    # transparent_template, _ = find_inner_region_and_make_transparent(
    #     scroll_template_path,
    #     output_template_path,
    #     debug=debug
    # )

    """
    安全地调用函数，处理返回 None 的情况
    """
    try:
        result = find_inner_region_and_make_transparent(
            scroll_template_path,
            output_template_path,
            debug=debug
        )
        
        if result is None:
            print("❌ 函数返回 None，使用默认模板")
            # # 返回一个默认的透明模板
            # default_template = create_default_template()
            # return default_template, np.ones((100, 100), dtype=np.uint8) * 255
        
        # 正常解包
        transparent_template, mask = result
        return transparent_template, mask
        
    except Exception as e:
        print(f"❌ 调用函数时出错: {e}")
        # 创建应急模板
        # emergency_template = create_emergency_template()
        # return emergency_template, None
    
    if transparent_template is None:
        print("❌ 无法创建透明模板")
        return None
    
    print("\n✅ 步骤1完成：透明模板已创建")
    
    # 步骤2: 合成书法作品（保持比例）
    final_result = insert_calligraphy_with_proportion(
        output_template_path,
        calligraphy_path,
        output_final_path,
        padding=padding,
        bg_color=bg_color,
        debug=debug
    )
    
    if final_result is None:
        print("❌ 无法合成书法作品")
        return None
    
    print("\n✅ 步骤2完成：书法作品已合成（保持比例）")
    print("=" * 60)
    print("🎉 全部完成！")
    print(f"📁 透明模板: {output_template_path}")
    print(f"📁 最终作品: {output_final_path}")
    
    return final_result

# 快速使用示例
def quick_insert_with_proportion(scroll_path, calligraphy_path, output_path, padding=30):
    """
    快速插入：保持书法比例，简单背景
    """
    # 这里假设你已经有了透明模板
    # 如果没有，先用前面的函数创建
    
    result = insert_calligraphy_with_proportion(
        scroll_path,
        calligraphy_path,
        output_path,
        padding=padding,
        bg_color=(255, 255, 255),  # 白色背景
        debug=False
    )
    
    return result

# 测试不同适配模式
def test_all_fit_modes(scroll_path, calligraphy_path, output_dir):
    """
    测试所有适配模式
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    modes = ['fit_center', 'stretch', 'crop', 'fit_width', 'fit_height']
    
    for mode in modes:
        output_path = os.path.join(output_dir, f'result_{mode}.png')
        print(f"\n测试模式: {mode}")
        
        try:
            insert_calligraphy_advanced(
                scroll_path,
                calligraphy_path,
                output_path,
                fit_mode=mode,
                padding=20,
                debug=False
            )
            print(f"✅ {mode} 模式完成")
        except Exception as e:
            print(f"❌ {mode} 模式失败: {e}")


def detect_torn_edge_background_no_skimage(calligraphy_path, debug=False):
    """
    检测撕边书法背景颜色 - 不依赖skimage的版本
    """
    
    print(f"🔍 分析撕边书法作品: {calligraphy_path}")
    
    # 1. 读取图像
    img = cv2.imread(calligraphy_path)
    if img is None:
        print("❌ 无法读取图像")
        return (255, 255, 255), 0.0
    
    height, width = img.shape[:2]
    print(f"📏 图像尺寸: {width}x{height}")
    
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. 撕边效果特征检测（使用纯OpenCV）
    print("🔄 检测撕边特征...")
    
    # 方法A: 多种边缘检测方法组合
    edges_canny = cv2.Canny(gray, 20, 60)  # 低阈值检测细微边缘
    
    # 方法B: Laplacian检测细节
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian_abs = np.uint8(np.absolute(laplacian))
    
    # 方法C: Sobel梯度
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    gradient_magnitude_norm = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # 方法D: 纹理分析 - 使用局部方差
    def calculate_local_variance(image, window_size=5):
        """计算局部方差（替代LBP）"""
        mean = cv2.boxFilter(image, cv2.CV_32F, (window_size, window_size))
        mean_square = cv2.boxFilter(image.astype(np.float32)**2, cv2.CV_32F, (window_size, window_size))
        variance = mean_square - mean**2
        return np.sqrt(np.maximum(variance, 0))
    
    local_var = calculate_local_variance(gray, window_size=7)
    local_var_norm = cv2.normalize(local_var, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # 3. 识别撕边区域
    print("🎨 识别撕边区域...")
    
    # 综合多种特征创建撕边掩码
    torn_edge_mask = np.zeros((height, width), dtype=np.uint8)
    
    # 特征融合
    for y in range(height):
        for x in range(width):
            # 多个条件判断是否是撕边区域
            conditions = 0
            
            # 条件1: 有边缘但不是强边缘
            if edges_canny[y, x] > 0:
                conditions += 1
            
            # 条件2: 中等梯度
            if 20 < gradient_magnitude_norm[y, x] < 150:
                conditions += 1
            
            # 条件3: 中等局部方差（有纹理但不是太强）
            if 30 < local_var_norm[y, x] < 150:
                conditions += 1
            
            # 条件4: 亮度在中间范围
            if 100 < gray[y, x] < 220:
                conditions += 1
            
            # 满足至少3个条件认为是撕边区域
            if conditions >= 3:
                torn_edge_mask[y, x] = 255
    
    # 形态学操作
    kernel = np.ones((3, 3), np.uint8)
    torn_edge_mask = cv2.morphologyEx(torn_edge_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    torn_edge_mask = cv2.morphologyEx(torn_edge_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # 4. 智能背景采样（避开撕边区域）
    print("💡 智能背景采样...")
    
    background_candidates = []
    
    # 动态生成采样网格
    grid_size = 8  # 8x8网格
    cell_w = width // grid_size
    cell_h = height // grid_size
    
    for i in range(grid_size):
        for j in range(grid_size):
            x1 = i * cell_w
            y1 = j * cell_h
            x2 = min((i + 1) * cell_w, width)
            y2 = min((j + 1) * cell_h, height)
            
            # 跳过太小的区域
            if (x2 - x1) < 10 or (y2 - y1) < 10:
                continue
            
            region = img[y1:y2, x1:x2]
            region_gray = gray[y1:y2, x1:x2]
            region_mask = torn_edge_mask[y1:y2, x1:x2]
            
            # 计算区域特征
            avg_color = np.median(region.reshape(-1, 3), axis=0).astype(int)
            avg_brightness = np.mean(region_gray)
            brightness_std = np.std(region_gray)
            torn_ratio = np.mean(region_mask) / 255.0
            
            # 背景区域评分
            score = 0
            
            # 规则1: 亮度高（+分）
            brightness_score = min(1.0, avg_brightness / 255.0)
            score += brightness_score * 0.4
            
            # 规则2: 亮度均匀（+分）
            uniformity_score = 1.0 - min(1.0, brightness_std / 100.0)
            score += uniformity_score * 0.3
            
            # 规则3: 撕边区域少（+分）
            no_torn_score = 1.0 - torn_ratio
            score += no_torn_score * 0.3
            
            # 如果是好的背景候选区域
            if score > 0.6:  # 阈值可调
                background_candidates.append({
                    'color': avg_color,
                    'brightness': avg_brightness,
                    'std': brightness_std,
                    'torn_ratio': torn_ratio,
                    'score': score,
                    'position': (i, j)  # 网格位置
                })
    
    print(f"📊 找到 {len(background_candidates)} 个高质量背景候选区域")
    
    # 5. 多尺度金字塔分析
    print("🔬 多尺度金字塔分析...")
    
    pyramid_colors = []
    
    # 创建高斯金字塔
    pyramid_levels = 3
    current_img = img.copy()
    
    for level in range(pyramid_levels):
        if level > 0:
            # 降采样
            current_img = cv2.pyrDown(current_img)
        
        level_img = current_img
        level_gray = cv2.cvtColor(level_img, cv2.COLOR_BGR2GRAY)
        h, w = level_gray.shape
        
        # 使用自适应阈值找到背景
        adaptive_thresh = cv2.adaptiveThreshold(level_gray, 255,
                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY, 11, 2)
        adaptive_thresh_inv = cv2.bitwise_not(adaptive_thresh)
        
        # 获取背景像素
        bg_pixels = level_img[adaptive_thresh_inv > 0]
        if len(bg_pixels) > 0:
            level_color = np.median(bg_pixels, axis=0).astype(int)
            pyramid_colors.append(level_color)
    
    # 6. 颜色选择策略
    print("🎨 智能颜色选择...")
    
    # 收集所有候选
    all_candidates = []
    
    # 添加网格候选
    for cand in background_candidates:
        all_candidates.append(cand['color'])
    
    # 添加金字塔候选
    all_candidates.extend(pyramid_colors)
    
    if len(all_candidates) == 0:
        print("⚠️  没有找到合适的背景颜色，使用保守估计")
        # 使用最亮的1%像素
        bright_threshold = np.percentile(gray, 99)
        bright_pixels = img[gray > bright_threshold]
        if len(bright_pixels) > 0:
            final_color = np.median(bright_pixels, axis=0).astype(int)
        else:
            final_color = np.array([255, 255, 255])
    else:
        all_candidates = np.array(all_candidates)
        
        # 策略1: 选择最亮的颜色
        brightness = 0.299 * all_candidates[:, 2] + 0.587 * all_candidates[:, 1] + 0.114 * all_candidates[:, 0]
        
        # 策略2: 考虑颜色的一致性
        color_variance = np.std(all_candidates, axis=0)
        
        # 策略3: 加权选择
        # 亮度权重 + 一致性权重
        brightness_weights = brightness / 255.0
        
        # 计算每个颜色到其他颜色的平均距离（越近权重越高）
        consistency_weights = []
        for i, color in enumerate(all_candidates):
            distances = np.sqrt(np.sum((all_candidates - color) ** 2, axis=1))
            avg_distance = np.mean(distances)
            consistency = 1.0 - min(1.0, avg_distance / 100.0)
            consistency_weights.append(consistency)
        
        consistency_weights = np.array(consistency_weights)
        
        # 综合权重
        total_weights = brightness_weights * 0.6 + consistency_weights * 0.4
        
        # 选择权重最高的颜色
        best_idx = np.argmax(total_weights)
        final_color = all_candidates[best_idx]
    
    # 7. 后处理优化
    print("🔄 后处理优化...")
    
    final_color = optimize_for_torn_edge(final_color, gray, torn_edge_mask, background_candidates)
    
    # 8. 计算置信度
    confidence = calculate_confidence_no_skimage(final_color, gray, background_candidates, torn_edge_mask)
    
    print(f"✅ 最终背景颜色: RGB{BGR_to_RGB(final_color)}")
    print(f"📈 亮度: {0.299*final_color[2]+0.587*final_color[1]+0.114*final_color[0]:.1f}")
    print(f"🎯 检测置信度: {confidence:.3f}")
    
    # 9. 调试显示
    if debug:
        show_analysis_no_skimage(img, gray, edges_canny, gradient_magnitude_norm,
                               local_var_norm, torn_edge_mask, background_candidates, 
                               final_color, confidence)
    
    return tuple(final_color.astype(int)), confidence

def optimize_for_torn_edge(color, gray, torn_mask, candidates):
    """
    针对撕边效果优化背景颜色
    """
    # 1. 确保足够的亮度
    brightness = 0.299 * color[2] + 0.587 * color[1] + 0.114 * color[0]
    
    if brightness < 180:
        print("⚠️  颜色偏暗，调亮处理")
        # 向白色方向调整
        adjustment = 0.25
        color = color.astype(np.float32)
        color = color + (255 - color) * adjustment
        color = np.clip(color, 0, 255).astype(int)
    
    # 2. 检查颜色通道平衡
    # 撕边书法背景通常是暖色调（红黄为主）
    red_ratio = color[2] / max(color[0], 1)  # R/B 比例
    if red_ratio < 0.9:  # 红色不足
        print("⚠️  红色不足，调整为暖色调")
        color[2] = min(255, int(color[2] * 1.15))  # 增加红色
        color[1] = min(255, int(color[1] * 1.05))  # 稍微增加绿色
        color[0] = int(color[0] * 0.9)  # 减少蓝色
    
    # 3. 如果有高质量候选区域，考虑使用最好的候选
    if candidates:
        best_candidate = max(candidates, key=lambda x: x['score'])
        if best_candidate['score'] > 0.8 and best_candidate['torn_ratio'] < 0.1:
            # 如果有一个非常好的候选，并且几乎没有撕边，可以信任它
            best_color = best_candidate['color']
            best_brightness = best_candidate['brightness']
            
            current_brightness = 0.299 * color[2] + 0.587 * color[1] + 0.114 * color[0]
            
            if abs(best_brightness - current_brightness) > 30:
                # 如果亮度差异大，考虑混合
                print("🔄 与高质量候选区域颜色混合")
                color = (color * 0.7 + best_color * 0.3).astype(int)
    
    return color

def calculate_confidence_no_skimage(color, gray, candidates, torn_mask):
    """
    计算置信度
    """
    confidence = 0.5
    
    # 1. 亮度得分
    brightness = 0.299 * color[2] + 0.587 * color[1] + 0.114 * color[0]
    brightness_score = min(1.0, brightness / 220.0)
    confidence += 0.25 * brightness_score
    
    # 2. 候选区域质量得分
    if candidates:
        best_score = max([c['score'] for c in candidates])
        candidate_score = best_score
        confidence += 0.25 * candidate_score
        
        # 候选区域一致性
        if len(candidates) >= 3:
            colors = np.array([c['color'] for c in candidates])
            color_std = np.mean(np.std(colors, axis=0))
            consistency = 1.0 - min(1.0, color_std / 50.0)
            confidence += 0.15 * consistency
    
    # 3. 撕边识别合理性
    torn_ratio = np.sum(torn_mask > 0) / (gray.shape[0] * gray.shape[1])
    # 合理的撕边比例是5-20%
    torn_score = 1.0 - min(1.0, abs(torn_ratio - 0.12) / 0.12)
    confidence += 0.15 * torn_score
    
    # 4. 图像对比度
    contrast = np.std(gray)
    contrast_score = min(1.0, contrast / 80.0)
    confidence += 0.1 * contrast_score
    
    # 5. 颜色合理性（暖色调）
    warmth = color[2] / max(color[0], 1)  # R/B比例
    warmth_score = min(1.0, warmth / 1.5)
    confidence += 0.1 * warmth_score
    
    return min(1.0, confidence)

def BGR_to_RGB(bgr_color):
    """BGR转RGB"""
    return (bgr_color[2], bgr_color[1], bgr_color[0])

def RGB_to_BGR(rgb_color):
    """RGB转BGR"""
    return (rgb_color[2], rgb_color[1], rgb_color[0])

def show_analysis_no_skimage(img, gray, edges, gradient, local_var, 
                           torn_mask, candidates, final_color, confidence):
    """显示分析过程"""
    
    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    
    # 1. 原始图像
    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title(f'原始撕边书法\n{img.shape[1]}x{img.shape[0]}')
    axes[0, 0].axis('off')
    
    # 2. 灰度图像
    axes[0, 1].imshow(gray, cmap='gray')
    axes[0, 1].set_title('灰度图像')
    axes[0, 1].axis('off')
    
    # 3. 边缘检测
    axes[0, 2].imshow(edges, cmap='gray')
    axes[0, 2].set_title('边缘检测')
    axes[0, 2].axis('off')
    
    # 4. 梯度幅度
    axes[0, 3].imshow(gradient, cmap='hot')
    axes[0, 3].set_title('梯度幅度')
    axes[0, 3].axis('off')
    
    # 5. 局部方差
    axes[1, 0].imshow(local_var, cmap='viridis')
    axes[1, 0].set_title('局部方差（纹理）')
    axes[1, 0].axis('off')
    
    # 6. 撕边掩码
    axes[1, 1].imshow(torn_mask, cmap='gray')
    axes[1, 1].set_title('撕边区域检测')
    axes[1, 1].axis('off')
    
    # 7. 叠加显示撕边
    overlay = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).copy()
    overlay[torn_mask > 0] = [255, 0, 0]
    axes[1, 2].imshow(overlay)
    axes[1, 2].set_title('撕边标记(红色)')
    axes[1, 2].axis('off')
    
    # 8. 候选区域网格
    grid_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).copy()
    
    # 绘制网格
    grid_size = 8
    h, w = gray.shape
    cell_w = w // grid_size
    cell_h = h // grid_size
    
    for i in range(grid_size + 1):
        x = i * cell_w
        cv2.line(grid_img, (x, 0), (x, h), (0, 255, 0), 1)
    for j in range(grid_size + 1):
        y = j * cell_h
        cv2.line(grid_img, (0, y), (w, y), (0, 255, 0), 1)
    
    # 标记高质量候选区域
    for cand in candidates:
        if cand['score'] > 0.7:
            i, j = cand['position']
            x1 = i * cell_w
            y1 = j * cell_h
            x2 = min((i + 1) * cell_w, w)
            y2 = min((j + 1) * cell_h, h)
            
            cv2.rectangle(grid_img, (x1, y1), (x2, y2), (255, 255, 0), 2)
    
    axes[1, 3].imshow(grid_img)
    axes[1, 3].set_title(f'候选区域网格\n找到{len(candidates)}个候选')
    axes[1, 3].axis('off')
    
    # 9. 候选颜色展示
    if candidates:
        # 显示前4个最佳候选
        sorted_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)[:4]
        
        color_grid = np.zeros((100, 400, 3), dtype=np.uint8)
        for idx, cand in enumerate(sorted_candidates):
            block = np.ones((50, 50, 3), dtype=np.uint8)
            block[:] = BGR_to_RGB(cand['color'])
            
            x_start = idx * 100
            color_grid[25:75, x_start+25:x_start+75] = block
            
            # 添加分数标签
            cv2.putText(color_grid, f"{cand['score']:.2f}", 
                       (x_start+20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        axes[2, 0].imshow(color_grid)
        axes[2, 0].set_title('最佳候选颜色(带分数)')
        axes[2, 0].axis('off')
    else:
        axes[2, 0].text(0.5, 0.5, '无候选区域', 
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=axes[2, 0].transAxes)
        axes[2, 0].axis('off')
    
    # 10. 最终颜色
    final_block = np.ones((100, 100, 3), dtype=np.uint8)
    final_block[:] = BGR_to_RGB(final_color)
    
    axes[2, 1].imshow(final_block)
    axes[2, 1].set_title(f'最终背景颜色\nRGB{BGR_to_RGB(final_color)}')
    axes[2, 1].axis('off')
    
    # 11. 预览效果
    preview = np.ones_like(img)
    preview[:] = final_color
    
    # 提取文字（简单阈值）
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 将文字叠加到背景
    preview[thresh > 0] = img[thresh > 0]
    
    axes[2, 2].imshow(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB))
    axes[2, 2].set_title('背景应用预览')
    axes[2, 2].axis('off')
    
    # 12. 置信度信息
    axes[2, 3].text(0.5, 0.5, 
                   f'检测结果\n\n'
                   f'置信度: {confidence:.3f}\n\n'
                   f'亮度: {0.299*final_color[2]+0.587*final_color[1]+0.114*final_color[0]:.0f}\n'
                   f'色调(R/B): {final_color[2]/max(final_color[0],1):.2f}\n'
                   f'撕边区域: {np.sum(torn_mask>0)/(gray.shape[0]*gray.shape[1]):.1%}',
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=10,
                   transform=axes[2, 3].transAxes)
    
    # 根据置信度添加颜色标记
    if confidence > 0.7:
        color = 'green'
        text = '✅ 高可信度'
    elif confidence > 0.5:
        color = 'orange'
        text = '⚠️  中等可信度'
    else:
        color = 'red'
        text = '❌ 低可信度'
    
    axes[2, 3].text(0.5, 0.1, text, 
                   horizontalalignment='center',
                   color=color,
                   fontsize=12,
                   transform=axes[2, 3].transAxes)
    axes[2, 3].axis('off')
    
    plt.tight_layout()
    plt.show()

# 简化的主函数
def smart_insert_for_torn_edge(scroll_template_path, calligraphy_path, output_path,
                              padding=30, debug=True):
    """
    针对撕边书法的智能合成
    """
    
    print("=" * 60)
    print("撕边书法智能合成")
    print("=" * 60)
    
    # 1. 检测背景颜色
    bg_color_bgr, confidence = detect_torn_edge_background_no_skimage(calligraphy_path, debug=debug)
    
    print(f"🎯 检测完成 - 置信度: {confidence:.3f}")
    
    # 2. 读取图像
    scroll = cv2.imread(scroll_template_path, cv2.IMREAD_UNCHANGED)
    calligraphy = cv2.imread(calligraphy_path)
    
    if scroll is None or calligraphy is None:
        print("❌ 无法读取图像")
        return None, confidence
    
    # 3. 合成
    result = simple_composite(scroll, calligraphy, bg_color_bgr, padding)
    
    if result is not None:
        cv2.imwrite(output_path, result)
        print(f"✅ 已保存: {output_path}")
    
    return result, confidence

def simple_composite(scroll, calligraphy, bg_color, padding=30):
    """
    简单的合成函数
    """
    # 获取透明区域
    if scroll.shape[2] != 4:
        return None
    
    alpha_channel = scroll[:, :, 3]
    transparent_pixels = np.where(alpha_channel == 0)
    
    if len(transparent_pixels[0]) == 0:
        return None
    
    y_min, y_max = np.min(transparent_pixels[0]), np.max(transparent_pixels[0])
    x_min, x_max = np.min(transparent_pixels[1]), np.max(transparent_pixels[1])
    region_width, region_height = x_max - x_min, y_max - y_min
    
    # 保持比例调整书法大小
    calligraphy_h, calligraphy_w = calligraphy.shape[:2]
    avail_w = region_width - 2 * padding
    avail_h = region_height - 2 * padding
    
    # 计算缩放比例
    width_ratio = avail_w / calligraphy_w
    height_ratio = avail_h / calligraphy_h
    scale = min(width_ratio, height_ratio)
    new_w = int(calligraphy_w * scale)
    new_h = int(calligraphy_h * scale)
    
    # 调整大小
    if scale != 1.0:
        calligraphy_resized = cv2.resize(calligraphy, (new_w, new_h), cv2.INTER_AREA)
    else:
        calligraphy_resized = calligraphy.copy()
    
    # 创建背景
    calligraphy_with_bg = np.ones((avail_h, avail_w, 3), dtype=np.uint8)
    calligraphy_with_bg[:] = bg_color
    
    # 居中放置
    x_offset = (avail_w - new_w) // 2
    y_offset = (avail_h - new_h) // 2
    calligraphy_with_bg[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = calligraphy_resized
    
    # 合成
    composite = scroll.copy()
    composite[y_min+padding:y_min+padding+avail_h, 
             x_min+padding:x_min+padding+avail_w, :3] = calligraphy_with_bg
    composite[y_min:y_min+region_height, x_min:x_max, 3] = 255
    
    return composite

import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def detect_torn_edge_background_improved(calligraphy_path, debug=False):
    """
    改进的撕边书法背景检测 - 避免纯白色背景
    """
    
    print(f"🔍 分析撕边书法作品: {calligraphy_path}")
    
    # 1. 读取图像
    img = cv2.imread(calligraphy_path)
    if img is None:
        print("❌ 无法读取图像")
        return (240, 230, 210), 0.0  # 返回宣纸色而不是白色
    
    height, width = img.shape[:2]
    
    # 2. 分析图像整体色调
    print("🎨 分析整体色调...")
    
    # 转换为HSV色彩空间分析色调
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 计算平均色调（排除太暗和太亮的像素）
    mask = (hsv[:,:,2] > 50) & (hsv[:,:,2] < 200)  # 中等亮度区域
    if np.any(mask):
        avg_hue = np.mean(hsv[:,:,0][mask])
        avg_saturation = np.mean(hsv[:,:,1][mask])
        avg_value = np.mean(hsv[:,:,2][mask])
        
        print(f"📊 平均色调: H={avg_hue:.1f}, S={avg_saturation:.1f}, V={avg_value:.1f}")
        
        # 根据色调选择基础颜色
        base_color = select_base_color_by_hue(avg_hue, avg_saturation, avg_value)
    else:
        base_color = (240, 230, 210)  # 默认宣纸色
    
    # 3. 智能边缘采样（专门针对撕边）
    print("📊 智能边缘采样...")
    
    # 创建采样掩码：避开中央文字区域
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 使用自适应阈值找到文字区域
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255,
                                           cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 11, 2)
    
    # 膨胀文字区域掩码
    kernel = np.ones((5,5), np.uint8)
    text_mask = cv2.dilate(adaptive_thresh, kernel, iterations=2)
    
    # 创建边缘采样掩码（避开文字）
    edge_mask = np.ones_like(gray, dtype=np.uint8) * 255
    edge_mask[text_mask > 0] = 0  # 文字区域不采样
    
    # 进一步限制采样区域到图像边缘
    margin = int(min(width, height) * 0.15)  # 15%的边缘区域
    center_mask = np.zeros_like(gray, dtype=np.uint8)
    center_mask[margin:-margin, margin:-margin] = 255
    edge_mask = cv2.bitwise_and(edge_mask, center_mask)
    
    # 4. 采样边缘像素
    edge_pixels = img[edge_mask > 0]
    
    if len(edge_pixels) > 0:
        # 分析边缘像素的颜色分布
        edge_colors_bgr = edge_pixels.reshape(-1, 3)
        
        # 使用K-means聚类找到主要颜色（最多3类）
        n_clusters = min(3, len(edge_colors_bgr))
        
        if n_clusters > 1:
            # 将像素转换为float32
            edge_colors_float = np.float32(edge_colors_bgr)
            
            # 定义K-means参数
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, centers = cv2.kmeans(edge_colors_float, n_clusters, None, 
                                          criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # 将中心转换为整数
            centers = np.uint8(centers)
            
            # 统计每个聚类的数量
            unique_labels, counts = np.unique(labels, return_counts=True)
            
            # 计算每个聚类的亮度
            brightness_scores = []
            for i, center in enumerate(centers):
                b = 0.299 * center[2] + 0.587 * center[1] + 0.114 * center[0]
                brightness_scores.append(b)
            
            # 选择最亮的聚类，但不是纯白色
            brightest_idx = np.argmax(brightness_scores)
            
            # 如果最亮的是近白色（亮度>240），选择次亮的
            if brightness_scores[brightest_idx] > 240:
                # 找次亮的
                brightness_scores_copy = brightness_scores.copy()
                brightness_scores_copy[brightest_idx] = 0
                second_brightest_idx = np.argmax(brightness_scores_copy)
                
                # 如果次亮的亮度也合理，使用它
                if brightness_scores[second_brightest_idx] > 180:
                    selected_color = centers[second_brightest_idx]
                else:
                    # 调整最亮的颜色，使其不是纯白
                    selected_color = adjust_away_from_white(centers[brightest_idx])
            else:
                selected_color = centers[brightest_idx]
            
            edge_bg_color = tuple(selected_color)
            print(f"📊 边缘采样颜色: RGB{selected_color[::-1]}")
        else:
            # 如果只有一个聚类，使用中值
            edge_bg_color = tuple(np.median(edge_colors_bgr, axis=0).astype(int))
    else:
        edge_bg_color = base_color
    
    # 5. 分析中心区域颜色（作为参考）
    print("📊 分析中心区域...")
    
    # 取图像中心区域（避开边缘）
    center_region = img[height//4:3*height//4, width//4:3*width//4]
    
    if center_region.size > 0:
        # 计算中心区域的平均颜色
        center_avg = np.median(center_region.reshape(-1, 3), axis=0).astype(int)
        center_brightness = 0.299 * center_avg[2] + 0.587 * center_avg[1] + 0.114 * center_avg[0]
        
        print(f"📊 中心区域颜色: RGB{center_avg[::-1]}, 亮度: {center_brightness:.1f}")
        
        # 如果中心区域很亮，可能是背景
        if center_brightness > 180:
            center_color = tuple(center_avg)
        else:
            center_color = None
    else:
        center_color = None
    
    # 6. 融合多种颜色来源
    print("🔄 融合颜色来源...")
    
    color_sources = []
    weights = []
    
    # 源1: 基于色调的基础颜色 (权重0.3)
    color_sources.append(base_color)
    weights.append(0.3)
    
    # 源2: 边缘采样颜色 (权重0.4)
    color_sources.append(edge_bg_color)
    weights.append(0.4)
    
    # 源3: 中心区域颜色（如果可用） (权重0.3)
    if center_color is not None:
        color_sources.append(center_color)
        weights.append(0.3)
    
    # 归一化权重
    total_weight = sum(weights)
    weights = [w/total_weight for w in weights]
    
    # 计算加权平均
    final_color = np.zeros(3, dtype=np.float32)
    for color, weight in zip(color_sources, weights):
        final_color += np.array(color, dtype=np.float32) * weight
    
    final_color = final_color.astype(int)
    
    # 7. 后处理：确保颜色合理
    print("🎨 后处理颜色...")
    
    # 检查并调整
    final_color = ensure_reasonable_color(final_color, gray, debug)
    
    # 8. 计算置信度
    confidence = calculate_final_confidence(final_color, edge_pixels, gray)
    
    print(f"✅ 最终背景颜色: RGB{final_color[::-1]}")
    print(f"📈 亮度: {0.299*final_color[2]+0.587*final_color[1]+0.114*final_color[0]:.1f}")
    print(f"🎯 检测置信度: {confidence:.3f}")
    
    # 9. 调试显示
    if debug:
        show_improved_analysis(img, gray, edge_mask, text_mask, 
                             color_sources, final_color, confidence)
    
    return tuple(final_color), confidence

def select_base_color_by_hue(hue, saturation, value):
    """
    根据HSV值选择基础颜色
    """
    # 宣纸色系（暖黄调）
    paper_colors = [
        (240, 230, 210),  # 标准宣纸色
        (245, 240, 225),  # 亮宣纸色
        (235, 220, 200),  # 暗宣纸色
        (250, 245, 235),  # 象牙宣纸
    ]
    
    # 如果饱和度低、亮度高，可能是老旧纸张
    if saturation < 30 and value > 180:
        return paper_colors[1]  # 亮宣纸色
    
    # 根据色调选择
    if 15 <= hue <= 45:  # 黄色调
        return paper_colors[0]  # 标准宣纸色
    elif hue < 15 or hue > 165:  # 红/品红调
        return (245, 235, 225)  # 偏红的宣纸色
    else:  # 绿/蓝调
        return (235, 240, 230)  # 偏绿的宣纸色

def adjust_away_from_white(color, target_brightness=220):
    """
    将接近白色的颜色调整为目标亮度
    """
    current_brightness = 0.299 * color[2] + 0.587 * color[1] + 0.114 * color[0]
    
    if current_brightness > target_brightness:
        # 计算调整比例
        ratio = target_brightness / current_brightness
        
        # 调整颜色
        adjusted = color.astype(np.float32) * ratio
        adjusted = np.clip(adjusted, 0, 255).astype(int)
        
        # 确保不是纯灰色（保持一点色调）
        if abs(adjusted[0] - adjusted[1]) < 10 and abs(adjusted[1] - adjusted[2]) < 10:
            # 随机添加一点色调
            hue_shift = np.random.randint(-10, 10)
            adjusted[2] = np.clip(adjusted[2] + hue_shift, 0, 255)  # 调整红色
        
        return adjusted
    else:
        return color

def ensure_reasonable_color(color, gray_img, debug=False):
    """
    确保最终颜色合理（不是纯白，有适当的色调）
    """
    # 计算亮度
    brightness = 0.299 * color[2] + 0.587 * color[1] + 0.114 * color[0]
    
    # 规则1: 不能是纯白色
    if brightness > 245:
        if debug:
            print("⚠️  颜色太接近白色，调整为宣纸色")
        # 调整为宣纸色
        color = np.array([240, 230, 210])
    
    # 规则2: 不能太暗
    elif brightness < 150:
        if debug:
            print("⚠️  颜色太暗，调亮")
        # 调亮
        adjustment = 0.4
        color = color.astype(np.float32)
        color = color + (220 - color) * adjustment
        color = np.clip(color, 0, 255).astype(int)
    
    # 规则3: 检查颜色平衡（避免冷色调）
    # 撕边书法背景通常是暖色调
    red_blue_ratio = color[2] / max(color[0], 1)
    if red_blue_ratio < 0.9:  # 蓝色偏多
        if debug:
            print("⚠️  颜色偏冷，调整为暖色调")
        # 增加红色，减少蓝色
        color[2] = min(255, int(color[2] * 1.15))  # 增加红色
        color[0] = int(color[0] * 0.85)  # 减少蓝色
    
    # 规则4: 与图像整体亮度协调
    img_brightness = np.mean(gray_img)
    color_brightness = 0.299 * color[2] + 0.587 * color[1] + 0.114 * color[0]
    
    # 背景应该比图像平均亮度更亮
    if color_brightness < img_brightness:
        if debug:
            print(f"⚠️  背景亮度({color_brightness:.0f})低于图像平均({img_brightness:.0f})，调亮")
        # 调亮到比平均亮度高30
        target = img_brightness + 30
        if target > color_brightness:
            ratio = target / max(color_brightness, 1)
            color = np.clip(color.astype(np.float32) * ratio, 0, 255).astype(int)
    
    return color

def calculate_final_confidence(color, edge_pixels, gray_img):
    """
    计算最终置信度
    """
    confidence = 0.6  # 基础置信度
    
    # 1. 亮度合理性得分
    brightness = 0.299 * color[2] + 0.587 * color[1] + 0.114 * color[0]
    
    # 理想的背景亮度范围：180-230
    if 180 <= brightness <= 230:
        brightness_score = 1.0
    elif 170 <= brightness < 180 or 230 < brightness <= 240:
        brightness_score = 0.8
    elif 150 <= brightness < 170 or 240 < brightness <= 250:
        brightness_score = 0.6
    else:
        brightness_score = 0.3
    
    confidence += 0.2 * brightness_score
    
    # 2. 颜色丰富性得分（不是纯灰色）
    color_variance = np.std(color)
    if color_variance > 15:
        color_score = 1.0
    elif color_variance > 10:
        color_score = 0.8
    elif color_variance > 5:
        color_score = 0.6
    else:
        color_score = 0.3
    
    confidence += 0.2 * color_score
    
    # 3. 暖色调得分（撕边书法通常是暖色）
    red_blue_ratio = color[2] / max(color[0], 1)
    if red_blue_ratio > 1.2:
        warmth_score = 1.0  # 明显的暖色调
    elif red_blue_ratio > 1.0:
        warmth_score = 0.8  # 轻微暖色调
    elif red_blue_ratio > 0.8:
        warmth_score = 0.6  # 中性
    else:
        warmth_score = 0.3  # 冷色调
    
    confidence += 0.1 * warmth_score
    
    # 4. 边缘采样质量得分
    if len(edge_pixels) > 100:
        edge_score = 1.0
    elif len(edge_pixels) > 50:
        edge_score = 0.8
    elif len(edge_pixels) > 20:
        edge_score = 0.6
    else:
        edge_score = 0.3
    
    confidence += 0.1 * edge_score
    
    return min(1.0, confidence)

def show_improved_analysis(img, gray, edge_mask, text_mask, 
                         color_sources, final_color, confidence):
    """显示分析过程"""
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    # 1. 原始图像
    axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('原始撕边书法')
    axes[0, 0].axis('off')
    
    # 2. 文字区域掩码
    axes[0, 1].imshow(text_mask, cmap='gray')
    axes[0, 1].set_title('文字区域检测\n(避开采样)')
    axes[0, 1].axis('off')
    
    # 3. 边缘采样掩码
    axes[0, 2].imshow(edge_mask, cmap='gray')
    axes[0, 2].set_title('边缘采样区域\n(绿色区域)')
    axes[0, 2].axis('off')
    
    # 4. 采样区域叠加
    overlay = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).copy()
    overlay[edge_mask > 0] = [0, 255, 0]  # 绿色标记采样区域
    axes[0, 3].imshow(overlay)
    axes[0, 3].set_title('采样区域标记')
    axes[0, 3].axis('off')
    
    # 5. 颜色来源展示
    color_grid = np.zeros((100, 400, 3), dtype=np.uint8)
    
    source_names = ['基础色调', '边缘采样', '中心区域']
    for i, (color, name) in enumerate(zip(color_sources, source_names)):
        if i >= 3:  # 最多显示3个
            break
            
        block = np.ones((80, 80, 3), dtype=np.uint8)
        block[:] = color[::-1]  # BGR转RGB
        
        x_start = i * 120 + 20
        color_grid[10:90, x_start:x_start+80] = block
        
        # 添加名称
        cv2.putText(color_grid, name, (x_start, 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    axes[1, 0].imshow(color_grid)
    axes[1, 0].set_title('颜色来源')
    axes[1, 0].axis('off')
    
    # 6. 最终颜色
    final_block = np.ones((100, 100, 3), dtype=np.uint8)
    final_block[:] = final_color[::-1]
    
    axes[1, 1].imshow(final_block)
    
    # 计算颜色信息
    brightness = 0.299 * final_color[2] + 0.587 * final_color[1] + 0.114 * final_color[0]
    warmth = final_color[2] / max(final_color[0], 1)
    
    axes[1, 1].set_title(f'最终背景颜色\nRGB{final_color[::-1]}\n亮度: {brightness:.0f}\nR/B比: {warmth:.2f}')
    axes[1, 1].axis('off')
    
    # 7. 预览效果
    preview = np.ones_like(img)
    preview[:] = final_color
    
    # 提取文字
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    preview[thresh > 0] = img[thresh > 0]
    
    axes[1, 2].imshow(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB))
    axes[1, 2].set_title('背景应用预览')
    axes[1, 2].axis('off')
    
    # 8. 置信度信息
    info_text = f'检测结果\n\n'
    info_text += f'置信度: {confidence:.3f}\n\n'
    
    if confidence > 0.7:
        info_text += '✅ 高可信度\n'
        info_text += '颜色适合撕边书法'
        color = 'green'
    elif confidence > 0.5:
        info_text += '⚠️ 中等可信度\n'
        info_text += '颜色基本合理'
        color = 'orange'
    else:
        info_text += '❌ 低可信度\n'
        info_text += '建议手动调整'
        color = 'red'
    
    axes[1, 3].text(0.5, 0.5, info_text,
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=11,
                   color=color,
                   transform=axes[1, 3].transAxes)
    axes[1, 3].set_title('置信度评估')
    axes[1, 3].axis('off')
    
    plt.tight_layout()
    plt.show()

# 简单易用的主函数
def get_background_color_for_calligraphy(calligraphy_path, force_warm_color=True):
    """
    获取书法作品的背景颜色（简化版）
    
    参数:
    - force_warm_color: 强制使用暖色调（适合书法）
    
    返回:
    - background_color_rgb: RGB格式的背景颜色
    - confidence: 置信度
    """
    
    print(f"分析书法作品: {calligraphy_path}")
    
    # 读取图像
    img = cv2.imread(calligraphy_path)
    if img is None:
        print("无法读取图像")
        return (240, 230, 210), 0.0  # 返回宣纸色
    
    # 转换为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 方法1: 取最亮的5%像素的中值
    bright_threshold = np.percentile(gray, 95)
    bright_pixels = img[gray > bright_threshold]
    
    if len(bright_pixels) > 0:
        bg_color_bgr = np.median(bright_pixels, axis=0).astype(int)
    else:
        bg_color_bgr = np.array([255, 255, 255])
    
    # 转换为RGB
    bg_color_rgb = (int(bg_color_bgr[2]), int(bg_color_bgr[1]), int(bg_color_bgr[0]))
    
    # 强制暖色调（如果需要）
    if force_warm_color:
        # 检查是否是暖色调
        r, g, b = bg_color_rgb
        if r < max(g, b) + 20:  # 红色不是最突出的
            # 调整为宣纸色系
            paper_colors = [
                (240, 230, 210),  # 标准宣纸色
                (245, 240, 225),  # 亮宣纸色
                (235, 220, 200),  # 暗宣纸色
            ]
            
            # 选择最接近的宣纸色
            distances = []
            for paper_color in paper_colors:
                dist = np.sqrt((r-paper_color[0])**2 + (g-paper_color[1])**2 + (b-paper_color[2])**2)
                distances.append(dist)
            
            best_idx = np.argmin(distances)
            bg_color_rgb = paper_colors[best_idx]
    
    # 计算亮度
    brightness = 0.299 * bg_color_rgb[0] + 0.587 * bg_color_rgb[1] + 0.114 * bg_color_rgb[2]
    
    # 简单置信度计算
    if 180 <= brightness <= 230:
        confidence = 0.8
    elif 150 <= brightness < 180 or 230 < brightness <= 245:
        confidence = 0.6
    else:
        confidence = 0.4
    
    print(f"背景颜色: RGB{bg_color_rgb}")
    print(f"亮度: {brightness:.0f}")
    print(f"置信度: {confidence:.2f}")
    
    return bg_color_rgb, confidence

def get_dominant_color(image_path, k=3, background_threshold=0.3):
    """
    获取图像的主背景颜色
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("无法读取图像")
    
    # 转换为RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_shape = image_rgb.shape
    
    # 将图像展平为像素列表
    pixels = image.reshape(-1, 3)
    
    # 使用K-means聚类找到主要颜色
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # 获取聚类中心和标签
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    
    # 统计每个聚类的像素数量
    label_counts = Counter(labels)
    
    # 找到最大聚类（最可能是背景）
    dominant_label = label_counts.most_common(1)[0][0]
    dominant_color = colors[dominant_label]
    
    return dominant_color, colors, label_counts, image_shape

def visualize_colors(colors_bgr, label_counts, image_shape):
    """可视化检测到的颜色"""
    total_pixels = sum(label_counts.values())
    
    fig, axes = plt.subplots(1, len(colors_bgr) + 1, figsize=(15, 3))

    # 将BGR转换为RGB
    colors_rgb = [color_bgr[::-1] for color_bgr in colors_bgr]
    
    # 显示颜色块
    for i, (color, count) in enumerate(zip(colors_rgb, label_counts.values())):
        color_block = np.ones((100, 100, 3), dtype=np.uint8) * color
        axes[i].imshow(color_block)
        axes[i].axis('off')
        percentage = count / total_pixels * 100
        axes[i].set_title(f'Cluster {i}\n{color}\n{percentage:.1f}%')
    
    # 最后一个显示所有颜色
    all_colors = np.zeros((100, 300, 3), dtype=np.uint8)
    for i, color in enumerate(colors_rgb):
        all_colors[:, i*100:(i+1)*100] = color
    axes[-1].imshow(all_colors)
    axes[-1].axis('off')
    axes[-1].set_title('All Colors')
    
    plt.tight_layout()
    plt.show()

# 使用示例
# if __name__ == "__main__":
    # 方法1: 使用完整算法（推荐）
    # bg_color, confidence = detect_torn_edge_background_improved(
    #     "your_calligraphy.jpg",  # 你的书法作品
    #     debug=True
    # )
    
    # print(f"\n完整算法结果:")
    # print(f"背景颜色 (BGR): {bg_color}")
    # print(f"背景颜色 (RGB): {bg_color[::-1]}")
    # print(f"置信度: {confidence:.3f}")
    
    # 方法2: 使用简化版（快速）
    # bg_color_rgb, confidence = get_background_color_for_calligraphy(
    #     "your_calligraphy.jpg",
    #     force_warm_color=True  # 强制暖色调
    # )
    # 
    # print(f"\n简化版结果:")
    # print(f"背景颜色 (RGB): {bg_color_rgb}")
    # print(f"置信度: {confidence:.2f}")

# 使用示例
# if __name__ == "__main__":
    # # 测试撕边书法检测
    # bg_color, confidence = detect_torn_edge_background_no_skimage(
    #     "your_torn_calligraphy.jpg",  # 你的撕边书法作品
    #     debug=True
    # )
    
    # print(f"\n检测结果:")
    # print(f"背景颜色 (RGB): {BGR_to_RGB(bg_color)}")
    # print(f"置信度: {confidence:.3f}")
    
    # 如果需要合成
    # result, confidence = smart_insert_for_torn_edge(
    #     "transparent_template.png",
    #     "your_torn_calligraphy.jpg",
    #     "output_torn_edge.png",
    #     padding=30,
    #     debug=True
    # )

# 主程序
# if __name__ == "__main__":
    # 方法1: 使用保持比例的方法（推荐）
    # result = complete_workflow_with_proportion(
    #     scroll_template_path="blank_scroll.jpg",  # 空白卷轴模板
    #     calligraphy_path="calligraphy.jpg",       # 书法作品
    #     output_template_path="transparent_template.png",
    #     output_final_path="final_proportional.png",
    #     padding=30,  # 书法与边缘的间距
    #     debug=True
    # )
    
    # 方法2: 快速使用
    # quick_insert_with_proportion(
    #     "transparent_template.png",  # 透明模板
    #     "calligraphy.jpg",
    #     "quick_result.png",
    #     padding=30
    # )
    
    # 方法3: 测试所有模式
    # test_all_fit_modes(
    #     "transparent_template.png",
    #     "calligraphy.jpg",#
    #     "test_results"
    # )

# 使用示例
if __name__ == "__main__":
    scroll_image_template = "Frames/scroll_horizontal_green_black.png"
    calligraphy_image = "Frames/calligraphy_work_torn_edge.png"

    # 测试撕边书法检测
    # bg_color, confidence = detect_torn_edge_background_improved(
    #     scroll_image_template,  # 你的撕边书法作品
    #     debug=True
    # )

    # print(f"\n完整算法结果:")
    # print(f"背景颜色 (BGR): {bg_color}")
    # print(f"背景颜色 (RGB): {bg_color[::-1]}")
    # print(f"置信度: {confidence:.3f}")

    dominant_color, all_colors, label_counts, image_shape = get_dominant_color(calligraphy_image, k=3)
    
    print("\n📈 正在生成可视化结果...")
    visualize_colors(all_colors, label_counts, image_shape)
    
    # !!!这是 OpenCV的颜色通道顺序问题！OpenCV使用 BGR 格式（蓝、绿、红），而不是常见的 RGB 格式。
    # RGB格式的米黄色
    rgb_beige = dominant_color

    # 转换为BGR格式
    bgr_beige = (rgb_beige[2], rgb_beige[1], rgb_beige[0])  # BGR
    # 即 (210, 230, 240)

    # 使用
    uncovered_area_color = bgr_beige  # 或者直接写 (210, 230, 240)

    # 方法1: 自动检测（推荐）
    result = complete_workflow_with_proportion(
        scroll_template_path=scroll_image_template,  # 你的空白卷轴模板
        calligraphy_path=calligraphy_image,           # 你的书法作品
        output_template_path="transparent_template.png",   # 输出的透明模板
        output_final_path="final_composition.png",         # 最终合成作品
        padding=30,
        bg_color=uncovered_area_color,
        debug=True  # 设置为True查看处理过程
    )
    
    # 方法2: 简单手动指定（如果自动检测不好用）
    # simple_scroll_insertion(
    #     scroll_path="blank_scroll_template.jpg",
    #     calligraphy_path="calligraphy_work.jpg",
    #     output_path="simple_result.png"
    # )