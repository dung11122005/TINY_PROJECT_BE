from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from apps.students.models.student import Student
from apps.students.models.classroom import ClassRoom
from apps.students.api.serializers import (
    StudentSerializer,
    ClassRoomSerializer,
    AddStudentsSerializer,
)


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all().order_by("name")
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def add_students(self, request, pk=None):
        serializer = AddStudentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        class_room = serializer.validated_data["class_room"]
        user_ids = serializer.validated_data["user_ids"]

        created_students = []
        for user in user_ids:
            student_obj, created = Student.objects.get_or_create(
                user=user, class_room=class_room
            )
            created_students.append(student_obj)

        return Response(
            StudentSerializer(created_students, many=True).data,
            status=status.HTTP_201_CREATED,
        )


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by("id")
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    # search by full_name or email
    def get_queryset(self):
        qs = super().get_queryset()
        # filter theo class
        class_room_id = self.request.query_params.get("class_room_id")
        if class_room_id:
            qs = qs.filter(class_room_id=class_room_id)

        # search theo user full_name hoặc email
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(
                Q(user__full_name__icontains=q) | Q(user__email__icontains=q)
            )

        return qs
