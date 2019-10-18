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
    path('delete_storagepath/',views.Delete_PathView.as_view()),
    #添加章节
    path('add_section/',views.AddSection.as_view()),
    #展示课程
    path('courselist/',views.CourseList.as_view()),
    #展示章节
    path('sectionlist/',views.Sectionlist.as_view()),

    #修改章节
    path('updatesection/',views.UpdateSection.as_view()),
    #删除章节
    path('deletesection/',views.DeleteSection.as_view()),

    # todo 标签表
    path('tag_list/', views.TagList.as_view()),  # 增删改查
    path('tag_deletes/', views.TagDeletes.as_view()),  # 批量删除


    # 老师添加
    path('teacher_add/', views.Teacher_add.as_view()),
    # 老师删除
    path('teacher_delete/', views.TeacherDelete.as_view()),
    # 老师展示
    path('teacher_list/', views.Teacher_list.as_view()),
    # 老师修改
    path('teacher_update/', views.Teacher_update.as_view()),

    # 获取课程列表及相关信息
    path('get_classes/', views.GetClasses.as_view()),
    # 添加课程
    path('add_course/', views.Addclasses.as_view()),
    # 批量删除课程
    path('delete_classes/', views.DeleteClasses.as_view()),
    # 删除课程
    path('delete_class/', views.DeleteClass.as_view()),

    # 添加路径
    path('path_add/', views.Path_Add.as_view()),
    # 删除路径
    path('deletepath/', views.DeletePath.as_view()),
    # 修改路径
    path('updatepath/', views.Updatepath.as_view()),
    # 展示路径
    path('show_path/', views.Show_Path.as_view()),

    # 本地upload上传图片
    path('uploadImg/', views.uploadImg),
    # 删除本地upload图片
    path('delete_img/', views.delete_uploadimg),
    # fastdfs上传图片
    path('upload_pic/', views.uploadmingwebimg),
    # # 删除阿里云服务器的图片
    # path('delete_pic/', views.get_ssh),
    # #阿里云备份数据库
    # path('beifen_ssh/', views.beifen_ssh),

    # 展示课程价格接口
    path('get_price/', views.GetPrice.as_view()),
    # 添加课程价格
    path('add_price/', views.AddPrice.as_view()),
    # 删除课程价格
    path('delete_price/', views.DeletePrice.as_view()),
    # 批量删除课程价格
    path('delete_prices/', views.DeletePrices.as_view()),

    # 获取优惠券展示
    path('get_coupon/', views.GetCoupon.as_view()),
    path('add_coupon/', views.AddCoupon.as_view()),
    path('delete_coupon/', views.DeleteCoupon.as_view()),
    path('delete_coupons/', views.DeleteCoupons.as_view()),
    # 可视化编辑窗口的显示
    path('webssh/', views.webssh),
    # 创建索引
    path('redis_search/', views.RedisSearch.as_view()),




]














