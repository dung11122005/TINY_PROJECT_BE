from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer
from apps.account.models.user import User
from apps.account.models.role import Role
from apps.account.models.permission import Permission
from .permissions import HasEndpointPermission
from django.db.models import Q


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD cho User.
    """

    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [HasEndpointPermission]

    def get_queryset(self):
        """
        Cho phép search bằng query param ?q=keyword
        """
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(email__icontains=q))
        return qs


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD cho Role.
    """

    queryset = Role.objects.all().order_by("-id")
    serializer_class = RoleSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [HasEndpointPermission]


class PermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD cho Permission.
    """

    queryset = Permission.objects.all().order_by("-id")
    serializer_class = PermissionSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [HasEndpointPermission]

    def create(self, request, *args, **kwargs):
        # Kiểm tra nếu request.data là list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)
