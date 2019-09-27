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

#等级列表的修改
class UserLevelUpdate(APIView):
    def post(self,request):
        id = request.POST.get('id')
        data = request.POST.copy()
        data = request.data.copy()
        print(data)
        data['id'] = id
        if data['id']:
            c1 = UserLevel.objects.get(id=data['id'])
            c = UserLevelConditionModelSerializer(c1,data=data)
        else:
            c= UserLevelConditionModelSerializer(data=data)

        mes={}
        if c.is_valid():
            c.save()
            mes['code'] = 200
            mes['msg'] = '修改成功'
        else:
            print(c.errors)
            mes['code'] = 400
            mes['msg'] = '修改失败'
        return Response(mes)
#等级列表的删除
class DeleteUser(APIView):
    def delete(self,request):
        id = request.GET.get('id')
        print(id)
        user_level = UserLevel.objects.filter(id=id).first()
        user_level.delete()
        return Response('删除完成')
        
  """等级条件展示"""
class Show_UserLevel(APIView):
    def get(self,request):
        # 获取等级
        show_userlrvelcondition = UserLevelCondition.objects.all()
        mes = {}
        mes['userlevelcondition'] = UserLevelConditionSerializer(show_userlrvelcondition,many=True).data
        mes['code'] = 200

        return Response(mes)      
        