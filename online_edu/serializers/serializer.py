coding=utf-8
from rest_framework import serializers
from edu.models import *
class UserLevelConditionModelSerializer(serializers.ModelSerializer):
    # one_level=serializers.SerializerMethodField()
    # def get_one_level(self,row):
    #     a_level=UserLevel.objects.filter(id=row.level_id).first()
    #     return a_level
    class Meta():
        model=UserLevelCondition
        fields='__all__'
        
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

