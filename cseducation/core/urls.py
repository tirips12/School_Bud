from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('github-projects/<int:pk>/remove/', views.remove_github_project, name='remove_github_project'),
    path('github-projects/comment/<int:comment_id>/remove/', views.remove_github_comment, name='remove_github_comment'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/ask/', views.question_new, name='question_new_course'),
    path('courses/<int:course_id>/project-discussions/new/', views.project_discussion_new, name='project_discussion_new'),
    path('project-discussions/<int:pk>/', views.project_discussion_detail, name='project_discussion_detail'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    # GitHub Projects Showcase
    path('github-projects/', views.github_projects_list, name='github_projects_list'),
    path('github-projects/<int:pk>/', views.github_project_detail, name='github_project_detail'),
    path('github-projects/<int:pk>/comment/', views.github_repo_comment, name='github_repo_comment'),
    path('github-projects/<int:pk>/vote/', views.github_repo_vote, name='github_repo_vote'),
]
