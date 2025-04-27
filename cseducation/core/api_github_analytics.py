from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import GitHubShowcasedRepo, GitHubRepoComment
from .serializers import GitHubShowcasedRepoSerializer, GitHubRepoCommentSerializer
from django.db import models

@api_view(['GET'])
@permission_classes([IsAdminUser])
def github_repo_analytics(request):
    """API endpoint for GitHub repo analytics: top repos, most commented, most voted."""
    # Top 5 repos by votes
    top_voted = GitHubShowcasedRepo.objects.order_by('-votes')[:5]
    top_voted_data = GitHubShowcasedRepoSerializer(top_voted, many=True).data
    # Top 5 repos by comments
    top_commented = GitHubShowcasedRepo.objects.annotate(num_comments=models.Count('comments')).order_by('-num_comments')[:5]
    # Attach num_comments to metadata for frontend display
    top_commented_data = GitHubShowcasedRepoSerializer(top_commented, many=True).data
    for i, repo in enumerate(top_commented):
        if i < len(top_commented_data):
            if not top_commented_data[i].get('metadata'):
                top_commented_data[i]['metadata'] = {}
            top_commented_data[i]['metadata']['num_comments'] = repo.num_comments
    # Recent comments
    recent_comments = GitHubRepoComment.objects.order_by('-created_at')[:10]
    recent_comments_data = GitHubRepoCommentSerializer(recent_comments, many=True).data
    return Response({
        'top_voted': top_voted_data,
        'top_commented': top_commented_data,
        'recent_comments': recent_comments_data
    })
