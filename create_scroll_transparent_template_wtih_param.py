import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

def create_scroll_template_correct_coords(image_path, output_path, inner_top, inner_bottom, inner_left, inner_right, transparency_level=128):
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
    
    
    # 创建透明度掩码 & 获取alpha通道的引用
    alpha = rgba[:, :, 3]
    
    # 设置内部区域为半透明
    alpha[inner_top:inner_bottom, inner_left:inner_right] = transparency_level
    
    # 应用透明度
    rgba[:, :, 3] = alpha
    
    # 计算内部区域信息
    inner_height = inner_bottom - inner_top
    inner_width = inner_right - inner_left
    
    print(f"\n🎨 内部透明区域:")
    print(f"   坐标范围: y={inner_top}~{inner_bottom}, x={inner_left}~{inner_right}")
    print(f"   尺寸: {inner_width}x{inner_height}")
    print(f"   透明度: {transparency_level}/255 ({transparency_level/255:.0%})")
    print(f"   面积占比: {inner_width*inner_height/(width*height):.1%}")
    
    # 保存结果
    if output_path:
        cv2.imwrite(output_path, rgba)
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
        transparency_level=128  # 卷轴内部50%透明
    )
    
    if scroll_template is None:
        print("❌ 卷轴模板创建失败")
        return None
    
    # 2. 准备书法图像
    print("\n步骤2: 准备书法图像")
    
    # 计算可用于书法的区域（减去边距）
    calligraphy_area_width = (inner_right - inner_left) - 2 * calligraphy_margin
    calligraphy_area_height = (inner_bottom - inner_top) - 2 * calligraphy_margin
    
    if calligraphy_area_width <= 0 or calligraphy_area_height <= 0:
        print(f"❌ 书法区域太小: {calligraphy_area_width}x{calligraphy_area_height}")
        return None
    
    calligraphy_prepared = prepare_calligraphy_image(
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
    scale = min(target_width / w, target_height / h)
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


# 主要程序
if __name__ == "__main__":
    scroll_path = "Source/scroll_horizontal_green_black.png"    # 你的卷轴模板
    scroll_output_path = "scroll_template_coordinates.png"
    calligraphy_path = "Source/calligraphy_work_torn_edge.png"  # 你的书法作品
    output_path = "calligraphy_in_scroll_final.png"
    
    print("=" * 60)
    print("卷轴模板创建工具 - 坐标版本")
    print("=" * 60)
    
    # 方法1: 交互式选择坐标
    print("\n方法1: 交互式选择内部区域坐标")
    print("提示: 请在显示的图像上点击两次:")
    print("      第一次点击: 内部区域左上角")
    print("      第二次点击: 内部区域右下角")
    
    coords = None   #interactive_coordinate_selector(scroll_path)
    
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
            transparency_level=128  # 50%透明度
        )

        
        
    else:
        print("\n⚠️ 未选择坐标，使用预设坐标")
        
        # 方法2: 使用预设坐标（需要你提供）
        # 根据你的测量，请提供这4个值：
        
        inner_top = 756    # 内部区域上边界Y坐标
        inner_bottom = 1824 # 内部区域下边界Y坐标  
        inner_left = 480   # 内部区域左边界X坐标
        inner_right = 3062  # 内部区域右边界X坐标
        
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
        template, alpha = create_scroll_template_correct_coords(
            scroll_path,
            scroll_output_path,
            inner_top, inner_bottom, inner_left, inner_right,
            transparency_level=128
        )

    # 融合书法和卷轴
    result = embed_calligraphy_in_scroll(
        scroll_output_path,
        calligraphy_path,
        output_path,
        inner_top, inner_bottom, inner_left, inner_right,
        calligraphy_opacity=0.5,  # 书法完全显示
        blend_mode='normal',      # 正常混合
        calligraphy_margin=30,    # 书法边距30像素
        debug=True               # 显示调试信息
    )
    
    if result is not None:
        print(f"\n🎉 融合成功！")
        print(f"📁 输出文件: {output_path}")
        
        # 显示最终结果
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
        plt.title('书法卷轴融合作品', fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    else:
        print(f"\n❌ 融合失败")
        

        