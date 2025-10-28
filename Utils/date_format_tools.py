from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from datetime import datetime
from zhdate import ZhDate

def get_lunar_date():
    """获取传统农历日期"""
    today = datetime.now()
    lunar = ZhDate.from_datetime(today)
    
    # 天干地支纪年
    heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    year_index = (lunar.lunar_year - 4) % 60  # 从甲子年开始
    stem_index = year_index % 10
    branch_index = year_index % 12
    
    year_name = f"{heavenly_stems[stem_index]}{earthly_branches[branch_index]}"
    
    # 农历月份
    lunar_months = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
    month_name = lunar_months[lunar.lunar_month - 1]
    
    
    # 农历日期
    lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                 "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                 "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    
    day_name = lunar_days[lunar.lunar_day - 1]
    
    return [
        f"岁次{year_name}年",
        f"{month_name}{day_name}"
    ]

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
