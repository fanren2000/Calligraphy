import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math
import time
from datetime import datetime
from zhdate import ZhDate

from Utils import get_vertical_lunar_date, get_precise_font_metrics
from Utils import parse_position_shift, apply_position_shift
from Calli_Utils import create_authentic_torn_paper
from Calli_Utils import add_vertical_upper_inscription, add_vertical_lower_inscription, add_special_lower_inscription
from Calli_Utils import add_ink_bleed_effect, add_ink_bleed_effect_enhanced, add_ink_bleed_effect_optimized
from Calli_Utils import get_lishu_spacing
from Calli_Utils import add_formal_seal, add_note_seal

# ==================== 基础工具函数 ====================

def create_test_image():
    """创建测试书法图像"""
    paper = Image.new('RGB', (400, 200), (248, 240, 228))
    draw = ImageDraw.Draw(paper)
    
    try:
        font = ImageFont.truetype("simkai.ttf", 48)
    except:
        try:
            font = ImageFont.truetype("simsun.ttc", 48)
        except:
            font = ImageFont.load_default()
    
    draw.text((120, 70), "测试文字", fill=(30, 30, 30), font=font)
    return paper

# ==================== 横幅创建函数 ====================

def create_traditional_banner(text_chars, paper_size=(1000, 300)):
    """创建传统从右到左的横幅"""
    if len(text_chars) != 4:
        raise ValueError("横幅应为四个汉字")
    
    # 创建宣纸背景
    paper = create_authentic_torn_paper("handscroll", "xuan", 0.2)
    paper = paper.resize(paper_size)
    
    draw = ImageDraw.Draw(paper)
    
    try:
        # 尝试加载书法字体
        font = ImageFont.truetype("simkai.ttf", 120)
    except:
        try:
            font = ImageFont.truetype("simsun.ttc", 120)
        except:
            font = ImageFont.load_default()
    
    width, height = paper_size
    
    # 传统从右到左布局
    char_width = width // 5
    start_x = width - char_width
    
    print("📜 传统横幅布局（从右到左）:")
    
    for i, char in enumerate(text_chars):
        x_pos = start_x - i * char_width
        y_pos = height // 2 - 60
        
        print(f"  位置 {i+1}: '{char}' at ({x_pos}, {y_pos})")
        draw.text((x_pos, y_pos), char, fill=(30, 30, 30), font=font)
    
    return paper

def create_modern_banner(text_chars, paper_size=(1000, 300)):
    """创建现代从左到右的横幅"""
    paper = create_authentic_torn_paper("handscroll", "xuan", 0.2)
    paper = paper.resize(paper_size)
    
    draw = ImageDraw.Draw(paper)
    
    try:
        font = ImageFont.truetype("simkai.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    width, height = paper_size
    
    # 现代从左到右布局
    char_width = width // 5
    start_x = char_width
    
    print("🏙️ 现代横幅布局（从左到右）:")
    
    for i, char in enumerate(text_chars):
        x_pos = start_x + i * char_width
        y_pos = height // 2 - 60
        
        print(f"  位置 {i+1}: '{char}' at ({x_pos}, {y_pos})")
        draw.text((x_pos, y_pos), char, fill=(30, 30, 30), font=font)
    
    return paper

# ==================== 落款系统 ====================


def add_banner_signature(banner, layout="traditional", author_name="某某"):
    """添加横幅下款"""
    width, height = banner.size
    draw = ImageDraw.Draw(banner)
    
    try:
        small_font = ImageFont.truetype("simkai.ttf", 24)
    except:
        small_font = ImageFont.load_default()
    
    # 根据布局决定落款位置
    if layout == "traditional":
        signature_x = width // 10
        signature_y = height - 60
        signature_text = f"{author_name}书"
    else:
        signature_x = width - 150
        signature_y = height - 60
        signature_text = f"{author_name}书"
    
    draw.text((signature_x, signature_y), signature_text, 
              fill=(80, 80, 80), font=small_font)
    
    print(f"  下款位置: ({signature_x}, {signature_y}) - '{signature_text}'")
    
    return banner

# 修改后的落款函数

def explain_lower_inscription_columns():
    """解释下款分列规则"""
    
    print("=== 下款分列规则 ===\n")
    
    column_rules = {
        "单列下款": {
            "内容": "作者名 + 书",
            "字数": "2-4字",
            "适用": "极简风格、空间有限",
            "示例": "张书法"
        },
        "双列下款": {
            "内容": "时间 + 作者 + 书",
            "字数": "5-8字", 
            "适用": "标准格式、最常见",
            "示例": "甲辰年仲春\n张书法书"
        },
        "三列下款": {
            "内容": "时间 + 地点 + 作者 + 书",
            "字数": "8-12字",
            "适用": "详细记录、重要作品",
            "示例": "岁次甲辰\n于北京\n张书法书"
        },
        "分列原则": {
            "内容分组": "时间、地点、作者信息分开",
            "字数均衡": "每列2-4字，避免过长",
            "阅读顺序": "从右到左，从上到下",
            "视觉平衡": "各列长度相近"
        }
    }
    
    for category, info in column_rules.items():
        print(f"📝 {category}:")
        if isinstance(info, dict):
            for key, value in info.items():
                print(f"   {key}: {value}")
        else:
            print(f"   {info}")
        print()



def create_correct_traditional_banner(text_chars, paper_size=(1000, 300)):
    """正确的传统横幅 - 横排但从右到左"""
    
    if len(text_chars) != 4:
        raise ValueError("横幅应为四个汉字")
    
    # 创建宣纸背景
    paper = create_authentic_torn_paper("handscroll", "xuan", 0.2)
    paper = paper.resize(paper_size)
    
    draw = ImageDraw.Draw(paper)
    
    try:
        # 主体文字用较大字体
        main_font = ImageFont.truetype("simkai.ttf", 120)
    except:
        main_font = ImageFont.load_default()
    
    width, height = paper_size
    
    # 🎯 正确的从右到左排列逻辑
    total_chars = len(text_chars)
    char_width = width // (total_chars + 2)  # 留出边距
    total_text_width = char_width * total_chars
    
    # 起始位置：从右侧开始，但要居中
    start_x = (width - total_text_width) // 2 + total_text_width - char_width
    
    print("📜 传统横幅正确格式:")
    print(f"   文字顺序: {' → '.join(text_chars[::-1])} (从右到左阅读)")
    print(f"   布局参数: 总宽={width}, 字宽={char_width}, 起始X={start_x}")
    
    # 🎯 正确的传统排列：从右到左
    for i, char in enumerate(text_chars):
        # 从右向左递减
        x_pos = start_x - (i * char_width)
        y_pos = height // 2 - 60
        
        print(f"   第{i}字 '{char}': x={x_pos}")
        draw.text((x_pos, y_pos), char, fill=(30, 30, 30), font=main_font)
    
    return paper


# 在您的代码中使用
main_font = ImageFont.truetype("ShanHaiBoYaGuLiW-2.ttf", 240)
metrics = get_precise_font_metrics(main_font, "汉")

char_width = metrics['full_width']
char_height = metrics['actual_height']  # 使用实际高度，而不是包含边距的高度

def create_perfectly_centered_banner(text_chars, paper_size=(1000, 300), position_shift=None):
    """修正垂直居中的横幅"""
    tear_intensity = 0.15       # 0.35, 0.40, 0.45
    
    paper = create_authentic_torn_paper("tall-handscroll", "xuan", tear_intensity)
    # paper = paper.resize(paper_size)
    draw = ImageDraw.Draw(paper)
    
    width, height = paper_size
    
    main_font = ImageFont.truetype("ShanHaiBoYaGuLiW-2.ttf", 260)
    
    # 获取精确的字体度量
    metrics = get_precise_font_metrics(main_font, "汉")
    char_width = metrics['full_width']
    actual_char_height = metrics['actual_height']
    ascent = metrics['ascent']
    
    # 🎯 关键修正：正确的垂直居中
    total_chars = len(text_chars)
    # 计算隶属的字间距
    spacing = get_lishu_spacing(char_width, "traditional")
    total_width = (char_width * total_chars) + (spacing * (total_chars - 1))
    
    # 水平居中
    start_x = (width - total_width) / 2
    
    # 🎯 垂直居中修正：考虑基线位置
    # 传统方法：start_y = (height - char_height) / 2  ← 这是错误的！
    # 正确方法：
    start_y = (height - actual_char_height) / 2 - metrics['descent'] * 0.5

    if position_shift:
        start_x, start_y, width_new, width_height = apply_position_shift(start_x, start_y, width, height, position_shift)
    
    print(f"🎯 修正后的布局参数:")
    print(f"   字体实际高度: {actual_char_height}")
    print(f"   字体总高度: {metrics['full_height']}")
    print(f"   上边距(ascent): {ascent}")
    print(f"   下边距(descent): {metrics['descent']}")
    print(f"   起始X坐标: {start_x}")
    print(f"   起始Y坐标: {start_y}")
    
    # 绘制文字（从右到左）
    for i, char in enumerate(text_chars):
        traditional_index = total_chars - 1 - i
        x_pos = start_x + traditional_index * (char_width + spacing)
        
        draw.text((x_pos, start_y), char, fill=(30, 30, 30), font=main_font)
        print(f"   '{char}' 位置: ({x_pos:.1f}, {start_y:.1f})")
    
    return paper


# ==================== 完整作品创建函数 ====================

def create_complete_banner(text, layout="traditional", 
                          paper_size=(1500, 500),  # 🆕 纸张尺寸参数
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
        banner = create_perfectly_centered_banner(text_chars, paper_size, position_shift_str)
        print("🎋 传统布局: 横排主体 + 竖排落款")
    else:
        banner = create_modern_banner(text_chars, paper_size)
        print("🏙️ 现代布局: 横排主体 + 竖排落款")
    
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
        "颂舞者健美肱肌",
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


    banner = add_formal_seal(banner, author_name, (60, 60), 100)   


    banner = add_note_seal(banner, "耗气长存", (width - 150, height - 160), 100)  # 耗气长存
    
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

# 运行指南
# usage_guide()

def demo_all_banner_types():
    """演示所有横幅类型"""
    
    print("=== 四字横幅完整演示 ===\n")
    
    # 示例1: 传统正式横幅
    print("1. 🎋 传统正式横幅")
    traditional_banner = create_complete_banner(
        text="厚德载物",
        layout="traditional",
        add_upper=True,
        recipient_info={"name": "王明", "honorific": "先生", "humble_word": "雅正"},
        add_ink_bleed=True,
        ink_intensity=0.3,
        author_name="张书法"
    )
    traditional_banner.save("banner_traditional_formal.png")
    print("   ✅ 保存: banner_traditional_formal.png\n")
    
    # 示例2: 现代艺术横幅
    print("2. 🏙️ 现代艺术横幅")
    modern_banner = create_complete_banner(
        text="宁静致远", 
        layout="modern",
        add_upper=False,
        add_ink_bleed=True,
        ink_intensity=0.6,
        author_name="李艺术"
    )
    modern_banner.save("banner_modern_artistic.png")
    print("   ✅ 保存: banner_modern_artistic.png\n")
    
    # 示例3: 极简风格
    print("3. ⚪ 极简风格横幅")
    minimal_banner = create_complete_banner(
        text="天道酬勤",
        layout="traditional",
        add_upper=False,
        add_ink_bleed=False,
        author_name="简书"
    )
    minimal_banner.save("banner_minimalist.png")
    print("   ✅ 保存: banner_minimalist.png\n")
    
    # 示例4: 使用预设
    print("4. 🎯 使用预设配置")
    preset_banner = apply_banner_preset(
        "海纳百川",
        "traditional_formal",
        recipient_info={"name": "李老师", "honorific": "老师", "humble_word": "教正"},
        author_name="王学生"
    )
    preset_banner.save("banner_preset.png")
    print("   ✅ 保存: banner_preset.png\n")

def demo_ink_bleed_effects():
    """演示不同墨迹渗透效果"""
    
    print("=== 墨迹渗透效果演示 ===\n")
    
    test_text = "水墨丹青"
    
    intensities = [0.1, 0.3, 0.6, 0.9]
    
    for intensity in intensities:
        print(f"🎨 墨迹强度: {intensity}")
        banner = create_complete_banner(
            text=test_text,
            layout="traditional",
            add_ink_bleed=True,
            ink_intensity=intensity,
            author_name="墨客"
        )
        banner.save(f"ink_bleed_{intensity}.png")
        print(f"   ✅ 保存: ink_bleed_{intensity}.png")
    
    print()

def demo_different_layouts():
    """演示不同布局"""
    
    print("=== 布局风格演示 ===\n")
    
    test_text = "风华正茂"
    
    # 传统布局
    traditional = create_complete_banner(
        text=test_text,
        layout="traditional", 
        add_upper=True,
        recipient_info={"name": "老王", "honorific": "教授", "humble_word": "指正"},
        author_name="传统书家"
    )
    traditional.save("layout_traditional.png")
    print("🎋 传统布局: layout_traditional.png")
    
    # 现代布局
    modern = create_complete_banner(
        text=test_text,
        layout="modern",
        author_name="现代书家"  
    )
    modern.save("layout_modern.png")
    print("🏙️ 现代布局: layout_modern.png")

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
        "氣勢如肱",         # "气势如肱",
        layout="traditional",
        add_upper=True, 
        recipient_info={"name": "认真儿", "honorific": "主播", "humble_word": "惠存"},      # 雅正
        add_ink_bleed=True,
        ink_intensity=0.3,
        author_name="玻璃耗子"
    )
    complete_banner.save("banner_complete.png")
    print("   创建: banner_complete.png")

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