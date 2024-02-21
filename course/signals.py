from django.db.models.signals import post_save
from django.dispatch import receiver

from course.models import Course, UserLesson


@receiver(post_save, sender=Course)
def add_lesson_to_user(sender, instance, created, **kwargs):

    users = instance.users.all(is_added=False)
    for user in users:
        user.is_added = True
        UserLesson.objects.create(

        )




