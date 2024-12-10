from social_core.backends.github import GithubOAuth2

from .models import Profile


def get_github_data(backend, user, response, *args, **kwargs):
    if isinstance(backend, GithubOAuth2):
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
            
        profile = user.profile
        profile.github_username = response.get('login')
        
        # Get additional GitHub data if needed
        if response.get('bio'):
            profile.bio = response.get('bio')
            
        profile.save() 