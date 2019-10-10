from django.urls import path
from shop import views
urlpatterns = [
    path('ceshi/', views.ceshi.as_view()),
    # path('getcode/',views.GetImageCode),
    path('register/', views.RegUser.as_view()),



]














