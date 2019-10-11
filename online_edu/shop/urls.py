from django.urls import path
from shop import views
urlpatterns = [
    # path('ceshi/', views.ceshi.as_view()),
    path('getcode/',views.generate_captcha),
    path('register/', views.RegUser.as_view()),
    path('send/', views.SendMailAPIView.as_view()),
    path('login/',views.Login.as_view()),
    path('active/',views.active)



]














