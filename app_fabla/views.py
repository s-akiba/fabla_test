
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .forms import AppFablaCreateForm,ReportForm
from .models import Post

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import *

from accounts.models import CustomUser

class IndexView(generic.TemplateView):
    template_name = "index.html"

class AppFablaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'fabla_create.html'
    form_class = AppFablaCreateForm
    success_url = reverse_lazy('app_fabla:index')

    def form_valid(self, form):
        appfabla = form.save(commit=False)
        appfabla.user = self.request.user
        appfabla.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)

# Create your views here.

class PostListView(generic.ListView):
    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
        return super().get_queryset()

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # ポストモデル
        p_id = Post.objects.get(post_id=self.kwargs['pk'])
        u_id = CustomUser.objects.get(user_id=self.request.user.user_id)
        ic_photo = u_id
        print(ic_photo,"これか")
        user = self.request.user
        print(user)
        if user.assembly == True:
            context['check'] = Checked.objects.update_or_create(post_id = p_id,user_id = u_id)
        return(context)

    def get_context_data(self, **kwargs):
        print("ArticlesView実行されました")
        post = Post.objects.get(post_id=self.kwargs['pk'])
        # liked_listというものを用意し、閲覧しているユーザー（request.userで取得）が過去にどの記事をいいねしたかを格納しておく。
        liked_list = []
        # good_setでarticleに紐づく全てのいいねを取得し、閲覧しているユーザーでフィルターをかけている。
        liked = post.good_set.filter(user_id=self.request.user)
        if liked.exists():
            liked_list.append(post.post_id)
            print(post.post_id)

        context = {
            'post': post,
            'liked_list': liked_list,
        }
        return(context)

class ReportFormView(generic.FormView):
    model = PostReport
    template_name = "post_report.html"
    form_class = ReportForm
    def get_success_url(self):
        return reverse_lazy('app_fabla:post_detail',kwargs={'pk':self.kwargs['pk']})

    def form_valid(self,form):
        postreport = form.save(commit=False)
        postreport.post_id = Post.objects.get(post_id=self.kwargs['pk'])
        print("==============おめでとう================",postreport,"=============================")
        postreport.user_id = self.request.user
        print("==============やったね================",postreport,"=============================")
        postreport.save()
        messages.success(self.request,'通報完了')
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,'通報の送信に失敗しました')
        return super().form_invalid(form)

# コメントの処理
def CommentView(request):
    print("＝＝＝＝＝＝f＝＝＝comment＝＝＝＝a＝a＝＝＝coment＝＝＝")
    return HttpResponse('')