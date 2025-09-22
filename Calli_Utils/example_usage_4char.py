from PIL import Image, ImageDraw, ImageFont
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Calli_Utils import (
    add_circular_seal_with_border_4char, 
    add_circular_seal_advanced,
    add_circular_seal_with_rotation,
    add_circular_seal_visual_debug,
    add_circular_seal_with_traditional_layout
)

# 使用示例
def example_usage():
    """使用示例"""
    
    # 创建测试图像
    image = Image.new('RGB', (300, 300), (245, 235, 215))
    
    # 使用基本版本
    # image = add_circular_seal_with_border_4char(image, "上官婉儿", (150, 150), 120)
    
    # 使用高级版本
    # image = add_circular_seal_advanced(image, "上官婉儿", (150, 150), 125)

    # 使用精确版本
    # image = add_circular_seal_precise(image, "上官婉儿", (150, 150), 130)
    
    # 使用传统版本
    # image = add_circular_seal_with_traditional_layout(image, "上官婉儿", (150, 150), 125)

    # 使用旋转版本
    image = add_circular_seal_with_rotation(image, "上官婉儿", (150, 150), 130, 0.5, 15)

    # 使用测试版本
    #image = add_circular_seal_visual_debug(image, "上官婉儿", (150, 150), 125, 0.5)
    
    image.save("四字圆形印章.png", quality=95)
    print("生成完成：四字圆形印章.png")

if __name__ == "__main__":
    example_usage()