# Generated by Django 5.1.4 on 2025-04-15 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_assignment_assignmentsubmission_course_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectdiscussion",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="project_discussions",
                to="core.course",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="questions",
                to="core.course",
            ),
        ),
    ]
