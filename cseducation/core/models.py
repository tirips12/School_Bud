from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reputation = models.IntegerField(default=0)
    github_username = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    github_repos = models.JSONField(null=True, blank=True)
    last_github_sync = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User) # pylint: disable=unused-argument if not used in the code for now
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()

class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(User, null=True, blank=True, related_name='removed_questions', on_delete=models.SET_NULL)
    removed_at = models.DateTimeField(null=True, blank=True)
    removal_reason = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(User, null=True, blank=True, related_name='removed_answers', on_delete=models.SET_NULL)
    removed_at = models.DateTimeField(null=True, blank=True)
    removal_reason = models.TextField(blank=True)

class Vote(models.Model):
    VOTE_TYPES = (
        ('UP', 'Upvote'),
        ('DOWN', 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
