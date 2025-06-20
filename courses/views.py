from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer
from rest_framework.viewsets import ModelViewSet


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


class LessonCreateAPIView(CreateAPIView):
    """API для создания урока.

    Доступные методы:
    - POST: Создать новый урок
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    """API для получения списка уроков.

    Доступные методы:
    - GET: Получить список всех уроков
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """API для получения деталей урока.

    Доступные методы:
    - GET: Получить данные урока по ID
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """API для обновления урока.

    Доступные методы:
    - PUT: Полное обновление урока
    - PATCH: Частичное обновление урока
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """API для удаления урока.

    Доступные методы:
    - DELETE: Удалить урок по ID
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
