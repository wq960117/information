from django.db import models

#
# # 用户表
# class User(models.Model):
#     email=models.EmailField()     #邮箱
#     password=models.CharField(max_length=255)     #密码
#     img=models.CharField(max_length=255)
#     name=models.CharField(max_length=30)
#     integral=models.IntegerField(default=0)      #积分
#     invitation_code=models.CharField(max_length=255)      #邀请码
#     is_active=models.IntegerField(default=0)           #是否激活
#     level=models.IntegerField(default=0)       #会员等级
#
# #会员表
# class Member(models.Model):
#     user=models.ForeignKey('User',on_delete=models.CASCADE)
#     level=models.IntegerField()
#     start_time=models.DateTimeField()     #开始时间
#     end_time=models.DateTimeField()       #结束时间
#
# # 会员订单记录表
# class MemberOrder(models.Model):
#     order_sn=models.CharField(max_length=50)    #订单号
#