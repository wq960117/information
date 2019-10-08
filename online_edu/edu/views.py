from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView                                    # 类方法序列化继承APIView
from rest_framework.response import Response                                # 返回json格式
from edu.models import *                                               # 导入models对象
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
        paginator = Paginator(userlevel,4)  # 将所有的数据放到分页容器中
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

# 阶段的添加
class AddPath_stageView(APIView):
    def post(self,request):
        ser = Path_stageSerializers(data=request.data)
        mes = {}
        print('aaaaaaaaaaaaaaaaaaaaaa')
        if ser.is_valid():
            print('sssssssssssssssssssssssss')
            ser.save()
            mes['code'] = 200
            mes['msg'] = '添加成功'
            mes['data'] = ser.data
        else:
            mes['code'] = 400
            mes['msg'] = '添加失败'
        return Response(mes)
# 阶段的展示
class Path_stagelistView(APIView):
    def get(self,request):
        mes={}
        path = Path_stage.objects.all()
        pathlist = Path_stageSerializers(path, many=True)
        mes['pathlist'] = pathlist.data  # 序列化当前页的数据
        mes['code'] = 200
        return Response(mes)
# 阶段的修改
class UpdatePath_stageView(APIView):
    def post(self,request):
        id = request.POST.get('id')
        data = request.data.copy()
        print(data)
        data['id'] = id
        if data['id']:
            c1 = Path_stage.objects.get(id=data['id'])
            c = Path_stageSerializers(c1, data=data)
        else:
            c = Path_stageSerializers(data=data)
        mes = {}
        if c.is_valid():
            c.save()
            mes['code'] = 200
            mes['msg'] = '修改成功'
        else:
            print(c.errors)
            mes['code'] = 400
            mes['msg'] = '修改失败'
        return Response(mes)

#阶段的删除
class Delete_PathView(APIView):
    def post(self,request):
        mes = {}
        data = request.data
        Path = Path_stage.objects.filter(id=int(data['id'])).first()
        Path.delete()
        mes['code'] = 200
        mes['msg'] = '删除成功'

        return Response(mes)



# 展示课程
class CourseList(APIView):
    def get(self, request):
        mes = {}
        course = Course.objects.all()
        c = CourseModelSerializer(course, many=True)
        mes['code'] = 200
        mes['courselist'] = c.data
        return Response(mes)

# django上传图片方法
def uploadImg(request):
    file = request.FILES.get('image')
    mes = {}
    mes['code'] = 10010
    mes['url'] = 'error'
    if file:
        f = open(os.path.join(UPLOAD, '', file.name), 'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()

        mes['code'] = 200
        mes['name'] = file.name
        mes['url'] = 'http://127.0.0.1:8000/static/upload/' + file.name
    return JsonResponse(mes)

# 添加章节
class AddSection(APIView):
    def post(self,request):
        mes={}

        data=request.data
        s=SectionUserserializers(data=data)
        if s.is_valid():
            print(data, 'ok-----------------------------------------------')
            s.save()
            mes['code']=200
            mes['message']='添加成功'
        return Response(mes)

#展示章节
class Sectionlist(APIView):
    def get(self,request):
        mes={}
        sectionlists=Section.objects.all()
        s=SectionModelSerializer(sectionlists,many=True)
        mes['code']=200
        mes['sectionlist']=s.data
        return Response(mes)

#删除章节
class DeleteSection(APIView):
    def post(self,request):
        mes={}
        data=request.data
        print(data)
        one_section=Section.objects.filter(id=int(data['id'])).first()
        # print(one_section,'+++++++++++++++++++++++++++++++++')
        video_name=one_section.video
        # print(video_name)
        video=video_name.split('/')[-1]
        # print(video,'-----------------------------')
        os.chdir(UPLOAD)
        # print(os.getcwd())
        try:
            #删除
            os.remove(video)
            one_section.delete()
            # print('aaaaaaaaaaaaaaaa')
            mes['code'] = 200
            mes['msg'] = '删除成功'
        except:
            # print('adfsdfasdf')
            mes['code'] = 201
            mes['msg'] = '删除失败'

        return Response(mes)

# 修改章节
class UpdateSection(APIView):
    def post(self, request):
        mes = {}
        data=request.data.copy()
        print(data,'-------------------------------------------')
        print(data)
        try:
            if data['id']:
                id=int(data['id'])
                one_section = Section.objects.get(id=id)
                # 根据修改的外键名字换取对应的外键ID
                one_course = Course.objects.filter(id=data['course']).first()
                one_section.course_id = one_course.id
                one_section.section=data['new_section']
                one_section.course_id=data['course_id']
                # one_section.video=data['video']
                one_section.save()
                mes['code'] = 200
                mes['message'] = '修改成功'
            else:
                mes['code'] = 201
                mes['message'] = '修改失败'
        except:
            mes['code'] = 202
            mes['message'] = '错误信息'
        return Response(mes)

"""
标签操作
------------------------------------------------------------------------------------------------------------------------
"""
class TagList(APIView):
    def get(self, request):                                                     # todo 展示标签
        tag = Tag.objects.all().order_by('id')

        p = int(request.GET.get('page',1))                  # 获取网页参数 默认第1页
        page = Paginator(tag,2)                             # 实例化分页对象，每页3条数据
        tag_list = page.get_page(p)                         # 获取当前页的数据.get_page(p)
        tpage = page.num_pages                              # 获取总页数

        ser = TagModelSerializer(tag_list, many=True)

        mes = {}
        mes['code'] = 200
        mes['data'] = ser.data
        mes['tpage'] = tpage
        return Response(mes)

    def post(self, request):                                                    # todo 添加标签
        ser = TagModelSerializer(data=request.data)
        mes = {}
        if ser.is_valid():
            ser.save()
            mes['code'] = '200'
            mes['msg'] = '成功'
            mes['data'] = ser.data
        else:
            print(ser.errors)
            mes['code'] = 400
            mes['msg'] = '失败'
        return Response(mes)


    def put(self,request):                                                       # todo 修改标签
        content = request.data
        id = int(content['id'])                             # 获取点击后的内容id
        c1 = Tag.objects.get(id=id)
        c = TagModelSerializer(c1,data=content)

        mes = {}
        if c.is_valid():
            c.save()
            mes['code'] = 200
            mes['message'] = '修改成功'
        else:
            print(c.errors)
            mes['code'] = 400
            mes['message'] = '修改失败'
        return Response(mes)

    def delete(self, request):                                                    # todo 删除标签
        id = request.GET.get('id')
        tag = Tag.objects.filter(id=id).first()
        tag.delete()
        return Response('删除完成')

class TagDeletes(APIView):                                                       # todo 批量删除标签
    def post(self,request):
        data=request.data
        ids=data['ids']
        id_list=ids.split(',')

        for id in id_list:
            id=int(id)
            one_Tag=Tag.objects.get(id=id)
            one_Tag.delete()

            mes = {}
            mes['code']=200
            mes['message']='删除成功'
        return Response(mes)

'''
老师相关
'''
#老师添加
class Teacher_add(APIView):
    def post(self, request):
        ts = TeacherSerializer(data=request.data)
        print(ts)
        mes = {}
        if ts.is_valid():
            ts.save()
            mes["code"] = 200
            mes["data"] = ts.data
        else:
            mes["code"] = 400
        return Response(mes)

#老师删除
class TeacherDelete(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        teacher_d = Teacher.objects.filter(id=id).first()
        teacher_d.delete()
        mes['code'] = 200
        mes['msg'] = '删除成功'
        return Response(mes)

#老师展示
class Teacher_list(APIView):
    def get(self, request):
        teachers = Teacher.objects.all().order_by('id')

        p = int(request.GET.get('page', 1))
        page = Paginator(teachers, 3)
        teacher_list = page.get_page(p)
        tpage = page = page.num_pages

        tea = TeacherSerializer(teacher_list, many=True)
        mes = {}
        mes['code'] = 200
        mes['teacher_list'] = tea.data
        mes['tpage'] = tpage
        return Response(mes)

#老师修改
class Teacher_update(APIView):
    def post(self, request):
        id = request.POST.get('id')
        data = request.POST.copy()
        data = request.data.copy()
        print(data)
        data['id'] = id
        if data['id']:
            c1 = Teacher.objects.get(id=data['id'])
            c = TeacherSerializer(c1, data=data)
        else:
            c = TeacherSerializer(data=data)

        mes = {}
        if c.is_valid():
            c.save()
            mes['code'] = 200
            mes['msg'] = '修改成功'
        else:
            print(c.errors)
            mes['code'] = 400
            mes['msg'] = '修改失败'
        return Response(mes)