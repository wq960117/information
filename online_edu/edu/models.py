from django.db import models



# 收藏实验问答表
class Collect_Answer(models.Model):
    answer=models.ForeignKey('Answer',on_delete=models.CASCADE)       #问答表外键
    user=models.ForeignKey('User',on_delete=models.CASCADE)

# 课程订单表
class Cours_order(models.Model):
    order_number=models.CharField(max_length=100)        #订单编号
    user=models.ForeignKey('User',on_delete=models.CASCADE)    #用户外键
    course=models.ForeignKey('Course',on_delete=models.CASCADE)     #课程外键
    pyt_type=models.IntegerField()      #支付方式  1微信  2支付宝
    price=models.DecimalField(max_digits=7,decimal_places=2)   #商品价格
    pay_price=models.DecimalField(max_digits=7,decimal_places=2)   #实际支付
    preferential_way=models.IntegerField()     #优惠方式  0 未使用  1积分  2优惠券
    preferential_money=models.DecimalField(max_digits=7,decimal_places=2)   #优惠金额
    order_status=models.IntegerField()      #订单状态  1待支付  2支付成功
    code=models.CharField(max_length=100)    #流水号
    coupon=models.CharField(max_length=100)   #优惠码

# 积分兑换规则表
class rule(models.Model):
    ratio=models.FloatField(default=0.01)      #兑换比例
    min_integral=models.IntegerField(default=100)     #最低兑换门槛
    max_integral=models.IntegerField(default=10000)   #最高兑换门槛

# 优惠券表
class Coupon(models.Model):
    course=models.ForeignKey('Course',on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    count=models.IntegerField()        #数量
    type=models.IntegerField()       #类型  1全场通用   2指定商品
    start_time=models.DateTimeField()    #开始时间
    end_time=models.DateTimeField()       #结束时间
    condition=models.DecimalField(max_digits=7,decimal_places=2)     #满多少可以
    integral=models.IntegerField()   #兑换所需积分数量
    money=models.DecimalField(max_digits=7,decimal_places=2)          #实际抵消金额
    status=models.IntegerField()  #状态  1可用  2过期

# 用户优惠卷使用表
class Integral_coupon(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE)          #兑换用户
    coupon_order=models.CharField(max_length=100)  # 优惠券编码
    count=models.IntegerField()        #数量
    start_time=models.DecimalField()    #使用时间
    end_time=models.DateTimeField()     # 结束时间
    coupon_money=models.DecimalField(max_digits=7,decimal_places=2)    #优惠券金额
    max_money=models.DecimalField(max_digits=7,decimal_places=2)        #满多少可以用
    type=models.IntegerField()          #类型   1全场通用   2指定商品
    status=models.IntegerField()     #状态  1已用  2未用  3过期

# 积分记录表        总积分
class Coupon_record(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    x_integral=models.IntegerField()          #操作类型  1增加  2减少
    s_integral=models.IntegerField()          #当前总积分
    before_integral=models.IntegerField()     #本次使用积分
    end_integral=models.IntegerField()        #使用后剩余积分
    effect=models.IntegerField()         #使用方式   1抵扣金额  2优惠卷
    coupon_code=models.CharField()           #优惠券码























