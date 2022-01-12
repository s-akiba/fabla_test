from django.urls import path
from . import views

app_name = 'app_fabla'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('post-list/',views.PostListView.as_view(), name="post_list"),
    # 画面詳細へ
    path('post-detail/<str:pk>/',views.PostDetail.as_view(), name="post_detail"),
    path('congressman/',views.CongressmanListView.as_view(), name="congressman"),
    path('cong-list/',views.CongListView.as_view(), name="cong_list"),
    path('profile/<str:pk>/',views.profileDetail.as_view(), name="profile"),
    path('fabla-create/',views.AppFablaCreateView.as_view(), name="fabla_create"),
    path('ad/',views.AdListView.as_view(), name="ad"),
    # 投稿通報
    path('post-report/<str:pk>/',views.ReportFormView.as_view(),name="post_report"),

    path('like', views.LikeView, name='like'),
]
