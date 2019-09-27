# coding=utf-8
from rest_framework import serializers
from edu.models import *
class UserLevelConditionModelSerializer(serializers.ModelSerializer):
    # level_name =serializers.CharField(source='level.level')
    level_name1=serializers.SerializerMethodField()
    def get_level_name1(self,row):
        print(row.level_id)
        one_level=UserLevel.objects.filter(id=row.level_id).first()
        print(one_level)
        # one_level=UserLevelSerializer(one_level).data
        return one_level.level
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