from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
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
        print(request.data,'aaaaaaaaaaaaaaaaaaaaaa')
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
        pathlist = Path_stageModelSerializer(path, many=True)
        mes['pathlist'] = pathlist.data  # 序列化当前页的数据
        mes['code'] = 200
        return Response(mes)
# 阶段的修改
class UpdatePath_stageView(APIView):
    def post(self,request):
        data = request.data.copy()
        datas = {}
        datas['stage_name']=data['stage_name']
        datas['path_id']=data['path_id']
        datas['sort']=data['sort']
        print(datas)
        if data['id']:
            c1 = Path_stage.objects.get(id=data['id'])
            c = Path_stageSerializers(c1, data=datas)
        else:
            c = Path_stageSerializers(data=datas)
        mes = {}
        if c.is_valid():
            c.save()
            mes['code'] = 200
            mes['msg'] = '修改成功'
        else:
            # print(c.errors)
            mes['code'] = 400
            mes['msg'] = '修改失败'
        return Response(mes)

#阶段的删除
class Delete_PathView(APIView):
    def post(self,request):
        mes = {}
        data = request.data
        print(data,'============================================')
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
        section=request.POST.get('section')
        video=request.POST.get('video')
        sort=request.POST.get('sort')
        course_id=request.POST.get('course_id')
        print(section,video,course_id,sort,'======================')
        section=Section(video=video,section=section,sort=sort,course_id=course_id)
        section.save()
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

class GetClasses(APIView):
    """获取课程相关信息"""
    def get(self,request):
        mes={}
        all_classes=Course.objects.all()
        page=request.GET.get('page')

        if page:
            page=int(page)
        else:
            page=1
        paginator=Paginator(all_classes,2)
        current_classes=paginator.get_page(page)
        current_classes=ClassesModelSerializer(current_classes,many=True)
        total=paginator.num_pages

        all_teachers=Teacher.objects.all()
        all_teachers=TeacherSerializer(all_teachers,many=True)
        all_paths=Path.objects.all()
        all_paths=PathModelSerializer(all_paths,many=True)
        all_stages=Path_stage.objects.all()
        all_stages=Path_stageModelSerializer(all_stages,many=True)
        all_tags=Tag.objects.all()
        all_tags=TagModelSerializer(all_tags,many=True)
        mes['code']=200
        mes['total']=total
        mes['all_classes']=current_classes.data
        mes['all_teachers']=all_teachers.data
        mes['all_paths']=all_paths.data
        mes['all_stages']=all_stages.data
        mes['all_tags']=all_tags.data
        return Response(mes)
class Addclasses(APIView):
    """添加课程"""
    def post(self,request):
        mes={}
        data=request.data.copy()
        print(data)
        id=data['id']
        # 因为data里传递了修改对应的ID，所以存储序列化的时候无法验证，所以重新定义数据，将除了ID以外的数据重新赋值
        datas={}
        datas['title']=data['title']
        datas['pic']=data['pic']
        datas['info']=data['info']
        datas['member']=data['member']
        datas['attention']=data['attention']
        datas['learn']=data['learn']
        datas['teacher_id']=data['teacher_id']
        datas['comment_num']=data['comment_num']
        datas['stage_id']=data['stage_id']
        datas['tag_id']=data['tag_id']
        datas['recommand']=data['recommand']
        datas['detail']=data['detail']
        datas['section_num']=data['section_num']
        datas['path_id']=data['path_id']
        datas['online']=data['online']
        print(datas)
        if id:
            """如果ID存在则修改"""
            a_course=Course.objects.get(id=id)
            pic_name = a_course.pic
            print(pic_name)
            pic = pic_name.split('/')[-1]
            print(pic)
            # 跳转到指定目录
            os.chdir(UPLOAD)
            print(os.getcwd())
            try:
                # 删除
                os.remove(pic)
                mes['code'] = 200
                mes['msg'] = '删除成功'

            except:
                mes['code'] = 201
                mes['msg'] = '删除失败'
            one_course = ClassesSerializers(a_course, data=datas)
        else:
            """ID不存在为添加"""
            one_course=ClassesSerializers(data=datas)
        try:
            if one_course.is_valid():
                one_course.save()
                mes['code'] = 200
                mes['message'] = '成功'
                # except:
                #     mes['code'] = 200
                #     mes['message'] = '修改失败'
            else:
                mes['code'] = 201
                mes['message'] = '添加失败'
        except:
            mes['code'] = 400
            mes['message'] = '信息错误'
        return Response(mes)
class DeleteClasses(APIView):
    """批量删除课程"""
    def post(self,request):
        mes = {}
        data = request.data
        ids = data['ids']
        id_list = ids.split(',')
        for id in id_list:
            id = int(id)
            print(id)
            one_course = Course.objects.get(id=id)
            try:
                one_course.delete()
                mes['code'] = 200
                mes['message'] = '删除成功'
            except:
                mes['code'] = 201
                mes['message'] = '删除失败'
        return Response(mes)
class DeleteClass(APIView):
    """删除课程接口"""
    def post(self,request):
        mes={}
        data = request.data
        one_course = Course.objects.filter(id=int(data['id'])).first()
        pic_name=one_course.pic
        pic=pic_name.split('/')[-1]
        print(pic)
        # 跳转到指定目录
        os.chdir(UPLOAD)
        print(os.getcwd())
        try:
            # 删除
            os.remove(pic)
            one_course.delete()

            mes['code'] = 200
            mes['msg'] = '删除成功'
        except:
            print('adfsdfasdf')
            mes['code'] = 201
            mes['msg'] = '删除失败'
        return Response(mes)
import os
from online_edu.settings import UPLOAD
import paramiko

def delete_uploadimg(request):
    '''页面加载图片后点击删除接口'''
    mes={}
    os.chdir(UPLOAD)
    print(os.getcwd())
    url=request.POST.get('url')
    print(url)
    pic_name=url.split('/')[-1]
    print(pic_name)
    try:
        os.remove(pic_name)
        print('删除成功')
        mes['code']=200
    except:
        print('删除失败')
        mes['code']=201
    return JsonResponse(mes)


# 添加路径
class Path_Add(APIView):
    def post(self,requset):
        mes = {}
        content = requset.data
        print(content)
        pat = PathSerializers(data=content)
        if pat.is_valid():
            pat.save()
            mes["code"] = 200
            mes["message"] = '成功'
        else:
            mes["code"] = 400
            mes["message"] = '失败'
        return Response(mes)
# 路径删除
class DeletePath(APIView):
    def post(self,request):
        mes={}
        data = request.data
        path = Path.objects.filter(id=int(data['id'])).first()
        path.delete()
        mes['code'] = 200
        mes['message'] = '删除成功'
        return Response(mes)

# 路径修改
class Updatepath(APIView):
    def post(self,request):
        mes={}
        data = request.data
        print(data)
        if data['id']:
            pp = Path.objects.get(id=data['id'])
            pic_name = pp.pic
            print(pic_name)
            pic = pic_name.split('/')[-1]
            print(pic)
            # 跳转到指定目录
            os.chdir(UPLOAD)
            print(os.getcwd())
            try:
                # 删除
                os.remove(pic)
                mes['code'] = 200
                mes['msg'] = '删除成功'

            except:
                mes['code'] = 201
                mes['msg'] = '删除失败'
            p = PathSerializers(pp,data=data)
        else:
            p = PathSerializers(data=data)
        if p.is_valid():
            p.save()

            mes['code'] = 200
            mes['message'] = '成功'
        else:

            mes['code'] = 400
            mes['message'] = '失败'
        return Response(mes)

'''路径展示'''
class Show_Path(APIView):
    def get(self,request):
        mes = {}
        # 获取等级
        show_path = Path.objects.all()
        mes['path'] = PathModelSerializer(show_path,many=True).data   #   序列化当前页的数据
        mes['code'] = 200
        return Response(mes)


class GetPrice(APIView):
    """获取课程价格展示"""
    def get(self,request):
        mes = {}
        all_prices = Price.objects.all()
        page = request.GET.get('page')
        if page:
            page = int(page)
        else:
            page = 1
        paginator = Paginator(all_prices, 2)
        current_prices = paginator.get_page(page)
        current_prices = PriceModelSerializer(current_prices, many=True)
        total = paginator.num_pages
        all_userlevel = UserLevel.objects.all()
        all_course = Course.objects.all()
        all_userlevel = UserLevelSerializer(all_userlevel, many=True)
        all_course = ClassesModelSerializer(all_course, many=True)
        mes['code'] = 200
        mes['total'] = total
        mes['all_price'] = current_prices.data
        mes['all_userlevel'] = all_userlevel.data
        mes['all_course'] = all_course.data
        return Response(mes)
class AddPrice(APIView):
    """添加课程价格"""
    def post(self,request):
        mes={}
        data=request.data.copy()
        print(data)
        id=data['id']
        # 因为data里传递了修改对应的ID，所以存储序列化的时候无法验证，所以重新定义数据，将除了ID以外的数据重新赋值
        datas={}
        datas['type_id']=data['type']
        datas['course_id']=data['course']
        datas['discount']=float(data['discount'])
        datas['pre_price']=float(data['pre_price'])
        datas['discount_price']=float(data['pre_price'])*float(data['discount'])
        print(datas)
        if id:
            """如果ID存在则修改"""
            a_price=Price.objects.get(id=int(data['id']))
            one_price = PriceSerializers(a_price, data=datas)
        else:
            """ID不存在为添加"""
            one_price=PriceSerializers(data=datas)
        try:
            if one_price.is_valid():
                one_price.save()
                # email = data['email']
                # send_m = EmailMessage('欢迎注册',"欢迎你:<a href='http://localhost:8000/valid_email?code=" + token + "'>点此</a>点此链接进行激活",settings.DEFAULT_FROM_EMAIL, [email, '1254918445@qq.com'])
                # send_m.content_subtype = 'html'
                # send_m.send()
                mes['code'] = 200
                mes['message'] = '成功'

            else:
                mes['code'] = 201
                mes['message'] = '添加失败'
        except:
            mes['code'] = 400
            mes['message'] = '信息错误'
        return Response(mes)
class DeletePrice(APIView):
    """删除课程价格接口"""
    def post(self,request):
        mes={}
        data = request.data
        one_price = Price.objects.filter(id=int(data['id'])).first()
        one_price.delete()
        mes['code'] = 200
        mes['msg'] = '删除成功'
        return Response(mes)
class DeletePrices(APIView):
    """批量删除课程价格接口"""
    def post(self,request):
        mes={}
        data=request.data
        ids=data['ids']
        id_list =ids.split(',')
        for id in id_list:
            id=int(id)
            one_price=Price.objects.get(id=id)
            try:
                one_price.delete()
                mes['code']=200
                mes['message']='删除成功'
            except:
                mes['code']=201
                mes['message']='删除失败'
        return Response(mes)
from fdfs_client.client import Fdfs_client
def uploadmingwebimg(request):
    file = request.FILES.get('image')
    print(file.name)
    client=Fdfs_client('/Users/qianqian/githubproject/information/online_edu/edu/client.conf')
    res=client.upload_by_filename('/Users/qianqian/Desktop/小可爱/'+file.name)
    # res=client.upload_by_filename('/Users/qianqian/Desktop/小可爱/5.jpg')
    print(res)
    return HttpResponse('ok')
#
# import paramiko
#
# def get_ssh(host,username,password):
#     sh = paramiko.SSHClient()
#     sh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     sh.connect(host, username=username, password=password) #host是阿里云服务器的ip，username是root，password是ssh连接阿里云服务器的密码
#     t = 'abc' #对应操作的文件信息
#     stdin, stdout, stderr = sh.exec_command('cd /home/test;rm -rf '+t)
#     result = stdout.read()
#     sh.close()
#     return result
#
# def beifen_ssh(request):
#
#     sh = paramiko.SSHClient()
#     sh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#     sh.connect('120.27.246.172', username = 'root', password = 'Wq960117') #host是阿里云服务器的ip，username是root，password是ssh连接阿里云服务器的密码
#     stdin, stdout, stderr = sh.exec_command('sh /home/soft/backupdb.sh')
#     result = stdout.read()
#     sh.close()
#     return HttpResponse('ok')


class GetCoupon(APIView):
    """获取优惠券相关信息"""
    def get(self,request):
        mes={}
        all_coupon=Coupon.objects.all()
        page=request.GET.get('page')
        if page:
            page=int(page)
        else:
            page=1
        print(page)
        paginator=Paginator(all_coupon,2)
        current_coupon=paginator.get_page(page)
        current_coupon=CouponModelSerializer(current_coupon,many=True)
        total=paginator.num_pages

        all_course=Course.objects.all()
        all_course=ClassesModelSerializer(all_course,many=True)

        mes['code']=200
        mes['total']=total
        mes['all_coupon']=current_coupon.data
        mes['all_course']=all_course.data
        return Response(mes)
class AddCoupon(APIView):
    """添加优惠券价格"""
    def post(self,request):
        mes={}
        data=request.data.copy()
        print(data)
        id=data['id']
        # 因为data里传递了修改对应的ID，所以存储序列化的时候无法验证，所以重新定义数据，将除了ID以外的数据重新赋值
        datas={}
        # if (data['course']==''):
        datas['course_id']=None
        datas['name']=data['name']
        datas['count']=data['count']
        datas['type']=data['type']
        datas['start_time']=data['start_time']
        datas['end_time']=data['end_time']
        datas['condition']=data['condition']
        datas['integral']=data['integral']
        datas['money']=float(data['money'])
        datas['status']=data['status']
        print(datas)

        if id:
            """如果ID存在则修改"""
            a_coupon=Coupon.objects.get(id=int(data['id']))
            one_coupon = CouponSerializers(a_coupon, data=datas)
        else:
            """ID不存在为添加"""
            one_coupon=CouponSerializers(data=datas)
        try:
            if one_coupon.is_valid():
                one_coupon.save()
                mes['code'] = 200
                mes['message'] = '成功'

            else:
                mes['code'] = 201
                mes['message'] = '添加失败'
        except:
            mes['code'] = 400
            mes['message'] = '信息错误'
        return Response(mes)
class DeleteCoupon(APIView):
    """删除优惠券价格接口"""
    def post(self,request):
        mes={}
        data = request.data
        one_coupon = Coupon.objects.filter(id=int(data['id'])).first()
        one_coupon.delete()
        mes['code'] = 200
        mes['msg'] = '删除成功'
        return Response(mes)
class DeleteCoupons(APIView):
    """批量删除优惠券价格接口"""
    def post(self,request):
        mes={}
        data=request.data
        ids=data['ids']
        id_list =ids.split(',')
        for id in id_list:
            id=int(id)
            one_coupon=Coupon.objects.get(id=id)
            try:
                one_coupon.delete()
                mes['code']=200
                mes['message']='删除成功'
            except:
                mes['code']=201
                mes['message']='删除失败'
        return Response(mes)

from django.shortcuts import render
from dwebsocket import accept_websocket
import time
import paramiko
import re
import threading
import time
import sys
host = '120.27.246.172'
username = 'root'
password = 'Wq960117'


def recv_ssh_msg(channle, ws):
    '''
        channle: 建立好的SSH连接通道
        这个函数会不停的接收ssh通道返回的命令
        返回到前端的ws套接字里
    '''
    while not channle.exit_status_ready():
        try:
            buf = channle.recv(1024)  # 接收 蓝色
            ws.send(buf)  # 巧克力色
        except:
            break


@accept_websocket
def webssh(request):
    '''
        1: 接收前端(ws)的命令，发给后台(ssh)
        2: 接收后台的返回结果，给到前端
    '''
    if request.is_websocket:
        # 判断是否属于websocket连接
        sh = paramiko.SSHClient()

        sh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sh.connect(host, username=username, password=password)
        channle = sh.invoke_shell(term='xterm')  #
        ws = request.websocket
        t = threading.Thread(target=recv_ssh_msg, args=(channle, ws))
        t.setDaemon(True)  # 会随着主进程的消亡而消亡
        t.start()
        # 连接的客户端套接字对象
        # ws.recv() ws.read() ws.wait() 接受前端发来的数据
        # ws.send() ws.send() 发送给浏览器数据
        while not channle.exit_status_ready():
            # time.sleep(0.1)
            cmd = ws.wait()  # 前台发来命令 红色
            if cmd:
                # 转交给后端
                channle.send(cmd)  # 黄色
            else:
                # cmd为空，连接断开的标志
                break
        ws.close()
        channle.close()
    return HttpResponse('ok')
import datetime
from datetime import timedelta

class SKAPIView(APIView):
    def get(self, request):
        ret = {}
        activeList = Act.objects.all()
        skList = Sk.objects.all()
        timeList = Time.objects.all()
        activeList = ActModelSerializer(activeList, many=True)
        skList = SkModelSerializer(skList, many=True)
        timeList = TimeModelSerializer(timeList, many=True)
        ret['activeList'] = activeList.data
        ret['skList'] = skList.data
        ret['timeList'] = timeList.data
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)

    def post(self, request):
        ret = {}
        ret['code'] = 200
        ret['message'] = '成功'
        data = request.data.copy()
        if data.get('start') and data.get('end'):
            data['start'] = datetime.datetime.strptime(data['start'].replace('T', ' ')[:-5], "%Y-%m-%d %H:%M:%S")+ timedelta(hours=8)
            data['end'] = datetime.datetime.strptime(data['end'].replace('T', ' ')[:-5], "%Y-%m-%d %H:%M:%S")+ timedelta(hours=8)
            # print(data['start'],data['end'],data['act_id'],'======================================')
            Time.objects.create(start=data['start'],end=data['end'],act_id=data['act_id'])
        elif data.get('title') and data.get('date'):
            print('添加活动')
            data['date'] = datetime.datetime.strptime(data['date'].replace('T', ' ')[:-5], "%Y-%m-%d %H:%M:%S")+ timedelta(hours=8)
            data['date']=data['date']
            print(data)
            Act.objects.create(title=data['title'],data=data['date'])
        elif data.get('course_id') and data.get('time_id') and data.get('act_id'):
            print('添加秒杀商品')
            Sk.objects.create(course_id=data.get('course_id'), time_id=data['time_id'], act_id=data['act_id'],price=data['sk_price'], count=data['count'])
        else:
            ret['code'] = 601
            ret['message'] = '失败'
        return Response(ret)

    def delete(self, request):
        data = request.data.copy()
        mes = {}
        mes['code'] = 200
        mes['msg'] = "删除成功"
        if data.get('sk_id'):
            Sk.objects.get(id=data.get('sk_id')).delete()
        elif data.get('time_id'):
            Time.objects.get(id=data.get('time_id')).delete()
        elif data.get('active_id'):
            Act.objects.get(id=data.get('active_id')).delete()
        else:
            mes['code'] = 400
            mes['msg'] = "删除失败"
        return Response(mes)
