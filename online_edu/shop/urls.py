from django.urls import path
from shop import views
from shop import pay
urlpatterns = [
    # path('ceshi/', views.ceshi.as_view()),
    # 获取验证码接口
    path('getcode/', views.generate_captcha),
    # 用户注册接口
    path('register/', views.RegUser.as_view()),
    # 测试发邮件接口
    path('send/', views.SendMailAPIView.as_view()),
    # 用户登录接口
    path('login/', views.Login.as_view()),
    # 邮件激活修改用户状态接口
    path('active/', views.active),
    # 获取第三方微博登录授权页面的接口
    path('get_url/', views.get_url),
    # 第三方认证接口
    path('get_token/', views.get_access_token),
    # 第三方授权成功后用户绑定信息接口
    path('user_bind/', views.UserBind.as_view()),
    # 前台展示所有路径接口
    path('all_path/', views.AllPath.as_view()),
    # 首页所有推荐课程展示
    path('course/', views.Courses.as_view()),
    # 首页点击对应分类下课程展示
    path('courselist/',views.Courselist.as_view()),
    # 获取某一课程的详细信息
    path('get_course/',views.GetCourse.as_view()),
    #路径展示
    path('path/',views.PathView.as_view()),
    # 所有优惠券展示
    path('get_coupons/',views.GetCoupons.as_view()),
    # 添加用户优惠券
    path('add_coupon/',views.AddCoupon.as_view()),
    # 获取支付宝支付接口
    path('getpayurl/', pay.page1),
    # 生成用户邀请码接口
    path('get_invitation_code/', views.GetInvitationCode.as_view()),
    # 生成会员订单
    path('add_order/', views.AddOrder.as_view()),
    # 根据传回的流水号
    path('finish_pay/', views.FinishPay.as_view()),




]














