from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView                                    # 类方法序列化继承APIView
from rest_framework.response import Response                                # 返回json格式
from edu.models import *                                                    # 导入models对象
from serializers.serializer import *                                        # 序列化文件类
from django.contrib.auth.hashers import make_password,check_password        # 生成哈希 校验哈希
from django.core.paginator import Paginator                                 # 分页

class UserLevel_Add(APIView):
    """用户的等级的添加"""
    def post(self,request):
        # 反序列化验证数据
        ser = UserLevelSerializers(data=request.data)
        mes = {}
        if ser.is_valid():
            # 如果数据通过验证，则保存到数据库中
            ser.save()
            mes['code'] = '200'
            mes['msg'] = '成功'
            mes['data'] = ser.data
        else:
            # 如果数据不符合验证，则返回提示信息
            print(ser.errors)
            mes['code'] = 400
            mes['msg'] = '失败'
        return Response(mes)


class UserLevel_List(APIView):
    """分页获取用户等级接口"""
    def get(self,request):
        mes={}
        userlevel = UserLevel.objects.all() #获取所有的用户等级数据
        current_page = int(request.GET.get('page'))  # 获取当前页的页码
        paginator = Paginator(userlevel,2)  # 将所有的数据放到分页容器中
        current_data = paginator.get_page(current_page)  # 获取当前页的数据，前台显示当前页的数据就可以
        total_page = paginator.num_pages  # 获取总页数
        userlevels = UserLevelSerializer(current_data,many=True) # 序列化当前页的数据
        mes['userlevels'] = userlevels.data  # 返回序列化后的当前页的数据
        mes['code'] = 200
        mes['total'] = total_page   #   返回总页数
        return Response(mes)

class Get_UserLevels(APIView):
    """获取所有用户等级的数据，显示在添加用户等级条件的页面，因为如果直接调用分页获取用户等级的接口，如果用户等级多，第二页的用户等级在添加的时候显示不到，只能显示第一页的第一页的用户等级 """
    def get(self,request):
        mes={}
        userlevel = UserLevel.objects.all()
        userlevels = UserLevelSerializer(userlevel,many=True)
        mes['userlevels'] = userlevels.data  # 序列化当前页的数据
        mes['code'] = 200
        return Response(mes)
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
    def post(self,request):
        mes={}
        data=request.data
        ids=data['ids']
        print(ids)
        id_list=[]
        id_list=ids.split(',')
        for id in id_list:
            id=int(id)
            print(id)
            one_relation=UserLevelCondition.objects.get(id=id)
            try:
                one_relation.delete()
                mes['code']=200
                mes['message']='删除成功'
            except:
                mes['code']=201
                mes['message']='删除失败'
        return Response(mes)

class EditRelation(APIView):
    """修改条件接口"""
    def post(self, request):
        mes = {}
        data=request.data.copy()
        print(data)
        try:
            if data['id']:
                id=int(data['id'])
                one_relation = UserLevelCondition.objects.get(id=id)
                # 根据修改的外键名字换取对应的外键ID
                one_level = UserLevel.objects.filter(level=data['level_name1']).first()
                one_relation.level_id = one_level.id
                one_relation.time=data['time']
                one_relation.price=data['price']
                one_relation.save()
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
        # 什么意思？？？？？？？？
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
    def post(self,request):
        mes={}
        data = request.data
        user_level = UserLevel.objects.filter(id=int(data['id'])).first()
        user_level.delete()
        mes['code'] = 200
        mes['msg'] = '删除成功'
        return Response(mes)
class DeleteUsers(APIView):
    """批量删除用户接口"""
    def post(self,request):
        mes={}
        data=request.data
        ids=data['ids']
        print(ids)

        id_list=ids.split(',')
        for id in id_list:
            id=int(id)
            print(id)
            one_level=UserLevel.objects.get(id=id)
            try:
                one_level.delete()
                mes['code']=200
                mes['message']='删除成功'
            except:
                mes['code']=201
                mes['message']='删除失败'
        return Response(mes)
        
# 等级条件展示
class Show_UserLevel(APIView):
    def get(self,request):
        mes = {}
        # 获取等级
        show_userlrvelcondition = UserLevelCondition.objects.all()
        # current_page=request.GET.get('page') #  获取当前页的页码
        # paginator=Paginator(show_userlrvelcondition,1)  #   将所有的数据放到分页容器中
        # current_data=paginator.get_page(current_page)   #   获取当前页的数据，前台显示当前页的数据就可以
        # total_page = paginator.num_pages  #   获取总页数
        # print(total_page)
        mes['userlevelcondition'] = UserLevelConditionSerializer(show_userlrvelcondition,many=True).data   #   序列化当前页的数据
        mes['code'] = 200
        # mes['total'] = total_page
        return Response(mes)

# 等级条件展示

class GetRelations(APIView):
    """查询等级条件接口"""
    def get(self,request):
        mes = {}
        # 获取等级
        show_userlrvelcondition = UserLevelCondition.objects.all()
        print(show_userlrvelcondition)
        # 获取当前页的页码
        current_page = request.GET.get('page')
        print('&&&&&&&&&&&&&&&&&&&&&&&')
        print(current_page)
        # 将所有的数据放到分页容器中
        paginator = Paginator(show_userlrvelcondition,1)
        # 获取当前页的数据，前台显示当前页的数据就可以
        current_data = paginator.get_page(current_page)
        # 获取总页数
        total_page =paginator.num_pages
        print(total_page)
        print('&&&&w&&&&&&&&&&&&&&&&&&&')
        userlevelcondition = UserLevelConditionModelSerializer(current_data, many=True).data  # 序列化当前页的数据
        # userlevelcondition=UserLevelConditionModelSerializer(show_userlrvelcondition,many=True).data
        mes['all_relations'] = userlevelcondition  # 序列化当前页的数据
        mes['code'] = 200
        mes['total'] = total_page
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
        username=data['username']
        password=data['password']

        if not all([username,password]):
            mes['code']=10010
            mes['message']='账号或者密码'
        else:
            # 查询是否有该用户
            admin=Admin.objects.filter(username=username).first()
            if admin:
                if check_password(password,admin.password):
                    admin=AdminModelSerializer(admin)
                    mes['code']=200
                    mes['message']='登录成功'
                    mes['user']=admin.data
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

