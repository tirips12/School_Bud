# Generated by Django 4.2.16 on 2024-12-02 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="github_repos",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="last_github_sync",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
