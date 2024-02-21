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

    is_added = models.BooleanField(default=False, editable=False)

    def save(self, *args, **kwargs):
        if self.is_added is False:
            self.is_added = True
            lessons = self.course.lessons.all()
            for lesson in lessons:
                UserLesson.objects.create(
                    user=self.user,
                    lesson=lesson
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} -> {self.course}"


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

    def change_watched_time(self, time):
        self.watched_times += time
        self.save()


class LessonWatched(BaseModel):
    user_lesson = models.ForeignKey(UserLesson, on_delete=models.CASCADE,
                                    related_name='watched_lessons')
    from_time = models.IntegerField(default=0)
    to_time = models.IntegerField(default=0)
    watch_time = models.IntegerField(default=0, editable=False)

    is_used = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f'{self.user_lesson}'

    def save(self, *args, **kwargs):
        if self.is_used is False:
            self.is_used = True
            self.watch_time = self.to_time - self.from_time
            self.user_lesson.change_watched_time(self.watch_time)
            self.user_lesson.change_status()
        super().save(*args, **kwargs)







