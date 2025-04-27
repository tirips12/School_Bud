import base64
from django.core.management.base import BaseCommand
from core.models import GitHubShowcasedRepo
from github import Github
from django.utils import timezone
from datetime import datetime
import requests

REPO = "skooter500/OOP-2021-2022"
GITHUB_API = "https://api.github.com"
import os
from dotenv import load_dotenv
load_dotenv()
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("WARNING: No GITHUB_TOKEN set. You will be rate-limited by GitHub API. Add GITHUB_TOKEN to your environment or .env file.")

class Command(BaseCommand):
    help = 'Fetch all forkers of the repo and their original (non-forked) repos and cache them.'

    def handle(self, *args, **options):
        # Optionally: read GITHUB_TOKEN from settings
        g = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()
        main_repo = g.get_repo(REPO)
        print(f"Fetching forks for {REPO}...")
        forkers = list(main_repo.get_forks())
        print(f"Found {len(forkers)} forkers.")
        for user in forkers:
            username = user.owner.login
            avatar_url = user.owner.avatar_url
            print(f"Fetching repos for {username}...")
            try:
                user_obj = g.get_user(username)
                for repo in user_obj.get_repos():
                    if repo.fork:
                        continue  # Only original repos
                    readme_content = ''
                    try:
                        readme = repo.get_readme()
                        content = base64.b64decode(readme.content)
                        readme_content = content.decode('utf-8', errors='replace')
                    except Exception:
                        pass
                    # Upsert
                    obj, created = GitHubShowcasedRepo.objects.update_or_create(
                        owner=username,
                        name=repo.name,
                        defaults={
                            'owner_avatar_url': avatar_url,
                            'url': repo.html_url,
                            'description': repo.description or '',
                            'readme': readme_content,
                            'stargazers_count': repo.stargazers_count,
                            'language': repo.language or '',
                            'created_at': repo.created_at or timezone.now(),
                            'updated_at': repo.updated_at or timezone.now(),
                            'metadata': {
                                'forks_count': repo.forks_count,
                                'watchers_count': repo.watchers_count,
                            }
                        }
                    )
                    print(f"{'Created' if created else 'Updated'}: {username}/{repo.name}")
            except Exception as e:
                print(f"Error fetching repos for {username}: {e}")
