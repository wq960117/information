from django.urls import path
from edu import views
urlpatterns = [
    # 添加用户等级
    path('userleveladd/', views.UserLevel_Add.as_view()),
    # 用户等级展示
    path('userlevellist/', views.UserLevel_List.as_view()),
    path('get_userLevels/', views.Get_UserLevels.as_view()),
    # 更新用户等级
    path('update_userlevel/', views.UserLevelUpdate.as_view()),
    # 删除用户等级
    path('delete_userlevel/', views.DeleteUser.as_view()),
    # 批量删除用户等级
    path('delete_userlevels/', views.DeleteUsers.as_view()),

    # 添加用户等级条件
    path('ulc_add/', views.UserLevelCondition_add.as_view()),  # 添加
    # 修改用户等级关系
    path('edit_relation/',views.EditRelation.as_view()),
    # 删除用户等级关系
    path('delete_relation/',views.DeleteRelation.as_view()),
    # 批量删除用户等级关系
    path('delete_relations/',views.DeleteRelations.as_view()),
    # 用户等级关系展示
    path('get_relations/',views.GetRelations.as_view()),
    # 用户等级关系展示
    path('show_userLevel/',views.Show_UserLevel.as_view()),

    # 注册管理员
    path('reg_admin/',views.RegAdmin.as_view()),
    # 登录管理员
    path('login_admin/',views.LoginAdmin.as_view()),

    #阶段的添加
    path('AddPath/',views.AddPath_stageView.as_view()),
    # 阶段的展示
    path('Path_list/',views.Path_stagelistView.as_view()),
    # 阶段的修改
    path('update_Path/',views.UpdatePath_stageView.as_view()),
    #阶段的删除
    path('delete_path/',views.Delete_PathView.as_view()),


]














