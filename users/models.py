from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создаёт и сохраняет пользователя с указанным email и паролем."""
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создаёт и сохраняет суперпользователя с указанным email и паролем."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Кастомная модель пользователя с расширенными полями.

    Attributes:
        email (EmailField): Уникальный email пользователя (используется как username).
        avatar (ImageField): Аватар пользователя. Загружается в 'users/avatars/'.
        phone_number (PhoneNumberField): Номер телефона в международном формате.
        city (CharField): Город проживания пользователя.

    Meta:
        verbose_name (str): Человекочитаемое имя в единственном числе.
        verbose_name_plural (str): Человекочитаемое имя во множественном числе.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите email")
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите изображение"
    )
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Телефон", help_text="Введите номер телефона")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город", help_text="Введите город")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель платежа пользователя за курсы или уроки.

    Attributes:
        user (ForeignKey): Ссылка на пользователя, совершившего платеж.
        payment_date (DateTimeField): Дата и время платежа (автоматически заполняется).
        paid_course (ForeignKey): Оплаченный курс (может быть пустым).
        paid_lesson (ForeignKey): Оплаченный урок (может быть пустым).
        amount (DecimalField): Сумма платежа с точностью до 2 знаков после запятой.
        payment_method (str): Способ оплаты ('cash' или 'transfer').

    Meta:
        verbose_name (str): Человекочитаемое имя в единственном числе.
        verbose_name_plural (str): Человекочитаемое имя во множественном числе.
        ordering (list): Сортировка по умолчанию (по дате платежа, новые сначала).
    """

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.payment_date})"
