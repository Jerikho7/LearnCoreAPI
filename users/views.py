from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from courses.models import Course
from users.models import User, Payment
from users.permissions import IsOwner
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_checkout_session


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
        if self.action == "create":
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


class PaymentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        user = request.user

        # Создаём продукт
        product_result = create_stripe_product(course)
        if "error" in product_result:
            return Response({"error": product_result["error"]}, status=400)
        product_id = product_result["product_id"]

        # Создаём цену
        price_result = create_stripe_price(course, product_id)
        if "error" in price_result:
            return Response({"error": price_result["error"]}, status=400)
        price_id = price_result["price_id"]

        # Создаём сессию
        session_result = create_stripe_checkout_session(user, course, price_id)
        if "error" in session_result:
            return Response({"error": session_result["error"]}, status=400)

        # Сохраняем платёж
        payment = Payment.objects.create(
            user=user,
            paid_course=course,
            amount=course.price,
            stripe_session_id=session_result["session_id"],
            payment_url=session_result["payment_url"],
        )

        return Response({"payment_id": payment.id, "payment_url": payment.payment_url}, status=201)
