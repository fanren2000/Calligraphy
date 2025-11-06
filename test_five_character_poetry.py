from PIL import Image, ImageDraw, ImageFont, ImageFilter
from Utils.font_tools import safe_get_font
from Utils.date_format_tools import get_vertical_lunar_date
from Calli_Utils import add_four_character_seal, add_leisure_oval_seal
from Calli_Utils import poem_to_flat_char_list, convert_poem_to_char_matrix, poem_to_char_matrix
from Calli_Utils import add_organic_torn_mask, safe_apply_mask
from Calli_Utils import create_authentic_paper_texture, add_realistic_aging
from Calli_Utils import apply_seal_safely, create_realistic_seal, add_texture_and_aging
from Calli_Utils import add_circular_seal_with_rotation
from Calli_Utils import add_ink_bleed_effect, add_ink_bleed_effect_optimized
from Calli_Utils import create_authentic_torn_paper, add_vertical_upper_inscription, add_special_lower_inscription
from Calli_Utils import add_formal_seal, add_note_seal
import os
import numpy as np
import random
import math
import re

def diagnose_drawing_issue():
    """诊断绘制印章时撕边消失的问题"""
    
    # 1. 创建有撕边效果的宣纸
    paper = create_authentic_torn_paper("small_xuan", "xuan", 0.5)
    print(f"原始纸张模式: {paper.mode}")
    
    # 检查alpha通道
    if paper.mode == 'RGBA':
        alpha_before = np.array(paper.getchannel('A'))
        print(f"绘制前Alpha唯一值: {np.unique(alpha_before)}")
        print(f"绘制前Alpha形状: {alpha_before.shape}")
    
    # 2. 模拟绘制印章（可能有问题的方式）
    draw = ImageDraw.Draw(paper)  # 这里可能就是问题所在！
    
    # 绘制一个红色方形模拟印章
    bbox = [300, 400, 450, 550]  # 印章位置和大小
    draw.rectangle(bbox, fill=(200, 0, 0, 255))  # 红色，不透明
    
    # 检查绘制后的alpha通道
    if paper.mode == 'RGBA':
        alpha_after = np.array(paper.getchannel('A'))
        print(f"绘制后Alpha唯一值: {np.unique(alpha_after)}")
    
    paper.save("debug_drawing_issue.png")
    return paper

# 运行诊断
diagnose_drawing_issue()

def debug_your_current_code():
    """帮助您调试当前代码"""
    
    print("请告诉我您当前是如何绘制印章的？")
    print("\n可能的问题代码示例：")
    print("""
    # 问题代码1: 直接在有alpha通道的图像上绘制
    paper = create_authentic_torn_paper(...)  # 有alpha通道
    draw = ImageDraw.Draw(paper)  # ← 这里会破坏alpha通道!
    draw.rectangle(..., fill=(255,0,0,255))  # 覆盖alpha值
    
    # 问题代码2: 错误的粘贴方式  
    paper.paste(seal, position)  # ← 没有使用mask参数
    """)
    
    print("\n正确的代码示例：")
    print("""
    # 正确方法1: 使用alpha_composite
    paper = create_authentic_torn_paper(...)
    seal_layer = Image.new('RGBA', paper.size, (0,0,0,0))
    seal_layer.paste(seal, position, seal)
    result = Image.alpha_composite(paper, seal_layer)
    
    # 正确方法2: 分离RGB和Alpha
    paper = create_authentic_torn_paper(...)
    original_alpha = paper.getchannel('A')
    paper_rgb = paper.convert('RGB')
    # ... 在paper_rgb上绘制 ...
    result = paper_rgb.convert('RGBA')
    result.putalpha(original_alpha)
    """)

# 快速测试修复
def quick_fix_test():
    """快速测试修复效果"""
    
    # 创建测试
    paper = create_authentic_torn_paper("small_xuan", "xuan", 0.5)
    paper.save("test_original.png")
    
    # 创建印章
    seal = create_realistic_seal("测试", "square", 150)
    seal.save("test_seal.png")
    
    # 应用印章（使用安全方法）
    result = apply_seal_safely(paper, seal, (200, 300))
    result.save("test_fixed.png")
    
    print("测试完成！请检查:")
    print("- test_original.png: 原始撕边纸张")
    print("- test_seal.png: 印章图像") 
    print("- test_fixed.png: 修复后的效果")
    
    # 验证
    original_alpha = np.array(paper.getchannel('A'))
    fixed_alpha = np.array(result.getchannel('A'))
    
    print(f"原始Alpha唯一值: {np.unique(original_alpha)}")
    print(f"修复后Alpha唯一值: {np.unique(fixed_alpha)}")
    
    if np.array_equal(original_alpha, fixed_alpha):
        print("✓ 撕边效果完美保留！")
    else:
        print("✗ 撕边效果有变化")

def create_vertical_five_character_poem(image, poem_title, 
                                        poem_text, 
                                        layout="traditional", 
                                        add_upper=False, recipient_info=None,
                                        add_ink_bleed=False, ink_intensity=0.3,
                                        author_name="某某", include_date=True):
    """生成真正的竖排五言诗"""
    chars_by_column = 5
    width, height = image.size
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    try:
        large_font = safe_get_font("方正隶书.ttf", 75)        #五言75点；七言60点     || 方正行楷_GBK
        medium_font = safe_get_font("方正隶书.ttf", 55)        #五言55点；七言45点
        small_font = ImageFont.truetype("FZZJ-XTCSJW.ttf", 30)      #方正字迹-邢体草书简体
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    

     # 竖排参数：从右向左，从上到下
    start_x = 1200  # 从右侧开始
    start_y = 150  # 从顶部开始。五言200点；七言150点
    char_spacing = 90  # 字间距（垂直）。五言90点；七言60点
    line_spacing = 120  # 行间距（水平）
    
    # 添加竖排上款
    if add_upper and recipient_info:
        banner = add_vertical_upper_inscription(
            banner, 
            recipient_info['name'],
            recipient_info.get('honorific', '先生'),
            recipient_info.get('humble_word', '雅正'),      # 这里雅正是缺省值
            layout=layout
        )

   

    # 添加标题（竖排在右侧）
    title_chars = list(poem_title)
    title_x = start_x + 180  # 诗句右侧
    title_y_offset = 30
    for i, char in enumerate(title_chars):
        draw.text((title_x, start_y + title_y_offset + i * 60), char, font=medium_font, fill=(0, 0, 0))  


    # 《彩书怨》全文（每个字单独）
    # poem_matrix = poem_to_char_matrix(poem_text, cols=5)
    poem_chars = poem_to_flat_char_list(poem_text)

    print("转换完成的字列：")
    print(poem_chars)
    # 绘制竖排诗文（8列，每列5个字）
    for col in range(8):  # 8句诗
        for row in range(chars_by_column):  # 每句5个字（五言）或七个字（七言）
            char_index = col * chars_by_column + row      #五言5；七言7
            if char_index < len(poem_chars):
                char = poem_chars[char_index]
                char_x = start_x - col * line_spacing
                char_y = start_y + row * char_spacing
                draw.text((char_x, char_y), char, font=large_font, fill=(0, 0, 0))
    
    
    
    # 添加作者"上官婉儿"（竖排在标题右侧）
    author_chars = list(poem_author)
    author_x = char_x - 120
    author_y = start_y + 55
    for i, char in enumerate(author_chars):
        draw.text((author_x, author_y + i * char_spacing), char, font=small_font, fill=(0, 0, 0))

    # 添加竖排下款
    lower_inscription_bottom_margin = 140
    image = add_special_lower_inscription(
        image, 
        author_name, 
        "舞蹈主播生日宴有感",
        include_date,
        layout=layout,
        bottom_margin = lower_inscription_bottom_margin
    )        

    # 添加墨迹渗透效果
    if add_ink_bleed:
        # 添加墨迹渗透效果
        bleeding_intensity = 0.45
        image = add_ink_bleed_effect_optimized(image, bleeding_intensity) 
        print(f"🎨 添加墨迹渗透效果，强度: {ink_intensity}")

    seal_side_len = 120
    seal_vertical_offsize = -10

    image = add_formal_seal(image, author_name, (140, height - lower_inscription_bottom_margin - seal_side_len + seal_vertical_offsize), seal_side_len, 0.75)   

    note_seal_diameter = 100
    image = add_note_seal(image, "耗气长存", (width - 240, height - lower_inscription_bottom_margin + seal_vertical_offsize - note_seal_diameter), note_seal_diameter)  # 

    image = add_leisure_oval_seal(image, "鼠灯十三",  (80, start_y), 120, 30, 3)
    
    return image
  

# 运行修复测试
if __name__ == "__main__":
    print("修复印章绘制导致的撕边消失问题...")
    
    # 显示问题诊断
    # diagnose_drawing_issue()
    
    # 显示正确方法
    # correct_seal_drawing_method()
    
    # 提供调试帮助
    # debug_your_current_code()
    
    # 快速测试
    # quick_fix_test()

    # 创建宣纸
    intensity = 0.35    #, 0.40, 0.45
    bleeding_intensity = 0.45
    paper = create_authentic_torn_paper("large_xuan", "xuan", intensity)
    
    if paper.mode != 'RGBA':
        paper = paper.convert('RGBA')

    poem_title = "贺认真儿芳辰"
    poem_author =  "玻璃耗子"   
    poem_text = """
                花簪欹云鬓，桃靥映霓裳。
                贺客星云集，钻榜翻锦浪。
                樱口呼红烛，玉手分琼酪。
                江城舞彩练，廿载正韶光。
                    """
    ink_intensity = 0.45
    paper = create_vertical_five_character_poem(paper, poem_title, poem_text, "traditional", False, None, True, ink_intensity, poem_author, True)
    
    # 添加墨迹渗透效果
    paper = add_ink_bleed_effect(paper, bleeding_intensity) 
    if paper:
        paper.save(f"five_character_poemtry_{ink_intensity}.png")
        print(f"撕边强度 {intensity} 创建成功")
    else:
        print(f"撕边强度 {intensity} 创建失败")
                
 