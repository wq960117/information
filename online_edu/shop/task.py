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

    # 所有活动，精确到日

    # 计算活动开始时间对于
    # 获取当前时间,转为字符串
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    one_act=Act.objects.filter(data=date_now).first()
    print(one_act)
    all_time=Time.objects.filter(act_id=one_act.id).all()
    all_time=TimeModelSerializer(all_time,many=True).data
    # 属性按照日期，在value中包含时间和课程的信息
    conn.hset(one_act.data, one_act.data, json.dumps(all_time))
    conn.expire(one_act.data, 86440)
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

from django.shortcuts import render, HttpResponse, redirect

# @task
# def AddSk():
#     print('定时任务开始')
#     conn = get_redis_connection('default')
#     # 把属于今天的秒杀商品添加到redis
#
#     # 查找当前时间
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d')
#     activeList = Act.objects.filter(data=now_time).all()
#
#     # 查询当前时间的场次
#     for act in activeList:
#         timelist = Time.objects.filter(act_id=act.id).all()  # 该活动下的所有场次
#         alist = []
#         for time in timelist:
#             print(time.start.strftime('%H:%M:%S'))
#             info = {}
#             print(time.start)
#             sklist = Sk.objects.filter(time=time, act_id=act.id).all()
#             skList = SkModelSerializer(sklist, many=True).data
#             mapping = {
#                 "start_time": time.start.strftime('%H:%M:%S'),
#                 "end_time": time.end.strftime('%H:%M:%S'),
#                 "content": skList
#             }
#             info ={
#                 'course_info': mapping
#             }
#             alist.append(info)
#         info = json.dumps(alist)
#         print(info)
#         print(act.title)
#         conn.setex(act.title,info,86400)
#     print("定时任务结束")
#     return HttpResponse('ok')
