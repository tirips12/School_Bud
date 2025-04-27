from django.urls import path
from . import api_views

urlpatterns = [
    path('eventlogs/', api_views.eventlog_list, name='api_eventlog_list'),
]

from . import api_github_analytics
urlpatterns += [
    path('github-analytics/', api_github_analytics.github_repo_analytics, name='api_github_analytics'),
]
