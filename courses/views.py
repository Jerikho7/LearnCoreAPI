from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer
from rest_framework.viewsets import ModelViewSet

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
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['retrieve', 'update', 'partial_update', 'list']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


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

    def get_queryset(self):
        """Фильтрует уроки: не-модераторы видят только свои."""
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
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
