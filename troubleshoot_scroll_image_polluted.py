

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

def test_image_loading():
    """测试图像加载是否被破坏"""
    scroll_path = "Source/scroll_horizontal_green_black.png"
    
    print("=" * 60)
    print("测试图像加载过程")
    print("=" * 60)
    
    # 1. 直接读取并显示
    print("1. 直接读取图像...")
    img = cv2.imread(scroll_path, cv2.IMREAD_UNCHANGED)
    print(f"   ✅ 直接读取成功: {img.shape if img is not None else '失败'}")
    
    # 2. 转换为RGB供Matplotlib显示
    print("2. 转换为RGB...")
    if img is not None:
        # img_rgb = cv2.cvtColor(img_direct, cv2.COLOR_BGR2RGB)
        # print(f"   ✅ 转换成功: {img_rgb.shape}")

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

        # 创建透明度掩码
        # alpha = np.ones((height, width), dtype=np.uint8) * 255  # 默认全部不透明

          # 获取alpha通道的引用
        alpha = rgba[:, :, 3]
        
        # 设置内部区域为半透明
        alpha[100:600, 100:800] = 0.5
        
        # 应用透明度
        rgba[:, :, 3] = alpha

        # 2.5. 保存转换文件
        print("4. 保存转换文件...")
        test_output = "test_output.png"
        cv2.imwrite(test_output, rgba)
        
        # 3. 显示图像
        print("3. 显示图像...")
        plt.figure(figsize=(10, 8))
        plt.imshow(rgba)
        plt.title(f'测试显示 - 尺寸: {rgba.shape[1]}x{rgba.shape[0]}')
        plt.axis('off')
        plt.show()
        
        
        
        # 重新读取
        img_reloaded = cv2.imread(test_output, cv2.IMREAD_UNCHANGED)
        print(f"   ✅ 重新读取: {img_reloaded.shape if img_reloaded is not None else '失败'}")
        
        # 比较两个图像
        if rgba is not None and img_reloaded is not None:
            if rgba.shape == img_reloaded.shape:
                diff = np.sum(cv2.absdiff(rgba, img_reloaded))
                print(f"   📊 差异度: {diff} (0表示完全相同)")
            else:
                print(f"   ❌ 尺寸不同: {rgba.shape} vs {img_reloaded.shape}")
    else:
        print("❌ 无法读取图像")

def create_scroll_template_pure_opencv(scroll_path, output_path, 
                                      inner_top, inner_bottom, inner_left, inner_right):
    """
    纯OpenCV创建卷轴模板，完全不使用Matplotlib
    """
    print("🎨 纯OpenCV创建卷轴模板...")
    
    # 1. 直接读取图像
    img = cv2.imread(scroll_path, cv2.IMREAD_UNCHANGED)
    # img = Image.open(scroll_path)
    if img is None:
        print(f"❌ 无法读取图像: {scroll_path}")
        return None
    
    original_height, original_width = img.shape[:2]
    print(f"📐 原始图像尺寸: {original_width}x{original_height}")
    
    # 2. 验证坐标
    print(f"📏 验证坐标范围...")
    if not (0 <= inner_top < inner_bottom <= original_height and 
            0 <= inner_left < inner_right <= original_width):
        print(f"❌ 坐标无效!")
        print(f"   需要: 0 ≤ top < bottom ≤ {original_height}")
        print(f"         0 ≤ left < right ≤ {original_width}")
        return None
    
    print(f"✅ 坐标有效:")
    print(f"   内部区域: [{inner_top}:{inner_bottom}, {inner_left}:{inner_right}]")
    print(f"   内部尺寸: {inner_right-inner_left}x{inner_bottom-inner_top}")
    
    # 3. 转换为RGBA
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 4. 设置透明度
    # 创建alpha通道
    alpha = np.ones((original_height, original_width), dtype=np.uint8) * 255
    
    # 内部区域设为半透明（128 = 50%透明）
    alpha[inner_top:inner_bottom, inner_left:inner_right] = 128
    
    # 应用alpha通道
    rgba[:, :, 3] = alpha
    
    # 5. 保存为PNG
    print(f"💾 保存模板...")
    success = cv2.imwrite(output_path, rgba)
    
    if not success:
        print(f"❌ 保存失败: {output_path}")
        return None
    
    print(f"✅ 成功保存: {output_path}")
    
    # 6. 验证保存的文件
    print(f"🔍 验证保存的文件...")
    verify_saved_file(output_path, inner_top, inner_bottom, inner_left, inner_right)
    
    return rgba

def verify_saved_file(file_path, inner_top, inner_bottom, inner_left, inner_right):
    """验证保存的文件"""
    saved = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    if saved is None:
        print(f"❌ 无法读取保存的文件: {file_path}")
        return False
    
    if saved.shape[2] != 4:
        print(f"❌ 不是RGBA图像: {saved.shape}")
        return False
    
    height, width = saved.shape[:2]
    
    print(f"📐 保存的图像尺寸: {width}x{height}")
    
    # 检查关键点
    alpha = saved[:, :, 3]
    
    # 检查四个角（应该是255）
    corners = [
        (0, 0, "左上角"),
        (0, width-1, "右上角"),
        (height-1, 0, "左下角"),
        (height-1, width-1, "右下角")
    ]
    
    print("📊 边框检查:")
    for y, x, name in corners:
        val = alpha[y, x]
        if val == 255:
            print(f"  ✅ {name}: Alpha={val}")
        else:
            print(f"  ❌ {name}: Alpha={val} (应为255)")
    
    # 检查内部区域（应该是128）
    if inner_top < height and inner_left < width:
        inner_val = alpha[inner_top, inner_left]
        print(f"  📍 内部区域点({inner_left},{inner_top}): Alpha={inner_val} {'✅' if inner_val == 128 else '❌'}")
    
    return True

def get_coordinates_from_image(scroll_path):
    """从图像获取坐标（非交互式）"""
    print("📝 获取坐标信息...")
    
    # 读取图像获取尺寸
    img = cv2.imread(scroll_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
    
    height, width = img.shape[:2]
    
    print(f"📐 图像尺寸: {width}x{height}")
    
    # 使用简单的算法估算内部区域
    # 这里假设内部区域是中央80%的区域
    margin_h = int(height * 0.1)  # 10%边距
    margin_w = int(width * 0.1)   # 10%边距
    
    inner_top = margin_h
    inner_bottom = height - margin_h
    inner_left = margin_w
    inner_right = width - margin_w
    
    print(f"📏 估算的内部区域:")
    print(f"  inner_top: {inner_top} (上边距: {margin_h}px)")
    print(f"  inner_bottom: {inner_bottom} (下边距: {margin_h}px)")
    print(f"  inner_left: {inner_left} (左边距: {margin_w}px)")
    print(f"  inner_right: {inner_right} (右边距: {margin_w}px)")
    print(f"  内部尺寸: {inner_right-inner_left}x{inner_bottom-inner_top}")
    
    return inner_top, inner_bottom, inner_left, inner_right

def preview_with_opencv(image, window_name="预览"):
    """使用OpenCV预览图像"""
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)
    cv2.imshow(window_name, image)
    print("👀 按任意键关闭预览窗口...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main_pure_opencv():
    """主函数 - 纯OpenCV版本"""
    print("=" * 60)
    print("卷轴模板创建工具 - 纯OpenCV版本")
    print("=" * 60)
    
    scroll_path = "Source/scroll_horizontal_green_black.png"
    output_path = "scroll_template_pure_opencv.png"
    
    # 检查文件是否存在
    if not os.path.exists(scroll_path):
        print(f"❌ 文件不存在: {scroll_path}")
        return None
    
    print(f"📁 输入文件: {scroll_path}")
    print(f"📁 输出文件: {output_path}")
    
    # 选项1: 自动估算坐标
    print("\n选项1: 自动估算内部区域坐标")
    coords = get_coordinates_from_image(scroll_path)
    
    if coords is None:
        print("❌ 无法获取坐标")
        return None
    
    # 如果需要手动调整坐标，可以在这里修改
    print("\n💡 如果需要调整坐标，请修改以下值:")
    inner_top, inner_bottom, inner_left, inner_right = coords
    
    # 这里可以手动设置坐标
    # inner_top = 200    # 修改为你需要的值
    # inner_bottom = 2200  # 修改为你需要的值
    # inner_left = 300    # 修改为你需要的值
    # inner_right = 3200  # 修改为你需要的值
    
    # 创建模板
    print(f"\n🔄 创建模板...")
    template = create_scroll_template_pure_opencv(
        scroll_path,
        output_path,
        inner_top,
        inner_bottom,
        inner_left,
        inner_right
    )
    
    if template is not None:
        print(f"\n🎉 模板创建成功!")
        
        # 询问是否预览
        preview = input("\n是否预览结果？(y/n): ").lower().strip()
        if preview == 'y':
            # 使用OpenCV预览
            print("🖼️ 显示预览...")
            
            # 显示原始图像
            original = cv2.imread(scroll_path, cv2.IMREAD_UNCHANGED)
            if original is not None:
                cv2.namedWindow("原始卷轴", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("原始卷轴", 800, 600)
                cv2.imshow("原始卷轴", original)
            
            # 显示模板
            cv2.namedWindow("透明模板", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("透明模板", 800, 600)
            
            # 注意：OpenCV显示RGBA图像时需要特殊处理
            # 转换为BGR显示
            template_bgr = cv2.cvtColor(template, cv2.COLOR_BGRA2BGR)
            cv2.imshow("透明模板", template_bgr)
            
            print("👀 按任意键关闭预览窗口...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        print(f"📁 模板文件: {output_path}")
        print(f"📏 使用的坐标:")
        print(f"  inner_top: {inner_top}")
        print(f"  inner_bottom: {inner_bottom}")
        print(f"  inner_left: {inner_left}")
        print(f"  inner_right: {inner_right}")
        
        # 保存坐标到文件
        save_coords_to_file(inner_top, inner_bottom, inner_left, inner_right)
        
        return template
    else:
        print("\n❌ 模板创建失败")
        return None

def save_coords_to_file(inner_top, inner_bottom, inner_left, inner_right):
    """保存坐标到文件"""
    coords = {
        'inner_top': int(inner_top),
        'inner_bottom': int(inner_bottom),
        'inner_left': int(inner_left),
        'inner_right': int(inner_right),
        'transparency': 128
    }
    
    import json
    with open('scroll_coordinates.json', 'w') as f:
        json.dump(coords, f, indent=2)
    
    print(f"📁 坐标已保存到: scroll_coordinates.json")

def load_and_use_existing_coords():
    """加载并使用已有的坐标文件"""
    import json
    
    if not os.path.exists('scroll_coordinates.json'):
        print("❌ 坐标文件不存在")
        return None
    
    with open('scroll_coordinates.json', 'r') as f:
        coords = json.load(f)
    
    print(f"📁 从文件加载坐标:")
    print(f"  inner_top: {coords['inner_top']}")
    print(f"  inner_bottom: {coords['inner_bottom']}")
    print(f"  inner_left: {coords['inner_left']}")
    print(f"  inner_right: {coords['inner_right']}")
    
    scroll_path = "Source/scroll_horizontal_green_black.png"
    output_path = "scroll_from_saved_coords.png"
    
    template = create_scroll_template_pure_opencv(
        scroll_path,
        output_path,
        coords['inner_top'],
        coords['inner_bottom'],
        coords['inner_left'],
        coords['inner_right']
    )
    
    return template

# 直接运行
if __name__ == "__main__":
    print("🚫 警告: 此脚本完全不使用Matplotlib，避免图像破坏")
    
    # 选项1: 创建新模板
    print("\n请选择:")
    print("1. 创建新模板（自动估算坐标）")
    print("2. 使用已有的坐标文件")
    
    # choice = input("请输入选择 (1/2): ").strip()
    
    # if choice == '1':
    #     template = main_pure_opencv()
    # elif choice == '2':
    #     template = load_and_use_existing_coords()
    # else:
    #     print("❌ 无效选择")
    #     template = None
    
    # if template is not None:
    #     print("\n✅ 操作完成!")
    # else:
    #     print("\n❌ 操作失败")
# 运行测试
test_image_loading()