# import time
# from django.core.mail import send_mail
# from celery import task
# from online_edu import settings
# @task
# def send(email):
#     time.sleep(10)
#     token = 'ok'
#     title = '村口集合'
#     content = '<a href="http://127.0.0.1:8000/user/active/?token=' + token + '">激活账号</a>'
#     send_mail(title, content, settings.DEFAULT_FROM_EMAIL, [email], html_message=content)
#     return True

import time
from django.core.mail import EmailMessage
from django.conf import settings
from celery import task
from online_edu import settings
from edu.models import *
import datetime
from django_redis import get_redis_connection
from serializers.serializer import *
import json
@task
def sendmail(email,token):
    print(email,token)
    send_m = EmailMessage('欢迎注册',"欢迎你:<a href='http://127.0.0.1:8000/shop/active/?token="+token+"'>点此链接进行激活</a>",settings.DEFAULT_FROM_EMAIL, [email])
    send_m.content_subtype = 'html'
    send_m.send()
    print('已发送')
    return True
@task
def AddSk():
    print('开始定时任务')
    conn = get_redis_connection('default')
    # 获取当前时间,转为字符串
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    # 所有活动，精确到日
    all_act=Act.objects.all()
    for act in all_act:
        start_time=act.data
        # 计算活动开始时间对于
        today=datetime.datetime.strptime(date_now, "%Y-%m-%d")
        # 日期型之间进行比较
        total_interval_time = (start_time - today).total_seconds()
        # 以小时计算活动时间和当前时间的差值
        time_value=total_interval_time/3600

        print('距离活动还有' + str(time_value)+'个小时')
        if time_value<=24 and time_value>=0:
            all_time=Time.objects.filter(act_id=act.id)
            print(all_time)
            for time in all_time:
                all_sk = Sk.objects.filter(act_id=act.id,time_id=time.id).all()
                print(all_sk)
                print('开始添加活动时间')
                # 当天日期的key 对应第一个value是活动场次，第二个value秒杀产品的信息,第三个value是具体的课程信息
                all_sk = SkModelSerializer(all_sk,many=True).data
                # 遍历场次，属性按照场次
                conn.hset(date_now, time.start, json.dumps(all_sk))
                # key 和属性都按照日期存
                # conn.hset(date_now, date_now, json.dumps(all_sk))
                print('活动时间添加成功')
        print('结束定时任务')
    return True

@task
def DelSk():
    print('定时任务开始')
    conn = get_redis_connection('default')
    # 获取当前日期，到redis中查询
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    date_now = datetime.datetime.strptime(date_now, "%Y-%m-%d")
    # # 获取当天日期redis中所有de数据
    # conn.lrange(date_now,0,-1)
    # # 活动全部结束删除当天所有的活动信息
    # conn.lrem(date_now)
    print(date_now)
    print(type(date_now))
    print('定时任务结束')
