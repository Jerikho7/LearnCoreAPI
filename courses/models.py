from django.db import models

from users.models import User


class Course(models.Model):
    """Модель курса онлайн-обучения.

    Attributes:
        title (CharField): Название курса (максимум 150 символов).
        description (TextField): Подробное описание курса. Может быть пустым.
        preview (ImageField): Превью изображение курса. Загружается в `courses/img/`.

    Methods:
         __str__: Возвращает строку в формате "Название - Описание".
    """

    title = models.CharField(max_length=150, verbose_name="Название курса")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    preview = models.ImageField(upload_to="courses/img", null=True, blank=True)
    owner = models.ForeignKey(
        User, blank=True, null=True, related_name="courses", on_delete=models.SET_NULL, verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} - {self.description}"


class Lesson(models.Model):
    """Модель урока в рамках курса.

    Attributes:
        title (CharField): Название урока (максимум 150 символов).
        description (TextField): Содержание урока. Может быть пустым.
        preview (ImageField): Превью изображение урока. Загружается в `lessons/img/`.
        link (URLField): Ссылка на видео/материалы урока. Может быть пустой.
        course (ForeignKey): Связь с родительским курсом.

    Methods:
        __str__: Возвращает строку в формате "Название - Описание".
    """

    title = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    preview = models.ImageField(upload_to="lessons/img", null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, blank=True, null=True, related_name="lessons", on_delete=models.SET_NULL, verbose_name="Владелец"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} - {self.description}"


class Subscription(models.Model):
    """Модель подписки."""

    course = models.ForeignKey(Course, related_name="subscriptions", on_delete=models.CASCADE, verbose_name="Курс")
    user = models.ForeignKey(User, related_name="subscriptions", on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
