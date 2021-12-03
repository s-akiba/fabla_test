
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AppFablaCreateForm
from .models import Post


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

# 画面詳細
class PostDetail(generic.DetailView):
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