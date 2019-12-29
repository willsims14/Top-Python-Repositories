from django.db import models
from django.utils import timezone
import datetime


class Repository(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created_on = models.DateTimeField('date repo was created')
    last_push_on = models.DateTimeField('date of last git push')
    description = models.CharField(max_length=1000, null=True)
    star_count = models.IntegerField(default=0)
    data_retrieved_on = models.DateTimeField('date of last update')

    def was_updated_recently(self):
        now = timezone.now()  # To prevent dates from the future
        return now - datetime.timedelta(days=1) <= self.data_retrieved_on <= now

