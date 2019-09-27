from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView                                    # 类方法序列化继承APIView
from rest_framework.response import Response                                # 返回json格式
from edu.models import *                                                    # 导入models对象
from serializers.serializer import *                                        # 序列化文件类
from django.contrib.auth.hashers import make_password,check_password        # 生成哈希 校验哈希






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

        
  # 等级条件展示
class Show_UserLevel(APIView):
    def get(self,request):
        # 获取等级
        show_userlrvelcondition = UserLevelCondition.objects.all()
        mes = {}
        mes['userlevelcondition'] = UserLevelConditionSerializer(show_userlrvelcondition,many=True).data
        mes['code'] = 200

        return Response(mes)      


# 注册管理员
class RegAdmin(View):
    def get(self,request):
        password='123456'
        admin=Admin(username='李四',password=make_password(password),roles_id_id=1)
        admin.save()
        return HttpResponse('添加成功')

# 登录管理员
class LoginAdmin(APIView):
    def post(self,request):
        mes={}
        data=request.data
        # 用户信息
        username=data['name']
        password=data['passwd']

        if not all([username,password]):
            mes['code']=10010
            mes['message']='账号或者密码'
        else:
            # 查询是否有该用户
            admin=Admin.objects.filter(username=username).first()
            if admin:
                if check_password(password,admin.password):
                    mes['code']=200
                    mes['message']='登录成功'
                else:
                    mes['code']=10020
                    mes['message']='密码错误'
            else:
                mes['code']=10030
                mes['message']='用户不存在'
        return Response(mes)


class UserLevelCondition_add(APIView):
    def post(self,request):                                                         # todo 添加
        ulc = UserLevelConditionModelSerializer(data=request.data)
        print(ulc)
        mes={}
        if ulc.is_valid():
            ulc.save()
            mes["code"] = 200
            mes["data"] = ulc.data
        else:
            mes["code"] = 400
        print(ulc.errors)
        return Response(mes)

