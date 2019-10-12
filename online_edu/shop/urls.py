from django.urls import path
from shop import views
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
    path('courselist/',views.Courselist.as_view())



]














