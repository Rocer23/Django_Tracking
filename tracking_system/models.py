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
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.user.username} - {self.text[:50]}'
