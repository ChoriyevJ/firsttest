# Generated by Django 4.2.7 on 2024-02-21 16:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("url", models.URLField(blank=True, max_length=255, null=True)),
                (
                    "video",
                    models.FileField(
                        upload_to="videos/", validators=[django.core.validators.FileExtensionValidator(["mp4", "avi"])]
                    ),
                ),
                ("duration", models.IntegerField(default=0)),
                ("courses", models.ManyToManyField(related_name="lessons", to="course.course")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserLesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("VIEWED", "Просмотрено"), ("NO_VIEWED", "Не просмотрено")],
                        default="NO_VIEWED",
                        max_length=15,
                    ),
                ),
                ("watched_times", models.IntegerField(default=0)),
                ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="course.lesson")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserCourse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_added", models.BooleanField(default=False)),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="course.course")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LessonWatched",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("from_time", models.IntegerField(default=0)),
                ("to_time", models.IntegerField(default=0)),
                ("watch_time", models.IntegerField(default=0)),
                ("is_used", models.BooleanField(default=False)),
                (
                    "user_lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watched_lessons",
                        to="course.userlesson",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="lesson",
            name="users",
            field=models.ManyToManyField(
                related_name="lessons", through="course.UserLesson", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="user_courses", through="course.UserCourse", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
