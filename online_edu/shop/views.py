from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from edu.models import *
from django.contrib.auth.hashers import make_password,check_password
import re
from django.core.mail import EmailMessage
from online_edu import settings
import uuid
# from utils.captcha.captcha import captcha
from serializers.serializer import *
# 获取图片验证码
# def GetImageCode(request):
#     name,text,image=captcha.generate_captcha()
#     request.session['image_code']=text
#     return HttpResponse(image,'image/jpg')
# 注册
class RegUser(APIView):
    def post(self,request):
        mes={}
        one_leve = UserLevel.objects.get(level='普通用户')
        data=request.data.copy()
        password=data['password']
        email=data['email']
        data['level_id']=one_leve.id
        data['is_active']=0
        data['integral']=0
        data['invitation_code']=''
        token = str(uuid.uuid1())
        data['token'] = token
        data['password'] = make_password(password)
        print(data)
        #1  判断用户是否已经存在
        one_user=User.objects.filter(email=email).first()
        if one_user:
            mes['code'] = 402
            mes['message'] = '用户已存在'
            return mes
        #2  判断密码是否低于6位
        if len(password)<=6:
            mes['code'] = 403
            mes['message'] = '密码低于6位'
            return mes
        #3  判断邮箱格式是否正确
        if not re.match("^[a-z0-9A-Z]+[-|a-z0-9A-Z._]+@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-z]{2,}$",data[ 'email' ]):
            mes['code'] = 405
            mes['message'] = '邮箱格式不正确'
            return mes
        #4  信息匹配发送邮箱验证
        u=UserSerializer(data=data)
        if u.is_valid():
            u.save()
            email = data['email']
            send_m = EmailMessage('欢迎注册',"欢迎你:<a href='http://localhost:8000/valid_email?code=" + token + "'>点此</a>点此链接进行激活",settings.DEFAULT_FROM_EMAIL, [email, '1334178184@qq.com'])
            send_m.content_subtype = 'html'
            send_m.send()
            mes['code']=200
            mes['message']='注册成功'

        else:
            mes['code']=201
            mes['message']='注册失败'
        return Response(mes)


from django.db.models import Q
class Login(APIView):
    def post(self,request):
        mes={}
        data=request.data
        username=data['username']
        password=data['password']
        email=data['email']
        #1  判断用户是否已经存在
        one_user=User.objects.filter(Q(username=username)|Q(email=email)).first()
        if not one_user:
            mes['code'] = 402
            mes['message'] = '注册后登录'

        #2  判断密码是否低于6位
        if len(password)<=6:
            mes['code'] = 403
            mes['message'] = '密码低于6位'

        #3  信息匹配发送邮箱是否激活
        if one_user.is_active==0:
            mes['code'] = 406
            mes['message'] = '用户未激活'
        if check_password(password,one_user.password):
            # 生成token
            # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # payload = jwt_payload_handler(user)
            # token = jwt_encode_handler(payload)
            # user.token = token
            # u = {}
            # u['username'] = user.username
            # u['user_id'] = user.id
            # u['token'] = token
            # mes['code'] = 200
            # mes['user'] = u
            mes['code'] = 200
            mes['message'] = '登录成功'
        else:
            mes['code'] = 200
            mes['message'] = '密码错误'
        return Response(mes)
class ceshi(APIView):
    def get(self,request):
        mes={}
        mes['code']=200
        return Response(mes)

