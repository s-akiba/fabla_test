from unicodedata import name
from django.urls import path
from . import views

app_name = 'app_fabla'
urlpatterns = [
    # Topページ
    path('', views.IndexView.as_view(), name="index"),
    # 投稿一覧
    path('post-list/',views.PostListView.as_view(), name="post_list"),
    # 画面詳細へ
    path('post-detail/<str:pk>/',views.PostDetail.as_view(), name="post_detail"),
    # 議員一覧
    path('congressman/',views.CongressmanListView.as_view(), name="congressman"),
    # プロフィール
    path('profile/<str:pk>/',views.profileDetail.as_view(), name="profile"),
    # プロフィール編集
    path('profile-ed/<str:pk>/',views.profileEdit.as_view(), name="profile_edit"),
    # 新規投稿作成
    path('fabla-create/',views.AppFablaCreateView.as_view(), name="fabla_create"),
    # ？
    path('ad/',views.AdListView.as_view(), name="ad"),
    # 投稿通報
    path('post-report/<str:pk>/',views.ReportFormView.as_view(),name="post_report"),
    # いいね
    path('like', views.LikeView, name='like'),
    # コメント
    path('comment',views.CommentView,name="comment"),
    # いいね履歴
    path('good-history/',views.Goodhistory.as_view(),name='good_history'),
    # チャット参加履歴
    path('my-chat-list/<str:name>/', views.MyChatList, name="my_chat"),
    # チャットルーム作成
    path('create-chatroom/<str:post_id>/', views.CreateChatRoom, name="create_room"),
    # 条件別投稿ソート
    path('post-sort/', views.PostSortListView.as_view(), name='post-sort'),
    # 投稿に対するチャットルーム一覧
    path('chat-list/<str:post_id>/',views.ChatListView.as_view(), name="chat_list"),
    # チャット詳細
    path('chat-detail/<str:chatroom_id>/',views.ChatDetailView.as_view(), name="chat_detail"),
    # 電話番号入力
    path('phone-verify/', views.verify, name='verify'),
    # 電話番号認証 コード入力
    path('code-input/', views.code, name='code'),
]


