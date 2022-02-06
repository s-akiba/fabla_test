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
    path('profile/<str:pk>/',views.profileDetail.as_view(), name="profile"),
    path('profile-ed/<str:pk>/',views.profileEdit.as_view(), name="profile_edit"),
    path('fabla-create/',views.AppFablaCreateView.as_view(), name="fabla_create"),
    path('ad/',views.AdListView.as_view(), name="ad"),
    # 投稿通報
    path('post-report/<str:pk>/',views.ReportFormView.as_view(),name="post_report"),
    path('like', views.LikeView, name='like'),
    path('fabla-create/', views.AppFablaCreateView.as_view(), name="fabla_create"),
    path('comment',views.CommentView,name="comment"),
    path('good-history/',views.Goodhistory.as_view(),name='good_history'),
    path('my-chat-list/<str:name>/', views.MyChatList, name="my_chat"),
    path('create-chatroom/<str:post_id>/', views.CreateChatRoom, name="create_room"),
    path('post-sort/', views.PostSortListView.as_view(), name='post-sort'),
    path('chat-list/<str:post_id>/',views.ChatListView.as_view(), name="chat_list"),
    path('chat-detail/<str:chatroom_id>/',views.ChatDetailView.as_view(), name="chat_detail"),
    path('phone-verify/', views.verify, name='verify'),
    path('code-input/', views.code, name='code'),
]


