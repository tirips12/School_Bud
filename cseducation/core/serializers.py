from rest_framework import serializers
from .models import EventLog, GitHubShowcasedRepo, GitHubRepoComment

class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = ['id', 'user', 'event_type', 'description', 'timestamp', 'metadata']
        depth = 1

class GitHubShowcasedRepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubShowcasedRepo
        fields = ['id', 'owner', 'owner_avatar_url', 'name', 'url', 'description', 'stargazers_count', 'language', 'votes', 'created_at', 'updated_at', 'metadata']

class GitHubRepoCommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = GitHubRepoComment
        fields = ['id', 'repo', 'author', 'author_username', 'content', 'created_at']
