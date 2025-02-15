from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField()
    status = models.BooleanField()
    prioritet = models.IntegerField()
    permission = models.BooleanField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start']


class Comments(models.Model):
    text = models.TextField()
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.text}'
