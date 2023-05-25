from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="")
    display_name = models.CharField(default="", max_length=150)
    location = models.CharField(blank=True, max_length=150)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.display_name == "":
            self.display_name = self.user.username

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
