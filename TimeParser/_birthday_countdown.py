def get_birthday_countdown(
        birth_month:int,
        birth_day:int,
        name:str="",
        precise:bool=False
    ) -> str:
    '''
    获取距离生日还有多少天
    '''
    from datetime import datetime, timedelta
    now = datetime.now()
    current_year = now.year
    
    try:
        # 尝试创建今年的生日日期（判断闰年兼容性）
        birthday_this_year = datetime(current_year, birth_month, birth_day)
    except ValueError:
        # 处理闰年生日（如2月29日，非闰年时调整为3月1日）
        birthday_this_year = datetime(current_year, 3, 1)
    
    # 判断当前是否在生日当天
    if now.date() == birthday_this_year.date():
        return f"今天是{name}生日，Happy Birthday!"
    
    # 计算下一次生日的年份
    if now > birthday_this_year:
        next_year = current_year + 1
    else:
        next_year = current_year
    
    # 创建下一次生日的时间对象（精确到零点）
    try:
        next_birthday = datetime(next_year, birth_month, birth_day)
    except ValueError:
        next_birthday = datetime(next_year, 3, 1)
    
    # 计算时间差
    time_left = next_birthday - now
    
    # 处理时间差为负数的情况（确保逻辑正确）
    if time_left.total_seconds() < 0:
        next_birthday = datetime(next_year + 1, birth_month, birth_day)
        time_left = next_birthday - now
    
    # 分解天、小时、分钟、秒
    days = time_left.days
    seconds = time_left.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # 如果剩余时间不足一天但大于0秒，且不精确模式，则天数加1（向上取整）
    if not precise and seconds + minutes * 60 + hours * 3600 > 0:
        days += 1
    
    if precise:
        return f"距离{name}生日还有：{days}天 {hours}时 {minutes}分 {seconds}秒"
    else:
        return f"距离{name}生日还有：{days}天"