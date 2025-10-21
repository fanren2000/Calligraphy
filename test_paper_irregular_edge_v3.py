from PIL import Image, ImageDraw, ImageFont, ImageFilter
from Utils.font_tools import safe_get_font
from Utils.date_format_tools import get_vertical_lunar_date
from Calli_Utils.seal_border_fancy_4char import add_four_character_seal
from Calli_Utils import poem_to_flat_char_list, convert_poem_to_char_matrix, poem_to_char_matrix
from Calli_Utils import add_organic_torn_mask, safe_apply_mask
from Calli_Utils import create_authentic_paper_texture, add_realistic_aging
from Calli_Utils import apply_seal_safely, create_realistic_seal, add_texture_and_aging
from Calli_Utils import add_circular_seal_with_rotation
from Calli_Utils import add_ink_bleed_effect, add_ink_bleed_effect_optimized
import os
import numpy as np
import random
import math
import re

def create_authentic_torn_paper(paper_size="small_xuan", paper_type="xuan", tear_intensity=0.4):
    """创建真实的撕边纸张"""
    PAPER_SIZES = {
        "small_xuan": (400, 600),  # 减小尺寸便于测试
        "medium_xuan": (600, 800),
        "large_xuan": (1600, 800),
        "handscroll": (800, 200),
        "album_leaf": (400, 500),
    }
    
    width, height = PAPER_SIZES.get(paper_size, (400, 600))
    
    print(f"创建真实撕边纸张: {width} × {height}, 撕边强度: {tear_intensity}")
    
    try:
        # 1. 创建基础纹理
        paper = create_authentic_paper_texture(width, height, paper_type)
        
        # 2. 创建有机撕边蒙版
        mask = add_organic_torn_mask(width, height, tear_intensity)
        
        # 3. 安全应用蒙版
        final_paper = safe_apply_mask(paper, mask)
        
        # 4. 添加老化效果
        aged_paper = add_realistic_aging(paper, intensity=0.15)
        final_paper_aged = safe_apply_mask(aged_paper, mask)
        
        return final_paper_aged
        
    except Exception as e:
        print(f"创建纸张时出错: {e}")
        # 返回一个简单的备用图像
        return Image.new('RGBA', (width, height), (255, 255, 255, 255))


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


def correct_seal_drawing_method():
    """正确的印章绘制方法"""
    
    # 1. 创建撕边宣纸
    paper = create_authentic_torn_paper("small_xuan", "xuan", 0.5)
    original_alpha = paper.getchannel('A')  # 保存原始alpha通道
    
    print("=== 正确的绘制方法 ===")
    
    # 方法1: 在副本上绘制，然后合并
    def method1_separate_layers():
        """方法1: 分离图层绘制"""
        # 创建RGB副本用于绘制
        paper_rgb = paper.convert('RGB')
        draw = ImageDraw.Draw(paper_rgb)
        
        # 绘制印章（在RGB图像上）
        bbox = [300, 400, 450, 550]
        draw.rectangle(bbox, fill=(200, 0, 0))  # 注意：没有alpha值
        
        # 转换回RGBA并恢复原始alpha通道
        result = paper_rgb.convert('RGBA')
        result.putalpha(original_alpha)
        
        return result
    
    # 方法2: 使用透明图层叠加
    def method2_transparent_layer():
        """方法2: 透明图层叠加"""
        # 创建透明图层用于绘制印章
        seal_layer = Image.new('RGBA', paper.size, (0, 0, 0, 0))
        draw_seal = ImageDraw.Draw(seal_layer)
        
        # 在透明图层上绘制印章
        bbox = [300, 400, 450, 550]
        draw_seal.rectangle(bbox, fill=(200, 0, 0, 200))  # 半透明红色
        
        # 将印章图层合成到纸张上
        result = Image.alpha_composite(paper, seal_layer)
        return result
    
    # 方法3: 手动像素操作（最安全）
    def method3_manual_pixels():
        """方法3: 手动像素操作"""
        paper_array = np.array(paper)
        
        # 印章位置和大小
        seal_x1, seal_y1, seal_x2, seal_y2 = 300, 400, 450, 550
        
        # 只在印章区域内修改RGB值，保持Alpha不变
        for y in range(seal_y1, seal_y2):
            for x in range(seal_x1, seal_x2):
                if 0 <= y < paper_array.shape[0] and 0 <= x < paper_array.shape[1]:
                    # 只修改RGB通道，保持Alpha通道不变
                    paper_array[y, x, 0] = 200  # R
                    paper_array[y, x, 1] = 0    # G  
                    paper_array[y, x, 2] = 0    # B
                    # paper_array[y, x, 3] 保持不变!
        
        result = Image.fromarray(paper_array)
        return result
    
    # 测试所有方法
    methods = {
        "分离图层": method1_separate_layers,
        "透明图层": method2_transparent_layer, 
        "手动像素": method3_manual_pixels
    }
    
    results = {}
    for name, method in methods.items():
        print(f"\n测试方法: {name}")
        try:
            result = method()
            # 验证alpha通道
            alpha_check = np.array(result.getchannel('A'))
            unique_alpha = np.unique(alpha_check)
            print(f"  Alpha唯一值: {unique_alpha}")
            print(f"  撕边保留: {'✓' if len(unique_alpha) > 2 else '✗'}")
            
            results[name] = result
            result.save(f"correct_method_{name}.png")
            
        except Exception as e:
            print(f"  错误: {e}")
    
    return results

# 运行正确的方法测试
# correct_seal_drawing_method()

# 运行诊断
diagnose_drawing_issue()

def create_torn_paper_with_seal_fixed(seal_text="金石之章", seal_size=200, position=(300, 400)):
    """创建带印章的撕边宣纸（修复版）"""
    
    # 1. 创建撕边宣纸
    paper = create_authentic_torn_paper("medium_xuan", "xuan", 0.5)
    original_alpha = paper.getchannel('A').copy()  # 备份alpha通道
    
    # 2. 创建印章图像
    seal = create_realistic_seal(seal_text, "square", seal_size)
    
    # 3. 安全地应用印章（使用透明图层方法）
    paper_with_seal = apply_seal_safely(paper, seal, position)
    
    # 4. 双重保险：恢复原始alpha通道
    paper_with_seal.putalpha(original_alpha)
    
    return paper_with_seal

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

def create_real_vertical_poem(image, poem_title, poem_text, poem_author, poem_note, seal_official_text, seal_recreative_text):
    """生成真正的竖排《彩书怨》"""
    
    draw = ImageDraw.Draw(image)
    
    # 加载字体
    try:
        large_font = safe_get_font("方正行楷_GBK.ttf", 60)        #五言75点；七言55点
        medium_font = safe_get_font("方正行楷_GBK.ttf", 45)        #五言55点；七言45点
        small_font = ImageFont.truetype("FZZJ-XTCSJW.ttf", 30)      #方正字迹-邢体草书简体
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 《彩书怨》全文（每个字单独）
    # poem_matrix = poem_to_char_matrix(poem_text, cols=5)
    poem_chars = poem_to_flat_char_list(poem_text)

    print("转换完成的字列：")
    print(poem_chars)
    
    # print("转换完成的字矩阵：")
    # print(poem_matrix)

    # 竖排参数：从右向左，从上到下
    start_x = 1200  # 从右侧开始
    start_y = 150  # 从顶部开始。五言200点；七言150点
    char_spacing = 70  # 字间距（垂直）。五言90点；七言60点
    line_spacing = 90  # 行间距（水平）
    
    # 绘制竖排诗文（8列，每列5个字）
    for col in range(8):  # 8句诗
        for row in range(7):  # 每句5个字（五言）或七个字（七言）
            char_index = col * 7 + row      #五言5；七言7
            if char_index < len(poem_chars):
                char = poem_chars[char_index]
                char_x = start_x - col * line_spacing
                char_y = start_y + row * char_spacing
                draw.text((char_x, char_y), char, font=large_font, fill=(0, 0, 0))
    
    # 添加标题"彩书怨"（竖排在右侧）
    title_chars = list(poem_title)
    title_x = start_x + 120  # 诗句右侧
    for i, char in enumerate(title_chars):
        draw.text((title_x, start_y + i * 60), char, font=medium_font, fill=(0, 0, 0))   
    
    # 添加作者"上官婉儿"（竖排在标题右侧）
    author_chars = list(poem_author)
    author_x = char_x - 200
    author_y = start_y + 55
    for i, char in enumerate(author_chars):
        draw.text((author_x, author_y + i * char_spacing), char, font=small_font, fill=(0, 0, 0))

    # 添加说明文字
    author_note_chars = list(poem_note)   
    note_start_x = author_x - 35
    note_start_y = author_y
    for i, char in enumerate(author_note_chars):
        draw.text((note_start_x, note_start_y + i * 35), char, font=small_font, fill=(80, 80, 80))

    # 添加日期
    # 日期（右列，与作者名纵向对齐）
    lunar_date_chars = get_vertical_lunar_date()
    
    # 添加"书"字
    lunar_date_chars.append(["书"])

    date_start_x = note_start_x - 35
    date_start_y = author_y  # 与作者名顶部对齐
    
    for row_index, column_chars in enumerate(lunar_date_chars):
        for col_index, char in enumerate(column_chars):
            if char:
                draw.text((date_start_x + col_index * 35, date_start_y + row_index * 35), 
                         char, font=small_font, fill=(80, 80, 80))

    date_end_y = date_start_y + (row_index + 1) * 35    # 计算日期底部变量以使闲章与它对其           

    # 添加印章（在作者旁边）
    # 使用修正后的印章函数
    seal_x = date_start_x - 120
    seal_y = date_start_y + 15
    print(f"seal position: {seal_x, seal_y}")

    # 创建透明图层用于绘制印章
    seal_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    
    seal_layer = add_four_character_seal(seal_layer, seal_official_text, (seal_x, seal_y), 100)
    
    result = Image.alpha_composite(image, seal_layer)

    # 添加闲章（左下角）
    # note_chars = ["唐", "宫", "遗", "韵"]
    note_diameter = 100
    note_center_ratio = 0.3
    note_char_rotation_degree = 25
    note_text = seal_recreative_text
    note_x = seal_x + note_diameter // 2    # 圆形的半径
    note_y = date_end_y - note_diameter // 2    # 圆形的半径
    print(f"seal 2 position: {note_x, note_y}")
    seal2_layer = Image.new('RGBA', result.size, (0, 0, 0, 0))

    seal2_layer = add_circular_seal_with_rotation(seal2_layer, note_text, (note_x, note_y), note_diameter, note_center_ratio, note_char_rotation_degree)
    
    result = Image.alpha_composite(result, seal2_layer)

    # result.save("真正竖排格式_透明图层.png", quality=95)
    # print("生成完成：真正竖排格式.png")
    # print("布局：传统竖排，从右向左，从上到下")
    
    return result
  

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

    poem_title = "认真儿蟾宫折桂赋"
    poem_author =  "玻璃耗子"   
    poem_text = """
                霓裳旋舞动四方，抖音捷报誉飞扬。
                步随鼓韵如龙跃，袖舞春风似凤翔。  
                曼姿力压群芳艳，妙态终登金榜堂。
                今朝捧杯传佳话，丹心不负旧时妆。
                    """
    poem_note = "贺冠绝国潮风华舞赛魁"
    seal_official_text = "玻璃耗子"
    seal_recreative_text = "耗气长存"
    paper = create_real_vertical_poem(paper, poem_title, poem_text, poem_author, poem_note, seal_official_text, seal_recreative_text)
    
    # 添加墨迹渗透效果
    paper = add_ink_bleed_effect(paper, bleeding_intensity) 
    if paper:
        paper.save(f"torn_paper_{intensity}.png")
        print(f"撕边强度 {intensity} 创建成功")
    else:
        print(f"撕边强度 {intensity} 创建失败")
                
 