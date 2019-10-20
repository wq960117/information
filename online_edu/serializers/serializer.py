# coding=utf-8
from rest_framework import serializers
from edu.models import *
class UserLevelConditionModelSerializer(serializers.ModelSerializer):
    level_name1 =serializers.CharField(source='level.level')
    # level_name1=serializers.SerializerMethodField()
    # def get_level_name1(self,row):
    #     one_level=UserLevel.objects.filter(id=row.level_id).first()
    #     return one_level.level
    class Meta():
        model=UserLevelCondition
        fields=('id','level_name1','time','price','level',)

"""  李阿萨德"""
class UserLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLevel
        fields = '__all__'


class UserLevelConditionSerializer(serializers.Serializer):
    level_id = serializers.IntegerField()
    time = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)

    def create(self, data):
        return UserLevelCondition.objects.create(**data)

    def update(self, instance, validated_data):
        instance.level_id = validated_data.get('level_id', instance.level_id)
        instance.time = validated_data.get('time', instance.time)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
class UserLevelSerializers(serializers.Serializer):
    level= serializers.CharField(max_length=20)
    def create(self, data):
        return UserLevel.objects.create(**data)

    def update(self, instance, validated_data):
        instance.level = validated_data.get('level', instance.level)
        instance.save()
        return instance
class AdminModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

#阶段的序列化
class Path_stageModelSerializer(serializers.ModelSerializer):
    courses=serializers.SerializerMethodField()
    def get_courses(self,row):
        all_courses=Course.objects.filter(stage_id=row.id,path_id=row.path_id).all()
        all_courses=ClassesModelSerializer(all_courses,many=True)
        return all_courses.data
    class Meta:
        model = Path_stage
        fields = '__all__'
# 阶段的反序列化
class Path_stageSerializers(serializers.Serializer):
    stage_name = serializers.CharField(max_length=50)
    path_id = serializers.IntegerField()
    sort = serializers.IntegerField()
    def create(self, data):
        return Path_stage.objects.create(**data)
    def update(self, instance, validated_data):
        instance.stage_name = validated_data.get('stage_name', instance.stage_name)
        instance.save()
        return instance


# 反序列化添加章节
class SectionUserserializers(serializers.Serializer):
    section = serializers.CharField(max_length=50)
    course_id= serializers.IntegerField()
    video = serializers.CharField(max_length=255)
    sort =serializers.IntegerField()

    def create(self,data):
        return Section.objects.create(**data)
    def update(self, instance, validated_data):
        instance.section = validated_data.get('new_section', instance.section)
        instance.course=validated_data.get('course_id',instance.course)
        instance.video=validated_data.get('video',instance.video)
        instance.sort=validated_data.get('sort',instance.sort)
        instance.save()
        return instance

#序列化展示课程
class CourseModelSerializer(serializers.ModelSerializer):
    # course=serializers.SlugRelatedField(slug_field='course',read_only=True)
    # title=serializers.CharField(source='course.title')
    class Meta:
        model=Course
        fields='__all__'

# 序列化展示章节
class SectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields='__all__'

"""
标签表
========================================================================================================================
"""
class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ClassesModelSerializer(serializers.ModelSerializer):
    path_name=serializers.CharField(source='path.path')
    stage_name=serializers.CharField(source='stage.stage_name')
    class Meta:
        model=Course
        fields = ['id','title','pic','info','online','member','attention','learn','teacher_id','comment_num','stage_id','tag_id','recommand','detail','section_num','path_id','path_name','stage_name',]
class ClassesSerializers(serializers.Serializer):
    """创建管理员序列化保存"""
    title = serializers.CharField(max_length=50)
    pic = serializers.CharField(max_length=255)
    info = serializers.CharField(max_length=255)
    online = serializers.IntegerField(default=0)
    member = serializers.IntegerField(default=0)
    attention = serializers.IntegerField(default=0)
    learn = serializers.IntegerField(default=0)
    teacher_id = serializers.IntegerField(default=0)
    comment_num = serializers.IntegerField(default=0)
    stage_id = serializers.IntegerField(default=0)
    tag_id = serializers.IntegerField(default=0)
    recommand = serializers.CharField(max_length=50)
    detail = serializers.CharField(max_length=200)
    section_num = serializers.IntegerField(default=0)
    path_id = serializers.IntegerField(default=0)

    def create(self, data):
        return Course.objects.create(**data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.pic = validated_data.get('pic', instance.pic)
        instance.info = validated_data.get('info', instance.info)
        instance.online = validated_data.get('online', instance.online)
        instance.member = validated_data.get('member', instance.member)
        instance.attention = validated_data.get('attention', instance.attention)
        instance.teacher_id = validated_data.get('teacher_id', instance.teacher_id)
        instance.comment_num = validated_data.get('comment_num', instance.comment_num)
        instance.stage_id = validated_data.get('stage_id', instance.stage_id)
        instance.tag_id = validated_data.get('tag_id', instance.tag_id)
        instance.recommand = validated_data.get('recommand', instance.recommand)
        instance.detail = validated_data.get('detail', instance.detail)
        instance.section_num = validated_data.get('section_num', instance.section_num)
        instance.path_id = validated_data.get('path_id', instance.path_id)
        instance.save()
        return instance
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


# 路径序列化
class PathModelSerializer(serializers.ModelSerializer):
    path_amount = serializers.SerializerMethodField()

    def get_path_amount(self,row):
        amount=Course.objects.filter(path_id=row.id).count()
        return amount
    class Meta:
        model = Path
        fields = '__all__'

# 路径反序列化
class PathSerializers(serializers.Serializer):
    pic = serializers.CharField(max_length=255)
    path = serializers.CharField(max_length=255)
    info = serializers.CharField(max_length=255)
    studynum = serializers.IntegerField()
    def create(self, data):
        return Path.objects.create(**data)

    def update(self, instance, validated_data):
        instance.pic = validated_data.get('pic', instance.pic)
        instance.path = validated_data.get('path', instance.path)
        instance.info = validated_data.get('info', instance.info)
        instance.studynum = validated_data.get('studynum', instance.studynum)
        instance.save()
        return instance


class PriceModelSerializer(serializers.ModelSerializer):
    level_name=serializers.CharField(source='type.level')
    course_title=serializers.CharField(source='course.title')
    class Meta:
        model=Price
        fields = ['id','type','course','discount','pre_price','discount_price','level_name','course_title']
class PriceSerializers(serializers.Serializer):
    """课程价格反序列化"""
    type_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    discount = serializers.FloatField()
    pre_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    discount_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    def create(self, data):
        return Price.objects.create(**data)

    def update(self, instance, validated_data):
        instance.course_id = validated_data.get('course_id', instance.course_id)
        instance.type = validated_data.get('type', instance.type)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.pre_price = validated_data.get('pre_price', instance.pre_price)
        instance.discount_price = validated_data.get('discount_price', instance.discount_price)
        instance.save()
        return instance


class CouponModelSerializer(serializers.ModelSerializer):
    """优惠券序列化"""
    class Meta:
        model=Coupon
        fields='__all__'


class CouponSerializers(serializers.Serializer):
    """优惠券反序列化"""
    course_id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(max_length=30)
    count = serializers.IntegerField()
    type = serializers.IntegerField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    condition = serializers.DecimalField(max_digits=7, decimal_places=2)
    integral = serializers.IntegerField()
    money = serializers.DecimalField(max_digits=7, decimal_places=2)
    status = serializers.IntegerField()
    def create(self, data):
        return Coupon.objects.create(**data)

    def update(self, instance, validated_data):
        instance.course_id = validated_data.get('course_id', instance.course_id)
        instance.name = validated_data.get('name', instance.name)
        instance.count = validated_data.get('count', instance.count)
        instance.type = validated_data.get('type', instance.type)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.integral = validated_data.get('integral', instance.integral)
        instance.money = validated_data.get('money', instance.money)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
class UserSerializer(serializers.Serializer):
    """优惠券反序列化"""
    username = serializers.CharField(max_length=20,default='')
    password = serializers.CharField(max_length=255)
    pic = serializers.CharField(max_length=255,default='')
    level_id = serializers.IntegerField(default=0)
    is_active = serializers.IntegerField(default=0)
    integral = serializers.IntegerField(default=0)
    invitation_code = serializers.CharField(max_length=50,default='')
    token = serializers.CharField(max_length=255,default='')
    email = serializers.CharField(max_length=255)
    def create(self, data):
        return User.objects.create(**data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.pic = validated_data.get('pic', instance.pic)
        instance.level = validated_data.get('level', instance.level)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.integral = validated_data.get('integral', instance.integral)
        instance.invitation_code = validated_data.get('invitation_code', instance.invitation_code)
        instance.token = validated_data.get('token', instance.token)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
class UserModelSerializer(serializers.ModelSerializer):
    """用户序列化"""
    class Meta:
        model=User
        fields='__all__'
class CommentModelSerializer(serializers.ModelSerializer):
    """评论序列化"""
    class Meta:
        model=Comment
        fields='__all__'
class ReportModelSerializer(serializers.ModelSerializer):
    """实验报告序列化"""
    class Meta:
        model=Report
        fields='__all__'
class AnswerModelSerializer(serializers.ModelSerializer):
    """实验问答序列化"""
    class Meta:
        model=Answer
        fields='__all__'
class Integral_couponModelSerializer(serializers.ModelSerializer):
    """实验问答序列化"""
    class Meta:
        model=Integral_coupon
        fields='__all__'
class RuleModelSerializer(serializers.ModelSerializer):
    """积分兑换规则序列化"""
    class Meta:
        model=Rules
        fields='__all__'
class CoursOrderModelSerializer(serializers.ModelSerializer):
    """用户课程订单序列化"""
    class Meta:
        model=Cours_order
        fields='__all__'

class TimeModelSerializer(serializers.ModelSerializer):
    """秒杀活动序列化"""
    class Meta:
        model=Time
        fields=['id','start','end','act_id']
class ActModelSerializer(serializers.ModelSerializer):
    """活动时间段序列化"""
    class Meta:
        model=Act
        fields='__all__'

class SkModelSerializer(serializers.ModelSerializer):
    """秒杀产品序列化"""
    # 活动产品信息
    act_course=serializers.SerializerMethodField()
    # 活动信息
    act_info=serializers.SerializerMethodField()
    # 活动场次信息
    time_info=serializers.SerializerMethodField()
    def get_act_course(self,row):
        one_course=Course.objects.filter(id=row.course_id).first()
        one_course=ClassesModelSerializer(one_course).data
        return one_course
    def get_act_info(self,row):
        one_act=Act.objects.filter(id=row.act_id).first()
        one_act=ActModelSerializer(one_act).data
        return one_act
    def get_time_info(self,row):
        one_time=Time.objects.filter(id=row.time_id).first()
        one_time=TimeModelSerializer(one_time).data
        return one_time
    class Meta:
        model=Sk
        fields=['id','act_info','time_info','price','course','count','act_course']
class ActOrderSerializer(serializers.Serializer):
    """秒杀产品订单反序列化"""
    order_sn = serializers.CharField(max_length=255)
    start_time = serializers.DateTimeField()
    count = serializers.IntegerField(default=1)
    money = serializers.DecimalField(max_digits=7, decimal_places=2)
    user_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    status = serializers.IntegerField(default=0)  # 1支付成功2已评论
    code = serializers.CharField(max_length=255)

    def create(self, data):
        return Price.objects.create(**data)

    def update(self, instance, validated_data):
        instance.order_sn = validated_data.get('order_sn', instance.order_sn)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.count = validated_data.get('count', instance.count)
        instance.money = validated_data.get('money', instance.money)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.course_id = validated_data.get('course_id', instance.course_id)
        instance.status = validated_data.get('status', instance.status)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance

