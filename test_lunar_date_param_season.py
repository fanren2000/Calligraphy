import time
from datetime import datetime
from zhdate import ZhDate

def get_vertical_lunar_date(include_shu=True, include_author=None, include_season=False):
    """获取竖排农历日期 - 修正季节逻辑"""
    today = datetime.now()
    lunar = ZhDate.from_datetime(today)
    
    # 天干地支
    heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    year_index = (lunar.lunar_year - 4) % 60
    stem_char = heavenly_stems[year_index % 10]
    branch_char = earthly_branches[year_index % 12]
    
    # 农历月份
    lunar_months = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
    month_char = lunar_months[lunar.lunar_month - 1]
    
    # 农历日期
    lunar_days = {
        1: "初一", 2: "初二", 3: "初三", 4: "初四", 5: "初五", 6: "初六", 7: "初七", 8: "初八", 9: "初九", 10: "初十",
        11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五", 16: "十六", 17: "十七", 18: "十八", 19: "十九", 20: "二十",
        21: "廿一", 22: "廿二", 23: "廿三", 24: "廿四", 25: "廿五", 26: "廿六", 27: "廿七", 28: "廿八", 29: "廿九", 30: "三十"
    }
    
    day_text = lunar_days.get(lunar.lunar_day, "初一")
    
    # 季节映射（基于农历月份）
    def get_season_by_lunar_month(lunar_month):
        season_mapping = {
            1: "孟春",  2: "仲春",  3: "季春",
            4: "孟夏",  5: "仲夏",  6: "季夏", 
            7: "孟秋",  8: "仲秋",  9: "季秋",
            10: "孟冬", 11: "仲冬", 12: "季冬"
        }
        return season_mapping.get(lunar_month, "")
    
    # 构建基础部分
    date_parts = [
        ["岁"], ["次"], [stem_char], [branch_char], ["年"]
    ]
    
    # 🎯 修正：确保季节功能正常工作
    if include_season:
        # 使用季节模式：只显示季节
        season_text = get_season_by_lunar_month(lunar.lunar_month)
        print(f"🔍 调试信息: lunar_month={lunar.lunar_month}, season_text='{season_text}'")
        
        if season_text and len(season_text) == 2:
            date_parts.append([season_text[0]])  # 孟/仲/季
            date_parts.append([season_text[1]])  # 春/夏/秋/冬
            print(f"✅ 成功添加季节: {season_text}")
        else:
            print(f"❌ 季节获取失败，回退到传统模式")
            # 回退到传统模式
            date_parts.extend([
                [month_char], ["月"], [day_text[0]]
            ])
            if len(day_text) > 1 and day_text[1].strip():
                date_parts.append([day_text[1]])
    else:
        # 传统模式：显示具体月份和日期
        date_parts.extend([
            [month_char], ["月"], [day_text[0]]
        ])
        if len(day_text) > 1 and day_text[1].strip():
            date_parts.append([day_text[1]])
    
    # 添加作者（如果提供）
    if include_author:
        for char in include_author:
            date_parts.append([char])
    
    # 添加"书"字
    if include_shu:
        date_parts.append(["书"])
    
    # 打印最终结果
    final_text = "".join([part[0] for part in date_parts])
    print(f"📅 最终输出: {final_text}")
    
    return date_parts


# 测试函数
def test_season_function():
    """测试季节功能"""
    print("=== 测试季节功能 ===")
    
    # 测试包含季节
    print("\n1. 包含季节:")
    result1 = get_vertical_lunar_date(include_season=True)
    text1 = "".join([part[0] for part in result1])
    print(f"结果: {text1}")
    
    # 测试不包含季节
    print("\n2. 不包含季节:")
    result2 = get_vertical_lunar_date(include_season=False)
    text2 = "".join([part[0] for part in result2])
    print(f"结果: {text2}")
    
    # 测试在落款函数中的调用
    print("\n3. 在落款函数中测试:")
    # 模拟调用
    date_data = get_vertical_lunar_date(include_shu=False, include_author=None, include_season=True)
    date_text = [part[0] for part in date_data if part[0].strip()]
    print(f"日期文本: {''.join(date_text)}")


# 在落款函数中确保正确调用
def add_vertical_lower_inscription(image, author_name="某某", include_date=True, 
                                  layout="traditional", columns=2, location=None,
                                  include_season=False):  # 确保这个参数传递正确
    """修正版竖排下款 - 确保季节参数传递正确"""
    
    print(f"🎨 开始添加落款，include_season={include_season}")
    
    # 生成下款内容
    inscription_parts = []
    
    # 🎯 根据列数组织内容
    if columns == 1:
        inscription_parts.append([author_name, "书"])
        
    elif columns == 2:
        if include_date:
            # 🎯 确保include_season参数正确传递
            date_data = get_vertical_lunar_date(
                include_shu=False, 
                include_author=None, 
                include_season=include_season  # 这里传递参数
            )
            date_text = [part[0] for part in date_data if part[0].strip()]
            inscription_parts.append(date_text)
        
        author_chars = list(author_name) + ["书"]
        inscription_parts.append(author_chars)
        
    elif columns >= 3:
        if include_date:
            # 🎯 确保include_season参数正确传递
            date_data = get_vertical_lunar_date(
                include_shu=False, 
                include_author=None, 
                include_season=include_season  # 这里传递参数
            )
            date_text = [part[0] for part in date_data if part[0].strip()]
            inscription_parts.append(date_text)
        
        if location:
            location_chars = ["于"] + list(location)
            inscription_parts.append(location_chars)
        else:
            inscription_parts.append(["记"])
        
        author_chars = list(author_name) + ["书"]
        inscription_parts.append(author_chars)
    
    print(f"📝 最终落款内容 ({columns}列):")
    for i, column in enumerate(inscription_parts):
        print(f"   第{i+1}列: {''.join(column)}")
    
    # ... 其余绘制代码保持不变
    return image  # 简化返回


# 运行测试
if __name__ == "__main__":
    test_season_function()