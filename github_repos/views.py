from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.core import management
from .models import Repository


class IndexView(generic.ListView):
    template_name = 'github_repos/index.html'
    context_object_name = 'trending_repos'

    def get_queryset(self):
        """
        Return repositories that have been recently updated in
        descending order by star count
        """ 
        all_repos = Repository.objects.all()
        return all_repos.filter(
            data_retrieved_on__lte=timezone.now()
        ).order_by('-star_count')[:5]


class DetailView(generic.DetailView):

    def repo_detail(request, repo_id):
        template_name = 'github_repos/detail.html'
        repo = Repository.objects.get(pk=repo_id)
        return render(request, template_name, {'repository': repo})
