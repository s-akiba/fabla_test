from django.urls import path
from . import views

app_name = 'app_fabla'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('post-list/',views.PostListView.as_view(), name="post_list"),
    # 画面詳細へ
    path('post-detail/<uuid:pk>/',views.PostDetail.as_view(),name="post_detail"),
    path('fabla-create/', views.AppFablaCreateView.as_view(), name="fabla_create"),
]
