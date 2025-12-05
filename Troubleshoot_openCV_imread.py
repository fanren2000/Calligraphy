import cv2
import numpy as np
import os

def diagnose_fundamental():
    """基础诊断"""
    print("🔍 基础诊断开始...")
    
    # 1. 检查原始文件
    test_file = "Source/scroll_horizontal_green_black.png"
    
    if not os.path.exists(test_file):
        print(f"❌ 文件不存在: {test_file}")
        return
    
    # 获取文件信息
    file_size = os.path.getsize(test_file)
    print(f"📁 文件: {test_file}")
    print(f"📊 文件大小: {file_size:,} bytes")
    
    # 2. 直接读取并立即保存，不做任何处理
    print("\n🔄 测试1: 直接读取->保存")
    img = cv2.imread(test_file, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        print("❌ cv2.imread 失败")
        return
    
    print(f"📐 读取的图像形状: {img.shape}")
    print(f"🎨 图像类型: {img.dtype}")
    
    # 立即保存
    test_output = "test_direct_copy.png"
    success = cv2.imwrite(test_output, img)
    
    if success:
        print(f"✅ 直接保存成功: {test_output}")
        
        # 重新读取验证
        img_reloaded = cv2.imread(test_output, cv2.IMREAD_UNCHANGED)
        if img_reloaded is not None:
            print(f"📐 重新读取的形状: {img_reloaded.shape}")
            
            # 比较差异
            if img.shape == img_reloaded.shape:
                diff = np.sum(np.abs(img.astype(float) - img_reloaded.astype(float)))
                print(f"📊 差异度: {diff}")
                
                if diff == 0:
                    print("🎉 完全相同！")
                else:
                    print("⚠️ 有差异")
                    
                    # 找出差异位置
                    diff_mask = np.any(img != img_reloaded, axis=2)
                    diff_count = np.sum(diff_mask)
                    print(f"📊 不同像素数: {diff_count}")
                    
                    if diff_count < 100:
                        print("🔍 检查差异像素...")
                        diff_indices = np.where(diff_mask)
                        for i in range(min(5, len(diff_indices[0]))):
                            y, x = diff_indices[0][i], diff_indices[1][i]
                            print(f"  位置({x},{y}): 原={img[y,x]}, 新={img_reloaded[y,x]}")
        else:
            print("❌ 重新读取失败")
    else:
        print("❌ 直接保存失败")

# 运行诊断
diagnose_fundamental()