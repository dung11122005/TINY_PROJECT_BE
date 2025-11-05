from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    method = models.CharField(max_length=10)  # GET, POST, PUT, DELETE
    endpoint = models.CharField(max_length=255, null=True, blank=True)
    module = models.CharField(max_length=100, default="GENERAL")

    def __str__(self):
        return f"{self.method} {self.code}"
