from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User, Payment
from courses.models import Course, Lesson


class Command(BaseCommand):
    help = "Создает тестовые платежи с базовой проверкой данных"

    def handle(self, *args, **options):
        try:
            # 1. Создаем или получаем тестовые данные
            course, _ = Course.objects.get_or_create(
                title="Основы Python", defaults={"description": "Базовый курс по программированию на Python"}
            )

            lesson, _ = Lesson.objects.get_or_create(
                title="Введение в Python", defaults={"course": course, "description": "Первый урок курса"}
            )

            user, _ = User.objects.get_or_create(
                email="student1@example.com", defaults={"first_name": "Иван", "last_name": "Иванов"}
            )

            # 2. Подготовка данных для платежей
            payments_data = [
                {
                    "user": user,
                    "paid_course": course,
                    "paid_lesson": None,
                    "amount": 15000.00,
                    "payment_method": "transfer",
                    "payment_date": timezone.now() - timezone.timedelta(days=1),
                },
                {
                    "user": user,
                    "paid_course": None,
                    "paid_lesson": lesson,
                    "amount": 3000.00,
                    "payment_method": "cash",
                    "payment_date": timezone.now(),
                },
            ]

            # 3. Создание платежей с проверкой
            created_count = 0
            for data in payments_data:
                payment, created = Payment.objects.get_or_create(
                    user=data["user"], payment_date=data["payment_date"], defaults=data
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Создан платеж: {payment.amount} руб. ({payment.payment_method})")
                    )
                else:
                    self.stdout.write(self.style.NOTICE(f"Платеж уже существует: {payment.amount} руб."))

            self.stdout.write(
                self.style.SUCCESS(f"\nУспешно создано {created_count} из {len(payments_data)} платежей")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при создании тестовых данных: {str(e)}"))
