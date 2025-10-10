import random

def add_texture_and_aging(img, intensity=0.3):
    """添加纹理和老化效果"""
    width, height = img.size
    pixels = img.load()
    
    for i in range(width):
        for j in range(height):
            r, g, b, a = pixels[i, j]
            
            # 只处理非透明像素
            if a > 0:
                # 添加随机噪点模拟纹理
                if random.random() < intensity:
                    variation = random.randint(-20, 20)
                    r = max(0, min(255, r + variation))
                
                # 模拟墨水不均匀
                if random.random() < intensity/2:
                    a = max(0, min(255, a - random.randint(0, 30)))
                
                pixels[i, j] = (r, g, b, a)
    
    return img
