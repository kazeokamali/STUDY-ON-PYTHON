from datetime import datetime, timedelta
import time

# 获取当前日期
now = datetime.now()

# 创建一个表示今天 12:00 的 datetime 对象
noon = datetime(year=now.year, month=now.month, day=now.day, hour=12)

# 如果现在的时间已经超过了 12:00，那么我们应该获取明天 12:00 的时间戳
if now > noon:
    noon = noon + timedelta(days=1)

# 转换为时间戳
timestamp = time.mktime(noon.timetuple())

print(timestamp)
