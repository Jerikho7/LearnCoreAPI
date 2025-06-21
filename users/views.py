from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.permissions import IsOwner
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer


class UserViewSet(ModelViewSet):
    """ViewSet для работы с пользователями (CRUD).

    Поддерживает все стандартные действия:
    - list: Получить список пользователей
    - create: Создать нового пользователя
    - retrieve: Получить данные пользователя
    - update: Обновить данные пользователя
    - destroy: Удалить пользователя

    Attributes:
        queryset (QuerySet): Все пользователи системы.
        serializer_class (UserSerializer): Сериализатор для обработки данных.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Возвращает только текущего пользователя."""
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
            raise NotImplementedError("Use /register/ endpoint for user creation")
        return super().get_permissions()




class RegisterView(CreateAPIView):
    """API для регистрации нового пользователя.

    Доступные методы:
    - POST: Создать нового пользователя
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class PaymentViewSet(ModelViewSet):
    """ViewSet для работы с платежами (CRUD).

    Поддерживает:
    - Фильтрацию по payment_method, paid_course, paid_lesson
    - Сортировку по payment_date

    Attributes:
        queryset (QuerySet): Все платежи в системе.
        serializer_class (PaymentSerializer): Сериализатор для обработки данных.
        filter_backends (list): Подключенные фильтры (DjangoFilterBackend, OrderingFilter).
        filterset_fields (tuple): Поля для фильтрации.
        ordering_fields (tuple): Поля для сортировки.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("payment_method", "paid_course", "paid_lesson")
    ordering_fields = ("payment_date",)

    def get_queryset(self):
        """Возвращает только платежи текущего пользователя."""
        return Payment.objects.filter(user=self.request.user)
