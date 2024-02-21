from django.db.models.signals import post_save
from django.dispatch import receiver

from course.models import LessonWatched


# @receiver(post_save, sender=LessonWatched)
# def lesson_change_watched_time(sender, instance, created, **kwargs):
#
#     if created:
#         print('\n\n')
#         print(instance)
#         print('\n\n')





