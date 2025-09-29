import random

def add_subtle_ink_effect(image, strength=0.1):
    """
     subtle墨迹效果（最保守的版本）
    """
    width, height = image.size
    result = image.copy()
    gray = image.convert('L')
    
    # 只处理文字边缘
    for x in range(width):
        for y in range(height):
            # 如果是背景区域
            if gray.getpixel((x, y)) > 180:
                # 检查周围是否有文字
                has_nearby_text = False
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if gray.getpixel((nx, ny)) < 100:
                                has_nearby_text = True
                                break
                    if has_nearby_text:
                        break
                
                # 如果在文字附近，轻微变暗
                if has_nearby_text and random.random() < strength:
                    r, g, b = result.getpixel((x, y))
                    result.putpixel((x, y), (
                        max(0, r - 5),
                        max(0, g - 5),
                        max(0, b - 5)
                    ))
    
    return result
