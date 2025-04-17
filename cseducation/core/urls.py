from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/ask/', views.question_new, name='question_new_course'),
    path('courses/<int:course_id>/project-discussions/new/', views.project_discussion_new, name='project_discussion_new'),
    path('project-discussions/<int:pk>/', views.project_discussion_detail, name='project_discussion_detail'),
]
