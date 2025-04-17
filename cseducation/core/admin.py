from django.contrib import admin
from .models import Profile, ProjectDiscussion, ProjectComment, EventLog, Question, Answer, Vote, Course, Assignment, AssignmentSubmission

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'reputation', 'github_username', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'github_username')

@admin.register(ProjectDiscussion)
class ProjectDiscussionAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'course', 'created_by', 'created_at', 'votes')
    search_fields = ('group_name',)
    list_filter = ('course',)

@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'author', 'created_at')
    search_fields = ('discussion__group_name', 'author__username')

@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'timestamp')
    search_fields = ('user__username', 'event_type')
    list_filter = ('event_type',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'course', 'created_at', 'votes', 'removed')
    search_fields = ('title', 'author__username')
    list_filter = ('removed', 'course')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at', 'votes', 'removed')
    search_fields = ('question__title', 'author__username')
    list_filter = ('removed',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'vote_type', 'created_at')
    search_fields = ('user__username',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'lecturer')
    search_fields = ('code', 'name', 'lecturer__username')
    list_filter = ('lecturer',)
    filter_horizontal = ('students',)

class AssignmentSubmissionInline(admin.TabularInline):
    model = AssignmentSubmission
    extra = 0

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'created_at')
    search_fields = ('title', 'course__name', 'course__code')
    list_filter = ('course',)
    inlines = [AssignmentSubmissionInline]

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade')
    search_fields = ('assignment__title', 'student__username')
    list_filter = ('assignment', 'grade')
