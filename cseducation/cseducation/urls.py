"""
URL configuration for cseducation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from core import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('question/new/', views.question_new, name='question_new'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('vote/', views.vote, name='vote'),
    path('question/<int:question_id>/answer/', views.answer_question, name='answer_question'),
    path('question/<int:pk>/remove/', views.remove_question, name='remove_question'),
    path('question/<int:pk>/restore/', views.restore_question, name='restore_question'),
    path('answer/<int:pk>/remove/', views.remove_answer, name='remove_answer'),
    path('answer/<int:pk>/restore/', views.restore_answer, name='restore_answer'),
]
