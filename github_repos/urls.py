from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from . import views

app_name = 'github_repos'
urlpatterns = [
    path('', views.index, name='index'),
    # path('repos/', views.repo_list, name='repo_list'),
    path('repos/', views.RepositoryList.as_view()),
    path('author/<author>/repos/', views.AuthorRepositoryList.as_view()),
    path('repos/<int:repo_id>/', views.detail, name='detail'),
]
