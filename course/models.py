from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model


from utils.models import BaseModel


class Course(BaseModel):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              related_name='courses')
    users = models.ManyToManyField(get_user_model(),
                                   related_name='user_courses', blank=True, through="UserCourse")

    def __str__(self):
        return self.title


class Lesson(BaseModel):
    courses = models.ManyToManyField(Course,
                                     related_name='lessons')
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255, blank=True, null=True)
    video = models.FileField(upload_to='videos/', validators=[FileExtensionValidator(['mp4', 'avi'])])
    duration = models.IntegerField(default=0)

    users = models.ManyToManyField(get_user_model(),
                                   related_name='lessons', through="UserLesson")

    def __str__(self):
        return self.title


class UserCourse(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    is_added = models.BooleanField(default=False)


class UserLesson(BaseModel):

    class Status(models.TextChoices):
        VIEWED = 'VIEWED', 'Просмотрено',
        NO_VIEWED = 'NO_VIEWED', 'Не просмотрено',

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    status = models.CharField(max_length=15, choices=Status.choices,
                              default=Status.NO_VIEWED)
    watched_times = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} -> {self.lesson}'

    def change_status(self):
        if self.watched_times / self.lesson.duration >= 0.8:
            self.status = self.Status.VIEWED
            self.save()

    def change_watched_time(self):
        times = self.watched_lessons.filter(is_used=False)
        for w_time in times:
            w_time.is_used = True
            w_time.save()
            self.watched_times += w_time.watch_time
        self.save()


class LessonWatched(BaseModel):
    user_lesson = models.ForeignKey(UserLesson, on_delete=models.CASCADE,
                                    related_name='watched_lessons')
    from_time = models.IntegerField(default=0)
    to_time = models.IntegerField(default=0)
    watch_time = models.IntegerField(default=0)

    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.user_lesson

    def save(self, *args, **kwargs):
        if self.to_time - self.from_time == 15:
            self.watch_time = self.to_time - self.from_time
        super().save(*args, **kwargs)







