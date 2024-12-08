from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
    chat_id = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    
    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.chat_id} - {self.username}'