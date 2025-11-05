from apps.account.models.user import User
from apps.account.models.role import Role
from apps.account.models.permission import Permission
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Dùng RoleSerializer để trả ra object đầy đủ (kèm permissions)
        from .serializers import RoleSerializer  # tránh import vòng tròn

        role_data = None
        if user.role:
            role_data = RoleSerializer(user.role).data

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": role_data,
        }
        return data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "code", "endpoint", "method", "module"]


class RoleSerializer(serializers.ModelSerializer):
    # hiển thị danh sách permission chi tiết luôn
    permissions = PermissionSerializer(many=True, read_only=True)
    # cho phép gán permission qua danh sách id
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Permission.objects.all(),
        source="permissions",
    )

    class Meta:
        model = Role
        fields = ["id", "name", "permissions", "permission_ids"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Role.objects.all(), source="role"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "password",
            "is_active",
            "is_staff",
            "role",
            "role_id",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
