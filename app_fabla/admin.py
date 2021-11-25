from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','user_id', 'created_at')
    ordering = ('-created_at',)
    search_fields = ['title', 'content', 'user_id']
    date_hierarchy = 'created_at'
    list_filter = ('category_no',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'content')
    list_display_links = ('post_id',)
    search_fields = ['user_id', 'content']
    ordering = ('-created_at',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class GoodAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user_id')
    list_display_links = ('post_id', 'user_id')
    ordering = ('-created_at',)


class ChatAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user1_id', 'user2_id')
    list_display_links = ('post_id', 'user1_id', 'user2_id')
    ordering = ('-created_at',)


class ChatDetailAdmin(admin.ModelAdmin):
    list_display = ('chatroom_id', 'user_id', 'content')
    list_display_links = ('chatroom_id', 'user_id')
    search_fields = ['chatroom_id', 'user_id', 'content']
    ordering = ('-created_at',)


class PostReportAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user_id', 'report_reason')
    list_display_links = ('post_id', 'user_id')
    search_fields = ['post_id', 'user_id']
    ordering = ('-created_at',)


class ChatReportAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user_id', 'report_reason')
    list_display_links = ('chat_id', 'user_id')
    search_fields = ['chat_id', 'user_id']
    ordering = ('-created_at',)


class CommentReportAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'user_id', 'report_reason')
    list_display_links = ('comment_id', 'user_id')
    search_fields = ['comment_id', 'user_id']
    ordering = ('-created_at',)


class CheckedAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user_id')
    list_display_links = ('post_id', 'user_id')
    ordering = ('-created_at',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatDetail, ChatDetailAdmin)
admin.site.register(PostReport, PostReportAdmin)
admin.site.register(ChatReport, ChatReportAdmin)
admin.site.register(CommentReport, CommentReportAdmin)
admin.site.register(Checked, CheckedAdmin)