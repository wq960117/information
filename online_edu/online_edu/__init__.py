# import os
# import celery
import pymysql
# from django.conf import settings
#
pymysql.install_as_MySQLdb()
#
# # 项目名称
# project_name = 'online_edu'
# project_settings = '%s.settings' % project_name
#
# # 注册环境变量
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)
#
# app = celery.Celery(project_name,
#                     # 我使用的是阿里云ip
#                     backend='amqp://root:root@120.27.246.172:5672/myvhost',
#                     broker='amqp://root:root@120.27.246.172:5672/myvhost')
#
#
# # 从默认的配置文件读取配置信息
# app.config_from_object('django.conf:settings')
#
# # Celery加载所有注册的应用
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# # 添加定时任务
# """
# app.conf.update(
#     timezone='Asia/Shanghai',
#     enable_utc=True,
#     beat_schedule={
#         'task1': {
#             'task': 'tasks.print_dummy_info',
#             'schedule': crontab(),
#             'args': ('你妈喊你回家吃饭啦', )
#         },
#     },
# )
# """
