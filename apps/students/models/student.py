from django.db import models
from apps.account.models.user import User
from .classroom import ClassRoom


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} ({self.class_room.name})"
