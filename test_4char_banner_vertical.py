import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math
import time
from datetime import datetime
from zhdate import ZhDate

from Utils import get_vertical_lunar_date, get_precise_font_metrics, safe_get_font
from Utils import parse_position_shift, apply_position_shift
from Calli_Utils import create_authentic_torn_paper
from Calli_Utils import add_vertical_upper_inscription, add_vertical_lower_inscription, add_special_lower_inscription
from Calli_Utils import add_ink_bleed_effect, add_ink_bleed_effect_enhanced, add_ink_bleed_effect_optimized
from Calli_Utils import get_lishu_vertical_spacing
from Calli_Utils import add_formal_seal, add_note_seal

# 在您的代码中使用
main_font = ImageFont.truetype("ShanHaiBoYaGuLiW-2.ttf", 240)
metrics = get_precise_font_metrics(main_font, "汉")

char_width = metrics['full_width']
char_height = metrics['actual_height']  # 使用实际高度，而不是包含边距的高度

def calculate_smart_spacings(char_data):
    """
    改进的智能间距计算函数
    解决稀疏字和密集字之间间距过小的问题
    """
    spacings = []
    
    for i in range(len(char_data) - 1):
        current_char = char_data[i]
        next_char = char_data[i + 1]
        
        # 基础间距（整体偏宽松）
        base_spacing = -15
        
        # 1. 根据笔画密度调整（主要修正点）
        density_adjustment = 0
        if current_char["density"] == "sparse" and next_char["density"] == "dense":
            density_adjustment = 12   # 修正：稀疏字接密集字，间距要更大（正值）
        elif current_char["density"] == "dense" and next_char["density"] == "sparse":
            density_adjustment = 6   # 密集字接稀疏字，间距稍大
        elif current_char["density"] == "sparse" and next_char["density"] == "sparse":
            density_adjustment = 8   # 稀疏字接稀疏字，保持适度距离
        elif current_char["density"] == "dense" and next_char["density"] == "dense":
            density_adjustment = -3  # 密集字接密集字，可以紧凑
        
        # 2. 根据结构特征调整
        structure_adjustment = 0
        if current_char["structure"] == "simple" and next_char["structure"] == "complex":
            structure_adjustment = 6   # 简单字接复杂字，需要更多空间
        elif current_char["structure"] == "complex" and next_char["structure"] == "simple":
            structure_adjustment = 2   # 复杂字接简单字，适度空间
        elif current_char["structure"] == "complex" and next_char["structure"] == "complex":
            structure_adjustment = -4  # 复杂字接复杂字，可以紧凑
        
        # 3. 特殊字对处理（针对"一马当先"优化）
        special_pair_adjustment = 0
        current_char_name = current_char["char"]
        next_char_name = next_char["char"]
        
        special_pairs = {
            ("一", "马"): 18,    # "一"和"马"之间需要更多空间
            ("一", "当"): 8,     # "一"和其他密集字都需要空间
            ("一", "先"): 8,
            ("马", "当"): -8,    # "马"和"当"可以紧凑
            ("当", "先"): -3,    # "当"和"先"适度紧凑
        }
        
        special_pair_adjustment = special_pairs.get(
            (current_char_name, next_char_name), 0
        )
        
        # 4. 笔画数差异调整
        stroke_adjustment = 0
        stroke_diff = current_char["strokes"] - next_char["strokes"]
        if stroke_diff < -3:  # 当前字比下一字笔画少很多
            stroke_adjustment = 6   # 需要更多过渡空间
        elif stroke_diff > 3:  # 当前字比下一字笔画多很多
            stroke_adjustment = 2   # 需要适度空间
        
        # 最终间距计算
        final_spacing = (base_spacing + 
                        density_adjustment + 
                        structure_adjustment + 
                        special_pair_adjustment + 
                        stroke_adjustment)
        
        # 限制间距范围（避免极端值）
        final_spacing = max(-30, final_spacing)        # min(-5, final_spacing)
        
        spacings.append(final_spacing)
        
        # 调试信息
        print(f"间距计算: '{current_char_name}'→'{next_char_name}'")
        print(f"  基础: {base_spacing}, 密度调整: {density_adjustment}")
        print(f"  结构调整: {structure_adjustment}, 特殊对调整: {special_pair_adjustment}")
        print(f"  笔画调整: {stroke_adjustment}, 最终: {final_spacing}")
    
    return spacings

def calculate_smart_spacings_simple(char_data):
    """
    简化版的智能间距计算（更稳定）
    """
    spacings = []
    
    # 预定义的理想间距（基于书法美学）
    ideal_spacings = {
        # (当前字类型, 下一字类型): 理想间距
        ("sparse", "dense"): -8,    # 稀疏→密集：较大空间
        ("sparse", "medium"): -10,  # 稀疏→中等：适度空间
        ("sparse", "sparse"): -12,  # 稀疏→稀疏：较小空间
        ("dense", "sparse"): -12,   # 密集→稀疏：适度空间
        ("dense", "medium"): -18,   # 密集→中等：紧凑
        ("dense", "dense"): -22,    # 密集→密集：很紧凑
        ("medium", "sparse"): -10,  # 中等→稀疏：适度空间
        ("medium", "medium"): -16,  # 中等→中等：适中
        ("medium", "dense"): -20,   # 中等→密集：紧凑
    }
    
    for i in range(len(char_data) - 1):
        current_char = char_data[i]
        next_char = char_data[i + 1]
        
        # 获取理想间距
        spacing_key = (current_char["density"], next_char["density"])
        ideal_spacing = ideal_spacings.get(spacing_key, -15)
        
        # 根据特殊字对微调
        current_char_name = current_char["char"]
        next_char_name = next_char["char"]
        
        special_adjustments = {
            ("一", "马"): 4,    # "一马"组合需要额外空间
            ("一", "当"): 3,
            ("一", "先"): 3,
            ("马", "当"): -2,   # "马当"可以更紧凑
        }
        
        adjustment = special_adjustments.get(
            (current_char_name, next_char_name), 0
        )
        
        final_spacing = ideal_spacing + adjustment
        
        spacings.append(final_spacing)
    
    return spacings

# 测试函数
def test_smart_spacings():
    """
    测试智能间距计算
    """
    # 模拟"一马当先"的字数据
    test_data = [
        {"char": "一", "strokes": 1, "structure": "simple", "density": "sparse"},
        {"char": "马", "strokes": 3, "structure": "complex", "density": "dense"},
        {"char": "当", "strokes": 6, "structure": "balanced", "density": "dense"},
        {"char": "先", "strokes": 6, "structure": "balanced", "density": "dense"}
    ]
    
    print("=== 完整版智能间距计算 ===")
    spacings1 = calculate_smart_spacings(test_data)
    print(f"完整版结果: {spacings1}")
    
    print("\n=== 简化版智能间距计算 ===")
    spacings2 = calculate_smart_spacings_simple(test_data)
    print(f"简化版结果: {spacings2}")
    
    return spacings1, spacings2


def create_vertically_centered_banner(text_chars, position_shift=None):
    """修正垂直居中的横幅"""
    tear_intensity = 0.15       # 0.35, 0.40, 0.45
    
    paper = create_authentic_torn_paper("v_wide_handscroll", "xuan", tear_intensity)
    # paper = paper.resize(paper_size)
    draw = ImageDraw.Draw(paper)
    
    width, height = paper.size
    
    main_font = safe_get_font("FZDaCaoS-R-GB.ttf", 240)       # FZZJ-XTCSJW: 方正字迹-邢体草书简体; FZDaCaoS-R-GB: 方正大草简体（毛泽东书法字体）
    
    # 获取精确的字体度量
    metrics = get_precise_font_metrics(main_font, "汉")
    char_width = metrics['full_width']
    char_height = metrics['full_height']
    print(f'char height: {char_height}')

    actual_char_height = metrics['actual_height']
    print(f'char actual height: {actual_char_height}')
    ascent = metrics['ascent']
    
    # 🎯 关键修正：正确的垂直居中
    total_chars = len(text_chars)
    # 计算隶属的字间距
    # 笔画数据库（简化版）
    stroke_data = {
        "一": {"strokes": 1, "structure": "simple", "density": "sparse"},
        "马": {"strokes": 3, "structure": "complex", "density": "medium"},
        "当": {"strokes": 6, "structure": "balanced", "density": "dense"},
        "先": {"strokes": 6, "structure": "balanced", "density": "dense"}
    }
    
    temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 计算每个字的尺寸和间距
    char_data = []
    for char in text_chars:
        bbox = temp_draw.textbbox((0, 0), char, font=main_font)
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        
        char_info = stroke_data.get(char, {"strokes": 5, "structure": "balanced", "density": "medium"})
        char_data.append({
            "char": char,
            "width": char_width,
            "height": char_height,
            "strokes": char_info["strokes"],
            "density": char_info["density"],
            "structure": char_info["structure"]
        })
    
    # 智能计算间距
    spacings = calculate_smart_spacings(char_data)

    total_height = sum([data["height"] for data in char_data]) + sum(spacings)
    max_width = max([data["width"] for data in char_data])
    
    # 水平居中
    start_x = (width ) / 2
    
    # 🎯 垂直居中修正：考虑基线位置
    # 传统方法：start_y = (height - char_height) / 2  ← 这是错误的！
    # 正确方法：
    start_y = (height - total_height) / 2 - metrics['descent'] * 0.5

    # if position_shift:
    #     start_x, start_y, width_new, width_height = apply_position_shift(start_x, start_y, width, height, position_shift)
    
    print(f"🎯 修正后的布局参数:")
    print(f"   字体实际高度: {actual_char_height}")
    print(f"   字体总高度: {metrics['full_height']}")
    print(f"   上边距(ascent): {ascent}")
    print(f"   下边距(descent): {metrics['descent']}")
    print(f"   起始X坐标: {start_x}")
    print(f"   起始Y坐标: {start_y}")

    current_y = start_y
    
    # 绘制文字（从上到下）
    for i, data in enumerate(char_data):
        char_x = start_x - data["width"] // 2
        
        # 绘制文字
        shadow_color = (0, 0, 0, 80)
        text_color = (0, 0, 0, 255)
        
        draw.text((char_x + 2, current_y + 2), data["char"], font=main_font, fill=shadow_color)
        draw.text((char_x, current_y), data["char"], font=main_font, fill=text_color)
        
        # 更新位置（使用智能间距）
        if i < len(char_data) - 1:
            current_y += data["height"] + spacings[i]
    
    return paper


# ==================== 完整作品创建函数 ====================

def create_complete_banner(text, layout="traditional", 
                          paper_size=(1000, 2000),  # 🆕 纸张尺寸参数
                          add_upper=False, recipient_info=None,
                          add_ink_bleed=False, ink_intensity=0.3,
                          author_name="某某", include_date=True):
    """
    完整书法横幅创建函数 - 支持自定义纸张尺寸
    
    Args:
        text: 四个汉字
        layout: "traditional" 或 "modern"
        paper_size: (width, height) 元组，纸张尺寸 🆕
        add_upper: 是否添加上款
        recipient_info: 受赠人信息
        add_ink_bleed: 是否添加墨迹渗透
        ink_intensity: 墨迹强度
        author_name: 作者姓名
        include_date: 是否包含日期
    """
    
    if len(text) != 4:
        raise ValueError("请提供四个汉字")
    
    text_chars = list(text)
    width, height = paper_size
    
    print(f"=== 创建{layout}风格横幅: {text} ===")
    print(f"📐 纸张尺寸: {width} × {height} 像素 (比例: {width/height:.1f}:1)")
    
    # 创建基础横幅
    if layout == "traditional":
        position_shift_str = "R20"
        banner = create_vertically_centered_banner(text_chars, position_shift_str)
        print("🎋 传统布局: 竖排主体 + 竖排落款")
    else:
        # banner = create_modern_banner(text_chars, paper_size)
        print("🏙️ 现代布局: 竖排主体 + 竖排落款")
    
    # 添加竖排上款
    if add_upper and recipient_info:
        banner = add_vertical_upper_inscription(
            banner, 
            recipient_info['name'],
            recipient_info.get('honorific', '先生'),
            recipient_info.get('humble_word', '雅正'),      # 这里雅正是缺省值
            layout=layout,
            top_margin=60,
            horizontal_margin=110
        )
    
    # 添加竖排下款
    lower_inscription_bottom_margin = 60
    banner = add_special_lower_inscription(
        banner, 
        author_name, 
        "叹舞者冲天一字马",
        include_date,
        layout=layout,
        bottom_margin = lower_inscription_bottom_margin
    )
    
    # 添加墨迹渗透效果
    if add_ink_bleed:
        # 添加墨迹渗透效果
        bleeding_intensity = 0.45
        banner = add_ink_bleed_effect_optimized(banner, bleeding_intensity) 
        print(f"🎨 添加墨迹渗透效果，强度: {ink_intensity}")


    banner = add_formal_seal(banner, author_name, (60, 600), 100, 0.85)   


    # banner = add_note_seal(banner, "耗气长存", (width - 150, height - 160), 100)  # 耗气长存
    
    return banner
# ==================== 预设配置 ====================

def create_banner_presets():
    """创建横幅预设配置"""
    
    presets = {
        "traditional_formal": {
            "description": "传统正式横幅",
            "params": {
                "layout": "traditional",
                "add_upper": True,
                "add_ink_bleed": True,
                "ink_intensity": 0.2
            }
        },
        "modern_artistic": {
            "description": "现代艺术横幅", 
            "params": {
                "layout": "modern",
                "add_upper": False,
                "add_ink_bleed": True,
                "ink_intensity": 0.5
            }
        },
        "minimalist": {
            "description": "极简风格横幅",
            "params": {
                "layout": "traditional", 
                "add_upper": False,
                "add_ink_bleed": False
            }
        }
    }
    
    return presets

def apply_banner_preset(text, preset_name="traditional_formal", **kwargs):
    """应用横幅预设"""
    presets = create_banner_presets()
    
    if preset_name not in presets:
        print(f"预设 '{preset_name}' 不存在，使用传统预设")
        preset_name = "traditional_formal"
    
    preset = presets[preset_name]
    print(f"应用预设: {preset_name} - {preset['description']}")
    
    # 合并参数
    params = {**preset['params'], **kwargs}
    
    return create_complete_banner(text, **params)

def usage_guide():
    """使用指南"""
    
    print("=== 四字横幅系统使用指南 ===\n")
    
    guide = {
        "基础使用": [
            "create_complete_banner('厚德载物') - 最简单用法",
            "create_complete_banner('宁静致远', layout='modern') - 现代布局",
            "create_complete_banner('天道酬勤', add_ink_bleed=True) - 带墨迹效果"
        ],
        "高级功能": [
            "添加上款: add_upper=True + recipient_info参数",
            "墨迹渗透: add_ink_bleed=True + ink_intensity控制强度", 
            "作者署名: author_name参数设置下款",
            "预设系统: apply_banner_preset()快速应用配置"
        ],
        "参数说明": {
            "text": "四个汉字，如'厚德载物'",
            "layout": "'traditional'传统或'modern'现代",
            "add_upper": "是否添加上款",
            "recipient_info": "受赠人信息字典",
            "add_ink_bleed": "是否添加墨迹渗透", 
            "ink_intensity": "墨迹强度0.1-1.0",
            "author_name": "下款作者姓名"
        }
    }
    
    for category, content in guide.items():
        print(f"📖 {category}:")
        if isinstance(content, list):
            for item in content:
                print(f"   • {item}")
        else:
            for key, value in content.items():
                print(f"   {key}: {value}")
        print()

def quick_start_example():
    """快速开始示例"""
    
    print("=== 快速开始示例 ===\n")
    
    # 最简单的使用方式
    # print("🚀 最简单用法:")
    # simple_banner = create_complete_banner("吉祥如意")
    # simple_banner.save("banner_simple.png")
    # print("   创建: banner_simple.png")
    
    # # 带效果的用法
    # print("\n🎨 带效果用法:")
    # effect_banner = create_complete_banner(
    #     "福寿安康",
    #     add_ink_bleed=True,
    #     ink_intensity=0.4
    # )
    # effect_banner.save("banner_with_effects.png")
    # print("   创建: banner_with_effects.png")
    
    # 完整用法的用法
    print("\n💎 完整用法:")
    complete_banner = create_complete_banner(
        "一马当先",      # "一马当先", "气势如肱", "一馬當先"
        layout="traditional",
        add_upper=True, 
        recipient_info={"name": "认真儿", "honorific": "主播", "humble_word": "惠存"},      # 雅正
        add_ink_bleed=True,
        ink_intensity=0.3,
        author_name="玻璃耗子"
    )
    complete_banner.save("banner_vertical_complete.png")
    print("   创建: banner_vertical_complete.png")

# ==================== 主函数 ====================

if __name__ == "__main__":
    print("四字横幅创作系统")
    print("=" * 50)
    
    # 演示所有功能
    # demo_all_banner_types()
    # demo_ink_bleed_effects() 
    # demo_different_layouts()
    quick_start_example()
    
    print("\n🎉 所有演示完成！")
    print("生成的PNG文件包含:")
    print("  • 不同风格的横幅布局")
    print("  • 不同强度的墨迹效果") 
    print("  • 完整的上下款系统")
    print("  • 预设配置应用")