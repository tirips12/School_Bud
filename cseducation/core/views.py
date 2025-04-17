import base64
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from github import Github

from .forms import QuestionForm, RegistrationForm, ProjectDiscussionForm
from .models import Answer, Profile, Question, Vote, Course, ProjectDiscussion, ProjectComment


def home(request):
    questions = Question.objects.filter(removed=False).order_by('-created_at')
    if request.user.is_staff:
        removed_questions = Question.objects.filter(removed=True).order_by('-removed_at')
        return render(request, 'core/home.html', {
            'questions': questions,
            'removed_questions': removed_questions
        })
    return render(request, 'core/home.html', {'questions': questions})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def get_github_repos(github_username):
    try:
        g = Github(settings.SOCIAL_AUTH_GITHUB_KEY)  # or use a personal access token
        user = g.get_user(github_username)
        repos = []
        
        for repo in user.get_repos():
            try:
                # Get README content
                readme_content = None
                try:
                    readme = repo.get_contents("README.md")
                    if readme:
                        content = base64.b64decode(readme.content)
                        readme_content = content.decode('utf-8')
                except:
                    readme_content = None
                
                repo_data = {
                    'name': repo.name,
                    'description': repo.description,
                    'url': repo.html_url,
                    'stars': repo.stargazers_count,
                    'language': repo.language,
                    'readme': readme_content,
                    'created_at': repo.created_at.isoformat(),
                    'updated_at': repo.updated_at.isoformat(),
                }
                repos.append(repo_data)
            except Exception as e:
                print(f"Error fetching repo {repo.name}: {str(e)}")
                
        return repos
    except Exception as e:
        print(f"Error fetching GitHub data: {str(e)}")
        return None

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    questions = Question.objects.filter(author=user, removed=False)
    
    # Check if we need to update GitHub data
    if profile.github_username and (
        not profile.github_repos or 
        not profile.last_github_sync or 
        profile.last_github_sync < datetime.now() - timedelta(hours=24)
    ):
        repos = get_github_repos(profile.github_username)
        if repos:
            profile.github_repos = repos
            profile.last_github_sync = datetime.now()
            profile.save()
    
    return render(request, 'core/profile.html', {
        'profile': profile,
        'questions': questions,
        'github_repos': profile.github_repos if profile.github_repos else []
    })

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'core/question_detail.html', {'question': question})

@login_required
def question_new(request, course_id=None):
    course = None
    if course_id:
        course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            if course:
                question.course = course
            question.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm(initial={'course': course} if course else None)
    return render(request, 'core/question_form.html', {'form': form, 'course': course})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    questions = course.questions.filter(removed=False).order_by('-created_at')
    project_discussions = course.project_discussions.order_by('-created_at')
    return render(request, 'core/course_detail.html', {
        'course': course,
        'questions': questions,
        'project_discussions': project_discussions
    })


@login_required
def project_discussion_new(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        form = ProjectDiscussionForm(request.POST, course=course)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.created_by = request.user
            discussion.course = course
            # Ensure each project is stored as a dict with at least 'name'
            raw_projects = form.cleaned_data['projects']
            projects_list = []
            for p in raw_projects:
                if isinstance(p, dict):
                    projects_list.append(p)
                else:
                    projects_list.append({'name': p})
            discussion.projects = projects_list
            discussion.save()
            return redirect('project_discussion_detail', pk=discussion.pk)
    else:
        form = ProjectDiscussionForm(course=course)
    return render(request, 'core/project_discussion_form.html', {'form': form, 'course': course})


def project_discussion_detail(request, pk):
    discussion = get_object_or_404(ProjectDiscussion, pk=pk)
    if request.method == "POST" and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            ProjectComment.objects.create(
                discussion=discussion,
                author=request.user,
                content=content
            )
    return render(request, 'core/project_discussion_detail.html', {'discussion': discussion})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def vote(request):
    if not request.user.is_authenticated:
        print("User not authenticated")
        return HttpResponseForbidden()
        
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        object_id = request.POST.get('object_id')
        vote_type = request.POST.get('vote_type')
        
        print(f"Vote request: type={content_type}, id={object_id}, vote={vote_type}")
        
        try:
            if content_type == 'question':
                obj = Question.objects.get(id=object_id)
                content_author = obj.author
            else:
                obj = Answer.objects.get(id=object_id)
                content_author = obj.author
                
            print(f"Content author: {content_author.username}")
            print(f"Initial reputation: {content_author.profile.reputation}")
            
            # Check if user has already voted
            existing_vote = Vote.objects.filter(
                user=request.user,
                question=obj if content_type == 'question' else None,
                answer=obj if content_type == 'answer' else None
            ).first()
            
            # Calculate vote and reputation changes
            if existing_vote:
                if existing_vote.vote_type == vote_type:
                    # If same vote type, remove vote
                    existing_vote.delete()
                    vote_change = -1 if vote_type == 'UP' else 1
                    rep_change = -10 if vote_type == 'UP' else 5  # Reverse reputation
                else:
                    # If different vote type, change vote
                    existing_vote.vote_type = vote_type
                    existing_vote.save()
                    vote_change = 2 if vote_type == 'UP' else -2
                    rep_change = 20 if vote_type == 'UP' else -10  # Double reputation change
            else:
                # Create new vote
                Vote.objects.create(
                    user=request.user,
                    question=obj if content_type == 'question' else None,
                    answer=obj if content_type == 'answer' else None,
                    vote_type=vote_type
                )
                vote_change = 1 if vote_type == 'UP' else -1
                rep_change = 10 if vote_type == 'UP' else -5  # Base reputation change
            
            # Update vote count
            obj.votes = obj.votes + vote_change
            obj.save()
            
            # Update author's reputation
            if content_author != request.user:  # Don't change reputation if user votes on their own content
                profile = content_author.profile
                profile.reputation += rep_change
                profile.save()
            
            print(f"New reputation: {content_author.profile.reputation}")  # Debug log
            
            return JsonResponse({
                'status': 'success',
                'new_vote_count': obj.votes,
                'new_reputation': content_author.profile.reputation
            })
            
        except Exception as e:
            print(f"Error in vote view: {str(e)}")  # Debug log
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    }, status=400)

@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Answer.objects.create(
                question=question,
                author=request.user,
                content=content
            )
        return redirect('question_detail', pk=question.pk)
    return redirect('question_detail', pk=question.pk)

@staff_member_required
def remove_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        question.removed = True
        question.removed_by = request.user
        question.removed_at = timezone.now()
        question.removal_reason = reason
        question.save()
        messages.success(request, 'Question has been removed.')
        return redirect('home')
    return render(request, 'core/remove_content.html', {
        'content_type': 'question',
        'content': question
    })

@staff_member_required
def remove_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        answer.removed = True
        answer.removed_by = request.user
        answer.removed_at = timezone.now()
        answer.removal_reason = reason
        answer.save()
        messages.success(request, 'Answer has been removed.')
        return redirect('question_detail', pk=answer.question.pk)
    return render(request, 'core/remove_content.html', {
        'content_type': 'answer',
        'content': answer
    })

@staff_member_required
def restore_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.removed = False
    question.removed_by = None
    question.removed_at = None
    question.removal_reason = ''
    question.save()
    messages.success(request, 'Question has been restored.')
    return redirect('question_detail', pk=question.pk)

@staff_member_required
def restore_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    answer.removed = False
    answer.removed_by = None
    answer.removed_at = None
    answer.removal_reason = ''
    answer.save()
    messages.success(request, 'Answer has been restored.')
    return redirect('question_detail', pk=answer.question.pk)
