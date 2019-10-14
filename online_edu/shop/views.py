from django.shortcuts import render,HttpResponse,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from edu.models import *
from django.contrib.auth.hashers import make_password,check_password
import re
from django.core.mail import EmailMessage
from online_edu import settings
import uuid
from utils.captcha.captcha import captcha
from serializers.serializer import *
from django.db.models import Q
from rest_framework_jwt.settings import api_settings
from .task import sendmail



# 获取图片验证码
def generate_captcha(request):
    name,text,image=captcha.generate_captcha()
    request.session['image_code']=text
    print(request.session.get('image_code'))
    return HttpResponse(image,'image/png')
from django_redis import get_redis_connection
import json
# 注册
class RegUser(APIView):
    def post(self, request):
        conn = get_redis_connection('default')
        mes = {}
        one_leve = UserLevel.objects.get(level='普通用户')
        data = request.data.copy()
        password = data['password']
        email = data['email']
        data['level_id'] = one_leve.id
        password = make_password(password)
        print(data)
        code=request.session.get('image_code')
        print(request.session.get('image_code'))
        token = str(uuid.uuid1())
        # 1  判断用户是否已经存在
        # one_user = User.objects.filter(email=email).first()
        one_user=conn.get(token)
        print(one_user)
        if one_user:
            mes['code'] = 402
            mes['message'] = '用户已存在'
        # 2  判断密码是否低于6位
        if len(password) <= 6:
            mes['code'] = 403
            mes['message'] = '密码低于6位'
        # 3  判断邮箱格式是否正确
        if not re.match("^[a-z0-9A-Z]+[-|a-z0-9A-Z._]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$", data['email']):
            mes['code'] = 407
            mes['message'] = '邮箱格式不正确'
        if code!=data['code']:
            mes['code'] = 406
            mes['message'] = '验证码错误'
        try:
            # User.objects.create(password=password,email=email,level_id=data['level_id'],token=token)
            conn.set(token,json.dumps(data))
            sendmail.delay(email,token)
            # send_m=EmailMessage('欢迎注册',"欢迎你:<a href=' http://127.0.0.1:8000/shop/active/?token="+token+"'>点此链接进行激活</a>",settings.DEFAULT_FROM_EMAIL,[email,'1254918445@qq.com'])
            # send_m.content_subtype = 'html'
            # send_m.send()
            mes['code'] = 200
            mes['message'] = '请验证邮箱'
        except:
            mes['code'] = 201
            mes['message'] = '注册失败'
        return Response(mes)




'''用户名,密码,邮箱,判断用户表邮箱状态,比对密码'''
# 登录
class Login(APIView):
    def post(self,request):
        mes={}
        data=request.data
        print(data)
        # username=data['username']
        password=data['password']
        email=data['email']
        #  判断用户是否已经存在
        # one_user=User.objects.filter(Q(username=username)|Q(email=email)).first()
        one_user=User.objects.filter(email=email).first()
        if one_user:
            #判断状态,是否验证通过
            if one_user.is_active == 1:
                #判断图片验证码是否一致
                print(request.session.get('image_code'))
                if request.session.get('image_code')==data['code']:
                    #判断密码是否与获取到的一致
                    if check_password(password,one_user.password):
                    # if password==one_user.password:
                        #生成token保存到用户表中
                        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                        payload = jwt_payload_handler(one_user)
                        token = jwt_encode_handler(payload)
                        one_user.token=token
                        one_user.save()
                        mes['code'] = 200
                        # mes['']
                        mes['message'] = '登录成功'
                        mes['user_id'] = one_user.id
                        mes['username'] = one_user.email
                        mes['token'] = one_user.token
                    else:
                        mes['code'] = 401
                        mes['message'] = '密码错误'
                else:
                    mes['code'] = 405
                    mes['message'] = '验证码错误'
            else:
                mes['code'] = 402
                mes['message'] = '用户未激活'
        else:
            mes['code'] = 403
            mes['message'] = '用户不存在'
        return Response(mes)






# 发送邮件
class SendMailAPIView(APIView):
    def get(self, request):
        ret={}
        sendmail.delay('1334178184@qq.com','123')
        ret['code'] = 200
        ret['message'] = '成功'
        return Response(ret)


# 邮箱验证，修改用户状态
def active(request):
    token=request.GET.get('token')
    conn = get_redis_connection('default')
    print('用户点击验证')
    if token:
        one_user_data=conn.get(token)
        one_user_data=json.loads(one_user_data)
        print(one_user_data)
        print(one_user_data['email'])
        one_user=User.objects.create(password=make_password(one_user_data['password']), email=one_user_data['email'], level_id=one_user_data['level_id'], token=token)
        del token
        # one_user=User.objects.filter(token=token).first()
        if one_user:
            one_user.is_active=1
            one_user.save()
            return HttpResponse('激活成功~~~~')


"""
三方登录：
1、vue页面点击微博登录，调用get_url的接口，返回的是微博授权的url
2、requests请求微博授权的url，返回的是一个code
3、内部请求授权接口，拼接地址，请求一个界面，要求用户输入邮箱绑定账号
4、丙丁成功返回信息保存到第三3表中
"""
# 第三方登录授权页面的地址
def get_url(request):
    # #回调网址
    redirect_url = "http://127.0.0.1:8000/shop/get_token/"
    # #应用id
    client_id = '204877894'
    url = "https://api.weibo.com/oauth2/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_url}".format(client_id=client_id, redirect_url=redirect_url)
    return redirect(url)

import requests
from django.http import HttpResponseRedirect
def get_access_token(request):

    #获取回调的code
    code = request.GET.get('code')
    print(code)
    #微博认证地址
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    #参数
    response = requests.post(access_token_url,data={
        "client_id": '204877894',
        "client_secret": "14c2a1e227b3e073d4983c1258d424c6",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/shop/get_token/",
    })
    res = response.text
    res = eval(str(res))
    uid = res.get('uid')
    print(uid)
    #uid和网站用户绑定

    mes={}
    mes['uid']=uid
    one_user=ThirdPartyLogin.objects.filter(uid=uid).first()
    if one_user:
        return HttpResponseRedirect('http://127.0.0.1:8080/index')
    else:
        return HttpResponseRedirect('http://127.0.0.1:8080/user_bind/'+uid)
class UserBind(APIView):
    def post(self,request):
        mes={}
        data = request.data
        print(data)
        email=data['email']
        password=data['password']
        uid=data['uid']
        one_user=User.objects.filter(email=data['email']).first()
        if not all([email,password]):
            mes['code'] = 201
            mes['message'] = '信息不完整'
        if one_user:
            if check_password(data['password'],one_user.password):
                if one_user.is_active==1:
                    one_third=ThirdPartyLogin.objects.create(user=one_user,uid=uid,login_type=0) # 0微博，1微信，2qq
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(one_user)
                    token = jwt_encode_handler(payload)
                    one_user.token=token
                    one_third.save()
                    one_user.save()
                    mes['code'] = 200
                    mes['message'] = '绑定成功'
                    mes['token'] = token
                else:
                    mes['code'] = 204
                    mes['message'] = '邮箱未激活'
            else:
                mes['code'] = 202
                mes['message'] = '密码错误'
        else:

            mes['code'] = 203
            mes['message'] = '邮箱不存在'
        return Response(mes)

#首页展示学习路径,推荐课程
class AllPath(APIView):
    def get(self,request):
        mes = {}
        # 路径
        show_path = Path.objects.all()
        # 推荐课程
        course = Course.objects.filter(recommand=0) # 0推荐 1不推荐
        mes['course'] = CourseModelSerializer(course, many=True).data
        mes['pathlist'] = PathModelSerializer(show_path, many=True).data
        mes['code'] = 200
        return Response(mes)

# 课程首页信息展示 1--标签   2---课程    Python  Linux
class Courses(APIView):
    def get(self,request):
        mes={}
        tag=Tag.objects.all()
        course=Course.objects.all()
        path=Path.objects.all()
        c=CourseModelSerializer(course,many=True)
        t=TagModelSerializer(tag,many=True)
        p=PathModelSerializer(path,many=True)
        mes['code']=200
        mes['courselist']=c.data
        mes['taglist']=t.data
        mes['pathlist']=p.data
        return Response(mes)
# 课程展示    获取到前台的类别id,标签id,进行查找,默认展示所有课程
class Courselist(APIView):
    def post(self,request):
        mes={}
        data=request.data
        print(data)
        filterdict={}
        for i in data:
            if i != 'change_id' and data[i]!=-1:
                filterdict[i]=data[i]
            else:
                continue
        print(filterdict)
        # course = Course.objects.filter(**filterdict).order_by('-attention')
        if data['change_id']=='attention':
            course = Course.objects.filter(**filterdict).order_by('-attention')
        else:
            course = Course.objects.filter(**filterdict).order_by('-learn')
        course = CourseModelSerializer(course, many=True)
        mes['code']=200
        mes['courselist']=course.data
        return Response(mes)
class GetCourse(APIView):
    """获取某一课程的全部信息"""
    def post(self,request):
        mes={}
        data=request.data
        print(data)
        one_course=Course.objects.get(id=data['cid'])
        teacher_courses=Course.objects.filter(teacher_id=one_course.teacher_id).count()
        sections=Section.objects.filter(course_id=data['cid'])
        one_teacher=Teacher.objects.get(id=one_course.teacher_id)
        reports=Report.objects.filter(course_id_id=one_course.id).all()
        if data['comment_type']==1:
            comments=Comment.objects.filter(id=one_course.id).all()
            comments = CommentModelSerializer(comments, many=True)
        one_course = ClassesModelSerializer(one_course)
        one_teacher = TeacherSerializer(one_teacher)
        sections=SectionModelSerializer(sections,many=True)
        reports=ReportModelSerializer(reports,many=True)
        mes['code']=200
        mes['one_course']=one_course.data
        mes['sections']=sections.data
        mes['teacher_courses']=teacher_courses
        mes['one_teacher']=one_teacher.data
        mes['comments']=comments.data
        mes['reports']=reports.data
        return Response(mes)
#路径展示
class PathView(APIView):
    def get(self,request):
        mes = {}
        path = Path.objects.all()
        p = PathSerializers(path,many=True)
        mes['code'] = 200
        mes['pathlist'] = p.data
        return Response(mes)

# 所有优惠券展示接口
class GetCoupons(APIView):
    def get(self,request):
        mes={}
        user_id=request.GET.get('user_id')
        print(user_id)
        all_coupons=Coupon.objects.all()
        all_coupons=CouponModelSerializer(all_coupons,many=True)
        user_coupons = Integral_coupon.objects.filter(user_id=user_id).all()
        user_coupons = Integral_couponModelSerializer(user_coupons, many=True)
        mes['code']=200
        mes['all_coupons']=all_coupons.data
        mes['user_coupons'] = user_coupons.data
        return Response(mes)

class AddCoupon(APIView):
    """添加用户优惠券"""
    def post(self,request):
        mes={}
        data=request.data
        print(data)
        one_coupon=Coupon.objects.filter(id=data['id']).first()
        one_user_coupon=Integral_coupon.objects.filter(coupon_order=data['id'],user_id=data['user_id']).first()
        if one_user_coupon:
            mes['code']=202
            mes['message']='您已经领取该优惠券'
            mes['user_coupons']=[]
        else:
            # Integral_coupon.objects.create(user_id=36,coupon_order=data['id'],count=1,max_money=one_coupon.money,coupon_money=one_coupon.condition,type=one_coupon.type,status=1,start_time='2019-12-18 00:00:00',end_time='2019-12-20 00:00:00')
            Integral_coupon.objects.create(user_id=36,coupon_order=data['id'],count=1,max_money=one_coupon.money,coupon_money=one_coupon.condition,type=one_coupon.type,status=1)
            one_coupon.save()
            mes['code'] = 200
            mes['message'] = '领取成功'

        return Response(mes)
