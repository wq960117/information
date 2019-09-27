from django.urls import path
from edu import views
urlpatterns = [
    path('edit_relation/',views.EditRelation.as_view()),
    path('delete_relation/',views.DeleteRelation.as_view()),
    path('delete_relations/',views.DeleteRelations.as_view()),
    path('get_relations/',views.GetRelations.as_view()),
]
