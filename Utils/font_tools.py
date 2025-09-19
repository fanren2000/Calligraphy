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
