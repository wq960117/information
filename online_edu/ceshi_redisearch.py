# from redisearch import Client, TextField
# # 创建一个客户端与给定索引名称
# client = Client('AtIndex',host='120.27.246.172',port='6666')
#
#
# #创建索引定义和模式
# client.create_index((TextField('title'), TextField('body')))
#
# #索引文
# client.add_document('doc3', title = '你好啊', body = '我在学习人工智能',language='chinese')
#
# # 查找搜索
# res = client.search("人工智能")
#
# print(res.docs[0].title)

"""
python中时间差中seconds和total_seconds
在python中经常会用到计算两个时间差，两个日期类型进行相减可以获取到时间差

经常会使用seconds来获取，其实seconds获取的是时间差的秒数，遗漏了天

seconds是获取时间部分的差值，而total_seconds()是获取两个时间之间的总差
"""
import datetime
# t1 = datetime.datetime.strptime("2019-10-18", "%Y-%m-%d")
# t2 = datetime.datetime.strptime("2018-10-18 10:31:20", "%Y-%m-%d %H:%M:%S")
# interval_time = (t2 - t1).seconds  # 输入的结果：7200
# total_interval_time = (t2 - t1).total_seconds() # 输出结果也是: 266400
# print(interval_time)
# print(total_interval_time)
#
# date_now=datetime.datetime.now().strftime('%Y-%m-%d')
# date_now=datetime.datetime.now().strftime('%Y-%m-%d')
# date_now=datetime.datetime.strptime(date_now, "%Y-%m-%d")
# if date_now > t1:
#     print('11111111111')
# if date_now==t1:
#     print('2222222')
# total_interval_time = (date_now-t1).total_seconds()
# print(total_interval_time)
from edu.models import *
all_act = Act.objects.all()
for act in all_act:

    date_now=datetime.datetime.now()
    print(date_now)
    print(type(date_now))
    start_time = act.data
    # 计算活动开始时间对于
    total_interval_time = (start_time - date_now).total_seconds()
    print(total_interval_time)
    # 以小时计算活动时间和当前时间的差值
    time_value = total_interval_time / 3600
    print('距离活动还有' + str(time_value)+'个小时')
