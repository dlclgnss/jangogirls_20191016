from django.db import models
from django.utils import timezone
from django.conf import settings

#from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_data = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    #발행전이랑 발행후를 구별해주기위한 함수 기본은 발행하지 않은상태
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def summary(self):
        return self.text[:100]
