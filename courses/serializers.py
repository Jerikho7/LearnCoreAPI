from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import Course, Lesson, Subscription
from courses.validators import YouTubeLinkValidator


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели Lesson.

    Сериализует все поля урока, включая связь с курсом.
    Проверяет, что поле link содержит только ссылки на YouTube-видео.

    Attributes:
        validators: Список валидаторов, включая проверку ссылок на YouTube.
    """

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeLinkValidator(field="link")]


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели Course с дополнительными полями.

    Attributes:
        lesson_count (SerializerMethodField): Количество уроков в курсе.
        lessons (LessonSerializer): Список уроков курса (read-only).
        is_subscribed (SerializerMethodField): Признак подписки текущего пользователя на курс (read-only).

    Methods:
        get_lesson_count: Возвращает количество уроков.
        get_is_subscribed: Проверяет, подписан ли текущий пользователь на курс.
    """

    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    @staticmethod
    def get_lesson_count(instance):
        """Вычисляет количество уроков в курсе.

        Args:
            instance (Course): Объект курса.

        Returns:
            int: Число уроков.
        """
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        """Проверяет, подписан ли текущий пользователь на курс.

        Args:
            instance (Course): Объект курса.

        Returns:
            bool: True, если пользователь подписан, иначе False.
        """
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return instance.subscriptions.filter(user=user).exists()

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ("user", "subscribed_at")
