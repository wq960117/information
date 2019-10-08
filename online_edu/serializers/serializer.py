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
    video = serializers.CharField(max_length=200)
    sort =serializers.IntegerField()

    def create(self,data):
        return Section.objects.create(**data)
    def update(self, instance, validated_data):
        instance.section = validated_data.get('new_section', instance.section)
        instance.course=validated_data.get('course_id',instance.course)
        # instance.video=validated_data.get('video',instance.video)
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
    class Meta:
        model = Path
        fields = '__all__'

# 路径反序列化
class PathSerializers(serializers.Serializer):
    pic = serializers.CharField(max_length=50)
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