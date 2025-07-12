from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    SubscriptionView,
)
from users.views import PaymentCreateAPIView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson_create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson_list/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lesson/<int:pk>/update", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("subscriptions/", SubscriptionView.as_view(), name="subscriptions"),
    path("courses/<int:course_id>/payment/", PaymentCreateAPIView.as_view(), name="payment-create"),
]

urlpatterns += router.urls
