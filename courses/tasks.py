from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from users.models import User
from .models import Subscription


@shared_task
def send_course_update_notification(course_id):
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related("user")

    for subscription in subscriptions:
        send_mail(
            subject=f"Обновление курса {subscription.course.title}",
            message=f'Курс "{subscription.course.title}" был обновлен. Проверьте новые материалы!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )


@shared_task
def deactivate_inactive_users():
    """Блокирует пользователей, не заходивших более 30 дней."""
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(is_active=True, last_login__lt=one_month_ago)
    count = inactive_users.update(is_active=False)
    return f"Deactivated {count} inactive users"
