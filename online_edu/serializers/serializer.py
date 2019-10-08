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
        
"""�û��ȼ����л�  李阿萨德"""
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

# 阶段的序列化
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
