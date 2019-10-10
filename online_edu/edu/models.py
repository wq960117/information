from django.db import models
import datetime


class User(models.Model):
    '''用户信息表'''
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    pic = models.CharField(max_length=255, verbose_name='用户头像')
    level = models.IntegerField(default=0, verbose_name='用户类型，0普通用户，1普通会员，2高级会员')
    is_active = models.IntegerField(default=0, verbose_name='激活状态，0未激活，1激活')
    integral = models.IntegerField(default=0, verbose_name='积分')
    invitation_code = models.CharField(max_length=50, default='', verbose_name='邀请码')
    token = models.CharField(max_length=255, verbose_name='用户登录生成的token')

    class Meta():
        db_table = 'user'
#
#
# class Member(models.Model):
#     '''有效会员表'''
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联用户ID')
#     level = models.IntegerField(default=0, verbose_name='0普通会员，1高级会员')
#     start_time = models.DateTimeField(auto_now=True)
#     end_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta():
#         db_table = 'member'
#
#
# class MemberOrder(models.Model):
#     '''会员订单记录表'''
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联用户ID')
#     ordersn = models.CharField(max_length=255, verbose_name='订单号')
#     level = models.IntegerField(default=0, verbose_name='1普通会员，2高级会员')
#     status = models.IntegerField(default=0, verbose_name='支付状态')
#     amount = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='总价')
#     type = models.IntegerField(default=0, verbose_name='支付方式，0支付宝，1微信')
#     serial_number = models.CharField(max_length=255, default='', verbose_name='支付流水号')
#     time = models.IntegerField(default=0, verbose_name='会员时长')
#     code = models.CharField(max_length=50, default='', verbose_name='邀请码，如果是通过别人的邀请码开通的会员，则填对应邀请码')
#
#     class Meta():
#         db_table = 'memberorder'
#
#
class UserLevel(models.Model):
    '''用户等级表'''
    level = models.CharField(max_length=20)

    class Meta():
        db_table = 'userlevel'


class UserLevelCondition(models.Model):
    """用户等级条件表"""
    level = models.ForeignKey(UserLevel, on_delete=models.CASCADE, verbose_name='关联等级表ID')
    time = models.IntegerField(verbose_name='时长')
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta():
        db_table = 'userlevelcondition'
#
#
# class ThirdPartyLogin(models.Model):
#     '''第三方登录表'''
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联用户ID')
#     uid = models.CharField(max_length=20, verbose_name='第三方登录平台返回的唯一uid')
#     login_type = models.IntegerField(default=0, verbose_name='0微博，1微信，2qq')
#
#     class Meta():
#         db_table = 'thridpartylogin'
#
#
# class SiteMessage(models.Model):
#     '''站内信息表'''
#     title = models.CharField(max_length=255, verbose_name='站内信息标题')
#     content = models.TextField(verbose_name='站内信息内容')
#
#     class Meta():
#         db_table = 'sitemessage'
#
#
# class UserSiteMessage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='外键关联用户ID')
#     SiteMessage_id = models.ForeignKey(SiteMessage, on_delete=models.CASCADE, verbose_name='外键关联站内信息表')
#     status = models.IntegerField(verbose_name='状态，0未读，1已读')
#
#     class Meta():
#         db_table = 'usersitemessage'
#
#
# """路径表"""
#
#
class Path(models.Model):
    pic = models.CharField(max_length=50, verbose_name='路径图片')
    path = models.CharField(max_length=255, verbose_name='路径名称')
    info = models.CharField(max_length=255, verbose_name='路径简介')
    studynum = models.IntegerField(default=0, verbose_name='学习人数')

    class Meta:
        db_table = 'path'

#
# """标签表"""
#
#
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签名称')

    class Meta:
        db_table = 'tag'
#
#
# """阶段表"""
#
#路径-阶段-课程-章节
class Path_stage(models.Model):
    stage_name = models.CharField(max_length=50, verbose_name='阶段名称')
    path = models.ForeignKey(Path, on_delete=models.CASCADE, verbose_name='关联路径')
    sort = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'path_stage'
#
#
# # 老师表
class Teacher(models.Model):
    name = models.CharField(max_length=15, verbose_name='姓名')
    describe = models.CharField(max_length=255, verbose_name='讲师描述')
    pic = models.CharField(max_length=255, verbose_name='头像')
#
#
# """课程表"""
#


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='课程标题')
    pic = models.CharField(max_length=255, verbose_name='课程图片')
    info = models.CharField(max_length=255, verbose_name='课程简介')
    online = models.IntegerField(default=0, verbose_name='是否上线0没上线,1上线')
    member = models.IntegerField(default=0, verbose_name='是否会员，0非会员,1会员,2训练营')
    attention = models.IntegerField(default=0, verbose_name='关注量')
    learn = models.IntegerField(default=0, verbose_name='学过人数')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='关联老师')
    comment_num = models.IntegerField(default=0, verbose_name='评论数量')
    stage = models.ForeignKey(Path_stage, on_delete=models.CASCADE, verbose_name='关联阶段')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='关联标签')
    recommand = models.CharField(max_length=50, verbose_name='推荐课程，0是1否')
    detail = models.CharField(max_length=200, verbose_name='课程详情')
    section_num = models.IntegerField(default=0, verbose_name='章节数')
    path = models.ForeignKey(Path,on_delete=models.CASCADE, verbose_name='所属路径')

    class Meta:
        db_table = 'course'

#
# """价格表"""
#
#
class Price(models.Model):
    type = models.ForeignKey(UserLevel,on_delete=models.CASCADE, verbose_name='类型0普通,1会员,2高级会员')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='关联课程')
    discount = models.FloatField(max_length=50, verbose_name='折扣')
    pre_price=models.DecimalField(max_digits=7,decimal_places=2,verbose_name='原价格')
    discount_price = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='折扣后价格')

    class Meta:
        db_table = 'price'
#
#
# """章节表"""
#
#
class Section(models.Model):
    section = models.CharField(max_length=50, verbose_name='课程章节名称')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='关联课程')
    video = models.CharField(max_length=50, verbose_name='视频链接')
    sort = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'section'
#
#
# # 实验报告
# class Report(models.Model):
#     section_id = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='章节id')
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')
#     report_content = models.CharField(max_length=255, verbose_name='报告内容')
#     report_title = models.CharField(max_length=255, verbose_name='报告标题')
#     report_browse = models.IntegerField(verbose_name='实验报告浏览量')
#     linknum = models.IntegerField(verbose_name='点赞数')
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程id')
#
#
# # 评论表
# class Comment(models.Model):
#     content = models.TextField(verbose_name='评论内容')
#     pid = models.IntegerField(verbose_name='上一级评论id')
#     top = models.IntegerField(verbose_name='顶级评论')
#     type_ud = models.IntegerField(verbose_name='自身级别id')
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')
#     course = models.IntegerField(verbose_name='查询评论id')
#     comment_type = models.IntegerField(default=0, verbose_name='评论类型')
#     status = models.IntegerField(default=0, verbose_name='审核状态，0否1是')
#     reason = models.CharField(max_length=255, verbose_name='失败原因')
#
#
# # 实验问答表
# class Answer(models.Model):
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程id')
#     answer_title = models.CharField(max_length=50, verbose_name='问答标题')
#     answer_content = models.CharField(max_length=255, verbose_name='问答内容')
#     browse_id = models.IntegerField(verbose_name='浏览量')
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')
#     pid = models.IntegerField(verbose_name='上一级评论')
#     top = models.IntegerField(verbose_name='顶级评论')
#     type = models.IntegerField(verbose_name='自身级别评论')
#
#
#
#
# # 用户关注表
# class UserTeacher(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')
#     teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='课程id')
#
#
# # 用户和收藏实验问答表
# class Collect(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户id')
#     find_id = models.IntegerField(verbose_name='寻找对应id')
#     collect_type = models.IntegerField(default=0, verbose_name='收藏类型0实验报告1实验问答')
#
#
# # 课程订单表
# class Cours_order(models.Model):
#     order_number = models.CharField(max_length=100)  # 订单编号
#     user = models.ForeignKey('User', on_delete=models.CASCADE)  # 用户外键
#     course = models.ForeignKey('Course', on_delete=models.CASCADE)  # 课程外键
#     pyt_type = models.IntegerField()  # 支付方式  1微信  2支付宝
#     price = models.DecimalField(max_digits=7, decimal_places=2)  # 商品价格
#     pay_price = models.DecimalField(max_digits=7, decimal_places=2)  # 实际支付
#     preferential_way = models.IntegerField()  # 优惠方式  0 未使用  1积分  2优惠券
#     preferential_money = models.DecimalField(max_digits=7, decimal_places=2)  # 优惠金额
#     order_status = models.IntegerField()  # 订单状态  1待支付  2支付成功
#     code = models.CharField(max_length=100)  # 流水号
#     coupon = models.CharField(max_length=100)  # 优惠码
#
#
# # 积分兑换规则表
# class rule(models.Model):
#     ratio = models.FloatField(default=0.01)  # 兑换比例
#     min_integral = models.IntegerField(default=100)  # 最低兑换门槛
#     max_integral = models.IntegerField(default=10000)  # 最高兑换门槛
#
#
# # 优惠券表
class Coupon(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    count = models.IntegerField()  # 数量
    type = models.IntegerField()  # 类型  1全场通用   2指定商品
    start_time = models.DateTimeField()  # 开始时间
    end_time = models.DateTimeField()  # 结束时间
    condition = models.DecimalField(max_digits=7, decimal_places=2)  # 满多少可以
    integral = models.IntegerField()  # 兑换所需积分数量
    money = models.DecimalField(max_digits=7, decimal_places=2)  # 实际抵消金额
    status = models.IntegerField()  # 状态  1可用  2过期

#
# # 用户优惠卷使用表
# class Integral_coupon(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # 兑换用户
#     coupon_order = models.CharField(max_length=100)  # 优惠券编码
#     count = models.IntegerField()  # 数量
#     start_time = models.DecimalField()  # 使用时间
#     end_time = models.DateTimeField()  # 结束时间
#     coupon_money = models.DecimalField(max_digits=7, decimal_places=2)  # 优惠券金额
#     max_money = models.DecimalField(max_digits=7, decimal_places=2)  # 满多少可以用
#     type = models.IntegerField()  # 类型   1全场通用   2指定商品
#     status = models.IntegerField()  # 状态  1已用  2未用  3过期


# # 积分记录表        总积分
# class Coupon_record(models.Model):
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     x_integral = models.IntegerField()  # 操作类型  1增加  2减少
#     s_integral = models.IntegerField()  # 当前总积分
#     before_integral = models.IntegerField()  # 本次使用积分
#     end_integral = models.IntegerField()  # 使用后剩余积分
#     effect = models.IntegerField()  # 使用方式   1抵扣金额  2优惠卷
#     coupon_code = models.CharField()  # 优惠券码
#
#
# class User_path(models.Model):  # 用户路径表
#     user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # 用户id
#     path_id = models.ForeignKey(Path, null=True, on_delete=models.SET_NULL)  # 路径id
#
#
# class User_course(models.Model):  # 学习记录表
#     course_id = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)  # 课程外键
#     user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # 用户外键
#     section_id = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)  # 章节外键
#     status = models.IntegerField(default=0)  # 完成状态0未完成1完成
#
#
# class Banner(models.Model):  # 焦点图
#     name = models.CharField(max_length=50, unique=True)  # 名称
#     url = models.CharField(max_length=100)  # 跳转链接
#     pic = models.CharField(max_length=100)  # 图片
#     type = models.IntegerField()  # 类型（1首页 2课程 3路径 4训练营）
#     is_show = models.IntegerField(default=1)  # 是否显示（1显示,2不显示）
#     sort = models.IntegerField()  # 显示顺序





# 角色表    roles
class Roles(models.Model):
    name = models.CharField(max_length=155)  # 角色名称
    status = models.IntegerField(default=0)  # 状态(0为停用，1为启用)



# 资源表    resources
class Resources(models.Model):
    name = models.CharField(max_length=155)  # 权限名称
    url = models.CharField(max_length=155)  # 全线路有
    status = models.IntegerField(default=1)  # 状态(0为停用，1为启用)
    roles= models.ManyToManyField(Roles,related_name='resources')  # 使用多对多自动创建第三张表

# 角色资源表    roles_resources
# class Roles_Resources(models.Model):
#     roles= models.ForeignKey(Roles,on_delete=models.CASCADE)  # 权限名称
#     resources = models.ForeignKey(Resources,on_delete=models.CASCADE)  # 全线路有


class Admin(models.Model):  # 管理员用户表
    username = models.CharField(max_length=50)  # 管理员用户名
    password = models.CharField(max_length=255)  # 管理员密码
    roles = models.ForeignKey(Roles, on_delete=models.CASCADE)  # 外键关联角色表
#
# # 活动表    act
# class Act(models.Model):
#     title = models.CharField(max_length=155)  # 活动标题
#     data = models.DateTimeField(auto_now=True)  # 活动日期
#
#
# # 秒杀时间表    time
# class Time(models.Model):
#     start = models.DateTimeField(auto_now=True)  # 活动开始时间
#     end = models.DateTimeField(auto_now=True)  # 活动结束时间
#
#
# # 秒杀产品表    sk
# class Sk(models.Model):
#     act = models.ForeignKey(Act, on_delete=True)  # 秒杀活动外键
#     time = models.ForeignKey(Time, on_delete=True)  # 秒杀活动时间外键
#     price = models.DecimalField(max_digits=7,decimal_places=2)  # 秒杀价格
#     course = models.ForeignKey(Course, on_delete=True)  # 优惠券外键
#
#
# # 工单表    work_order
# class Work_Order(models.Model):
#     user_id = models.IntegerField()  # 外键关联用户表
#     problem = models.CharField(max_length=155)  # 问题标题
#     content = models.CharField(max_length=155)  # 问题内容
#     pid = models.CharField(max_length=155)  # 关联问题回复
#     status = models.IntegerField()  # 状态(0为未处理，1为处理)
#
#
# # 日志表    log
# class Log(models.Model):
#     dates = models.DateTimeField(auto_now=True)  # 执行时间
#     operation = models.CharField(max_length=155)  # 执行操作
#     result = models.IntegerField()  # 操作结果(0为失败，1为成功)
#     reason = models.CharField(max_length=155)  # 失败原因
#     admin_id = models.CharField(max_length=155)  # 操作管理员，外键关联管理员
#
#
# # 讨论区    forum
# class Forum(models.Model):
#     name = models.CharField(max_length=155)  # 优惠券名称
#     count = models.IntegerField()  # 优惠券数量
#     types = models.IntegerField()  # 类型（1首次注册会员送  2全场能用  3指定商品  4指定会员）
#     course_id = models.IntegerField()  # 类型为3时指定课程
#     start_time = models.DateTimeField()  # 优惠券使用开始时间
#     end_time = models.DateTimeField()  # 优惠券使用结束时间
#     status = models.IntegerField()  # 优惠券发放状态
#     condition = models.DecimalField(max_digits=7,decimal_places=2)  # 满多少钱可以使用
#     money = models.DecimalField(max_digits=7,decimal_places=2)  # 优惠券金额
#
#
# # 课程收藏表    course_collect
# class Course_Collect(models.Model):
#     user_id = models.ForeignKey(User,on_delete=models.CASCADE)  # 用户id
#     course_id = models.ForeignKey(Course,on_delete=models.CASCADE)  # 课程id
