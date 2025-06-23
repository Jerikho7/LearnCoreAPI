import re
from django.core.exceptions import ValidationError


class YouTubeLinkValidator:
    """Валидатор для проверки ссылок, разрешающий только YouTube.

    Проверяет, что ссылка либо пустая, либо соответствует шаблону YouTube-видео
    (youtube.com/watch?v=..., youtube.com/embed/...).
    Если ссылка не соответствует, вызывается ValidationError.

    Args:
        field (str): Имя поля, которое проверяется.

    Raises:
        ValidationError: Если ссылка не соответствует шаблону YouTube.
    """

    def __init__(self, field):
        self.field = field
        self.youtube_pattern = re.compile(
            r"^(?:https?://)?"
            r"(?:www\.)?"
            r"(?:youtube\.com/watch\?v=|youtube\.com/embed/)"
            r"[\w-]{11}"
            r"(?:\S*)?$"
        )

    def __call__(self, value):
        link = value.get(self.field)
        if not link:
            return

        if not self.youtube_pattern.match(link):
            raise ValidationError(
                f"Ссылка в поле {self.field} должна быть на YouTube (youtube.com/watch?v=..., youtube.com/embed/). "
                f"Получена ссылка: {link}"
            )
