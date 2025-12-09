import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

def create_scroll_template_correct_coords(image_path, output_path, inner_top, inner_bottom, inner_left, inner_right, transparency_level=128, bg_color = (255, 255, 255, 255)):
    """
    使用正确的坐标参数创建卷轴模板
    
    参数:
        image_path: 卷轴图像路径
        output_path: 输出路径
        inner_top: 内部区域上边界Y坐标
        inner_bottom: 内部区域下边界Y坐标
        inner_left: 内部区域左边界X坐标
        inner_right: 内部区域右边界X坐标
        transparency_level: 内部区域透明度
    """
    print("🎨 使用坐标参数创建卷轴模板...")
    
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(f"❌ 无法读取图像: {image_path}")
        return None, None
    
    print(f"   形状: {img.shape}")
    print(f"   类型: {img.dtype}")
    print(f"   通道: {img.shape[2] if len(img.shape) > 2 else 1}")

    # 根据通道数处理
    if len(img.shape) == 2:  # 灰度
        print("🎨 处理灰度图像...")
        # 灰度 -> BGR -> BGRA
        bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        rgba = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    elif img.shape[2] == 3:  # BGR
        print("🎨 处理BGR图像...")
        # BGR -> BGRA
        rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    elif img.shape[2] == 4:  # BGRA
        print("🎨 处理BGRA图像...")
        rgba = img.copy()  # 直接复制，不转换
    else:
        print(f"❌ 不支持的通道数: {img.shape[2]}")
        return None
    
    print(f"✅ 处理后: {rgba.shape}")
    
    # 4. 获取坐标
    height, width = rgba.shape[:2]
    
    print(f"\n📏 请输入内部区域坐标:")
    print(f"   图像尺寸: {width}x{height}")
    print(f"   有效范围: 0 ≤ top < bottom ≤ {height}, 0 ≤ left < right ≤ {width}")
    
    # 验证坐标
    if not (0 <= inner_top < inner_bottom <= height and 0 <= inner_left < inner_right <= width):
        print(f"❌ 坐标无效:")
        print(f"   需要: 0 <= top < bottom <= {height}")
        print(f"         0 <= left < right <= {width}")
        print(f"   实际: top={inner_top}, bottom={inner_bottom}, left={inner_left}, right={inner_right}")
        return None, None
    
    # 计算边框厚度
    border_top = inner_top  # 上边框厚度 = 内部区域上边界Y坐标
    border_bottom = height - inner_bottom  # 下边框厚度 = 图像高度 - 内部区域下边界Y坐标
    border_left = inner_left  # 左边框厚度 = 内部区域左边界X坐标
    border_right = width - inner_right  # 右边框厚度 = 图像宽度 - 内部区域右边界X坐标
    
    print(f"\n📏 计算出的边框厚度:")
    print(f"   上边框: {border_top}px")
    print(f"   下边框: {border_bottom}px")
    print(f"   左边框: {border_left}px")
    print(f"   右边框: {border_right}px")

    # 计算内部区域信息
    inner_height = inner_bottom - inner_top
    inner_width = inner_right - inner_left

    if bg_color != None:
        calligraphy_bg = np.full((inner_height, inner_width, 4), bg_color, dtype=np.uint8)
        rgba[inner_top:inner_bottom, inner_left:inner_right] = calligraphy_bg
    
    
    # 创建透明度掩码 & 获取alpha通道的引用
    alpha = rgba[:, :, 3]
    
    # 设置内部区域为半透明
    alpha[inner_top:inner_bottom, inner_left:inner_right] =  transparency_level
    
    # 应用透明度
    rgba[:, :, 3] = alpha
    
    
    
    print(f"\n🎨 内部透明区域:")
    print(f"   坐标范围: y={inner_top}~{inner_bottom}, x={inner_left}~{inner_right}")
    print(f"   尺寸: {inner_width}x{inner_height}")
    print(f"   透明度: {transparency_level}/255 ({transparency_level/255:.0%})")
    print(f"   面积占比: {inner_width*inner_height/(width*height):.1%}")
    
    # 保存结果
    if output_path:
        cv2.imwrite(output_path, cv2.cvtColor(rgba, cv2.COLOR_BGR2BGRA))
        print(f"\n✅ 模板已保存: {output_path}")
    
    # 可视化
    visualize_with_coordinates(img, rgba, alpha, inner_top, inner_bottom, inner_left, inner_right, transparency_level)
    
    return rgba, alpha

def visualize_with_coordinates(original, result, alpha, inner_top, inner_bottom, inner_left, inner_right, transparency_level):
    """使用坐标可视化"""
    height, width = original.shape[:2]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 原始图像 + 坐标标记
    marked_img = original.copy()
    
    # 绘制内部区域边界
    cv2.rectangle(marked_img, (inner_left, inner_top), (inner_right, inner_bottom), (0, 255, 0), 3)
    
    # 标记坐标点
    # 左上角
    cv2.circle(marked_img, (inner_left, inner_top), 10, (255, 0, 0), -1)
    cv2.putText(marked_img, f'({inner_left},{inner_top})', 
               (inner_left + 15, inner_top - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    
    # 右下角
    cv2.circle(marked_img, (inner_right, inner_bottom), 10, (0, 0, 255), -1)
    cv2.putText(marked_img, f'({inner_right},{inner_bottom})', 
               (inner_right - 100, inner_bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # 添加尺寸标注
    cv2.line(marked_img, (inner_left, inner_top-50), (inner_right, inner_top-50), (255, 255, 0), 2)
    cv2.putText(marked_img, f'宽度: {inner_right-inner_left}px', 
               ((inner_left+inner_right)//2 - 80, inner_top-60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    cv2.line(marked_img, (inner_left-50, inner_top), (inner_left-50, inner_bottom), (255, 255, 0), 2)
    cv2.putText(marked_img, f'高度: {inner_bottom-inner_top}px', 
               (inner_left-150, (inner_top+inner_bottom)//2), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    axes[0].imshow(cv2.cvtColor(marked_img, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f'内部区域坐标标记\n左上:({inner_left},{inner_top}), 右下:({inner_right},{inner_bottom})')
    axes[0].axis('off')
    
    # 透明度通道
    axes[1].imshow(alpha, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title(f'透明度通道\n边框:255, 内部:{transparency_level}')
    axes[1].axis('off')
    
    # 最终效果
    axes[2].imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    axes[2].set_title('透明模板效果')
    axes[2].axis('off')
    
    plt.suptitle('卷轴模板 - 基于坐标参数', fontsize=14)
    plt.tight_layout()
    plt.show()

# 交互式坐标选择工具
def interactive_coordinate_selector(image_path):
    """交互式选择内部区域坐标"""
    print("🖱️ 交互式坐标选择工具")
    print("=" * 50)
    
    img = cv2.imread(image_path)
    if img is None:
        print("❌ 无法读取图像")
        return None
    
    height, width = img.shape[:2]
    
    # 使用matplotlib交互功能
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.set_title(f'点击选择内部区域\n当前: 无选择 | 图像: {width}x{height}')
    ax.axis('off')
    
    # 存储点击坐标
    clicks = []
    
    def on_click(event):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            clicks.append((x, y))
            
            # 绘制点击点
            ax.plot(x, y, 'ro', markersize=8)
            
            if len(clicks) == 1:
                ax.set_title(f'点击选择内部区域\n已选择左上角: ({x},{y}) | 图像: {width}x{height}')
                plt.draw()
            elif len(clicks) == 2:
                x1, y1 = clicks[0]
                x2, y2 = clicks[1]
                
                # 确保左上角和右下角
                inner_left = min(x1, x2)
                inner_right = max(x1, x2)
                inner_top = min(y1, y2)
                inner_bottom = max(y1, y2)
                
                # 绘制矩形
                rect = plt.Rectangle((inner_left, inner_top), 
                                     inner_right-inner_left, 
                                     inner_bottom-inner_top,
                                     linewidth=2, edgecolor='green', facecolor='none')
                ax.add_patch(rect)
                
                ax.set_title(f'内部区域已选择\n左上:({inner_left},{inner_top}) 右下:({inner_right},{inner_bottom})\n尺寸: {inner_right-inner_left}x{inner_bottom-inner_top}')
                plt.draw()
                
                # 询问是否确认
                print(f"\n📏 选择的内部区域:")
                print(f"   左上角: ({inner_left}, {inner_top})")
                print(f"   右下角: ({inner_right}, {inner_bottom})")
                print(f"   宽度: {inner_right-inner_left}px")
                print(f"   高度: {inner_bottom-inner_top}px")
                
                confirm = input("\n确认使用这些坐标吗？(y/n): ")
                if confirm.lower() == 'y':
                    plt.close()
                    return inner_top, inner_bottom, inner_left, inner_right
                else:
                    # 重新开始
                    clicks.clear()
                    ax.clear()
                    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    ax.set_title(f'重新选择内部区域\n图像: {width}x{height}')
                    ax.axis('off')
                    plt.draw()
    
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()
    
    if len(clicks) >= 2:
        x1, y1 = clicks[0]
        x2, y2 = clicks[1]
        return min(y1, y2), max(y1, y2), min(x1, x2), max(x1, x2)
    
    return None

def embed_calligraphy_in_scroll(scroll_path, calligraphy_path, output_path, 
                                inner_top, inner_bottom, inner_left, inner_right,
                                scroll_area_trans_level=128,
                                calligraphy_opacity=1.0, blend_mode='normal',
                                calligraphy_margin=20, debug=False):
    """
    将书法作品嵌入卷轴中间透明区域
    
    参数:
        scroll_path: 卷轴图像路径
        calligraphy_path: 书法图像路径
        output_path: 输出路径
        inner_top, inner_bottom, inner_left, inner_right: 卷轴内部区域坐标
        calligraphy_opacity: 书法不透明度 (0.0-1.0)
        blend_mode: 混合模式
        calligraphy_margin: 书法距内部区域边缘的边距
        debug: 是否显示调试信息
    """
    print("=" * 60)
    print("🖼️ 书法卷轴融合")
    print("=" * 60)
    
    # 1. 创建卷轴模板
    print("\n步骤1: 创建卷轴模板")
    scroll_template_transparent = "scroll_template_transpare.png"
    scroll_template, alpha = create_scroll_template_correct_coords(
        scroll_path,
        scroll_template_transparent,
        inner_top, inner_bottom, inner_left, inner_right,
        transparency_level=scroll_area_trans_level,  # 卷轴内部50%透明
        bg_color=None
    )
    # img = cv2.imread(scroll_path)
    #  # 根据通道数处理
    # if len(img.shape) == 2:  # 灰度
    #     print("🎨 处理灰度图像...")
    #     # 灰度 -> BGR -> BGRA
    #     bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #     rgba = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    # elif img.shape[2] == 3:  # BGR
    #     print("🎨 处理BGR图像...")
    #     # BGR -> BGRA
    #     rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    # elif img.shape[2] == 4:  # BGRA
    #     print("🎨 处理BGRA图像...")
    #     rgba = img.copy()  # 直接复制，不转换
    # else:
    #     print(f"❌ 不支持的通道数: {img.shape[2]}")
    #     return None
    
    # print(f"✅ 处理后: {rgba.shape}")

    # scroll_template = rgba
    
    if scroll_template is None:
        print("❌ 卷轴模板创建失败")
        return None
    
    # 2. 准备书法图像
    print("\n步骤2: 准备书法图像")
    
    # 计算可用于书法的区域（减去边距）
    calligraphy_area_width = (inner_right - inner_left) - 2 * calligraphy_margin
    calligraphy_area_height = (inner_bottom - inner_top) - 2 * calligraphy_margin
    # calligraphy_area_width: 1872 - 589 - 2 * 1 = 1281
    
    if calligraphy_area_width <= 0 or calligraphy_area_height <= 0:
        print(f"❌ 书法区域太小: {calligraphy_area_width}x{calligraphy_area_height}")
        return None
    
    calligraphy_prepared = safe_resize_rgba_image(
        calligraphy_path,
        calligraphy_area_width,
        calligraphy_area_height
    )
    
    if calligraphy_prepared is None:
        print("❌ 书法图像准备失败")
        return None
    
    # 3. 将书法放置在卷轴内部区域
    print("\n步骤3: 融合书法与卷轴")
    
    # 创建结果图像
    result = scroll_template.copy()
    
    # 计算书法放置位置（居中）
    calligraphy_height, calligraphy_width = calligraphy_prepared.shape[:2]
    
    calligraphy_y = inner_top + calligraphy_margin + (calligraphy_area_height - calligraphy_height) // 2
    calligraphy_x = inner_left + calligraphy_margin + (calligraphy_area_width - calligraphy_width) // 2

    # calligraphy_x: 589 + 1 + (1281 - 1278) // 2 = 591
    
    print(f"   书法放置位置: x={calligraphy_x}, y={calligraphy_y}")
    print(f"   书法尺寸: {calligraphy_width}x{calligraphy_height}")
    
    # 提取卷轴内部区域
    scroll_inner_region = result[calligraphy_y:calligraphy_y+calligraphy_height, 
                                 calligraphy_x:calligraphy_x+calligraphy_width]
    
    # 混合书法和卷轴
    blended_region = blend_images(
        scroll_inner_region,
        calligraphy_prepared,
        blend_mode=blend_mode,
        opacity=calligraphy_opacity
    )
    
    # 放回结果图像
    result[calligraphy_y:calligraphy_y+calligraphy_height, 
           calligraphy_x:calligraphy_x+calligraphy_width] = blended_region
    
    # 4. 保存结果
    print("\n步骤4: 保存结果")
    cv2.imwrite(output_path, result)
    print(f"✅ 融合完成: {output_path}")
    
    # 5. 显示结果（如果开启调试）
    if debug:
        show_fusion_result(scroll_template, calligraphy_prepared, result, 
                          calligraphy_x, calligraphy_y, inner_top, inner_bottom, inner_left, inner_right)
    
    return result

def create_transparent_scroll_template(image_path, inner_top, inner_bottom, inner_left, inner_right, transparency_level=128):
    """
    创建内部透明的卷轴模板
    
    参数:
        image_path: 卷轴图像路径
        inner_top, inner_bottom, inner_left, inner_right: 内部区域坐标
        transparency_level: 内部区域透明度 (0-255)
    """
    print("🎨 创建卷轴模板...")
    
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ 无法读取卷轴图像: {image_path}")
        return None
    
    height, width = img.shape[:2]
    
    # 验证坐标
    if not (0 <= inner_top < inner_bottom <= height and 0 <= inner_left < inner_right <= width):
        print(f"❌ 坐标无效: top={inner_top}, bottom={inner_bottom}, left={inner_left}, right={inner_right}")
        return None
    
    # 转换为RGBA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 创建透明度掩码
    alpha = np.ones((height, width), dtype=np.uint8) * 255
    
    # 设置内部区域为半透明
    alpha[inner_top:inner_bottom, inner_left:inner_right] = transparency_level
    rgba[:, :, 3] = alpha
    
    print(f"✅ 卷轴模板创建完成")
    print(f"   内部透明区域: {inner_right-inner_left}x{inner_bottom-inner_top}")
    print(f"   透明度: {transparency_level}/255 ({transparency_level/255:.0%})")
    
    return rgba


def prepare_calligraphy_image(calligraphy_path, target_width, target_height):
    """
    准备书法图像：调整大小、去除背景等
    
    参数:
        calligraphy_path: 书法图像路径
        target_width, target_height: 目标尺寸
    """
    print("🖌️ 准备书法图像...")
    
    # 读取书法图像
    calligraphy = cv2.imread(calligraphy_path, cv2.IMREAD_UNCHANGED)
    if calligraphy is None:
        print(f"❌ 无法读取书法图像: {calligraphy_path}")
        return None
    
    print(f"   原始尺寸: {calligraphy.shape[1]}x{calligraphy.shape[0]}")
    
    # 如果是RGBA图像（已有透明度），直接使用
    if calligraphy.shape[2] == 4:
        print("   ✅ 书法图像已有透明度通道")
        calligraphy_rgba = calligraphy
    else:
        # 如果是RGB图像，转换为RGBA（完全不透明）
        print("   🔄 转换为RGBA格式")
        calligraphy_rgba = cv2.cvtColor(calligraphy, cv2.COLOR_BGR2BGRA)
    
    # 调整大小以适应目标区域（保持宽高比）
    h, w = calligraphy_rgba.shape[:2]
    
    # 计算缩放比例
    scale = max(target_width / w, target_height / h)
    new_width = int(w * scale)
    new_height = int(h * scale)
    
    print(f"   调整后尺寸: {new_width}x{new_height} (缩放比例: {scale:.2f})")
    
    # 调整大小
    if scale != 1.0:
        calligraphy_resized = cv2.resize(calligraphy_rgba, (new_width, new_height), interpolation=cv2.INTER_AREA)
    else:
        calligraphy_resized = calligraphy_rgba
    
    return calligraphy_resized

def blend_images(background, foreground, blend_mode='normal', opacity=1.0):
    """
    混合两个图像
    
    参数:
        background: 背景图像 (RGBA)
        foreground: 前景图像 (RGBA)
        blend_mode: 混合模式 ('normal', 'multiply', 'screen', 'overlay')
        opacity: 前景不透明度 (0.0-1.0)
    """
    # 分离通道
    bg_rgb = background[:, :, :3]
    bg_alpha = background[:, :, 3] / 255.0
    
    fg_rgb = foreground[:, :, :3]
    fg_alpha = foreground[:, :, 3] / 255.0 * opacity
    
    # 扩展alpha通道
    fg_alpha_expanded = np.stack([fg_alpha, fg_alpha, fg_alpha], axis=2)
    
    # 根据混合模式混合
    if blend_mode == 'normal':
        blended_rgb = fg_rgb * fg_alpha_expanded + bg_rgb * (1 - fg_alpha_expanded)
    elif blend_mode == 'multiply':
        blended_rgb = bg_rgb * fg_rgb / 255.0 * fg_alpha_expanded + bg_rgb * (1 - fg_alpha_expanded)
    elif blend_mode == 'screen':
        blended_rgb = (1 - (1 - bg_rgb/255.0) * (1 - fg_rgb/255.0)) * 255 * fg_alpha_expanded + bg_rgb * (1 - fg_alpha_expanded)
    elif blend_mode == 'overlay':
        mask = bg_rgb < 128
        blended_rgb = np.zeros_like(bg_rgb)
        blended_rgb[mask] = (2 * bg_rgb[mask] * fg_rgb[mask] / 255.0)
        blended_rgb[~mask] = (255 - 2 * (255 - bg_rgb[~mask]) * (255 - fg_rgb[~mask]) / 255.0)
        blended_rgb = blended_rgb * fg_alpha_expanded + bg_rgb * (1 - fg_alpha_expanded)
    else:
        blended_rgb = fg_rgb * fg_alpha_expanded + bg_rgb * (1 - fg_alpha_expanded)
    
    # 合并alpha通道
    result_alpha = np.clip(bg_alpha + fg_alpha * (1 - bg_alpha), 0, 1)
    
    # 组合结果
    result = np.zeros((background.shape[0], background.shape[1], 4), dtype=np.uint8)
    result[:, :, :3] = blended_rgb.astype(np.uint8)
    result[:, :, 3] = (result_alpha * 255).astype(np.uint8)
    
    return result

def show_fusion_result(scroll_template, calligraphy, result, 
                       calligraphy_x, calligraphy_y, inner_top, inner_bottom, inner_left, inner_right):
    """显示融合结果"""
    print("\n📊 显示融合结果...")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 卷轴模板
    axes[0, 0].imshow(cv2.cvtColor(scroll_template, cv2.COLOR_BGRA2RGBA))
    axes[0, 0].set_title('卷轴模板\n(内部透明)')
    axes[0, 0].axis('off')
    
    # 书法图像
    axes[0, 1].imshow(cv2.cvtColor(calligraphy, cv2.COLOR_BGRA2RGBA))
    axes[0, 1].set_title(f'书法图像\n{calligraphy.shape[1]}x{calligraphy.shape[0]}')
    axes[0, 1].axis('off')
    
    # 最终结果
    axes[0, 2].imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    axes[0, 2].set_title('融合结果')
    axes[0, 2].axis('off')
    
    # 融合细节
    detail_size = 300
    detail_y = max(0, calligraphy_y - 50)
    detail_x = max(0, calligraphy_x - 50)
    
    detail_region = result[detail_y:min(result.shape[0], detail_y+detail_size),
                          detail_x:min(result.shape[1], detail_x+detail_size)]
    
    axes[1, 0].imshow(cv2.cvtColor(detail_region, cv2.COLOR_BGRA2RGBA))
    axes[1, 0].set_title('融合细节')
    axes[1, 0].axis('off')
    
    # 显示坐标标记
    marked_result = result.copy()
    
    # 标记卷轴内部区域
    cv2.rectangle(marked_result, (inner_left, inner_top), (inner_right, inner_bottom), 
                 (0, 255, 0, 255), 3)
    
    # 标记书法区域
    cv2.rectangle(marked_result, (calligraphy_x, calligraphy_y), 
                 (calligraphy_x+calligraphy.shape[1], calligraphy_y+calligraphy.shape[0]), 
                 (255, 0, 0, 255), 2)
    
    axes[1, 1].imshow(cv2.cvtColor(marked_result, cv2.COLOR_BGRA2RGBA))
    axes[1, 1].set_title('区域标记\n绿色:卷轴内部, 蓝色:书法')
    axes[1, 1].axis('off')
    
    # 添加文字说明
    axes[1, 2].axis('off')
    info_text = f"""
                    融合参数:
                    卷轴内部区域:
                    坐标: ({inner_left}, {inner_top}) - ({inner_right}, {inner_bottom})
                    尺寸: {inner_right-inner_left}x{inner_bottom-inner_top}

                    书法图像:
                    位置: ({calligraphy_x}, {calligraphy_y})
                    尺寸: {calligraphy.shape[1]}x{calligraphy.shape[0]}

                    融合效果:
                    书法与卷轴风景自然融合
                    保留卷轴边框完整性
                    文字透过透明区域显示
                    """
    axes[1, 2].text(0.05, 0.95, info_text, fontsize=9, 
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.suptitle('书法卷轴融合结果', fontsize=16, y=0.98)
    plt.tight_layout()
    plt.show()

def safe_resize_rgba_image(calligraphy_path, target_width, target_height):
    """
    安全地调整RGBA图像大小
    """
    # 读取书法图像
    image_rgba = cv2.imread(calligraphy_path, cv2.IMREAD_UNCHANGED)

    # 去掉四周透明边
    image_rgba = crop_image_by_border_length(image_rgba, 20, 20, 20, 20)

    # 1. 验证输入
    if image_rgba is None:
        print("❌ 输入图像为空")
        return None
    
    if target_width <= 0 or target_height <= 0:
        print(f"❌ 目标尺寸无效: {target_width}x{target_height}")
        return None
    
    # 获取原始尺寸
    original_height, original_width = image_rgba.shape[:2]
    
    print(f"📏 调整尺寸: {original_width}x{original_height} -> {target_width}x{target_height}")
    
    # 2. 根据是放大还是缩小选择合适的插值方法
    if target_width < original_width or target_height < original_height:
        # 缩小图像：使用INTER_AREA（保持锐利边缘）
        interpolation = cv2.INTER_AREA
        print("  模式: 缩小 (使用INTER_AREA)")
    else:
        # 放大图像：使用INTER_CUBIC或INTER_LINEAR
        interpolation = cv2.INTER_CUBIC  # 或INTER_LANCZOS4，质量更好但更慢
        print("  模式: 放大 (使用INTER_CUBIC)")
    
    # 3. 确保目标尺寸是整数
    target_width = int(round(target_width))
    target_height = int(round(target_height))
    
    # 4. 确保最小尺寸
    if target_width < 1 or target_height < 1:
        print(f"⚠️  目标尺寸太小，调整为最小值")
        target_width = max(1, target_width)
        target_height = max(1, target_height)
    
    try:
        # 5. 调整大小
        resized = cv2.resize(
            image_rgba, 
            (target_width, target_height), 
            interpolation=interpolation
        )
        
        print(f"✅ 调整成功: {target_width}x{target_height}")
        return resized
        
    except Exception as e:
        print(f"❌ 调整大小失败: {e}")
        return None
    


def crop_image_by_border_length(image, top_len, bottom_len, left_len, right_len):
    """
    根据边框长度裁剪图像
    
    参数:
        image: 输入图像 (numpy数组或文件路径)
        top_len: 上边裁剪长度 (从顶部去掉的像素数)
        bottom_len: 下边裁剪长度 (从底部去掉的像素数)
        left_len: 左边裁剪长度 (从左边去掉的像素数)
        right_len: 右边裁剪长度 (从右边去掉的像素数)
    
    返回:
        cropped_image: 裁剪后的图像
    
    示例:
        # 从每边裁剪50像素
        cropped = crop_image_by_border_length(img, 50, 50, 50, 50)
        
        # 只裁剪上边和左边
        cropped = crop_image_by_border_length(img, 100, 0, 100, 0)
    """
    print("✂️ 按边框长度裁剪图像...")
    
    # 1. 处理输入：支持文件路径或图像数据
    if isinstance(image, str):
        # 输入是文件路径
        print(f"📁 读取图像: {image}")
        img = cv2.imread(image)
        if img is None:
            print(f"❌ 无法读取图像: {image}")
            return None
    elif isinstance(image, np.ndarray):
        # 输入已经是图像数据
        img = image.copy()  # 创建副本以避免修改原始图像
        print("✅ 使用提供的图像数据")
    else:
        print(f"❌ 不支持的输入类型: {type(image)}")
        return None
    
    # 2. 获取图像尺寸
    original_height, original_width = img.shape[:2]
    print(f"📐 原始图像尺寸: {original_width}x{original_height}")
    
    # 3. 验证和转换参数
    # 确保参数是非负整数
    try:
        top_len = int(top_len)
        bottom_len = int(bottom_len)
        left_len = int(left_len)
        right_len = int(right_len)
    except (ValueError, TypeError):
        print("❌ 裁剪长度必须是数字")
        return None
    
    # 确保非负
    if any(length < 0 for length in [top_len, bottom_len, left_len, right_len]):
        print("❌ 裁剪长度不能为负数")
        return None
    
    print(f"📏 裁剪长度设置:")
    print(f"  上边: {top_len}像素")
    print(f"  下边: {bottom_len}像素")
    print(f"  左边: {left_len}像素")
    print(f"  右边: {right_len}像素")
    
    # 4. 计算裁剪区域
    new_top = top_len
    new_bottom = original_height - bottom_len
    new_left = left_len
    new_right = original_width - right_len
    
    print(f"🔍 计算裁剪区域:")
    print(f"  原始范围: y=[0:{original_height}], x=[0:{original_width}]")
    print(f"  新范围: y=[{new_top}:{new_bottom}], x=[{new_left}:{new_right}]")
    
    # 5. 验证裁剪区域有效性
    if new_top >= new_bottom:
        print(f"❌ 垂直裁剪过多: {top_len}+{bottom_len} >= {original_height}")
        print(f"   剩余高度: {new_bottom - new_top} (应为正数)")
        return None
    
    if new_left >= new_right:
        print(f"❌ 水平裁剪过多: {left_len}+{right_len} >= {original_width}")
        print(f"   剩余宽度: {new_right - new_left} (应为正数)")
        return None
    
    # 6. 计算新尺寸
    new_height = new_bottom - new_top
    new_width = new_right - new_left
    
    print(f"📏 裁剪后尺寸: {new_width}x{new_height}")
    print(f"📊 占原图比例: {new_width/original_width:.1%} x {new_height/original_height:.1%}")
    
    # 7. 显示裁剪信息
    total_cropped_h = top_len + bottom_len
    total_cropped_w = left_len + right_len
    print(f"📊 总计裁剪:")
    print(f"  垂直裁剪: {total_cropped_h}像素 ({total_cropped_h/original_height:.1%})")
    print(f"  水平裁剪: {total_cropped_w}像素 ({total_cropped_w/original_width:.1%})")
    
    # 8. 执行裁剪
    try:
        # 使用numpy数组切片：img[y_start:y_end, x_start:x_end]
        cropped = img[new_top:new_bottom, new_left:new_right]
        
        print(f"✅ 裁剪成功: {cropped.shape[1]}x{cropped.shape[0]}")
        
        return cropped
        
    except Exception as e:
        print(f"❌ 裁剪失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def crop_with_auto_adjustment(image, top_len, bottom_len, left_len, right_len, min_size=50):
    """
    自动调整裁剪版本：确保最小尺寸
    """
    print("🔄 自动调整裁剪...")
    
    if isinstance(image, str):
        img = cv2.imread(image)
    elif isinstance(image, np.ndarray):
        img = image.copy()
    else:
        return None
    
    if img is None:
        return None
    
    original_height, original_width = img.shape[:2]
    
    # 自动调整裁剪长度
    adjusted_top = min(top_len, original_height - min_size)
    adjusted_bottom = min(bottom_len, original_height - min_size - adjusted_top)
    adjusted_left = min(left_len, original_width - min_size)
    adjusted_right = min(right_len, original_width - min_size - adjusted_left)
    
    print(f"🔧 自动调整:")
    print(f"  上边: {top_len} -> {adjusted_top}")
    print(f"  下边: {bottom_len} -> {adjusted_bottom}")
    print(f"  左边: {left_len} -> {adjusted_left}")
    print(f"  右边: {right_len} -> {adjusted_right}")
    
    # 调用基础函数
    return crop_image_by_border_length(img, adjusted_top, adjusted_bottom, adjusted_left, adjusted_right)

def crop_and_show_comparison(image, top_len, bottom_len, left_len, right_len):
    """
    裁剪并显示对比
    """
    import matplotlib.pyplot as plt
    
    # 读取或复制图像
    if isinstance(image, str):
        original = cv2.imread(image)
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    elif isinstance(image, np.ndarray):
        original = image.copy()
        if len(original.shape) == 3 and original.shape[2] == 3:
            original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        else:
            original_rgb = original
    else:
        return None
    
    # 裁剪
    cropped = crop_image_by_border_length(image, top_len, bottom_len, left_len, right_len)
    
    if cropped is None:
        return None
    
    # 转换颜色用于显示
    if len(cropped.shape) == 3 and cropped.shape[2] == 3:
        cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    else:
        cropped_rgb = cropped
    
    # 创建对比图
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 原始图像
    axes[0].imshow(original_rgb)
    axes[0].set_title(f'原始图像\n{original_rgb.shape[1]}x{original_rgb.shape[0]}')
    axes[0].axis('off')
    
    # 裁剪标记图
    marked = original_rgb.copy()
    h, w = original_rgb.shape[:2]
    
    # 绘制裁剪线
    cv2.line(marked, (left_len, 0), (left_len, h), (255, 0, 0), 2)
    cv2.line(marked, (w - right_len, 0), (w - right_len, h), (255, 0, 0), 2)
    cv2.line(marked, (0, top_len), (w, top_len), (0, 255, 0), 2)
    cv2.line(marked, (0, h - bottom_len), (w, h - bottom_len), (0, 255, 0), 2)
    
    # 添加文字
    cv2.putText(marked, f'Top: {top_len}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(marked, f'Bottom: {bottom_len}', (10, h - 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(marked, f'Left: {left_len}', (10, h//2), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(marked, f'Right: {right_len}', (w - 120, h//2), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    axes[1].imshow(marked)
    axes[1].set_title('裁剪标记\n蓝色:左右边界, 绿色:上下边界')
    axes[1].axis('off')
    
    # 裁剪结果
    axes[2].imshow(cropped_rgb)
    axes[2].set_title(f'裁剪结果\n{cropped_rgb.shape[1]}x{cropped_rgb.shape[0]}')
    axes[2].axis('off')
    
    plt.suptitle(f'图像裁剪对比 (上:{top_len},下:{bottom_len},左:{left_len},右:{right_len})', fontsize=14)
    plt.tight_layout()
    plt.show()
    
    return cropped

def crop_multiple_sides_only(image, crop_dict):
    """
    仅裁剪指定的边
    
    参数:
        image: 输入图像
        crop_dict: 字典，指定要裁剪的边和长度
                  例如: {'top': 50, 'left': 100}
    """
    print("🎯 选择性裁剪...")
    
    # 设置默认值
    top_len = crop_dict.get('top', 0)
    bottom_len = crop_dict.get('bottom', 0)
    left_len = crop_dict.get('left', 0)
    right_len = crop_dict.get('right', 0)
    
    print(f"📏 选择性裁剪设置:")
    for side, length in crop_dict.items():
        if length > 0:
            print(f"  {side}: {length}像素")
    
    return crop_image_by_border_length(image, top_len, bottom_len, left_len, right_len)

def batch_crop_images(image_list, top_len, bottom_len, left_len, right_len, output_dir="cropped"):
    """
    批量裁剪多张图像
    """
    print(f"📦 批量裁剪 {len(image_list)} 张图像...")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    for i, image_input in enumerate(image_list):
        print(f"\n[{i+1}/{len(image_list)}] 处理图像...")
        
        # 裁剪
        cropped = crop_image_by_border_length(image_input, top_len, bottom_len, left_len, right_len)
        
        if cropped is not None:
            # 生成输出路径
            if isinstance(image_input, str):
                base_name = os.path.basename(image_input)
                output_name = f"cropped_{base_name}"
            else:
                output_name = f"cropped_{i+1}.jpg"
            
            output_path = os.path.join(output_dir, output_name)
            
            # 保存
            success = cv2.imwrite(output_path, cropped)
            
            if success:
                print(f"✅ 保存: {output_path}")
                results.append({
                    'input': image_input,
                    'output': output_path,
                    'size': f"{cropped.shape[1]}x{cropped.shape[0]}"
                })
            else:
                print(f"❌ 保存失败: {output_path}")
        else:
            print(f"❌ 裁剪失败")
    
    print(f"\n📊 批量裁剪完成:")
    print(f"  成功: {len(results)}/{len(image_list)}")
    
    return results

# 测试函数
def test_crop_functions():
    """测试裁剪函数"""
    print("🧪 测试裁剪功能")
    print("=" * 50)
    
    # 创建测试图像
    test_img = np.zeros((400, 600, 3), dtype=np.uint8)
    test_img[:] = [100, 150, 200]  # 淡蓝色背景
    
    # 添加网格和文字以便观察裁剪效果
    for i in range(0, 600, 50):
        cv2.line(test_img, (i, 0), (i, 400), (255, 255, 255), 1)
        cv2.putText(test_img, str(i), (i, 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    for i in range(0, 400, 50):
        cv2.line(test_img, (0, i), (600, i), (255, 255, 255), 1)
        cv2.putText(test_img, str(i), (10, i), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    # 添加中心标记
    cv2.putText(test_img, "CENTER", (250, 200), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    print("📊 测试用例:")
    
    # 测试1: 四边均匀裁剪
    print("\n1. 四边均匀裁剪 (各50像素)")
    result1 = crop_image_by_border_length(test_img, 50, 50, 50, 50)
    if result1 is not None:
        print(f"   结果尺寸: {result1.shape[1]}x{result1.shape[0]}")
    
    # 测试2: 只裁剪上下边
    print("\n2. 只裁剪上下边 (各100像素)")
    result2 = crop_image_by_border_length(test_img, 100, 100, 0, 0)
    if result2 is not None:
        print(f"   结果尺寸: {result2.shape[1]}x{result2.shape[0]}")
    
    # 测试3: 只裁剪左右边
    print("\n3. 只裁剪左右边 (各150像素)")
    result3 = crop_image_by_border_length(test_img, 0, 0, 150, 150)
    if result3 is not None:
        print(f"   结果尺寸: {result3.shape[1]}x{result3.shape[0]}")
    
    # 测试4: 不对称裁剪
    print("\n4. 不对称裁剪 (上:30,下:70,左:50,右:100)")
    result4 = crop_image_by_border_length(test_img, 30, 70, 50, 100)
    if result4 is not None:
        print(f"   结果尺寸: {result4.shape[1]}x{result4.shape[0]}")
    
    # 测试5: 显示对比
    print("\n5. 显示裁剪对比")
    crop_and_show_comparison(test_img, 50, 50, 50, 50)
    
    print("\n✅ 测试完成")

# 使用示例
# def main():
#     """主函数示例"""
#     print("🎨 图像裁剪工具")
#     print("=" * 50)
    
#     # 方式1: 直接使用图像数据
#     print("\n方式1: 使用图像数据")
#     # 创建一个测试图像
#     test_image = np.zeros((300, 400, 3), dtype=np.uint8)
#     test_image[100:200, 150:250] = [0, 0, 255]  # 红色矩形
    
#     result = crop_image_by_border_length(test_image, 50, 50, 100, 100)
    
#     # 方式2: 使用文件路径
#     print("\n方式2: 使用文件路径")
#     image_path = "example.jpg"  # 替换为你的图像路径
#     if os.path.exists(image_path):
#         result = crop_image_by_border_length(image_path, 20, 20, 30, 30)
    
#     # 方式3: 选择性裁剪
#     print("\n方式3: 选择性裁剪")
#     crop_dict = {'top': 50, 'left': 100}  # 只裁剪上边和左边
#     result = crop_multiple_sides_only(test_image, crop_dict)
    
#     # 方式4: 显示对比
#     print("\n方式4: 显示裁剪对比")
#     result = crop_and_show_comparison(test_image, 30, 70, 50, 100)

# # 快速使用示例
# if __name__ == "__main__":
#     print("选择测试模式:")
#     print("1. 运行完整测试")
#     print("2. 简单示例")
    
#     choice = input("请选择 (1/2): ").strip()
    
#     if choice == '1':
#         test_crop_functions()
#     elif choice == '2':
#         # 简单示例
#         print("\n简单示例:")
#         print("-" * 30)
        
#         # 创建示例图像
#         img = np.zeros((200, 300, 3), dtype=np.uint8)
#         img[:] = [180, 180, 180]  # 灰色背景
        
#         # 裁剪示例
#         cropped = crop_image_by_border_length(img, 20, 30, 40, 50)
        
#         if cropped is not None:
#             print(f"\n原始尺寸: 300x200")
#             print(f"裁剪参数: 上20,下30,左40,右50")
#             print(f"裁剪后: {cropped.shape[1]}x{cropped.shape[0]}")
#     else:
#         print("❌ 无效选择")    

# 主要程序
if __name__ == "__main__":
    scroll_path = "Frames/scroll_vertical_brown_black.png"    # 你的卷轴模板
    scroll_output_path = "scroll_template_coordinates.png"
    embedded_img_path =  "Images/horse_transparent.png"     # "banner_vertical_transparent.png"  # 你的书法作品
    output_path = "calligraphy_in_scroll_vertical_transparent.png"
    output_path_2 = "calligraphy_in_scroll_vertical_transparent_2.png"
    print("=" * 60)
    print("卷轴模板创建工具 - 坐标版本")
    print("=" * 60)
    
    # 方法1: 交互式选择坐标
    print("\n方法1: 交互式选择内部区域坐标")
    print("提示: 请在显示的图像上点击两次:")
    print("      第一次点击: 内部区域左上角")
    print("      第二次点击: 内部区域右下角")
    
    coords = None   # interactive_coordinate_selector(scroll_path)
    
    if coords is not None:
        inner_top, inner_bottom, inner_left, inner_right = coords
        
        print(f"\n✅ 选择的坐标:")
        print(f"   内部区域: y={inner_top}~{inner_bottom}, x={inner_left}~{inner_right}")
        print(f"   尺寸: {inner_right-inner_left}x{inner_bottom-inner_top}")
        
        # 创建模板
        template, alpha = create_scroll_template_correct_coords(
            scroll_path,
            scroll_output_path,
            inner_top, inner_bottom, inner_left, inner_right,
            transparency_level=32,  # 128: 50%透明度; 64:25%
            bg_color=None
        )

        
        
    else:
        print("\n⚠️ 未选择坐标，使用预设坐标")
        
        # 方法2: 使用预设坐标（需要你提供）
        # 根据你的测量，请提供这4个值：
        
        inner_top = 482    # 内部区域上边界Y坐标
        inner_bottom = 3045 # 内部区域下边界Y坐标  
        inner_left = 589   # 内部区域左边界X坐标
        inner_right = 1880  # 内部区域右边界X坐标
        # 坐标范围: y=482~3040, x=589~1872
        
        # 示例：假设内部区域大致在图像中央
        # height, width = cv2.imread(scroll_path).shape[:2]
        
        # # 使用图像中央80%的区域
        # margin_h = int(height * 0.1)
        # margin_w = int(width * 0.1)
        
        # inner_top = margin_h
        # inner_bottom = height - margin_h
        # inner_left = margin_w
        # inner_right = width - margin_w
        
        print(f"\n📏 使用预设坐标:")
        print(f"   内部区域: y={inner_top}~{inner_bottom}, x={inner_left}~{inner_right}")
        # print(f"   尺寸: {inner_right-inner_left}x{inner_bottom-inner_top}")
        
        # 创建模板
        # 创建透明模板
        # template, alpha = create_scroll_template_correct_coords(
        #     scroll_path,
        #     scroll_output_path,
        #     inner_top, inner_bottom, inner_left, inner_right,
        #     transparency_level=16, bg_color=None
        # )
        # 创建单一颜色模板
        # template, alpha = create_scroll_template_correct_coords(
        #     scroll_path,
        #     scroll_output_path,
        #     inner_top, inner_bottom, inner_left, inner_right,
        #     transparency_level=255,
        #     bg_color=(0,255,255,0)
        # )

    # sys.exit(0)

    # 融合书法和卷轴
    result = embed_calligraphy_in_scroll(
        scroll_output_path,
        embedded_img_path,
        output_path,
        inner_top, inner_bottom, inner_left, inner_right,
        scroll_area_trans_level=64,
        calligraphy_opacity=0.65,  # 书法完全显示
        blend_mode='normal',      # 正常混合
        calligraphy_margin=1,    # 书法边距30像素
        debug=True               # 显示调试信息
    )
    
    if result is not None:
        print(f"\n🎉 融合成功！")
        print(f"📁 输出文件: {output_path}")
        
        # 显示最终结果
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
        cv2.imwrite(output_path_2, cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
        plt.title('书法卷轴融合作品', fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    else:
        print(f"\n❌ 融合失败")
        

        