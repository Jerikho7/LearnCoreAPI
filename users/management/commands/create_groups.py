from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson


class Command(BaseCommand):
    help = "Creates moderator group with permissions"

    def handle(self, *args, **options):
        # Создаем группу
        mod_group, created = Group.objects.get_or_create(name="moderators")

        # Получаем ContentType для моделей
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)

        # Получаем разрешения
        permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct],
            codename__in=["view_course", "change_course", "view_lesson", "change_lesson"],
        )

        # Назначаем разрешения группе
        mod_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Successfully created moderators group"))
