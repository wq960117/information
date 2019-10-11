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
@task
def sendmail(email,token):
    # print(email)
    send_m = EmailMessage('欢迎注册',"欢迎你:<a href=' " + token + "'>点此</a >点此链接进行激活",settings.DEFAULT_FROM_EMAIL, [email, '1334178184@qq.com'])
    send_m.content_subtype = 'html'
    send_m.send()
    time.sleep(10)
    return True
