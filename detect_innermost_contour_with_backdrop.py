import cv2
import numpy as np

def create_transparent_template_for_scroll_with_background(template_path, output_path=None, border_thickness=20, debug=False):
    """
    为带有背景图案的卷轴创建透明模板
    思路：找到矩形边框，让边框外部透明，边框内部保持不透明（保留水墨风景）
    """
    print(f"🎨 处理带背景图案的卷轴模板: {template_path}")
    
    # 1. 读取图像
    img = cv2.imread(template_path)
    if img is None:
        print("❌ 无法读取图像")
        return None, None
    
    height, width = img.shape[:2]
    print(f"📐 图像尺寸: {width}x{height}")
    
    # 2. 转换为RGBA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 3. 方法1：尝试检测矩形边框
    print("🔍 检测矩形边框...")
    border_mask = detect_scroll_border(img, border_thickness, debug)
    
    if border_mask is not None:
        print("✅ 成功检测到矩形边框")
        
        # 方法1A：使边框外部透明
        rgba[:, :, 3] = border_mask
        
    else:
        print("⚠️ 未检测到明显边框，使用自适应方法")
        
        # 方法2：边缘检测 + 矩形拟合
        border_mask = create_border_mask_adaptive(img, border_thickness)
        rgba[:, :, 3] = border_mask
    
    # 4. 保存结果
    if output_path:
        cv2.imwrite(output_path, rgba)
        print(f"💾 透明模板已保存: {output_path}")
    
    # 5. 调试显示
    if debug:
        show_scroll_debug_info(img, border_mask, rgba)
    
    return rgba, border_mask

def detect_scroll_border(img, border_thickness=20, debug=False):
    """
    检测卷轴的矩形边框
    """
    height, width = img.shape[:2]
    
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 使用Canny边缘检测
    edges = cv2.Canny(gray, 50, 150)
    
    # 膨胀边缘使其更连续
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # 寻找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # 找到最大的矩形轮廓
    largest_rect = None
    max_area = 0
    
    for contour in contours:
        # 近似多边形
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # 如果是四边形（矩形）
        if len(approx) == 4:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_rect = approx
    
    if largest_rect is None:
        return None
    
    # 创建掩码：矩形内部为白色（不透明），外部为黑色（透明）
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # 填充矩形
    cv2.drawContours(mask, [largest_rect], -1, 255, -1)
    
    # 稍微缩小矩形（确保边框本身也透明）
    if border_thickness > 0:
        # 创建稍小的矩形作为内部区域
        kernel = np.ones((border_thickness*2, border_thickness*2), np.uint8)
        inner_mask = cv2.erode(mask, kernel, iterations=1)
        
        # 边框区域设置为半透明或完全透明
        border_region = mask - inner_mask
        mask = inner_mask  # 只有内部区域完全不透明
    
    # 检查掩码是否合理
    mask_area = np.sum(mask == 255)
    total_area = height * width
    
    if mask_area / total_area < 0.1 or mask_area / total_area > 0.9:
        print(f"⚠️ 检测区域不合理: {mask_area/total_area:.1%}")
        return None
    
    return mask

def create_border_mask_adaptive(img, border_thickness=20):
    """
    自适应创建边框掩码
    """
    height, width = img.shape[:2]
    
    # 创建掩码：中心区域不透明，边缘透明
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # 计算中心区域（假设边框宽度为图像宽高的15%）
    h_border = int(height * 0.15)
    w_border = int(width * 0.15)
    
    # 内部区域（保留水墨风景）
    inner_top = h_border + border_thickness
    inner_bottom = height - h_border - border_thickness
    inner_left = w_border + border_thickness
    inner_right = width - w_border - border_thickness
    
    # 确保内部区域有效
    inner_top = max(inner_top, 0)
    inner_bottom = min(inner_bottom, height)
    inner_left = max(inner_left, 0)
    inner_right = min(inner_right, width)
    
    # 填充内部区域为白色（不透明）
    mask[inner_top:inner_bottom, inner_left:inner_right] = 255
    
    print(f"📐 内部区域: [{inner_top}:{inner_bottom}, {inner_left}:{inner_right}]")
    print(f"📊 透明边框占比: {(1 - (inner_bottom-inner_top)*(inner_right-inner_left)/(height*width)):.1%}")
    
    return mask

def show_scroll_debug_info(original, mask, result):
    """
    显示卷轴模板处理过程的调试信息
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 原始图像
    axes[0, 0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('原始卷轴模板')
    axes[0, 0].axis('off')
    
    # 灰度图
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    axes[0, 1].imshow(gray, cmap='gray')
    axes[0, 1].set_title('灰度图')
    axes[0, 1].axis('off')
    
    # 边缘检测
    edges = cv2.Canny(gray, 50, 150)
    axes[0, 2].imshow(edges, cmap='gray')
    axes[0, 2].set_title('边缘检测')
    axes[0, 2].axis('off')
    
    # 检测到的边框（掩码）
    axes[1, 0].imshow(mask, cmap='gray')
    white_pixels = np.sum(mask == 255)
    total_pixels = mask.shape[0] * mask.shape[1]
    axes[1, 0].set_title(f'边框掩码\n不透明区域: {white_pixels/total_pixels:.1%}')
    axes[1, 0].axis('off')
    
    # 叠加显示
    overlay = original.copy()
    overlay[mask == 255] = [0, 255, 0]  # 不透明区域标记为绿色
    axes[1, 1].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('不透明区域标记')
    axes[1, 1].axis('off')
    
    # 最终透明模板
    axes[1, 2].imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    axes[1, 2].set_title('透明模板')
    axes[1, 2].axis('off')
    
    plt.suptitle('卷轴模板处理过程', fontsize=16)
    plt.tight_layout()
    plt.show()

# 专门针对水平卷轴的优化版本
def process_horizontal_scroll_template(template_path, output_path=None, debug=False):
    """
    专门处理水平卷轴模板
    """
    print("🖼️ 处理水平卷轴模板")
    
    # 读取图像
    img = cv2.imread(template_path)
    if img is None:
        print("❌ 无法读取图像")
        return None, None
    
    height, width = img.shape[:2]
    
    # 判断是否为水平卷轴
    is_horizontal = width > height * 1.2  # 宽高比大于1.2
    print(f"📏 宽高比: {width/height:.2f} ({'水平' if is_horizontal else '垂直'})")
    
    # 转换为RGBA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 对于水平卷轴，通常左右边距较小，上下边距较大
    if is_horizontal:
        # 水平卷轴：上下边框较宽，左右边框较窄
        top_border = int(height * 0.10)    # 10%上边框
        bottom_border = int(height * 0.10) # 10%下边框
        left_border = int(width * 0.05)    # 5%左边框
        right_border = int(width * 0.05)   # 5%右边框
    else:
        # 垂直卷轴：左右边框较宽，上下边框较窄
        top_border = int(height * 0.05)    # 5%上边框
        bottom_border = int(height * 0.05) # 5%下边框
        left_border = int(width * 0.15)    # 15%左边框
        right_border = int(width * 0.15)   # 15%右边框
    
    # 创建掩码
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # 内部区域（保留水墨风景）
    inner_top = top_border
    inner_bottom = height - bottom_border
    inner_left = left_border
    inner_right = width - right_border
    
    # 确保有效
    inner_top = max(inner_top, 0)
    inner_bottom = min(inner_bottom, height)
    inner_left = max(inner_left, 0)
    inner_right = min(inner_right, width)
    
    mask[inner_top:inner_bottom, inner_left:inner_right] = 255
    
    print(f"📐 卷轴内部区域:")
    print(f"   上: {inner_top}, 下: {inner_bottom}")
    print(f"   左: {inner_left}, 右: {inner_right}")
    print(f"📊 内部区域占比: {(inner_bottom-inner_top)*(inner_right-inner_left)/(height*width):.1%}")
    
    # 应用透明度
    rgba[:, :, 3] = mask
    
    # 保存
    if output_path:
        cv2.imwrite(output_path, rgba)
        print(f"✅ 已保存: {output_path}")
    
    # 调试
    if debug:
        # 显示区域标记
        marked_img = img.copy()
        cv2.rectangle(marked_img, 
                     (inner_left, inner_top), 
                     (inner_right, inner_bottom),
                     (0, 255, 0), 3)
        
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axes[0].set_title('原始卷轴')
        axes[0].axis('off')
        
        axes[1].imshow(cv2.cvtColor(marked_img, cv2.COLOR_BGR2RGB))
        axes[1].set_title('内部区域标记')
        axes[1].axis('off')
        
        axes[2].imshow(cv2.cvtColor(rgba, cv2.COLOR_BGRA2RGBA))
        axes[2].set_title('透明模板')
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    return rgba, mask

# 使用示例
if __name__ == "__main__":
    # 方法1：通用处理
    template_path = "Frames/scroll_horizontal_green_black.png"
    output_path = "scroll_transparent.png"
    
    transparent_template, mask = create_transparent_template_for_scroll_with_background(
        template_path,
        output_path,
        border_thickness=15,
        debug=True  # 开启调试查看处理过程
    )
    
    # 方法2：专门针对水平卷轴
    # transparent_template, mask = process_horizontal_scroll_template(
    #     template_path,
    #     output_path,
    #     debug=True
    # )