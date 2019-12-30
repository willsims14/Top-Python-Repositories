from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from .models import Repository


def index(request):
    template_name = 'github_repos/index.html'
    trending_repos = Repository.objects.filter(
            data_retrieved_on__lte=timezone.now()
        ).order_by('-star_count')[:5]
    return render(request, template_name, {'trending_repos': trending_repos})


def detail(request, repo_id):
    template_name = 'github_repos/detail.html'
    try:
        repo = Repository.objects.get(pk=repo_id)
    except Repository.DoesNotExist:
        return render(request, template_name, {'repository': None})
    return render(request, template_name, {'repository': repo})


def redirect(request):
    return HttpResponseRedirect("/repos/")