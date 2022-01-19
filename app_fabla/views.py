from tabnanny import check
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .forms import AppFablaCreateForm,ReportForm
from .models import Post

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db.models import Q

from .forms import AppFablaCreateForm

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
    # def get_context_data(self, **kwargs):
    #     print("ArticlesView実行されました")
    #     post = Post.objects.get(post_id=self.kwargs['pk'])
    #     # liked_listというものを用意し、閲覧しているユーザー（request.userで取得）が過去にどの記事をいいねしたかを格納しておく。
    #     liked_list = []
    #     # good_setでarticleに紐づく全てのいいねを取得し、閲覧しているユーザーでフィルターをかけている。
    #     liked = post.good_set.filter(user_id=self.request.user)
    #     if liked.exists():
    #         liked_list.append(post.post_id)
    #         print(post.post_id)

    #     context = {
    #         'post': post,
    #         'liked_list': liked_list,
    #     }
    #     return(context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     # ポストモデル
    #     p_id = Post.objects.get(post_id=self.kwargs['pk'])
    #     print("ddddddddddddddddd",p_id,"dddddddddddddddddddd")

    #     po_check = p_id.checked_set.filter(post_id=p_id)
        
    #     print("関係してるデータベースは",po_check[0].user_id)
    #     photo = CustomUser.objects.get(user_id = po_check[2].user_id)
    #     print("関係のやつ２",photo.icon_photo)

    #     checked_list = []

    #     for i in po_check:
    #         print()
            

    #     u_id = CustomUser.objects.get(user_id=self.request.user.user_id)
    #     user = self.request.user

        # one = p_id.checked_set.filter(post_id=p_id,user_id=user)
        # print("aaaaaaaaaaaaaaaaaaaa",one,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # print(user)
        # if user.assembly == True:
        #    context['check'] = Checked.objects.update_or_create(post_id = p_id,user_id = u_id)
        # return(context)

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
        print("==============22222=============",post,"==================================")
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
        print("==============おめでとう================",postreport,"=============================")
        postreport.user_id = self.request.user
        print("==============やったね=======i=========",postreport,"=============================")
        postreport.save()
        messages.success(self.request,'通報完了')
        return super().form_valid(form)
    
    


    def form_invalid(self,form):
        messages.error(self.request,'通報の送信に失敗しました')
        return super().form_invalid(form)