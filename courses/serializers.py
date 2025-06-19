from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    @staticmethod
    def get_lesson_count(instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
