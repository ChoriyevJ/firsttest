from django.contrib import admin


from course import models


class UserCourseInline(admin.TabularInline):
    model = models.UserCourse
    extra = 0


class WatchedLessonInline(admin.StackedInline):
    model = models.LessonWatched
    extra = 0


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('title', )
    inlines = (UserCourseInline,)


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('title',)


@admin.register(models.UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    inlines = (WatchedLessonInline,)
    pass



