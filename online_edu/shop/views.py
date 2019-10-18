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
from redisearch import Client,TextField
from datetime import datetime


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
class GetInvitationCode(APIView):
    """获取邀请码"""
    def get(self,request):
        mes={}
        user_id=request.GET.get('user_id')
        one_user=User.objects.get(id=user_id)
        invitation_code=uuid.uuid4()
        one_user.invitation_code=invitation_code
        one_user.save()
        mes['code']=200
        mes['message']='邀请码获取成功，您的邀请码为：%s'%invitation_code
        return Response(mes)
# celery异步发送邮件
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
        # 保存注册人信息
        one_user=User.objects.create(password=make_password(one_user_data['password']), email=one_user_data['email'], level_id=one_user_data['level_id'], token=token,invitation_coded=one_user_data['invitation_coded'])

        # 查询邀请人信息
        invitater=User.objects.filter(invitation_code=one_user.invitation_coded).first()
        if invitater:
            # 修改邀请人信息,默认注册为普通用户，积分加100
            a_user=User.objects.get(id=invitater.id)
            a_user.integral+=100
            a_user.save()
        else:
            pass
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
    """用户授权后绑定网站账号信息"""
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
        user_id=data['user_id']
        if user_id!=None:
            one_user=User.objects.get(id=data['user_id'])
            levels=UserLevel.objects.filter(id__gt=one_user.level_id).all()
            # 用户价格及升级价格
            one_course = Course.objects.get(id=data['cid'])
            price = Price.objects.filter(course_id=one_course.id, type_id__gte=one_user.level_id).all()
            one_order = Cours_order.objects.filter(user_id=user_id, course_id=one_course.id, order_status=1).first()
            if one_order:
                one_order = CoursOrderModelSerializer(one_order)
                mes['one_order'] = one_order.data
            else:
                mes['one_order'] = 0
            # 用户账户内可用优惠券查询
            user_all_coupons = Integral_coupon.objects.filter(user_id=data['user_id'], status=2).all()
            coupons_id_list = []
            for coupon in user_all_coupons:
                # 绑定课程的优惠券以及未绑定课程的优惠券，在判断价格是否能用
                # 根据用户账户内的优惠券去优惠券表中查询优惠券的对应课程
                one_coupon = Coupon.objects.get(id=coupon.coupon_order)
                if one_coupon.course_id == one_course.id or one_coupon.course_id == None:
                    # 优惠券的满减金额小于价格表中查询出来的用户本身购买课程所需要的金额才可以用
                    if coupon.max_money <= price[0].discount_price:
                        # 将用户账户内可用优惠券的ID存在列表中
                        coupons_id_list.append(coupon.id)
                    else:
                        print('该优惠券金额不可以用于该课程')
                else:
                    print('该优惠券不可以用于这个课程')
            # 查询列表中对应的用户优惠券
            user_coupons = Integral_coupon.objects.filter(id__in=coupons_id_list).all()
            prices = PriceModelSerializer(price, many=True)
            one_user = UserModelSerializer(one_user)
            user_coupons = Integral_couponModelSerializer(user_coupons, many=True)
            mes['prices'] = prices.data
            mes['one_user'] = one_user.data
            mes['user_coupons'] = user_coupons.data


        one_course = Course.objects.get(id=data['cid'])
        teacher_courses=Course.objects.filter(teacher_id=one_course.teacher_id).count()
        sections=Section.objects.filter(course_id=data['cid'])
        one_teacher=Teacher.objects.get(id=one_course.teacher_id)
        reports=Report.objects.filter(course_id_id=one_course.id).all()
        rules = Rules.objects.all()
        print(rules)
        if data['comment_type']==1:
            comments=Comment.objects.filter(id=one_course.id).all()
            comments = CommentModelSerializer(comments, many=True)
        one_course = ClassesModelSerializer(one_course)
        one_teacher = TeacherSerializer(one_teacher)
        sections=SectionModelSerializer(sections,many=True)
        reports=ReportModelSerializer(reports,many=True)
        rules = RuleModelSerializer(rules,many=True)
        mes['code']=200
        mes['one_course']=one_course.data
        mes['sections']=sections.data
        mes['teacher_courses']=teacher_courses
        mes['one_teacher']=one_teacher.data
        mes['comments']=comments.data
        mes['reports']=reports.data
        mes['rules'] = rules.data
        print(rules.data)
        return Response(mes)
class GetUserInfo(APIView):
    def post(self,request):
        mes = {}
        data = request.data
        print(data)
        user_id = data['user_id']
        if user_id != None:
            one_user = User.objects.get(id=data['user_id'])
            levels = UserLevel.objects.filter(id__gt=one_user.level_id).all()
            # 用户价格及升级价格
            one_course = Course.objects.get(id=data['cid'])
            price = Price.objects.filter(course_id=one_course.id, type_id__gte=one_user.level_id).all()
            one_order = Cours_order.objects.filter(user_id=user_id, course_id=one_course.id, order_status=1).first()
            if one_order:
                one_order = CoursOrderModelSerializer(one_order)
                mes['one_order'] = one_order.data
            else:
                mes['one_order'] = 0
            # 用户账户内可用优惠券查询
            user_all_coupons = Integral_coupon.objects.filter(user_id=data['user_id'],status=2).all()
            coupons_id_list = []
            for coupon in user_all_coupons:
                # 绑定课程的优惠券以及未绑定课程的优惠券，在判断价格是否能用
                # 根据用户账户内的优惠券去优惠券表中查询优惠券的对应课程
                one_coupon = Coupon.objects.get(id=coupon.coupon_order)
                if one_coupon.course_id == one_course.id or one_coupon.course_id == None:
                    # 优惠券的满减金额小于价格表中查询出来的用户本身购买课程所需要的金额才可以用
                    if coupon.max_money <= price[0].discount_price:
                        # 将用户账户内可用优惠券的ID存在列表中
                        coupons_id_list.append(coupon.id)
                    else:
                        print('该优惠券金额不可以用于该课程')
                else:
                    print('该优惠券不可以用于这个课程')
            # 查询列表中对应的用户优惠券
            user_coupons = Integral_coupon.objects.filter(id__in=coupons_id_list).all()
            prices = PriceModelSerializer(price, many=True)
            one_user = UserModelSerializer(one_user)
            user_coupons = Integral_couponModelSerializer(user_coupons, many=True)
            mes['prices'] = prices.data
            mes['one_user'] = one_user.data
            mes['user_coupons'] = user_coupons.data
        return Response(mes)

#路径展示
class PathView(APIView):
    def get(self,request):
        mes = {}
        id=request.GET.get('id')

        path = Path.objects.all()
        p = PathModelSerializer(path,many=True)
        if id:
            one_path=Path.objects.get(id=id)
            all_strage=Path_stage.objects.filter(path_id=id).all()
            one_path = PathModelSerializer(one_path)
            all_strage = Path_stageModelSerializer(all_strage,many=True)
            mes['code'] = 200
            mes['pathlist'] = p.data
            mes['one_path'] = one_path.data
            mes['all_strage'] = all_strage.data
        else:
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
        one_user=User.objects.get(id=user_id)
        invitation_code=one_user.invitation_code
        mes['code']=200
        mes['all_coupons']=all_coupons.data
        mes['user_coupons'] = user_coupons.data
        mes['invitation_code'] = invitation_code
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
        else:
            # Integral_coupon.objects.create(user_id=36,coupon_order=data['id'],count=1,max_money=one_coupon.money,coupon_money=one_coupon.condition,type=one_coupon.type,status=1,start_time='2019-12-18 00:00:00',end_time='2019-12-20 00:00:00')
            Integral_coupon.objects.create(user_id=data['user_id'],coupon_order=data['id'],count=1,max_money=one_coupon.money,coupon_money=one_coupon.condition,type=one_coupon.type,status=1)
            one_coupon.save()
            mes['code'] = 200
            mes['message'] = '领取成功'
        print(mes['message'])

        return Response(mes)
class AddOrder(APIView):
    """添加会员订单接口"""
    def post(self,request):
        mes={}
        data=request.data
        print(data)
        code=request.session.get('image_code')
        print(code)
        if code!=data['code']:
            mes['code'] = 406
            mes['message'] = '验证码错误'
            mes['order_sn'] = ''
        else:
            order_sn=uuid.uuid1()
            one_order= MemberOrder.objects.filter(order_sn=order_sn).first()
            if one_order:
                mes['code'] = 407
                mes['message'] = '已有重复未支付订单'
                mes['order_sn'] = ''
            else:
                one_member=Member.objects.filter(user_id=data['user_id']).first()
                if one_member:
                #     在有效会员表中判断是否有会员信息，如果在有效会员时间内，则不能购买
                    mes['code'] = 408
                    mes['message'] = '已购买会员在有效时间内'
                    mes['order_sn'] = ''
                else:
                    MemberOrder.objects.create(order_sn=order_sn,amount=data['money'],level=data['level'],status=0,type=data['type'],user_id=data['user_id'])
                    mes['code']=200
                    mes['message'] = '生成订单成功'
                    mes['order_sn'] = order_sn
        return Response(mes)
class FinishPay(APIView):
    """支付完成后修改订单信息接口"""
    def get(self,request):
        mes={}
        # 接收支付成功后返回的流水号和订单号
        out_trade_no=request.GET.get('out_trade_no') # 流水号
        order_sn=request.GET.get('order_sn')    # 订单号
        # 查询并修改对应订单信息，支付状态，流水号等
        one_order=MemberOrder.objects.filter(order_sn=order_sn).first()
        # 处理会员订单的信息
        if one_order:
            one_order.serial_number=out_trade_no
            one_order.status=1
            one_order.save()
            # 将信息存入有效订单表
            Member.objects.create(user_id=one_order.user_id,level=one_order.level)
            # 修改用户状态
            one_user=User.objects.get(id=one_order.id)
            one_user.level_id=one_order.level
            one_user.save()
            print(out_trade_no)
            mes['code']=200
            return HttpResponseRedirect('http://127.0.0.1:8080/index')
        else:
            conn=get_redis_connection('default')
            one_order=conn.get(order_sn)
            one_order=json.loads(one_order)
            print(one_order)
            if one_order['coupon'] != -1:
                one_user_coupon = Integral_coupon.objects.get(id=one_order['coupon'])
                print(one_user_coupon)
                """使用优惠券情况"""
                one_coupon = Coupon.objects.get(id=one_user_coupon.coupon_order)
                print(one_coupon)
                try:
                # 修改订单状态
                    print('begin')
                    Cours_order.objects.create(code=out_trade_no,order_number=order_sn, user_id=one_order['user_id'], course_id=one_order['course_id'],pyt_type=one_order['pyt_type'], pay_price=float(one_order['total_price']), price=float(one_order['price']), order_status=1,coupon=one_coupon.id, preferential_way=one_order['preferential_way'],preferential_money=one_order['preferential_money'])
                #     修改优惠券状态
                    one_user_coupon = Integral_coupon.objects.get(user_id=one_order['user_id'],coupon_order=one_coupon.id)
                    one_user_coupon.status=1
                    one_user_coupon.save()
                    mes['code'] = 200
                    mes['message'] = '购买成功'
                    print('success1')
                except Exception as e:
                    print(e)
                    mes['code'] = 200
                    mes['message'] = '购买失败'
                    print('error1')

            else:
                try:
                    Cours_order.objects.create(code=out_trade_no,order_number=order_sn, user_id=one_order['user_id'], course_id=one_order['course_id'],pyt_type=one_order['pyt_type'], pay_price=float(one_order['pay_price']), price=float(one_order['price']), order_status=1,preferential_way=one_order['preferential_way'], preferential_money=one_order['preferential_money'])
                    # 修改积分
                    one_user = User.objects.get(id=one_order['user_id'])
                    one_user.inintegral -= one_order['inintegral']
                    one_user.save()
                    mes['code'] = 200
                    mes['message'] = '购买成功'
                    print('success2')
                except Exception as e:
                    print(e)
                    mes['code'] = 200
                    mes['message'] = '购买失败'
                    print('error2')

            # # one_user.integral-=

            return HttpResponseRedirect('http://127.0.0.1:8080/index')

"""
    order_number = models.CharField(max_length=100)  # 订单编号
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 用户外键
    course = models.ForeignKey('Course', on_delete=models.CASCADE)  # 课程外键
    pyt_type = models.IntegerField()  # 支付方式  1微信  2支付宝
    price = models.DecimalField(max_digits=7, decimal_places=2)  # 商品价格
    pay_price = models.DecimalField(max_digits=7, decimal_places=2)  # 实际支付
    preferential_way = models.IntegerField()  # 优惠方式  0 未使用  1积分  2优惠券
    preferential_money = models.DecimalField(max_digits=7, decimal_places=2)  # 优惠金额
    order_status = models.IntegerField()  # 订单状态  0待支付  1支付成功
    code = models.CharField(max_length=100)  # 流水号
    coupon = models.CharField(max_length=100)  # 优惠码,存的是优惠券表中优惠券对应的ID
    {'user_id': '36', 'course_id': 1, 'price': '400.00', 'pyt_type': 1, 'total_price': 380, 'integral': 0, 'preferential_way': 2, 'coupon': 17}
"""
class AddCourse(APIView):
    """添加课程订单接口"""
    def post(self,request):
        conn = get_redis_connection('default')
        mes={}
        data=request.data
        print(data)
        order_number=uuid.uuid1() #订单号


        try:
            # conn.set(order_number,json.dumps(data),timeout=300)
            conn.set(order_number, json.dumps(data),300)
            mes['code'] = 200
            mes['message'] = '订单生成成功'
            mes['order_sn'] = order_number
        except Exception as e:
            print(e)
            mes['code'] = 201
            mes['message'] = '订单生成失败'
        # user_id=data['user_id'] #用户外键
        # course_id=data['course_id'] #课程外键
        # pyt_type=data['pyt_type'] #支付方式
        # price=data['price'] #商品价格
        # pay_price=data['total_price'] #商品实际支付价格
        # preferential_way=data['preferential_way'] #优惠方式 0 未使用  1积分  2优惠券
        # preferential_money=data['preferential_money']
        # if data['coupon']!=-1:
        #     one_user_coupon = Integral_coupon.objects.get(id=data['coupon'])
        #     """使用优惠券情况"""
        #     one_coupon = Coupon.objects.get(id=one_user_coupon.coupon_order)
        #     one_order=Cours_order.objects.filter(user_id=user_id,course_id=course_id,price=price,order_status=0,coupon=one_coupon.id,preferential_way=preferential_way,preferential_money=preferential_money).first()
        # else:
        #     """使用积分情况"""
        #     one_order = Cours_order.objects.filter(user_id=user_id, course_id=course_id, price=price, order_status=0,preferential_way=preferential_way,preferential_money=preferential_money).first()
        # if one_order:
        #     mes['code'] = 203
        #     mes['message'] = '存在相同未支付订单'
        #     mes['order_sn'] = one_order.order_number
        # else:
        #     if data['coupon'] != -1:
        #         # one_user_coupon = Integral_coupon.objects.get(id=data['coupon'])
        #         # """使用优惠券情况"""
        #         # one_coupon = Coupon.objects.get(id=one_user_coupon.coupon_order)
        #         try:
        #             Cours_order.objects.create(order_number=order_number,user_id=user_id,course_id=course_id,pyt_type=pyt_type,pay_price=pay_price,price=price,order_status=0,coupon=one_coupon.id,preferential_way=preferential_way,preferential_money=preferential_money)
        #             mes['code']=200
        #             mes['message']='订单生成成功'
        #             mes['order_sn']=order_number
        #         except:
        #             mes['code'] = 201
        #             mes['message'] = '订单生成失败'
        #     else:
        #         print('aasdfghjk,m.gdtfhgjkldfg_______________________')
        #         try:
        #             Cours_order.objects.create(order_number=order_number, user_id=user_id, course_id=course_id,pyt_type=pyt_type, pay_price=pay_price, price=price, order_status=0,preferential_way=preferential_way,preferential_money=preferential_money)
        #             mes['code'] = 200
        #             mes['message'] = '订单生成成功'
        #             mes['order_sn'] = order_number
        #         except:
        #             mes['code'] = 201
        #             mes['message'] = '订单生成失败'
        return Response(mes)
class GetCoupon(APIView):
    def post(self,request):

        mes={}
        data=request.data
        print(data)
        one_user_coupon=Integral_coupon.objects.get(id=data['coupon'])
        one_coupon=Coupon.objects.get(id=one_user_coupon.coupon_order)
        one_coupon=CouponModelSerializer(one_coupon)
        mes['code']=200
        mes['one_coupon']=one_coupon.data
        return Response(mes)
#
# class FullTextSearch(APIView):
#     def post(self,request):
#         #获取前台查找的关键字
#         data=request.data
#         #创建一个客户端与给定索引名称
#         client= Client('oneindex', host='localhost', port='6379')
#         #创建索引定义和模式
#         client.create_index((TextField('title'),TextField('body')))
#         # 索引文件
#         client.add_document('doc2', title='你好', body='中国上下5000年,唐诗三百首', language='chinese')
#         # 查找搜索
#         res=client.search(('上下'))
#         print(res.docs[0].title)


class RedisSearch(APIView):
    def get(self, request):
        # data=request.data
        mes = {}
        search_key=request.GET.get('key')
        print(search_key)
        all_classes = Course.objects.all()
        print("开始创建索引——————————————————————————")
        # 创建一个客户端与给定索引名称
        client = Client('CII' + str(datetime.now()), host='101.37.25.38', port='6666')

        # 创建索引定义和模式
        client.create_index((TextField('title'), TextField('body')))
        print('索引创建完毕————————————————————————————————')
        print('开始添加数据————————————————————————————————')

        for i in all_classes:
            print(str(i.id) + str(i.title))
            # 索引文
            client.add_document('result' + str(datetime.now()), title=i.title + '@' + str(i.id), info=i.info,
                                language='chinese')
            print(333333333)
        print('数据添加完毕————————————————————————————————')
        print(client.info())
        # 查找搜索
        res = client.search(search_key)
        print('查询结束————————————————————————————————————————————————')
        id_list=[]
        print(res.docs)
        for i in res.docs:
            # print(i.title)  # 取出title，以@切割，取课程ID查询，然后序列化展示
            id=i.title.split('@')[1]
            id_list.append(id)
        course=Course.objects.filter(id__in=id_list).all()
        c=CourseModelSerializer(course,many=True)
        mes['course']=c.data
        mes['code'] = 200
        mes['message'] = '搜索完毕'
        return Response(mes)