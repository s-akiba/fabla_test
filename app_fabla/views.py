import profile
from tabnanny import check
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .forms import AppFablaCreateForm,ReportForm
from .models import Post

from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers

from .forms import SignUpForm
from .forms import AppFablaCreateForm

from .models import *

from accounts.models import CustomUser
from django.utils import timezone

from django.utils import timezone

class IndexView(generic.TemplateView):
    template_name = "index.html"


class AppFablaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'fabla_create.html'
    form_class = AppFablaCreateForm
    success_url = reverse_lazy('app_fabla:index')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)

# Create your views here.


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
        query_set = CustomUser.objects.all().filter(assembly=True)
        return query_set

class CongListView(generic.ListView):
    template_name='cong_list.html'
    model = CustomUser
    def get_queryset(self):
        query_set = CustomUser.objects.all().filter(assembly=True)
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
        context['comment_list'] = Comment.objects.filter(post_id = p_id_comment,)
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
            'user_name': str(comment2.user_id),
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

class HisPosListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'post_list.html'
    def get_queryset(self):
        user = self.request.user
        hispost = Post.objects.filter(user_id=user)
        print(hispost)
        return hispost

<<<<<<< HEAD
class Signup(generic.CreateView):
    template_name = 'user_form.html'
    form_class = SignUpForm

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
=======
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
>>>>>>> 560b6e4477cadc2b6a53ea5eae9587f0f69d94ae
