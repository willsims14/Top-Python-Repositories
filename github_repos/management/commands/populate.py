from django.core.management.base import BaseCommand
from django.utils import timezone
import requests

from github_repos.models import Repository, GithubUser


class Command(BaseCommand):
    help = 'Updates data in database using Github API'

    api_root = "https://api.github.com"
    header = {'Accept':'application/vnd.github.v3+json'}
    query_string = '?q=language:python&sort=stars&order=desc'
    endpoint_url = api_root + '/search/repositories' + query_string

    def handle(self, *args, **options):
        r = requests.get(self.endpoint_url, headers=self.header)
        data = r.json()['items']
        for i, repo_object in enumerate(data):

            # Create GithubUser in Database if it doesn't exist
            user, created = GithubUser.objects.get_or_create(
                user_id=repo_object['owner']['id'],
                defaults={
                    'username': repo_object['owner']['login'],
                    'avatar_url':repo_object['owner']['avatar_url'],
                    'profile_url':repo_object['owner']['url'],
                }
            )
            user.save()
            db_operation = '[INSERT]' if created else '[UPDATE]'
            print('{} Github User: {}'.format(db_operation, user.username))

            # Create Repository in database if it doesn't exist
            repo, created = Repository.objects.get_or_create(
                url=repo_object['html_url'],
                defaults={
                    'name': repo_object['name'],
                    'author': user,
                    'created_on':repo_object['created_at'],
                    'last_push_on':repo_object['pushed_at'],
                    'description': repo_object['description'],
                    'star_count':repo_object['stargazers_count'],
                    'data_retrieved_on': timezone.now()
                }
            )
            repo.save()
            db_operation = '[INSERT]' if created else '[UPDATE]'
            print('{} {} has {:>4} stargazers.'.format(db_operation,
                                                       repo.name,
                                                       repo.star_count))





