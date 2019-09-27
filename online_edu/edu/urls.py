from django.urls import path
from edu import views
urlpatterns = [
    path('edit_relation/',views.EditRelation.as_view()),
    path('delete_relation/',views.DeleteRelation.as_view()),
    path('delete_relations/',views.DeleteRelations.as_view()),
    path('get_relations/',views.GetRelations.as_view()),
    path('update_user/',views.UserLevelUpdate.as_view()),
    path('delete_user/',views.DeleteUser.as_view()),
    path('show_userLevel/',views.Show_UserLevel.as_view()),
    # 注册管理员
    path('reg_admin/',RegAdmin.as_view()),
    # 登录管理员
    path('login_admin/',LoginAdmin.as_view())
]














