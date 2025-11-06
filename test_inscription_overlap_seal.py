from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_calligraphy_stamp(text, font_size=120, font_path="calligraphy.ttf"):
    # 创建临时图像计算文本大小
    temp_font = ImageFont.truetype(font_path, font_size)
    temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    bbox = temp_draw.textbbox((0, 0), text, font=temp_font)
    
    text_width = bbox[2] - bbox[0] + 20
    text_height = bbox[3] - bbox[1] + 20
    
    # 创建临时图像（带白色背景用于处理）
    temp_img = Image.new('RGB', (text_width, text_height), 'white')
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 绘制文本（黑色）
    temp_draw.text((10 - bbox[0], 10 - bbox[1]), text, font=temp_font, fill='black')
    
    # 转换为numpy数组进行处理
    img_array = np.array(temp_img)
    
    # 创建透明图像
    result = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
    result_array = np.array(result)
    
    # 将非白色像素转换为红色并保持透明度
    # 找到文本像素（非白色）
    mask = np.all(img_array < 200, axis=2)  # 阈值处理
    
    # 在结果图像中设置红色文本
    result_array[mask] = [255, 0, 0, 255]  # 红色不透明
    result_array[~mask] = [0, 0, 0, 0]     # 其他区域完全透明
    
    # 转换回PIL图像
    result = Image.fromarray(result_array, 'RGBA')
    return result

# 使用示例
stamp = create_calligraphy_stamp("书法文字", font_path="方圆印章篆体.ttf")
stamp.save("calligraphy_stamp.png")