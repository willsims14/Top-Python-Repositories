from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from . import views

app_name = 'github_repos'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.redirect, name='index'),
    path('repos/', views.index, name='index'),
    path('repos/<int:repo_id>/', views.detail, name='detail'),
]
