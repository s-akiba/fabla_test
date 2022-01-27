from unicodedata import name
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
    path('profile-ed/<str:pk>/',views.profileEdit.as_view(), name="profile_edit"),
    path('fabla-create/',views.AppFablaCreateView.as_view(), name="fabla_create"),
    path('ad/',views.AdListView.as_view(), name="ad"),
    # 投稿通報
    path('post-report/<str:pk>/',views.ReportFormView.as_view(),name="post_report"),
    path('like', views.LikeView, name='like'),
    path('comment',views.CommentView,name="comment"),
    path('hispost-list/',views.HisPosListView.as_view(),name="his_post_list"),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signup_done/', views.SignupDone.as_view(), name='sign_up_done'),
    path('hispost-list/',views.HisPosListView.as_view(),name="post_list"),
    path('good-history/',views.Goodhistory.as_view(),name='good_history')

]


