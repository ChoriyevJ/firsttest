from rest_framework import serializers


from course import models


'''
# class LessonSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.Lesson
#         fields = (
#             'title',
#             'url',
#             'video',
#             'duration',
#         )
'''


class LessonListSerializer(serializers.ModelSerializer):

    title = serializers.StringRelatedField(source="lesson.title")
    url = serializers.StringRelatedField(source="lesson.url")
    video = serializers.StringRelatedField(source="lesson.video")
    duration = serializers.StringRelatedField(source="lesson.duration")

    class Meta:
        model = models.UserLesson
        fields = (
            'title',
            'url',
            'video',
            'duration',
            'status',
            'watched_times'
        )


class LessonListInCourseSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(source="lesson.title")
    url = serializers.StringRelatedField(source="lesson.url")
    video = serializers.StringRelatedField(source="lesson.video")
    duration = serializers.StringRelatedField(source="lesson.duration")

    class Meta:
        model = models.UserLesson
        fields = (
            'title',
            'url',
            'video',
            'duration',
            'status',
            'watched_times',
            'last_watched_at'
        )


class CourseListSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField(source="owner.username")
    quantity_views = serializers.IntegerField()
    wasted_time = serializers.IntegerField()
    quantity_users = serializers.IntegerField()
    percentage = serializers.FloatField()
    # total_users = serializers.IntegerField()

    class Meta:
        model = models.Course
        fields = (
            'title',
            'owner',
            'quantity_views',
            'wasted_time',
            'quantity_users',
            'percentage',
            # 'total_users',
        )

    # def get_percentage(self, obj):
    #     total_users = obj.total_users
    #     quantity_users = obj.quantity_users
    #     return quantity_users / total_users * 100


'''
# class CourseSerializer(serializers.ModelSerializer):
#
#     lessons = LessonSerializer(many=True)
    # lessons_with_status = serializers.SerializerMethodField()
    # user_lesson = UserLessonSerializer(many=True)

    # class Meta:
    #     model = models.Course
    #     fields = ('title', 'lessons')

    # def get_lessons_with_status(self, obj):
    #     user = self.context['request'].user
    #     lessons = obj.lessons.all()
    #     user_lessons = models.UserLesson.objects.filter(
    #         lesson__in=lessons, user=user
    #     )
    #
    #     lessons_data = []
    #     for lesson in lessons:
    #         try:
    #             user_lesson = user_lessons.get(lesson=lesson)
    #             lesson_data = LessonSerializer(lesson).data
    #             lesson_data['status'] = user_lesson.status
    #             lesson_data['watched_times'] = user_lesson.watched_times
    #         except models.UserLesson.DoesNotExist:
    #             lesson_data = LessonSerializer(lesson).data
    #             lesson_data['status'] = None
    #             lesson_data['watched_times'] = None
    #         lessons_data.append(lesson_data)
    #     return lessons_data
'''












