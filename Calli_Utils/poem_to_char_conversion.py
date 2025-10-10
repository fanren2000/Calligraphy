import re

def convert_poem_to_chars(poem_text):
    """将诗歌转换为单独的字列表，去除标点符号"""
    
    # 定义中文标点符号（可以根据需要扩展）
    chinese_punctuation = '，。！？；：“”‘’（）【】《》…—～·'
    english_punctuation = ',.!?;:\"\"\'\'()[]<>...-~`'
    all_punctuation = chinese_punctuation + english_punctuation
    
    # 去除所有标点符号
    clean_text = re.sub(f'[{re.escape(all_punctuation)}]', '', poem_text)
    
    # 去除空格和换行符，只保留纯汉字
    clean_text = clean_text.replace(' ', '').replace('\n', '').replace('\r', '')
    
    # 转换为单个字符的列表
    characters = list(clean_text)
    
    return characters

def convert_poem_to_char_matrix(poem_text, cols=None, fill_char='  '):
    """
    将诗歌转换为字矩阵
    Args:
        poem_text: 诗歌文本
        cols: 矩阵列数，如果为None则自动计算
        fill_char: 填充字符，用于对齐矩阵
    """
    # 提取所有汉字
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', poem_text)
    
    if not chinese_chars:
        return []
    
    total_chars = len(chinese_chars)
    
    # 自动计算列数（尽量接近正方形）
    if cols is None:
        cols = int(total_chars ** 0.5)
        # 确保列数合理
        cols = max(3, min(cols, 8))
    
    # 计算需要的行数
    rows = (total_chars + cols - 1) // cols
    
    # 创建矩阵
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            index = i * cols + j
            if index < total_chars:
                row.append(chinese_chars[index])
            else:
                row.append(fill_char)  # 填充空白
        matrix.append(row)
    
    return matrix

def print_character_matrix(matrix, separator='  '):
    """打印字矩阵"""
    for row in matrix:
        print(separator.join(row))

def poem_to_vertical_matrix(poem_text, rows=None, fill_char='  '):
    """
    创建竖排字矩阵（传统书法格式）
    Args:
        poem_text: 诗歌文本
        rows: 每列行数，如果为None则自动计算
        fill_char: 填充字符
    """
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', poem_text)
    
    if not chinese_chars:
        return []
    
    total_chars = len(chinese_chars)
    
    # 自动计算每列行数（传统竖排通常是5-7字）
    if rows is None:
        rows = 5  # 传统诗歌常见的每列字数
    
    # 计算需要的列数
    cols = (total_chars + rows - 1) // rows
    
    # 创建竖排矩阵（转置）
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            index = j * rows + i
            if index < total_chars:
                row.append(chinese_chars[index])
            else:
                row.append(fill_char)
        matrix.append(row)
    
    return matrix

def poem_to_flat_char_list(poem_text):
    """
    将诗歌转换为扁平的字列表
    返回: ["字1", "字2", "字3", ...]
    """
    # 提取所有汉字，去除标点和空白
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', poem_text)
    return chinese_chars

def flat_list_to_matrix(char_list, cols=5):
    """
    将扁平字列表转换为二维矩阵
    Args:
        char_list: 扁平的字列表
        cols: 每行的列数
    """
    matrix = []
    for i in range(0, len(char_list), cols):
        row = char_list[i:i + cols]
        matrix.append(row)
    return matrix

def poem_to_char_matrix(poem_text, cols) :
    poem_chars = poem_to_flat_char_list(poem_text)
    poem_matrix = flat_list_to_matrix(poem_chars, cols=5)
    return poem_matrix


# 示例使用
if __name__ == "__main__":
    poems = [
        # 五言诗
        """
        《静夜思》
        床前明月光，疑是地上霜。
        举头望明月，低头思故乡。
        """,
        
        # 七言诗
        """
        《早发白帝城》
        朝辞白帝彩云间，千里江陵一日还。
        两岸猿声啼不住，轻舟已过万重山。
        """,
        
        # 四言诗
        """
        《关雎》
        关关雎鸠，在河之洲。
        窈窕淑女，君子好逑。
        """
    ]
    
    print("=== 横排字矩阵 ===")
    for i, poem in enumerate(poems, 1):
        print(f"\n诗歌 {i}:")
        matrix = poem_to_character_matrix(poem, cols=5)
        print_character_matrix(matrix)
    
    print("\n" + "="*50)
    print("=== 竖排字矩阵（传统格式）===")
    
    for i, poem in enumerate(poems, 1):
        print(f"\n诗歌 {i} 竖排:")
        vertical_matrix = poem_to_vertical_matrix(poem, rows=5)
        print_character_matrix(vertical_matrix)
