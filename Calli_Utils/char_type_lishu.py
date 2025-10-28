# helper functions for lishu character type

def get_lishu_spacing(char_width, style="traditional"):
    """获取隶书专用字间距"""
    
    if style == "traditional":
        # 传统隶书：非常紧凑，字距约为字宽的10-15%
        return char_width * 0.12
    elif style == "modern":
        # 现代隶书：稍宽松，字距约为字宽的15-20%
        return char_width * 0.18
    elif style == "decorative":
        # 装饰性隶书：更宽松，字距约为字宽的20-25%
        return char_width * 0.22
    else:
        # 默认：适中
        return char_width * 0.15
