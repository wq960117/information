from django.shortcuts import render,HttpResponse
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

# 注册
class RegUser(APIView):
    def post(self, request):
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
        one_user = User.objects.filter(email=email).first()
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
            User.objects.create(password=password,email=email,level_id=data['level_id'],token=token)
            sendmail.delay(email,token)
            # send_m=EmailMessage('欢迎注册',"欢迎你:<a href=' http://127.0.0.1:8000/shop/active/?token="+token+"'>点此链接进行激活</a>",settings.DEFAULT_FROM_EMAIL,[email,'1254918445@qq.com'])
            # send_m.content_subtype = 'html'
            # send_m.send()
            mes['code'] = 200
            mes['message'] = '注册成功'
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
                    # if check_password(password,one_user.password):
                    if password==one_user.password:
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
    print('用户点击验证')
    if token:
        one_user=User.objects.filter(token=token).first()
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
        return HttpResponseRedirect('http://127.0.0.1:8080/user_bind/?uid='+uid)
class UserBind(APIView):
    def post(self,request):
        mes={}
        data = request.data
        print(data)
        email=data['email']
        password=data['password']
        one_user=User.objects.filter(email=data['email']).first()
        if not all([email,password]):
            mes['code'] = 201
            mes['message'] = '信息不完整'
        if not one_user:
            mes['code']=201
            mes['message']='邮箱账号不存在'
        if check_password(data['password'],one_user.password):
            mes['code'] = 200
            mes['message'] = '绑定成功'
        return Response(mes)

#首页展示学习路径,推荐课程
class AllPath(APIView):
    def get(self,request):
        mes = {}
        # 路径
        show_path = Path.objects.all()
        # 推荐课程
        course = Course.objects.filter(recommand=1)
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
        c=CourseModelSerializer(course,many=True)
        t=TagModelSerializer(tag,many=True)
        mes['code']=200
        mes['courselist']=c.data
        mes['taglist']=t.data
        return Response(mes)

# 课程展示    获取到前台的类别id,标签id,进行查找,默认展示所有课程
class Courselist(APIView):
    def post(self,request):
        mes={}
        member_id=request.data['member_id']
        tag_id=request.data['tag_id']
        print(member_id,tag_id,'==========================')
        #判断两个id都为0时,展示所有课程
        if (member_id and tag_id)==0:
            course=Course.objects.all()
            mes['code']=200
            mes['course']=CourseModelSerializer(course,many=True).data
        #否则,按照条件查找
        else:
            course=Course.objects.filter(member=member_id,tag_id=tag_id).all()
            mes['code']=200
            mes['course']=CourseModelSerializer(course,many=True).data
        return Response(mes)
