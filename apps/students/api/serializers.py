from rest_framework import serializers
from apps.students.models.student import Student
from apps.students.models.classroom import ClassRoom
from apps.account.models.user import User
from apps.account.api.serializers import UserSerializer


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ["id", "name"]


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # nested serializer
    class_room = ClassRoomSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "user", "class_room"]


class AddStudentsSerializer(serializers.Serializer):
    class_room = serializers.PrimaryKeyRelatedField(queryset=ClassRoom.objects.all())
    user_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    )
