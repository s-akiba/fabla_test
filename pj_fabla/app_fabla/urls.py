from django.urls import path
from . import views

app_name = 'app_fabla'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
]