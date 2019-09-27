from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from edu.models import *
from serializers.serializer import *
class DeleteRelation(APIView):
    """删除关系接口"""
    def post(self,request):
        mes={}
        data=request.data
        print(data)
        try:
            id=int(data['id'])
            one_relation=UserLevelCondition.objects.get(id=id)
            one_relation.delete()
            mes['code']=200
            mes['message']='删除成功'
        except:
            mes['code']=201
            mes['message']='删除失败'
        return Response(mes)

class DeleteRelations(APIView):
    """批量删除关系接口"""
    def get(self,request):
        mes={}
        ids=request.GET.getlist('id')
        for id in ids:
            one_relation=UserLevelCondition.objects.get(id=id)
            try:
                one_relation.delete()
                mes['code']=200
                mes['message']='删除成功'
            except:
                mes['code']=201
                mes['message']='删除失败'
            return Response(mes)

class GetRelations(APIView):
    """批量删除关系接口"""
    def get(self,request):
        mes={}
        all_relations=UserLevelCondition.objects.all()
        all_relations=UserLevelConditionModelSerializer(all_relations,many=True)
        print(all_relations)
        mes['code']=201
        mes['all_relations']=all_relations.data
        # print(mes)
        return Response(mes)

class EditRelation(APIView):
    """修改条件接口"""
    def post(self, request):
        mes = {}
        data=request.data.copy()
        print(data)
        if data['id']:
            id=int(data['id'])
            one_relation = UserLevelCondition.objects.get(id=id)
            a_relation=UserLevelConditionSerializer(one_relation,data=data)
        else:
            a_relation=UserLevelConditionSerializer(data=data)
        try:
            if a_relation.is_valid():
                mes['code'] = 200
                mes['message'] = '修改成功'
            else:
                mes['code'] = 201
                mes['message'] = '修改失败'
        except:
            mes['code'] = 202
            mes['message'] = '错误信息'
        return Response(mes)

