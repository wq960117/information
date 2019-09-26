from django.db import models
import datetime
class User(models.Model):
    '''用户信息表'''
    username=models.CharField(max_length=20,verbose_name='用户名')
    password=models.CharField(max_length=255,verbose_name='密码')
    pic=models.CharField(max_length=255,verbose_name='用户头像')
    level=models.IntegerField(default=0,verbose_name='用户类型，0普通用户，1普通会员，2高级会员')
    is_active=models.IntegerField(default=0,verbose_name='激活状态，0未激活，1激活')
    integral=models.IntegerField(default=0,verbose_name='积分')
    invitation_code=models.CharField(max_length=50,default='',verbose_name='邀请码')
    token=models.CharField(max_length=255,verbose_name='用户登录生成的token')
    class Meta():
        db_table='user'


class Member(models.Model):
    '''有效会员表'''
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='关联用户ID')
    level=models.IntegerField(default=0,verbose_name='0普通会员，1高级会员')
    start_time=models.DateTimeField(auto_now=True)
    end_time=models.DateTimeField(auto_now_add=True)
    class Meta():
        db_table = 'member'

class MemberOrder(models.Model):
    '''会员订单记录表'''
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='关联用户ID')
    ordersn=models.CharField(max_length=255,verbose_name='订单号')
    level=models.IntegerField(default=0,verbose_name='1普通会员，2高级会员')
    status=models.IntegerField(default=0,verbose_name='支付状态')
    amount=models.DecimalField(max_digits=7,decimal_places=2,verbose_name='总价')
    type=models.IntegerField(default=0,verbose_name='支付方式，0支付宝，1微信')
    serial_number=models.CharField(max_length=255,default='',verbose_name='支付流水号')
    time=models.IntegerField(default=0,verbose_name='会员时长')
    code=models.CharField(max_length=50,default='',verbose_name='邀请码，如果是通过别人的邀请码开通的会员，则填对应邀请码')
    class Meta():
        db_table = 'memberorder'

class UserLevel(models.Model):
    '''用户等级表'''
    level=models.CharField(max_length=20)
    class Meta():
        db_table = 'userlevel'

class UserLevelCondition(models.Model):
    """用户等级条件表"""
    level=models.ForeignKey(UserLevel,on_delete=models.CASCADE,verbose_name='关联等级表ID')
    time=models.DateTimeField(auto_now=True,verbose_name='时长')
    price=models.DecimalField(max_digits=7,decimal_places=2)
    class Meta():
        db_table = 'userlevelcondition'

class ThirdPartyLogin(models.Model):
    '''第三方登录表'''
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='关联用户ID')
    uid=models.CharField(max_length=20,verbose_name='第三方登录平台返回的唯一uid')
    login_type=models.IntegerField(default=0,verbose_name='0微博，1微信，2qq')
    class Meta():
        db_table = 'thridpartylogin'
class SiteMessage(models.Model):
    '''站内信息表'''
    title=models.CharField(max_length=255,verbose_name='站内信息标题')
    content=models.TextField(verbose_name='站内信息内容')
    class Meta():
        db_table = 'sitemessage'
class UserSiteMessage(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='外键关联用户ID')
    SiteMessage_id=models.ForeignKey(SiteMessage,on_delete=models.CASCADE,verbose_name='外键关联站内信息表')
    status=models.IntegerField(verbose_name='状态，0未读，1已读')
    class Meta():
        db_table = 'usersitemessage'

"""路径表"""
class Path(models.Model):
    pic = models.CharField(max_length=50,verbose_name='路径图片')
    path = models.CharField(max_length=255,verbose_name='路径名称')
    info = models.CharField(max_length=255,verbose_name='路径简介')
    studynum = models.IntegerField(default=0,verbose_name='学习人数')
    class Meta:
        db_table = 'path'

"""标签表"""
class Tag(models.Model):
    name = models.CharField(max_length=50,verbose_name='标签名称')
    class Meta:
        db_table = 'tag'


"""阶段表"""
class Path_stage(models.Model):
    stage_name = models.CharField(max_length=50,verbose_name='阶段名称')
    path = models.ForeignKey(Path ,on_delete=models.CASCADE,verbose_name='关联路径')
    sort = models.IntegerField(default=0,verbose_name='排序')
    class Meta:
        db_table = 'path_stage'

"""课程表"""
class Course(models.Model):
    title = models.CharField(max_length=50,verbose_name='课程标题')
    pic = models.CharField(max_length=255,verbose_name='课程图片')
    info = models.CharField(max_length=255,verbose_name='课程简介')
    online = models.IntegerField(default=0,verbose_name='是否上线0没上线,1上线')
    member = models.IntegerField(default=0,verbose_name='是否会员0非会员,1会员,2训练营')
    attention = models.IntegerField(default=0,verbose_name='关注量')
    learn = models.IntegerField(default=0,verbose_name='学过人数')
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name='关联老师')
    comment_num = models.IntegerField(default=0,verbose_name='评论数量')
    path = models.ForeignKey(Path_stage,on_delete=models.CASCADE,verbose_name='关联阶段')
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE,verbose_name='关联标签')
    recommand = models.CharField(max_length=50,verbose_name='推荐课程')
    detail = models.CharField(max_length=200,verbose_name='课程详情')
    section_num = models.IntegerField(default=0,verbose_name='章节数')
    class Meta:
        db_table = 'course'

"""价格表"""
class Price(models.Model):
    type = models.IntegerField(default=0,verbose_name='类型0普通,1会员,2高级会员')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='关联课程')
    discount = models.FloatField(max_length=50,verbose_name='折扣')
    discount_price = models.DecimalField(verbose_name='折扣后价格')
    class Meta:
        db_table = 'price'

"""章节表"""
class Section(models.Model):
    section = models.CharField(max_length=50,verbose_name='课程章节名称')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='关联课程')
    video = models.CharField(max_length=50,verbose_name='视频链接')
    sort = models.IntegerField(default=0,verbose_name='排序')
    class Meta:
        db_table = 'section'