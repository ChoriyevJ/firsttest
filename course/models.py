from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from utils.models import BaseModel


class Status(models.TextChoices):
    VIEWED = 'Просмотрено', 'VIEWED'
    NO_VIEWED = 'Не просмотрено', 'NO_VIEWED'


class Course(BaseModel):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              related_name='courses')

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    courses = models.ManyToManyField(Course,
                                     related_name='lessons')
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255, blank=True, null=True)
    video = models.FileField(upload_to='videos/', validators=[FileExtensionValidator(['mp4', 'avi'])])
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserCourse(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='user_courses')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_courses')

    is_added = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if self.is_added is False:
            self.is_added = True
            lessons = self.course.lessons.all()
            # for lesson in lessons:
            #     UserLesson.objects.create(
            #         user=self.user,
            #         lesson=lesson
            #     )
            UserLesson.objects.bulk_create([
                UserLesson(lesson=lesson, user=self.user) for lesson in lessons
            ])

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user_lessons = UserLesson.objects.filter(
            user=self.user,
            lesson__courses=self.course
        )
        if user_lessons:
            user_lessons.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user} -> {self.course}"


class UserLesson(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_lessons')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                               related_name="user_lessons")

    status = models.CharField(max_length=15, choices=Status.choices,
                              default=Status.NO_VIEWED)
    watched_times = models.IntegerField(default=0)
    last_watched_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user} -> {self.lesson}'

    def change_status(self):
        if self.status == Status.NO_VIEWED and self.watched_times / self.lesson.duration >= 0.8:
            self.status = Status.VIEWED
            self.save()

    def change_watched_time(self, time):
        if self.status == Status.NO_VIEWED:
            self.watched_times += time
            if self.last_watched_at != timezone.now().date():
                self.last_watched_at = timezone.now().date()
            self.save()


class LessonWatched(BaseModel):
    user_lesson = models.ForeignKey(UserLesson, on_delete=models.CASCADE,
                                    related_name='watched_lessons')
    from_time = models.IntegerField(default=0)
    to_time = models.IntegerField(default=0)

    is_used = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f'{self.user_lesson}'

    def save(self, *args, **kwargs):
        if self.is_used is False:
            self.is_used = True
            watch_time = self.to_time - self.from_time
            self.user_lesson.change_watched_time(watch_time)
            self.user_lesson.change_status()
        super().save(*args, **kwargs)
