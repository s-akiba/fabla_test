from multiprocessing import context
import profile
from tabnanny import check
from unicodedata import category
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .forms import AppFablaCreateForm,ReportForm

from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
from accounts.forms import SignupForm
from .models import *

from accounts.forms import SignupForm
from accounts.models import CustomUser
from django.utils import timezone

from django.template.loader import render_to_string
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
import logging
from dateutil.relativedelta import relativedelta
import datetime
from django.db.models.aggregates import Count

logging.basicConfig()
logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class AppFablaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'fabla_create.html'
    form_class = AppFablaCreateForm
    success_url = reverse_lazy('app_fabla:index')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_id = self.request.user
        post.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)


class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
        return super().get_queryset()

# 画面詳細


class PostDetail(LoginRequiredMixin, generic.DetailView):
    template_name = "post_detail.html"
    model = Post

class CongressmanListView(generic.ListView):
    template_name = "congressman_list.html"
    model = CustomUser
    def get_queryset(self):
        query_set = CustomUser.objects.filter(assembly=True)
        return query_set


class profileDetail(generic.DetailView):
    template_name='profile.html'
    model = CustomUser

class profileEdit(generic.UpdateView):
    template_name='profile_edit.html'
    model = CustomUser
    fields = ('user_name', 'icon_photo', 'bio',)
    success_url = reverse_lazy('app_fabla:post_list')

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.updated_at = timezone.now()
        profile.save()
        return super().form_valid(form)

class AdListView(generic.ListView):
    template_name = "admin_list.html"
    model = CustomUser
    def get_queryset(self):
        query_set = CustomUser.objects.get(is_staff = self.request.user.is_staff)
        print(query_set)
        return query_set

def LikeView(request):
    print("LikeView実行されました")
    if request.method =="POST":
        ao = request.POST.get('article_id')
        print("ここから",ao,"ここまで")
        # articleにidを格納する
        post = get_object_or_404(Post, pk=request.POST.get('article_id'))
        # userにuser_idを格納する
        user = request.user
        liked = False
        # Goodモデルにpost_idかつuser_idがあればlikeに格納する
        like = Good.objects.filter(post_id=post, user_id=user)
        if like.exists():
            like.delete()
        else:
            like.create(post_id=post, user_id=user)
            liked = True
        context={
            'article_id': post.post_id,
            'liked': liked,
            'count': post.good_set.count(),
        }
    if request.is_ajax():
        return JsonResponse(context)

# 画面詳細
class PostDetail(generic.DetailView):
    template_name = "post_detail.html"
    model = Post

    def get_context_data(self, *args, **kwargs):
        # 以下既読の流れ========================================================================================================================
        context = super().get_context_data(*args, **kwargs)
        p_id = Post.objects.get(post_id=self.kwargs['pk'])
        po_check = p_id.checked_set.filter(post_id=p_id)
        checked_list = []
        try:
            for i in po_check:
                checked_user = CustomUser.objects.get(user_id = i.user_id)
                checked_list.append(checked_user)
        except:
            print('エラーだよ')
        u_id = CustomUser.objects.get(user_id=self.request.user.user_id)
        user = self.request.user
        one = p_id.checked_set.filter(post_id=p_id,user_id=user)
        ad = {
            'checked_list': checked_list,
        }
        context.update(ad)
        print("contextの中身",context)
        if user.assembly == True:
           context['check'] = Checked.objects.update_or_create(post_id = p_id,user_id = u_id)
        # 以上既読の流れ========================================================================================================================
        # 以下いいねの流れ========================================================================================================================
        post = Post.objects.get(post_id=self.kwargs['pk'])
        # liked_listというものを用意し、閲覧しているユーザー（request.userで取得）が過去にどの記事をいいねしたかを格納しておく。
        liked_list = []
        # good_setでarticleに紐づく全てのいいねを取得し、閲覧しているユーザーでフィルターをかけている。
        liked = post.good_set.filter(user_id=self.request.user)
        if liked.exists():
            liked_list.append(post.post_id)
            print(post.post_id)

        ad_nice = {
            'post': post,
            'liked_list': liked_list,
        }
        context.update(ad_nice)
        print(context,"これが中身や")
        # 以上いいねの流れ========================================================================================================================
        # 以下コメントリスト返す流れ========================================================================================================================
        p_id_comment = Post.objects.get(post_id=self.kwargs['pk'])
        context['comment_list'] = Comment.objects.filter(post_id = p_id_comment,).order_by('-created_at')
        # 以上コメントリスト返す流れ========================================================================================================================
        return(context)

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     p_id = Post.objects.get(post_id=self.kwargs['pk'])
    #     context['comment_list'] = Comment.objects.filter(post_id = p_id,)
    #     return context

# コメントの処理
def CommentView(request):
    if request.method =="POST":
        comment = request.POST.get('comment')
        user_id=request.user
        post = get_object_or_404(Post, pk=request.POST.get('post_id'))
        comment2 = Comment.objects.create(post_id=post,user_id=user_id,content=comment)
        d = {
            'comment': comment2.content,
            'user_id': str(comment2.user_id),
            'user_name': str(comment2.user_id.user_name),
            'icon_url':comment2.user_id.icon_photo.url,
        }
        return JsonResponse(d)

class ReportFormView(generic.FormView):
    model = PostReport
    template_name = "post_report.html"
    form_class = ReportForm
    def get_success_url(self):
        return reverse_lazy('app_fabla:post_detail',kwargs={'pk':self.kwargs['pk']})
    

    def form_valid(self,form):
        postreport = form.save(commit=False)
        postreport.post_id = Post.objects.get(post_id=self.kwargs['pk'])
        postreport.user_id = self.request.user
        postreport.save()
        messages.success(self.request,'通報完了')
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,'通報の送信に失敗しました')
        return super().form_invalid(form)


# good-history/
# profile -> good-history
class Goodhistory(LoginRequiredMixin, generic.ListView):
    template_name = "goodhistory.html"
    model = Post
    def get_context_data(self):
        user = self.request.user
        good_id = Good.objects.filter(user_id=user)
        good_list = []
        for i in good_id:
            good_list.append(i.post_id)
            print(good_list)
        
        context = {
            'good_list':good_list
        }
        return(context)

class Signup(generic.CreateView):
   template_name = 'user_form.html'
   form_class = SignupForm
   def form_valid(self, form):
       user = form.save() # formの情報を保存
       return redirect('app_fabla:sign_up_done')
    # データ送信
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context["process_name"] = "Sign up"
       return context

class SignupDone(generic.TemplateView):
    template_name = 'sign_up_done.html'
    def get_success_url(self):
        return reverse_lazy('accounts:login')


# chat-list/
# post-detail -> chat-list
class ChatListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'room_list'
    model = Chat
    template_name = 'chat_list.html'
    slug_url_kwarg= 'post_id'
    slug_field = 'post_id'
    

    def get_queryset(self):
        print(self.kwargs['post_id'])
        queryset = Chat.objects.filter(post_id=self.kwargs['post_id']).order_by('-created_at')
        return queryset


# chat-detail/
# chat-list -> chat-detail
class ChatDetailView(LoginRequiredMixin, View):
    slug_url_kwarg= 'chatroom_id'
    slug_field = 'chatroom_id'

    def get(self, request, *args, **kwargs):

        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if is_ajax:
            chat_contents   = ChatDetail.objects.filter(chatroom_id=self.kwargs['chatroom_id']).order_by('created_at')
            json    = { "error":False }
            context = { "chat_detail":chat_contents }
            content = render_to_string("chat_detail_content.html",context,request)
            json["content"] = content
            print('ajax_resp:', json['content'])
            return JsonResponse(json)
        else:
            chat_contents  = ChatDetail.objects.filter(chatroom_id=self.kwargs['chatroom_id']).order_by('created_at')
            chat_room = Chat.objects.get(chatroom_id=self.kwargs['chatroom_id'])
            context = { "chat_detail":chat_contents,
                        "user1_id":chat_room.user1_id.user_id,
                        "user2_id":chat_room.user2_id.user_id }
            print(context)
            return render(request,"chat_detail.html",context)

    def post(self, request, *args, **kwargs):
        print('room_id:{} user:{}'.format(self.kwargs['chatroom_id'], self.request.user))

        print(request.POST)

        json    = { "error":True }
        new_chat = ChatDetail(chatroom_id= Chat.objects.get(chatroom_id=self.kwargs['chatroom_id']), user_id=CustomUser.objects.get(user_id=self.request.user), content=request.POST.get('comment'))
        new_chat.save()
        if new_chat.chat_id is not None:
            json["error"]   = False

        chat_contents   = ChatDetail.objects.filter(chatroom_id=self.kwargs['chatroom_id']).order_by('created_at')
        context         = { "chat_detail":chat_contents }
        content         = render_to_string("chat_detail_content.html",context,request)

        json["content"] = content
        return JsonResponse(json)


# my-chat-list/
# profile -> my-chat-list
@login_required
def MyChatList(request, name):

    object_list = Chat.objects.filter(Q(user1_id=name) | Q(user2_id=name)).order_by('created_at')
    context = {'room_list': object_list}
    return render(request, 'chat_list.html', context)

# create-chatroom/
# post-detail -> create-chatroom
@login_required
def CreateChatRoom(request, post_id):
    if Chat.objects.filter(post_id=post_id, user1_id=request.user) or Chat.objects.filter(post_id=post_id, user2_id=request.user):
        messages.warning(request, '既にこの投稿に対するチャットがあります！')
        url = '/post-detail/'+post_id+'/'
        return redirect(to=url)
    else:
        target_post = Post.objects.get(post_id=post_id)
        new_chatroom = Chat(post_id=Post.objects.get(post_id=post_id), user1_id=request.user, user2_id=target_post.user_id)
        new_chatroom.save()
        if new_chatroom.chatroom_id is not None:
            url = '/chat-detail/'+ str(new_chatroom.chatroom_id) + '/'
            return redirect(to=url)
        else:
            messages.warning(request, '何らかの理由でチャットが作成出来ませんでした。')
            url = '/post-detail/'+post_id+'/'
            return redirect(to=url)



# post-sort/
class PostSortListView(LoginRequiredMixin, generic.ListView):
    context_objct_name = 'post_list'
    template_name = 'post_list.html'
    model = Post
    search_by = ''
    odr_by = ''
    def get_queryset(self):
        logger.info('1 byage:{} category:{} order:{}'.format(self.request.GET.get('byage'),self.request.GET.get('category'),self.request.GET.get('order')))
        if ('byage' not in self.request.GET) and ('category' not in self.request.GET) and ('order' not in self.request.GET):
            return redirect('../')
        
        elif 'byage' in self.request.GET:
            byage = self.request.GET.get('byage')
            odrby = self.request.GET.get('order')
            if odrby == 'new':
                PostSortListView.odr_by = '新規投稿'
            elif odrby == 'good':
                PostSortListView.odr_by = 'いいね数'
            else:
                return redirect('../')
            logger.info('2 byage:{} odrby:{}'.format(byage,odrby))
            nowdate = datetime.date.today()
            ago20 = nowdate - relativedelta(years=20)
            ago30 = nowdate - relativedelta(years=30)
            ago40 = nowdate - relativedelta(years=40)
            ago50 = nowdate - relativedelta(years=50)
            ago60 = nowdate - relativedelta(years=60)

            if byage == 'lt20':
                # 20未満
                lst = [usr.user_id for usr in CustomUser.objects.filter(birth__gt=ago20)]
                if odrby == 'new':
                    queryset = Post.objects.filter(user_id__in=lst).order_by('-created_at')
                else:
                    queryset = Post.objects.filter(user_id__in=lst).annotate(Count('good')).order_by('-good__count')
                    
                PostSortListView.search_by = '20才未満'
                return queryset
            elif byage == '20':
                # 20代
                lst = [usr.user_id for usr in CustomUser.objects.filter(birth__gt=ago30, birth__lte=ago20)]
                if odrby == 'new':
                    queryset = Post.objects.filter(user_id__in=lst).order_by('-created_at')
                else:
                    queryset = Post.objects.filter(user_id__in=lst).annotate(Count('good')).order_by('-good__count')
                PostSortListView.search_by = '{}代'.format(byage)
                return queryset
            elif byage == '30':
                # 30代
                lst = [usr.user_id for usr in CustomUser.objects.filter(birth__gt=ago40, birth__lte=ago30)]
                if odrby == 'new':
                    queryset = Post.objects.filter(user_id__in=lst).order_by('-created_at')
                else:
                    queryset = Post.objects.filter(user_id__in=lst).annotate(Count('good')).order_by('-good__count')
                PostSortListView.search_by = '{}代'.format(byage)
                return queryset
            elif byage == '40':
                # 40代
                lst = [usr.user_id for usr in CustomUser.objects.filter(birth__gt=ago50, birth__lte=ago40)]
                if odrby == 'new':
                    queryset = Post.objects.filter(user_id__in=lst).order_by('-created_at')
                else:
                    queryset = Post.objects.filter(user_id__in=lst).annotate(Count('good')).order_by('-good__count')
                PostSortListView.search_by = '{}代'.format(byage)
                return queryset
            elif byage == '50':
                # 50代
                lst = [usr.user_id for usr in CustomUser.objects.filter(birth__gt=ago60, birth__lte=ago50)]
                if odrby == 'new':
                    queryset = Post.objects.filter(user_id__in=lst).order_by('-created_at')
                else:
                    queryset = Post.objects.filter(user_id__in=lst).annotate(Count('good')).order_by('-good__count')
                PostSortListView.search_by = '{}代'.format(byage)
                return queryset
            elif byage == 'ov60':
                # 60代
                lst = [usr.user_id for usr in CustomUser.objects.filter(birth__lte=ago60)]
                if odrby == 'new':
                    queryset = Post.objects.filter(user_id__in=lst).order_by('-created_at')
                else:
                    queryset = Post.objects.filter(user_id__in=lst).annotate(Count('good')).order_by('-good__count')
                PostSortListView.search_by = '60才以上'
                return queryset
            elif byage == "all":
                queryset = Post.objects.annotate(Count('good')).order_by('-good__count')
                PostSortListView.search_by = '全て'
                return queryset
            else:
                return redirect('../')

        elif 'category' in self.request.GET:
            cate = self.request.GET.get('category')
            odrby = self.request.GET.get('order')
            if odrby == 'new':
                PostSortListView.odr_by = '新規投稿'
            elif odrby == 'good':
                PostSortListView.odr_by = 'いいね数'
            else:
                return redirect('../')
            logger.info('4 category:{} odrby:{}'.format(cate,odrby))
            try:
                cate_no = int(cate)
            except Exception :
                return redirect('../')
            
            max_no = Category.objects.all().count()
            if 1 <= cate_no and cate_no <= max_no:
                if odrby == 'new':
                    queryset = Post.objects.filter(category_no=cate_no).order_by('-created_at')
                else:
                    queryset = Post.objects.filter(category_no=cate_no).annotate(Count('good')).order_by('-good__count')
                
                cate_name = Category.objects.filter(id=cate_no).first()
                PostSortListView.search_by = 'カテゴリー : {}'.format(cate_name.name)
                return queryset
            else:
                return redirect('../')

        elif 'history' in self.request.GET:
            odrby = self.request.GET.get('order')
            if odrby == 'new':
                PostSortListView.odr_by = '新規投稿'
            elif odrby == 'good':
                PostSortListView.odr_by = 'いいね数'
            else:
                return redirect('../')
            logger.info('7 history odrby:{}'.format(odrby))
            his = CustomUser.objects.filter(user_id=self.request.user.user_id)
            if odrby == 'new':
                queryset = Post.objects.filter(user_id__in=his).order_by('-created_at')
            else:
                queryset = Post.objects.filter(user_id__in=his).annotate(Count('good')).order_by('-good__count')
            PostSortListView.search_by = '投稿履歴'
            return queryset
        
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostSortListView, self).get_context_data(*args, **kwargs)
        context['search_by'] = PostSortListView.search_by
        context['order_by'] = PostSortListView.odr_by
        context['category_list'] = Category.objects.all()
        logger.info('5 searchby:{}'.format(PostSortListView.search_by))
        logger.info('6 odrby:{}'.format(PostSortListView.odr_by))
        return context
