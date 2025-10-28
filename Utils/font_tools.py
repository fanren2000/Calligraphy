from PIL import Image, ImageDraw, ImageFont

def safe_get_font(font_path, size=50):
    """安全的字体加载函数"""
    try:
        # 方法一：直接加载
        return ImageFont.truetype(font_path, size)
    except Exception as e:
        print(f"方法一失败: {e}")
        try:
            # 方法二：指定索引
            return ImageFont.truetype(font_path, size, index=0)
        except Exception as e2:
            print(f"方法二失败: {e2}")
            try:
                # 方法三：使用默认编码
                return ImageFont.truetype(font_path, size, encoding="utf-8")
            except Exception as e3:
                print(f"方法三失败: {e3}")
                # 最终回退到系统字体
                return ImageFont.load_default()
            
def get_precise_font_metrics(font, test_char="汉"):
    """获取精确的字体度量"""
    try:
        # 方法1：使用getbbox（包含边距）
        bbox = font.getbbox(test_char)
        full_width = bbox[2] - bbox[0]
        full_height = bbox[3] - bbox[1]
        
        # 方法2：使用getmetrics获取基线信息
        ascent, descent = font.getmetrics()
        actual_height = ascent + descent
        
        print(f"📐 字体度量信息:")
        print(f"   getbbox 尺寸: {full_width} x {full_height}")
        print(f"   getmetrics 高度: {actual_height} (ascent={ascent}, descent={descent})")
        
        return {
            'full_width': full_width,
            'full_height': full_height,
            'actual_height': actual_height,
            'ascent': ascent,
            'descent': descent
        }
    except:
        # 备用方案
        bbox = font.getbbox(test_char)
        return {
            'full_width': bbox[2] - bbox[0],
            'full_height': bbox[3] - bbox[1],
            'actual_height': bbox[3] - bbox[1],
            'ascent': (bbox[3] - bbox[1]) * 0.8,  # 估算
            'descent': (bbox[3] - bbox[1]) * 0.2
        }

