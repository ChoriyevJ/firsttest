from django.shortcuts import render
from rest_framework import generics
from django.db.models import Case, When, BooleanField, functions, Exists, OuterRef

from course import models
from course import serializers


class LessonListAPIView(generics.ListAPIView):
    queryset = models.Lesson.objects.all()
    serializer_class = serializers.LessonSerializer

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            "courses"
        ).annotate(
            in_users=functions.Coalesce(
                Exists(self.request.user.user_courses.filter(
                    id=OuterRef("pk")
                )), False
            )
        ).filter(
            in_users=True
        )
        return queryset




