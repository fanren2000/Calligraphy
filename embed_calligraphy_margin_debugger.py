

import cv2
import numpy as np
import os

def embed_calligraphy_with_margin(scroll_template_path, calligraphy_path, output_path,
                                 inner_top, inner_bottom, inner_left, inner_right,
                                 calligraphy_margin=30,  # 默认30，但可以被覆盖
                                 scroll_transparency=128,
                                 debug=True):
    """
    嵌入书法到卷轴，支持自定义边距
    
    参数:
        calligraphy_margin: 书法距内部区域边缘的边距（像素）
    """
    print("=" * 60)
    print("嵌入书法（支持自定义边距）")
    print("=" * 60)
    
    print(f"📏 参数设置:")
    print(f"  书法边距: {calligraphy_margin}像素")
    print(f"  卷轴内部透明度: {scroll_transparency}")
    
    # 1. 读取卷轴模板
    print(f"\n📥 读取卷轴模板: {scroll_template_path}")
    scroll = cv2.imread(scroll_template_path, cv2.IMREAD_UNCHANGED)
    
    if scroll is None:
        print("❌ 无法读取卷轴模板")
        return None
    
    scroll_height, scroll_width = scroll.shape[:2]
    print(f"📐 卷轴尺寸: {scroll_width}x{scroll_height}")
    
    # 2. 读取书法图像
    print(f"\n📥 读取书法作品: {calligraphy_path}")
    calligraphy = cv2.imread(calligraphy_path)
    
    if calligraphy is None:
        print("❌ 无法读取书法作品")
        return None
    
    callig_height, callig_width = calligraphy.shape[:2]
    print(f"📐 书法原始尺寸: {callig_width}x{callig_height}")
    
    # 3. 计算可用于书法的区域（减去边距）
    # 关键：这里使用传入的 calligraphy_margin 参数
    usable_width = (inner_right - inner_left) - 2 * calligraphy_margin
    usable_height = (inner_bottom - inner_top) - 2 * calligraphy_margin
    
    print(f"\n📏 区域计算:")
    print(f"  卷轴内部区域: {inner_right-inner_left}x{inner_bottom-inner_top}")
    print(f"  书法边距: {calligraphy_margin}像素")
    print(f"  可用区域: {usable_width}x{usable_height}")
    
    # 检查可用区域是否有效
    if usable_width <= 0 or usable_height <= 0:
        print(f"❌ 可用区域太小或无效: {usable_width}x{usable_height}")
        print(f"   尝试减小边距或增大内部区域")
        return None
    
    # 4. 调整书法大小以适应可用区域（保持宽高比）
    scale = min(usable_width / callig_width, usable_height / callig_height)
    new_width = int(callig_width * scale)
    new_height = int(callig_height * scale)
    
    print(f"\n📏 调整书法尺寸:")
    print(f"  原始: {callig_width}x{callig_height}")
    print(f"  目标: {new_width}x{new_height}")
    print(f"  缩放比例: {scale:.3f}")
    
    if scale != 1.0:
        calligraphy_resized = cv2.resize(calligraphy, (new_width, new_height), interpolation=cv2.INTER_AREA)
    else:
        calligraphy_resized = calligraphy
    
    # 5. 计算书法放置位置（居中，考虑边距）
    # 关键：这里使用传入的 calligraphy_margin 参数
    start_x = inner_left + calligraphy_margin + (usable_width - new_width) // 2
    start_y = inner_top + calligraphy_margin + (usable_height - new_height) // 2
    
    print(f"\n📍 书法放置位置:")
    print(f"  理论位置: x={start_x}, y={start_y}")
    print(f"  放置区域: [{start_y}:{start_y+new_height}, {start_x}:{start_x+new_width}]")
    
    # 确保位置在有效范围内
    start_x = max(inner_left, min(start_x, scroll_width - inner_right - new_width))
    start_y = max(inner_top, min(start_y, scroll_height - inner_bottom - new_height))
    
    print(f"  调整后位置: x={start_x}, y={start_y}")
    
    # 6. 创建结果图像
    result = scroll.copy()
    
    # 7. 混合书法到卷轴
    print(f"\n🎨 混合图像...")
    
    # 获取放置区域
    if start_y + new_height <= scroll_height and start_x + new_width <= scroll_width:
        target_region = result[start_y:start_y+new_height, start_x:start_x+new_width]
        
        # 获取卷轴透明度
        scroll_alpha = target_region[:, :, 3] / 255.0
        
        # 混合RGB通道
        for c in range(3):
            target_region[:, :, c] = (
                calligraphy_resized[:, :, c] * (1 - scroll_alpha) + 
                target_region[:, :, c] * scroll_alpha
            ).astype(np.uint8)
    else:
        print(f"❌ 放置区域超出图像范围")
        return None
    
    # 8. 保存结果
    print(f"\n💾 保存结果...")
    success = cv2.imwrite(output_path, result)
    
    if success:
        print(f"✅ 保存成功: {output_path}")
        
        if debug:
            show_result_with_margin(scroll, calligraphy_resized, result, 
                                   start_x, start_y, new_width, new_height,
                                   inner_top, inner_bottom, inner_left, inner_right,
                                   calligraphy_margin)
    else:
        print(f"❌ 保存失败")
    
    return result

def show_result_with_margin(scroll, calligraphy, result, 
                           callig_x, callig_y, callig_w, callig_h,
                           inner_top, inner_bottom, inner_left, inner_right,
                           margin):
    """显示带边距的结果"""
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 1. 卷轴模板
    axes[0, 0].imshow(cv2.cvtColor(scroll, cv2.COLOR_BGRA2RGBA))
    axes[0, 0].set_title('卷轴模板')
    axes[0, 0].axis('off')
    
    # 2. 书法图像
    axes[0, 1].imshow(cv2.cvtColor(calligraphy, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title(f'书法 ({callig_w}x{callig_h})')
    axes[0, 1].axis('off')
    
    # 3. 最终结果
    axes[0, 2].imshow(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    axes[0, 2].set_title('融合结果')
    axes[0, 2].axis('off')
    
    # 4. 区域标记图
    marked = result.copy()
    
    # 标记卷轴内部区域（绿色）
    cv2.rectangle(marked, (inner_left, inner_top), (inner_right, inner_bottom), 
                 (0, 255, 0, 255), 2)
    
    # 标记书法区域（蓝色）
    cv2.rectangle(marked, (callig_x, callig_y), 
                 (callig_x + callig_w, callig_y + callig_h), 
                 (255, 0, 0, 255), 2)
    
    # 标记边距区域（红色虚线）
    margin_inner_left = inner_left + margin
    margin_inner_right = inner_right - margin
    margin_inner_top = inner_top + margin
    margin_inner_bottom = inner_bottom - margin
    
    # 左上角边距标记
    cv2.line(marked, (inner_left, inner_top), (margin_inner_left, inner_top), 
            (0, 0, 255, 255), 1, cv2.LINE_AA)
    cv2.line(marked, (inner_left, inner_top), (inner_left, margin_inner_top), 
            (0, 0, 255, 255), 1, cv2.LINE_AA)
    
    # 添加边距文字
    cv2.putText(marked, f'Margin: {margin}px', 
               (inner_left + 10, inner_top + 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255, 255), 1)
    
    axes[1, 0].imshow(cv2.cvtColor(marked, cv2.COLOR_BGRA2RGBA))
    axes[1, 0].set_title('区域标记\n绿色:卷轴内部, 蓝色:书法, 红色:边距')
    axes[1, 0].axis('off')
    
    # 5. 边距细节
    detail_size = 100
    detail_x = max(0, inner_left - 20)
    detail_y = max(0, inner_top - 20)
    
    detail = result[detail_y:detail_y+detail_size, detail_x:detail_x+detail_size]
    axes[1, 1].imshow(cv2.cvtColor(detail, cv2.COLOR_BGRA2RGBA))
    axes[1, 1].set_title(f'边距细节 ({margin}px)')
    axes[1, 1].axis('off')
    
    # 6. 参数信息
    axes[1, 2].axis('off')
    info_text = f"""
参数设置:
卷轴内部区域:
  坐标: ({inner_left}, {inner_top}) - ({inner_right}, {inner_bottom})
  尺寸: {inner_right-inner_left}x{inner_bottom-inner_top}

书法设置:
  原始尺寸: {calligraphy.shape[1]}x{calligraphy.shape[0]}
  调整后尺寸: {callig_w}x{callig_h}
  位置: ({callig_x}, {callig_y})
  边距: {margin}像素

可用区域:
  宽度: {inner_right-inner_left-2*margin}
  高度: {inner_bottom-inner_top-2*margin}
"""
    axes[1, 2].text(0.05, 0.95, info_text, fontsize=8, 
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.suptitle(f'书法卷轴融合 - 边距: {margin}像素', fontsize=16, y=0.98)
    plt.tight_layout()
    plt.show()

def test_different_margins():
    """测试不同的边距设置"""
    print("🧪 测试不同边距设置")
    
    scroll_path = "scroll_template_preserved_alpha.png"
    calligraphy_path = "calligraphy_work_torn_edge.png"
    
    # 读取卷轴获取内部区域坐标
    scroll = cv2.imread(scroll_path, cv2.IMREAD_UNCHANGED)
    if scroll is None:
        print("❌ 无法读取卷轴模板")
        return
    
    # 这里需要你的实际坐标
    # 示例坐标，请替换为实际的
    inner_top = 100
    inner_bottom = scroll.shape[0] - 100
    inner_left = 100
    inner_right = scroll.shape[1] - 100
    
    # 测试不同的边距
    margins_to_test = [1, 5, 10, 20, 30]
    
    for margin in margins_to_test:
        print(f"\n📏 测试边距: {margin}像素")
        output_path = f"result_margin_{margin}.png"
        
        result = embed_calligraphy_with_margin(
            scroll_path,
            calligraphy_path,
            output_path,
            inner_top, inner_bottom, inner_left, inner_right,
            calligraphy_margin=margin,
            debug=False  # 关闭单个调试，最后统一显示
        )
        
        if result is not None:
            print(f"✅ 生成: {output_path}")
        else:
            print(f"❌ 失败")
    
    # 显示所有结果对比
    show_margin_comparison(margins_to_test)

def show_margin_comparison(margins):
    """显示不同边距的对比"""
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, margin in enumerate(margins):
        if i < len(axes):
            file_path = f"result_margin_{margin}.png"
            if os.path.exists(file_path):
                img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
                if img is not None:
                    axes[i].imshow(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
                    axes[i].set_title(f'边距: {margin}px')
                    axes[i].axis('off')
            else:
                axes[i].text(0.5, 0.5, f'文件不存在\n边距: {margin}px', 
                           ha='center', va='center')
                axes[i].set_title(f'边距: {margin}px')
                axes[i].axis('off')
    
    # 隐藏多余的子图
    for i in range(len(margins), len(axes)):
        axes[i].axis('off')
    
    plt.suptitle('不同边距效果对比', fontsize=16)
    plt.tight_layout()
    plt.show()

# 主程序
def main():
    """主程序"""
    print("=" * 60)
    print("书法卷轴融合工具 - 支持自定义边距")
    print("=" * 60)
    
    # 文件路径
    scroll_template_path = "scroll_template_preserved_alpha.png"
    calligraphy_path = "calligraphy_work_torn_edge.png"
    output_path = "calligraphy_in_scroll_result.png"
    
    # 检查文件是否存在
    if not os.path.exists(scroll_template_path):
        print(f"❌ 卷轴模板不存在: {scroll_template_path}")
        return
    
    if not os.path.exists(calligraphy_path):
        print(f"❌ 书法作品不存在: {calligraphy_path}")
        return
    
    # 获取卷轴内部区域坐标
    # 这里需要你提供实际的坐标，或者从文件加载
    print("\n📏 请输入卷轴内部区域坐标:")
    
    scroll = cv2.imread(scroll_template_path, cv2.IMREAD_UNCHANGED)
    scroll_height, scroll_width = scroll.shape[:2]
    
    print(f"卷轴尺寸: {scroll_width}x{scroll_height}")
    
    try:
        inner_top = int(input(f"inner_top [建议 {scroll_height//4}]: ") or scroll_height//4)
        inner_bottom = int(input(f"inner_bottom [建议 {scroll_height*3//4}]: ") or scroll_height*3//4)
        inner_left = int(input(f"inner_left [建议 {scroll_width//4}]: ") or scroll_width//4)
        inner_right = int(input(f"inner_right [建议 {scroll_width*3//4}]: ") or scroll_width*3//4)
    except:
        print("⚠️ 输入错误，使用建议值")
        inner_top, inner_bottom, inner_left, inner_right = scroll_height//4, scroll_height*3//4, scroll_width//4, scroll_width*3//4
    
    # 输入边距
    print(f"\n🎯 设置书法边距:")
    print(f"  内部区域尺寸: {inner_right-inner_left}x{inner_bottom-inner_top}")
    
    max_recommended_margin = min(inner_right-inner_left, inner_bottom-inner_top) // 4
    try:
        margin = int(input(f"书法边距(像素) [建议1-{max_recommended_margin}, 默认1]: ") or "1")
        margin = max(0, min(margin, max_recommended_margin))
    except:
        margin = 1
    
    print(f"✅ 使用边距: {margin}像素")
    
    # 执行融合
    result = embed_calligraphy_with_margin(
        scroll_template_path,
        calligraphy_path,
        output_path,
        inner_top, inner_bottom, inner_left, inner_right,
        calligraphy_margin=margin,
        scroll_transparency=128,
        debug=True
    )
    
    if result is not None:
        print(f"\n🎉 融合成功!")
        print(f"📁 输出文件: {output_path}")
        print(f"📏 使用的边距: {margin}像素")
    else:
        print(f"\n❌ 融合失败")

# 快速测试函数
def quick_margin_test():
    """快速测试边距功能"""
    print("🚀 快速边距测试")
    
    # 使用示例文件
    scroll_path = "scroll_template_coordinates.png"
    calligraphy_path = "five_character_quatrain_poetry_0.45.png"
    
    # 读取卷轴获取尺寸
    scroll = cv2.imread(scroll_path, cv2.IMREAD_UNCHANGED)
    if scroll is None:
        print("❌ 无法读取卷轴")
        return
    
    # 使用中央区域
    inner_top = scroll.shape[0] // 4
    inner_bottom = scroll.shape[0] * 3 // 4
    inner_left = scroll.shape[1] // 4
    inner_right = scroll.shape[1] * 3 // 4
    
    # 测试极小边距
    margin = 1
    
    result = embed_calligraphy_with_margin(
        scroll_path,
        calligraphy_path,
        "test_margin_1.png",
        inner_top, inner_bottom, inner_left, inner_right,
        calligraphy_margin=margin,
        debug=True
    )
    
    if result is not None:
        print(f"✅ 边距{ margin }测试成功")

# 运行
if __name__ == "__main__":
    print("选择模式:")
    print("1. 完整流程（自定义边距）")
    print("2. 快速测试（边距=1）")
    print("3. 测试不同边距对比")
    
    choice = input("请选择 (1/2/3): ").strip()
    
    if choice == '1':
        main()
    elif choice == '2':
        quick_margin_test()
    elif choice == '3':
        test_different_margins()
    else:
        print("❌ 无效选择")