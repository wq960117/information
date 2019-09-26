from django.db import models


# 用户表
class User(models.Model):
    email=models.EmailField()     #邮箱
    password=models.CharField(max_length=255)     #密码
    img=models.CharField(max_length=255)
    name=models.CharField(max_length=30)
    integral=models.IntegerField(default=0)      #积分
    invitation_code=models.CharField(max_length=255)      #邀请码
    is_active=models.IntegerField(default=0)           #是否激活
    level=models.IntegerField(default=0)       #会员等级

#会员表
class Member(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    level=models.IntegerField()
    start_time=models.DateTimeField()     #开始时间
    end_time=models.DateTimeField()       #结束时间

# 会员订单记录表
class MemberOrder(models.Model):
    order_sn=models.CharField(max_length=50)    #订单号
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    level=models.IntegerField()      #会员级别
    time=models.IntegerField()        #时长
    serial_number=models.CharField(max_length=100)     #流水号
    status=models.IntegerField()       #1待支付   2交易成功
    amount=models.DecimalField(max_digits=7,decimal_places=2)    #总价
    pay_type=models.IntegerField(default=1)    #0支付宝  1微信
    code=models.CharField(max_length=255) #邀请码

# 用户等级表
class UserLevel(models.Model):
    level=models.CharField(max_length=100)     #用户级别

# 用户等级条件表
class UserLevelCondition(models.Model):
    level=models.ForeignKey('UserLevel',on_delete=models.CASCADE)
    time=models.IntegerField()
    amount=models.DecimalField(max_digits=7,decimal_places=0)

# 第三方登录表
class ThirdPartyLogin(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    login_type=models.IntegerField()
    uid=models.CharField(max_length=255)

# 站内信表
class SiteMessage(models.Model):
    title=models.CharField(max_length=100)
    content=models.CharField(max_length=255)

# 用户站内信表
class UserSiteMessage(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    type=models.IntegerField()
    content=models.CharField(max_length=255)
    status=models.IntegerField()       #状态  0未读, 1已读

# 讲师表
class Teacher(models.Model):
    name=models.CharField(max_length=50)
    describe=models.CharField(max_length=255)
    pic=models.CharField(max_length=255)

# 用户关注表
class UserTeacher(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    teacher_id=models.ForeignKey('Teacher',on_delete=models.CASCADE)

# 路径表
class Path(models.Model):
    pic=models.CharField(max_length=255)    #图片
    path=models.CharField(max_length=100)    #路径名称
    info=models.CharField(max_length=200)    #路径简介
    studynum=models.IntegerField()            #学习人数

# 用户路径表
class User_Path(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    path=models.ForeignKey('Path',on_delete=models.CASCADE)

# 阶段表
class Path_stage(models.Model):
    stage_name=models.CharField(max_length=30)
    path=models.ForeignKey('Path',on_delete=models.CASCADE)
    sort=models.IntegerField()

# 课程标签表
class Tag(models.Model):
    name=models.CharField(max_length=30)

# 课程表
class Course(models.Model):
    title=models.CharField(max_length=30)
    pic=models.CharField(max_length=200)
    info=models.CharField(max_length=255)   #简介
    online=models.IntegerField()    #上线状态  0即将上线,1已上线
    member=models.IntegerField()   #是否会员   0非会员  1会员  2训练营
    attention=models.IntegerField()    #关注量
    learn=models.IntegerField()   #学过人数
    teacher=models.ForeignKey('Teacher',on_delete=models.CASCADE)
    comment_num=models.IntegerField()    #评论数





















