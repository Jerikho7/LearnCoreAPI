from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели Lesson.

    Сериализует все поля урока, включая связь с курсом.
    """
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели Course с дополнительными полями.

    Attributes:
        lesson_count (SerializerMethodField): Количество уроков в курсе.
        lessons (LessonSerializer): Список уроков курса (read-only).

    Methods:
        get_lesson_count: Возвращает количество уроков.
    """
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    @staticmethod
    def get_lesson_count(instance):
        """Вычисляет количество уроков в курсе.

        Args:
            instance (Course): Объект курса.

        Returns:
            int: Число уроков.
        """
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
