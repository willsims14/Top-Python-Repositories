from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Repository, GithubUser


# def repo_list(request, start_index=None):
#     """ Repository list view """
#
#     template_name = 'github_repos/index.html'
#     trending_repos = Repository.objects.all()
#
#     if not start_index:
#         print('USING DEFAULT')
#         start_index = 5
#     else:
#         print('IN REQUEST')
#
#     paginator = Paginator(trending_repos, start_index)  # Show 25 contacts per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, template_name, {'page_obj': page_obj, 'next_start_index': start_index+5})


def detail(request, repo_id):
    template_name = 'github_repos/detail.html'
    try:
        repo = Repository.objects.get(pk=repo_id)
    except Repository.DoesNotExist:
        return render(request, template_name, {'repository': None})
    return render(request, template_name, {'repository': repo})


def index(request):
    # return HttpResponseRedirect("/repos/")
    template_name = 'index.html'
    context = {}
    return render(request, template_name, context)


class RepositoryList(ListView):
    model = Repository
    template_name = 'github_repos/index.html'
    context_object_name = 'repositories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repositories'] = Repository.objects.all()[:5]
        context['header'] = 'Popular Python Repositories'
        return context


class AuthorRepositoryList(ListView):
    template_name = 'github_repos/index.html'
    context_object_name = 'repositories'

    def get_queryset(self):
        self.author = get_object_or_404(GithubUser, id=self.kwargs['author'])
        return Repository.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.author = get_object_or_404(GithubUser, id=self.kwargs['author'])
        context['repositories'] = Repository.objects.filter(author=self.author)
        context['header'] = "{}'s Repositories".format(self.author.username)
        return context