from django.contrib.auth.models import User
from django.db import models
import uuid

from accounts.models import CustomUser

# Create your models here.


class Post(models.Model):
    """投稿テーブル"""
    post_id = models.UUIDField(verbose_name='投稿ID', primary_key=True, default=uuid.uuid4, editable=False)

    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.CASCADE)
    category_no = models.ForeignKey('Category', verbose_name='カテゴリ番号', on_delete=models.SET_NULL, null=True)
    title = models.CharField(verbose_name='タイトル', max_length=30)
    content = models.TextField(verbose_name='内容', blank=False)
    photo = models.ImageField(verbose_name='写真')
    hide_reason = models.TextField(verbose_name='伏字化理由', blank=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = '投稿テーブル'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """コメントテーブル"""
    comment_id = models.UUIDField(verbose_name='コメントID', primary_key=True, default=uuid.uuid4, editable=False)

    post_id = models.ForeignKey('Post', verbose_name='投稿ID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='コメント内容', blank=False)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'コメントテーブル'

    def __str__(self):
        return self.comment_id


class Category(models.Model):
    """カテゴリテーブル"""
    name = models.CharField(verbose_name='カテゴリ名', max_length=20, blank=False)

    class Meta:
        verbose_name_plural = 'カテゴリテーブル'

    def __str__(self):
        return self.name


class Good(models.Model):
    """イイネテーブル"""
    post_id = models.ForeignKey('Post', verbose_name='投稿ID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'イイネテーブル'


class Chat(models.Model):
    """チャット(部屋)テーブル"""
    chatroom_id = models.UUIDField(verbose_name='チャットルームID', primary_key=True, default=uuid.uuid4, editable=False)

    post_id = models.ForeignKey('Post', verbose_name='投稿ID', on_delete=models.CASCADE)
    user1_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID_議員', on_delete=models.SET_NULL, null=True, related_name='assembly_user')
    user2_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID_一般', on_delete=models.SET_NULL, null=True, related_name='normal_user')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'チャット(部屋)テーブル'

    def __str__(self):
        return self.post_id


class ChatDetail(models.Model):
    """チャット(詳細)テーブル"""
    chat_id = models.UUIDField(verbose_name='チャット詳細ID', primary_key=True, default=uuid.uuid4, editable=False)

    chatroom_id = models.ForeignKey('Chat', verbose_name='チャットルームID', on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name='投稿内容', blank=False)
    created_at = models.DateTimeField(verbose_name='投稿日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'チャット(詳細)テーブル'

    def __str__(self):
        return self.chatroom_id


class PostReport(models.Model):
    """投稿通報テーブル"""
    post_id = models.ForeignKey('Post', verbose_name='投稿ID', on_delete=models.PROTECT)
    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.PROTECT)
    report_reason = models.TextField(verbose_name='通報理由', blank=False)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = '投稿通報テーブル'

    def __str__(self):
        return self.post_id


class ChatReport(models.Model):
    """チャット通報テーブル"""
    chat_id = models.ForeignKey('ChatDetail', verbose_name='チャット詳細ID', on_delete=models.PROTECT)
    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.PROTECT)
    report_reason = models.TextField(verbose_name='通報理由', blank=False)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'チャット通報テーブル'

    def __str__(self):
        return self.chat_id



class CommentReport(models.Model):
    """コメント通報テーブル"""
    comment_id = models.ForeignKey('Comment', verbose_name='コメントID', on_delete=models.PROTECT)
    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.PROTECT)
    report_reason = models.TextField(verbose_name='通報理由', blank=False)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'コメント通報テーブル'

    def __str__(self):
        return self.comment_id


class Checked(models.Model):
    """既読テーブル"""
    post_id = models.ForeignKey('Post', verbose_name='投稿ID', on_delete=models.PROTECT)
    user_id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    class Meta:
        verbose_name_plural = '既読テーブル'
