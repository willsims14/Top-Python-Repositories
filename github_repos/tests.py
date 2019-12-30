import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime

from .models import Repository


class RepositoryModelTests(TestCase):

    def test_was_updated_recently_with_future_repository(self):
        """
        was_updated_recently() returns False for repositories whose 
        data_retrieved_on date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_repo = Repository(data_retrieved_on=time)
        self.assertIs(future_repo.was_updated_recently(), False)

    def test_was_updated_recently_with_old_repository(self):
        """
        was_updated_recently() returns False for repositories whose
        data_retrieved_on date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        out_of_date_repo = Repository(data_retrieved_on=time)
        self.assertIs(out_of_date_repo.was_updated_recently(), False)

    def test_was_updated_recently_with_recent_repository(self):
        """
        was_updated_recently() returns True for repositories whose
        data_retrieved_on date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recently_updated_repo = Repository(data_retrieved_on=time)
        self.assertIs(recently_updated_repo.was_updated_recently(), True)



def create_repository(name, days):
    """
    Create a repository with the given `name` and
    `data_retrieved_on` values
    """
    time = timezone.now() + datetime.timedelta(days=days)
    yesterday = timezone.now() - datetime.timedelta(days=1)
    return Repository.objects.create(
        name=name, 
        url='https://{}'.format(name),
        created_on=timezone.now(),
        last_push_on=yesterday,
        description='testing',
        star_count=1,
        data_retrieved_on=time
    )


class RepositoryIndexViewTests(TestCase):
    def test_no_repositories(self):
        """
        If no repository exists, an appropriate message is displayed.
        """
        response = self.client.get(reverse('github_repos:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No repositories are available.")
        self.assertQuerysetEqual(response.context['trending_repos'], [])

    def test_past_repository(self):
        """
        Repositories with a data_retrieved_on date in the past are 
        displayed on the index page.
        """
        create_repository(name="Past repo", days=-30)
        response = self.client.get(reverse('github_repos:index'))
        self.assertQuerysetEqual(
            response.context['trending_repos'],
            ['<Repository: Repository object (1)>']
        )

    def test_future_repository(self):
        """
        Repositories with a data_retrieved_on date in the future 
        aren't displayed on the index page.
        """
        create_repository(name="Future repo.", days=30)
        response = self.client.get(reverse('github_repos:index'))
        self.assertContains(response, "No repositories are available.")
        self.assertQuerysetEqual(response.context['trending_repos'], [])

    def test_future_repository_and_past_repository(self):
        """
        Even if both past and future repositories exist, only past
        repositories are displayed.
        """
        create_repository(name="Past repo.", days=-30)
        create_repository(name="Future repo.", days=30)
        response = self.client.get(reverse('github_repos:index'))
        self.assertQuerysetEqual(
            response.context['trending_repos'],
            ['<Repository: Repository object (1)>']
        )

    def test_two_past_repositories(self):
        """
        The repositories index page may display multiple repositories.
        """
        create_repository(name="Past repo 1.", days=-30)
        create_repository(name="Past repo 2.", days=-5)
        response = self.client.get(reverse('github_repos:index'))
        self.assertQuerysetEqual(
            response.context['trending_repos'],
            ['<Repository: Repository object (1)>', '<Repository: Repository object (2)>']
        )