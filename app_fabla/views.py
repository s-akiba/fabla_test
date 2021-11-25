from django.views import generic

from .models import *

class IndexView(generic.TemplateView):
    template_name = "index.html"

# Create your views here.

class PostListView(generic.ListView):
    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
        return super().get_queryset()