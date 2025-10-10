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

def get_vertical_lunar_date():
    """获取正确的竖排农历日期（数字保持完整竖排）"""
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
    
    # 农历日期（保持完整数字）
    lunar_days = {
        1: "初一", 2: "初二", 3: "初三", 4: "初四", 5: "初五", 6: "初六", 7: "初七", 8: "初八", 9: "初九", 10: "初十",
        11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五", 16: "十六", 17: "十七", 18: "十八", 19: "十九", 20: "二十",
        21: "廿一", 22: "廿二", 23: "廿三", 24: "廿四", 25: "廿五", 26: "廿六", 27: "廿七", 28: "廿八", 29: "廿九", 30: "三十"
    }
    
    day_text = lunar_days.get(lunar.lunar_day, "初一")
    
    # 正确的竖排格式：每列包含完整的文字
    # 例如："三十"应该在一列中竖排显示，而不是拆成"三"和"十"两列
    # 正确的竖排格式：月份永远包含"月"字
    return [
        ["岁"],          # 第一列
        ["次"],          # 第二列
        [stem_char],     # 第三列：天干
        [branch_char],   # 第四列：地支
        ["年"],          # 第五列
        [month_char],    # 第六列：月份数字
        ["月"],          # 第七列："月"字（永远显示）
        [day_text[0]],   # 第八列：日期第一部分
        [day_text[1]] if len(day_text) > 1 else [""]  # 第九列：日期第二部分
    ]
