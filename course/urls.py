from django.urls import path


from course import views


urlpatterns = [
    path('list/', views.LessonListAPIView.as_view()),
    path('list/<int:course_id>/', views.LessonListInCourseAPIView.as_view()),

    path('home/', views.CourseListAPIView.as_view())
]
