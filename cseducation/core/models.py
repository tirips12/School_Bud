from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reputation = models.IntegerField(default=0)
    github_username = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    github_repos = models.JSONField(null=True, blank=True)
    last_github_sync = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

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
# Removed instance.profile.save() to prevent recursion

# Signal to sync Profile.role with User.is_staff/is_superuser
def sync_user_role(sender, instance, **kwargs):
    if instance.role == 'admin':
        instance.user.is_staff = True
        instance.user.is_superuser = True
        instance.user.save()
    elif instance.role == 'lecturer':
        instance.user.is_staff = True
        instance.user.is_superuser = False
        instance.user.save()
    else:
        instance.user.is_staff = False
        instance.user.is_superuser = False
        instance.user.save()

from django.db.models.signals import post_save
post_save.connect(sync_user_role, sender=Profile)

class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    removed = models.BooleanField(default=False)
    removed_by = models.ForeignKey(User, null=True, blank=True, related_name='removed_questions', on_delete=models.SET_NULL)
    removed_at = models.DateTimeField(null=True, blank=True)
    removal_reason = models.TextField(blank=True)

    def __str__(self):
        return self.title

def log_question_event(sender, instance, created, **kwargs):
    from .models import EventLog
    if created:
        EventLog.objects.create(user=instance.author, event_type='question_created', description=instance.title)

post_save.connect(log_question_event, sender='core.Question')

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

def log_answer_event(sender, instance, created, **kwargs):
    from .models import EventLog
    if created:
        EventLog.objects.create(user=instance.author, event_type='answer_created', description=instance.content[:100])

post_save.connect(log_answer_event, sender='core.Answer')

class Vote(models.Model):
    VOTE_TYPES = (
        ('UP', 'Upvote'),
        ('DOWN', 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    github_repo = models.ForeignKey('GitHubShowcasedRepo', on_delete=models.CASCADE, null=True, blank=True)
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

def log_vote_event(sender, instance, created, **kwargs):
    from .models import EventLog
    if created:
        target = instance.question or instance.answer
        desc = f"Voted {instance.vote_type} on {target}"
        EventLog.objects.create(user=instance.user, event_type='vote', description=desc)

post_save.connect(log_vote_event, sender='core.Vote')

class ProjectDiscussion(models.Model):
    """
    Represents a discussion around a GitHub project or a group of similar projects.
    """
    group_name = models.CharField(max_length=200)  # e.g. 'OOP lab2'
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='project_discussions')
    projects = models.JSONField()  # List of dicts: {name, owner, url, summary, readme}
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.group_name

class ProjectComment(models.Model):
    discussion = models.ForeignKey(ProjectDiscussion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class EventLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    lecturer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_led')
    students = models.ManyToManyField(User, related_name='courses_enrolled', blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.code})"

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='assignment_submissions/', blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username}"

# --- GitHub Projects Showcase ---
class GitHubShowcasedRepo(models.Model):
    owner = models.CharField(max_length=100)
    owner_avatar_url = models.URLField(blank=True)
    name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    readme = models.TextField(blank=True)
    stargazers_count = models.IntegerField(default=0)
    language = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    votes = models.IntegerField(default=0)
    # Optionally: cache JSON metadata
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner}/{self.name}"

class GitHubRepoComment(models.Model):
    repo = models.ForeignKey(GitHubShowcasedRepo, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} on {self.repo.owner}/{self.repo.name}"
