from django.shortcuts import render
from rest_framework import generics
from django.db import models as db_models

from course import models
from course import serializers

'''
# class LessonListAPIView(generics.ListAPIView):
#     queryset = models.Course.objects.all()
#     serializer_class = serializers.CourseSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#
#         courses = super().get_queryset().filter(
#             user_courses__user=user, lessons__user_lessons__user__id=user.id
#         ).prefetch_related("lessons", "lessons__user_lessons", "lessons__user_lessons__user")
#
#         return courses
'''


class LessonListAPIView(generics.ListAPIView):
    queryset = models.UserLesson.objects.all()
    serializer_class = serializers.LessonListSerializer

    def get_queryset(self):
        user = self.request.user
        lessons = super().get_queryset().filter(
            user=user,
            lesson__courses__user_courses__user=user,
        ).select_related("lesson")

        return lessons


class LessonListInCourseAPIView(generics.ListAPIView):
    queryset = models.UserLesson.objects.all()
    serializer_class = serializers.LessonListInCourseSerializer

    def get_queryset(self):
        user = self.request.user
        lessons = super().get_queryset().filter(
            user=user,
            lesson__courses__user_courses__user=user,
            lesson__courses__user_courses__course__id=self.kwargs.get('course_id')
        ).select_related("lesson")

        return lessons


class CourseListAPIView(generics.ListAPIView):
    queryset = models.Course.objects.all().select_related("owner")
    serializer_class = serializers.CourseListSerializer

    def get_queryset(self):

        users_count = models.get_user_model().objects.select_related("users").aggregate(
            users_count=db_models.Count('id'))['users_count']

        courses = super().get_queryset().annotate(
            quantity_views=db_models.Count(
                "lessons",
                filter=db_models.Q(lessons__user_lessons__status=models.Status.VIEWED),
                output_field=db_models.IntegerField()
            ),
            wasted_time=db_models.Sum(
                "lessons__user_lessons__watched_times"
            ),
            quantity_users=db_models.Count(
                "user_courses",
                distinct=True
            ),
            percentage=(db_models.F('quantity_users') * 100 / users_count)
        )

        return courses







