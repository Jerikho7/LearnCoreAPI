from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Group
from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonAndSubscriptionTests(APITestCase):
    """Тесты для CRUD операций с уроками и функционала подписки на курс."""

    def setUp(self):
        """Создаёт тестовые данные для всех тестов."""
        # Создаём пользователей
        self.user = User.objects.create_user(email="user@example.com", password="password123", is_active=True)
        self.moderator = User.objects.create_user(
            email="moderator@example.com", password="password123", is_active=True
        )
        self.other_user = User.objects.create_user(email="other@example.com", password="password123", is_active=True)

        moderator_group = Group.objects.create(name="moderators")
        self.moderator.groups.add(moderator_group)

        # Создаём курс
        self.course = Course.objects.create(title="Test Course", description="Test description", owner=self.user)

        # Создаём уроки
        self.lesson1 = Lesson.objects.create(
            title="Lesson 1",
            description="Description 1",
            link="https://www.youtube.com/watch?v=abc123xyz12",
            course=self.course,
            owner=self.user,
        )
        self.lesson2 = Lesson.objects.create(
            title="Lesson 2",
            description="Description 2",
            link="https://youtu.be/def456xyz12",
            course=self.course,
            owner=self.other_user,
        )

        # Создаём подписку
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)

    def test_lesson_create_authenticated_non_moderator(self):
        """Проверяет создание урока авторизованным не-модератором."""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "New Lesson",
            "description": "New description",
            "link": "https://www.youtube.com/watch?v=ghi789xyz12",
            "course": self.course.id,
        }
        response = self.client.post(reverse("courses:lesson_create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 3)
        self.assertEqual(Lesson.objects.last().owner, self.user)
        self.assertEqual(Lesson.objects.last().title, "New Lesson")

    def test_lesson_create_moderator_forbidden(self):
        """Проверяет, что модератор не может создать урок."""
        self.client.force_authenticate(user=self.moderator)
        data = {
            "title": "New Lesson",
            "description": "New description",
            "link": "https://www.youtube.com/watch?v=ghi789xyz12",
            "course": self.course.id,
        }
        response = self.client.post(reverse("courses:lesson_create"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_unauthenticated_forbidden(self):
        """Проверяет, что неавторизованный пользователь не может создать урок."""
        self.client.force_authenticate(user=None)
        data = {
            "title": "New Lesson",
            "description": "New description",
            "link": "https://www.youtube.com/watch?v=ghi789xyz12",
            "course": self.course.id,
        }
        response = self.client.post(reverse("courses:lesson_create"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_list_non_moderator_own_lessons(self):
        """Проверяет, что не-модератор видит только свои уроки."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("courses:lesson_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Lesson 1")

    def test_lesson_list_moderator_all_lessons(self):
        """Проверяет, что модератор видит все уроки."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(reverse("courses:lesson_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Оба урока

    def test_lesson_list_unauthenticated_forbidden(self):
        """Проверяет, что неавторизованный пользователь не может видеть список уроков."""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("courses:lesson_list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_retrieve_owner(self):
        """Проверяет, что владелец может просматривать свой урок."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("courses:lesson_retrieve", args=(self.lesson1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Lesson 1")

    def test_lesson_retrieve_moderator(self):
        """Проверяет, что модератор может просматривать любой урок."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(reverse("courses:lesson_retrieve", args=(self.lesson1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Lesson 1")

    def test_lesson_retrieve_non_owner_forbidden(self):
        """Проверяет, что не-модератор и не-владелец не может просматривать чужой урок."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(reverse("courses:lesson_retrieve", args=(self.lesson1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_owner(self):
        """Проверяет, что владелец может обновить свой урок."""
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Updated Lesson",
            "description": "Updated description",
            "link": "https://www.youtube.com/watch?v=ghi789xyz12",
            "course": self.course.id,
        }
        response = self.client.put(reverse("courses:lesson_update", args=(self.lesson1.pk,)), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.title, "Updated Lesson")

    def test_lesson_update_moderator(self):
        """Проверяет, что модератор может обновить любой урок."""
        self.client.force_authenticate(user=self.moderator)
        data = {
            "title": "Updated Lesson",
            "description": "Updated description",
            "link": "https://www.youtube.com/watch?v=ghi789xyz12",
            "course": self.course.id,
        }
        response = self.client.put(reverse("courses:lesson_update", args=(self.lesson1.pk,)), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.title, "Updated Lesson")

    def test_lesson_update_non_owner_forbidden(self):
        """Проверяет, что не-модератор и не-владелец не может обновить чужой урок."""
        self.client.force_authenticate(user=self.other_user)
        data = {
            "title": "Updated Lesson",
            "description": "Updated description",
            "link": "https://www.youtube.com/watch?v=ghi789xyz12",
            "course": self.course.id,
        }
        response = self.client.put(reverse("courses:lesson_update", args=(self.lesson1.pk,)), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_destroy_owner(self):
        """Проверяет, что владелец может удалить свой урок."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("courses:lesson_delete", args=(self.lesson1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_destroy_moderator_forbidden(self):
        """Проверяет, что модератор не может удалить урок."""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(reverse("courses:lesson_delete", args=(self.lesson1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_destroy_non_owner_forbidden(self):
        """Проверяет, что не-модератор и не-владелец не может удалить чужой урок."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse("courses:lesson_delete", args=(self.lesson1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_subscription_create(self):
        """Проверяет создание подписки авторизованным пользователем."""
        self.client.force_authenticate(user=self.other_user)
        data = {"course_id": self.course.id}
        response = self.client.post(reverse("courses:subscriptions"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.other_user, course=self.course).exists())

    def test_subscription_delete(self):
        """Проверяет удаление подписки авторизованным пользователем."""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}
        response = self.client.post(reverse("courses:subscriptions"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_unauthenticated_forbidden(self):
        """Проверяет, что неавторизованный пользователь не может управлять подпиской."""
        self.client.force_authenticate(user=None)
        data = {"course_id": self.course.id}
        response = self.client.post(reverse("courses:subscriptions"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_invalid_course(self):
        """Проверяет попытку подписки на несуществующий курс."""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": 999}
        response = self.client.post(reverse("courses:subscriptions"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
