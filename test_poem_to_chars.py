import re

def poem_to_characters(poem_text):
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

# 示例
poem = """
静夜思
床前明月光，疑是地上霜。
举头望明月，低头思故乡。
"""

char_list = poem_to_characters(poem)
print("字列表:", char_list)
print("总字数:", len(char_list))


def process_poem_for_printing(poem_text, columns=4):
    """为印刷准备的诗歌处理"""
    
    # 移除所有非中文字符（保留汉字）
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', poem_text)
    
    print(f"提取到 {len(chinese_chars)} 个汉字")
    print("字序列:", ''.join(chinese_chars))
    
    # 按列分组
    result_columns = []
    for i in range(0, len(chinese_chars), columns):
        column = chinese_chars[i:i + columns]
        result_columns.append(column)
    
    return result_columns

def save_poem_characters(poem_text, filename):
    """保存处理后的字序列到文件"""
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', poem_text)
    
    with open(filename, 'w', encoding='utf-8') as f:
        # 保存为单行（方便复制）
        f.write(''.join(chinese_chars) + '\n\n')
        
        # 保存为每字一行（方便计数）
        for char in chinese_chars:
            f.write(char + '\n')
    
    print(f"已保存到 {filename}")

# 综合示例
if __name__ == "__main__":
    test_poems = [
        """
        静夜思
        床前明月光，疑是地上霜。
        举头望明月，低头思故乡。
        """,
        
        """
        《相思》
        红豆生南国，春来发几枝。
        愿君多采撷，此物最相思。
        """,
        
        """
        悯农
        锄禾日当午，汗滴禾下土。
        谁知盘中餐，粒粒皆辛苦。
        """
    ]
    
    for i, poem in enumerate(test_poems, 1):
        print(f"\n=== 诗歌 {i} ===")
        print("原始:", poem.replace('\n', ' '))
        
        chars = poem_to_characters(poem)
        print("处理后:", ''.join(chars))
        print("字列表:", chars)
        
        # 保存到文件
        save_poem_characters(poem, f"poem_{i}_characters.txt")