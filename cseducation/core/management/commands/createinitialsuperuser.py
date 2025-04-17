from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates an initial superuser with default credentials.'

    def handle(self, *args, **kwargs):
        username = 'admin'
        password = 'admin123'
        email = 'admin@gmail.com'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists.'))
