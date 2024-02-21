from django.urls import path


from course import views


urlpatterns = [
    path('', views.LessonListAPIView.as_view()),
]
