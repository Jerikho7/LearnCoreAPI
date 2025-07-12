from rest_framework.decorators import action
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from courses.models import Course, Lesson, Subscription
from courses.paginators import Paginator
from courses.serializers import CourseSerializer, LessonSerializer
from rest_framework.viewsets import ModelViewSet

from courses.tasks import send_course_update_notification
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """ViewSet для работы с курсами (CRUD).

    Поддерживает все стандартные действия:
    - list: Получить список курсов
    - create: Создать новый курс
    - retrieve: Получить детали курса
    - update: Обновить курс
    - destroy: Удалить курс
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = Paginator

    def get_queryset(self):
        """Фильтрует курсы: не-модераторы видят только свои."""
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            return Course.objects.filter(owner=user)
        return Course.objects.all()

    def perform_create(self, serializer):
        """Автоматически устанавливает текущего пользователя как владельца."""
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["retrieve", "update", "partial_update", "list"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        send_course_update_notification.delay(instance.id)

    @action(detail=True, methods=["post", "delete"])
    def subscribe(self, request, pk=None):
        course = self.get_object()
        user = request.user

        if request.method == "POST":
            Subscription.objects.get_or_create(user=user, course=course)
            return Response({"status": "subscribed"}, status=201)

        Subscription.objects.filter(user=user, course=course).delete()
        return Response({"status": "unsubscribed"}, status=204)


class LessonCreateAPIView(CreateAPIView):
    """API для создания урока.

    Доступные методы:
    - POST: Создать новый урок
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """Автоматически устанавливает текущего пользователя как владельца."""
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """API для получения списка уроков.

    Доступные методы:
    - GET: Получить список всех уроков
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Paginator

    def get_queryset(self):
        """Фильтрует уроки: не-модераторы видят только свои."""
        user = self.request.user
        if user.is_authenticated and not user.groups.filter(name="moderators").exists():
            return Lesson.objects.filter(owner=user)
        return Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    """API для получения деталей урока.

    Доступные методы:
    - GET: Получить данные урока по ID
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    """API для обновления урока.

    Доступные методы:
    - PUT: Полное обновление урока
    - PATCH: Частичное обновление урока
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """API для удаления урока.

    Доступные методы:
    - DELETE: Удалить урок по ID
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionView(APIView):
    """API для управления подпиской пользователя на курс.

    Доступные методы:
    - POST: Добавить или удалить подписку на курс.

    Attributes:
        permission_classes: Требует аутентификацию пользователя.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Обрабатывает подписку или отписку от курса.

        Если пользователь уже подписан на курс, подписка удаляется.
        Если подписки нет, создаётся новая подписка.

        Args:
            request: HTTP-запрос с данными, содержащими course_id.

        Returns:
            Response: JSON-ответ с сообщением о результате ('подписка добавлена' или 'подписка удалена').

        Raises:
            Http404: Если курс с указанным course_id не существует.
        """
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            return Response({"message": "подписка удалена"}, status=status.HTTP_204_NO_CONTENT)
        else:
            Subscription.objects.create(user=user, course=course_item)
            return Response({"message": "подписка добавлена"}, status=status.HTTP_201_CREATED)
