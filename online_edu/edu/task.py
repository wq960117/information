import time
from django.core.mail import send_mail
from celery import task
from online_edu import settings
@task
def send(email):
    time.sleep(10)
    token = 'ok'
    title = '村口集合'
    content = '<a href="http://127.0.0.1:8000/user/active/?token=' + token + '">激活账号</a>'
    send_mail(title, content, settings.DEFAULT_FROM_EMAIL, [email], html_message=content)
    return True
