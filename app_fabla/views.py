from django.views import generic

from .models import *

from accounts.models import CustomUser

class IndexView(generic.TemplateView):
    template_name = "index.html"

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