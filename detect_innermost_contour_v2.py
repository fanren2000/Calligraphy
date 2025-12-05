

import cv2
import numpy as np

def find_inner_region_and_make_transparent_fixed(template_path, output_path=None, debug=False):
    """
    修复版：找到书法卷轴的内边缘区域并使其透明
    返回: (transparent_template, mask)
    """
    print(f"🔍 处理卷轴模板: {template_path}")
    
    # 1. 读取图像
    img = cv2.imread(template_path)
    if img is None:
        print(f"❌ 无法读取模板图像: {template_path}")
        # 创建默认返回值
        default_img = np.zeros((600, 800, 4), dtype=np.uint8)
        default_mask = np.zeros((600, 800), dtype=np.uint8)
        return default_img, default_mask
    
    print(f"✅ 成功读取图像，尺寸: {img.shape}")
    
    # 2. 转换为RGBA
    if img.shape[2] == 3:  # BGR
        rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    else:
        rgba = img.copy()
    
    height, width = rgba.shape[:2]
    
    # 3. 尝试多种方法找到内部区域
    mask = find_inner_region_robust(img, debug=debug)
    
    if mask is None:
        print("⚠️ 无法自动检测内部区域，使用默认区域")
        # 使用默认的内部区域（中央80%的区域）
        margin_h = int(height * 0.1)
        margin_w = int(width * 0.1)
        mask = np.zeros((height, width), dtype=np.uint8)
        mask[margin_h:height-margin_h, margin_w:width-margin_w] = 255
        
        if debug:
            print(f"使用默认区域: [{margin_h}:{height-margin_h}, {margin_w}:{width-margin_w}]")
    
    # 4. 应用透明度
    rgba[:, :, 3] = mask
    
    # 5. 保存结果
    if output_path:
        cv2.imwrite(output_path, rgba)
        print(f"✅ 已保存透明模板: {output_path}")
    
    # 6. 调试显示
    if debug:
        show_debug_info(img, mask, rgba)
    
    return rgba, mask

def find_inner_region_robust(img, debug=False):
    """
    鲁棒地找到内部区域（多种方法）
    """
    height, width = img.shape[:2]
    
    # 方法1: 基于颜色阈值
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 尝试自适应阈值
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
    
    # 寻找轮廓
    contours, _ = cv2.findContours(adaptive_thresh, 
                                  cv2.RETR_EXTERNAL, 
                                  cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # 找到最大的轮廓
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 创建掩码
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [largest_contour], -1, 255, -1)
        
        # 检查掩码是否合理
        mask_area = np.sum(mask == 255)
        total_area = height * width
        
        if 0.1 < mask_area / total_area < 0.9:  # 合理的区域大小
            print(f"✅ 方法1成功: 找到内部区域 ({mask_area/total_area:.1%})")
            return mask
    
    # 方法2: 基于边缘检测
    edges = cv2.Canny(gray, 50, 150)
    
    # 膨胀边缘
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=3)
    
    # 反转：内部为白色
    mask = cv2.bitwise_not(dilated)
    
    # 清理小区域
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 填充孔洞
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    mask_area = np.sum(mask == 255)
    total_area = height * width
    
    if 0.1 < mask_area / total_area < 0.9:
        print(f"✅ 方法2成功: 找到内部区域 ({mask_area/total_area:.1%})")
        return mask
    
    # 方法3: 简单矩形区域（最后的手段）
    print("⚠️ 所有自动方法失败，使用预设区域")
    return None

def show_debug_info(original, mask, result):
    """
    显示调试信息
    """
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    
    # 原始图像
    axes[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0].set_title('原始模板')
    axes[0].axis('off')
    
    # 灰度图
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    axes[1].imshow(gray, cmap='gray')
    axes[1].set_title('灰度图')
    axes[1].axis('off')
    
    # 检测到的掩码
    axes[2].imshow(mask, cmap='gray')
    axes[2].set_title(f'内部区域掩码\n白色区域: {np.sum(mask==255)/mask.size:.1%}')
    axes[2].axis('off')
    
    # 最终结果（带透明度）
    axes[3].imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    axes[3].set_title('透明模板')
    axes[3].axis('off')
    
    plt.tight_layout()
    plt.show()

# 使用修复版函数
scroll_template_path = "Source/scroll_horizontal_green_black.png"
output_template_path = "transparent_template_v2.png"
transparent_template, mask = find_inner_region_and_make_transparent_fixed(
    scroll_template_path,
    output_template_path,
    debug=True  # 开启调试查看过程
)