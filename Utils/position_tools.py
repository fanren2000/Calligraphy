

def parse_position_shift(shift_str):
    """
    解析位置修正字符串，返回左右上下的像素值
    
    Args:
        shift_str (str): 位置修正字符串，格式如 "L10,R10,T10,B10"
    
    Returns:
        dict: 包含左右上下像素值的字典
    """
    # 初始化默认值
    position = {'L': 0, 'R': 0, 'T': 0, 'B': 0}
    
    # 按逗号分割
    parts = shift_str.split(',')
    
    for part in parts:
        part = part.strip().upper()  # 清理空格并转为大写
        
        # 解析每个部分
        if part.startswith(('L', 'R', 'T', 'B')):
            direction = part[0]
            try:
                # 提取数字部分
                value = int(part[1:])
                position[direction] = value
            except ValueError:
                print(f"警告: 无法解析数值 '{part[1:]}' 在 '{part}' 中")
    
    return position

def apply_position_shift(base_x, base_y, width, height, shift_str, style="traditional"):
    """
    应用位置修正到基础坐标
    
    Args:
        base_x (int): 基础X坐标
        base_y (int): 基础Y坐标
        width (int): 元素宽度
        height (int): 元素高度
        shift_str (str): 位置修正字符串
    
    Returns:
        tuple: 修正后的 (x, y, width, height)
    """
    shifts = parse_position_shift(shift_str)
    
    # 应用修正
    if style == "traditional":
        new_x = base_x - shifts['L'] + shifts['R']
        new_y = base_y - shifts['T'] + shifts['B']
        new_width = width - shifts['L'] + shifts['R']
        new_height = height + shifts['T'] - shifts['B']
    else:
        new_x = base_x + shifts['L'] - shifts['R']
        new_y = base_y + shifts['T'] - shifts['B']
        new_width = width - shifts['L'] - shifts['R']
        new_height = height - shifts['T'] - shifts['B']
    
    return new_x, new_y, new_width, new_height

def format_position_shift(left=0, right=0, top=0, bottom=0):
    """
    将左右上下的像素值格式化为位置修正字符串
    
    Args:
        left (int): 左偏移
        right (int): 右偏移  
        top (int): 上偏移
        bottom (int): 下偏移
    
    Returns:
        str: 格式化的位置修正字符串
    """
    parts = []
    if left != 0:
        parts.append(f"L{left}")
    if right != 0:
        parts.append(f"R{right}")
    if top != 0:
        parts.append(f"T{top}")
    if bottom != 0:
        parts.append(f"B{bottom}")
    
    return ','.join(parts) if parts else "L0,R0,T0,B0"

# 使用示例
# if __name__ == "__main__":
#     # 示例1: 解析位置修正
#     shift_str = "L10,R5,T8,B12"
#     position = parse_position_shift(shift_str)
#     print(f"解析结果: {position}")
#     # 输出: {'L': 10, 'R': 5, 'T': 8, 'B': 12}
    
#     # 示例2: 应用位置修正
#     base_x, base_y = 100, 100
#     width, height = 200, 150
#     new_pos = apply_position_shift(base_x, base_y, width, height, shift_str)
#     print(f"修正后位置: {new_pos}")
#     # 输出: (105, 96, 185, 130)
    
#     # 示例3: 格式化位置修正
#     formatted = format_position_shift(left=15, top=20, bottom=5)
#     print(f"格式化结果: {formatted}")
#     # 输出: L15,T20,B5
    
#     # 示例4: 处理各种格式
#     test_cases = [
#         "L10,R10,T10,B10",
#         "l5, r8, t3, b2",  # 大小写混合
#         "T15,B5",           # 只指定部分方向
#         "L20",              # 只指定一个方向
#     ]
    
#     for case in test_cases:
#         result = parse_position_shift(case)
#         print(f"'{case}' -> {result}")