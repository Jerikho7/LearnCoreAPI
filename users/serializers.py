from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField, ValidationError

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    """Сериализатор для модели User.

    Сериализует все поля пользователя, включая:
    - Основные данные (email, имя, фамилия)
    - Дополнительные поля (аватар, телефон, город)
    """

    class Meta:
        model = User
        fields = "__all__"


class RegisterSerializer(ModelSerializer):
    """Сериализатор для регистрации нового пользователя.

    Позволяет создать пользователя с указанием email, пароля и дополнительных данных.
    Проверяет совпадение паролей и создаёт пользователя с помощью UserManager.

    Attributes:
        password (CharField): Пароль пользователя (только для записи, валидируется).
        password2 (CharField): Подтверждение пароля (для проверки совпадения).

     Methods:
        validate: Проверяет совпадение паролей.
        create: Создаёт нового пользователя с хэшированным паролем.
    """
    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2", "first_name", "last_name", "avatar", "phone_number", "city")

    def validate(self, data):
        """Проверяет, что пароли совпадают.

        Args:
            data (dict): Входные данные сериализатора.

        Raises:
            ValidationError: Если пароли не совпадают.

        Returns:
            dict: Валидированные данные.
        """
        if data["password"] != data["password2"]:
            raise ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        """Создаёт нового пользователя с хэшированным паролем.

        Удаляет поле password2 и использует UserManager.create_user для создания пользователя.

        Args:
            validated_data (dict): Валидированные данные сериализатора.

        Returns:
            User: Созданный пользователь.
        """
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class PaymentSerializer(ModelSerializer):
    """Сериализатор для модели Payment.

    Сериализует все поля платежа, включая:
    - Ссылки на пользователя, курс и урок
    - Сумму и способ оплаты
    - Дату создания платежа
    """

    class Meta:
        model = Payment
        fields = "__all__"
