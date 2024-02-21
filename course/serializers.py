from rest_framework import serializers


from course import models


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lesson
        fields = (
            'title',
            'url',
            'video',
            'duration'
        )



