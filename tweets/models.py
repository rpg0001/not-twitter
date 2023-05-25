from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Tweet(models.Model):
    text = models.CharField(max_length=144)
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.text


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=144)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-date"]


class Retweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.tweet.text + "(retweet)"

    class Meta:
        ordering = ["-date"]