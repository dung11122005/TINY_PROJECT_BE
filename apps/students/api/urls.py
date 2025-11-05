from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassRoomViewSet, StudentViewSet

router = DefaultRouter()
router.register(r"classrooms", ClassRoomViewSet, basename="classroom")
router.register(r"students", StudentViewSet, basename="student")

urlpatterns = [
    path("", include(router.urls)),
]
