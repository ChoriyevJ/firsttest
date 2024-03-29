# Generated by Django 4.2.7 on 2024-02-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lessonwatched",
            name="is_used",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name="lessonwatched",
            name="watch_time",
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name="usercourse",
            name="is_added",
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
