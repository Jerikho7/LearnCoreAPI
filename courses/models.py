from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название курса")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    preview = models.ImageField(upload_to="courses/img", null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} - {self.description}"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    preview = models.ImageField(upload_to="lessons/img", null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} - {self.description}"
