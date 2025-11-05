from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Tổng hợp API
    path("api/", include("apps.account.api.urls")),  # tất cả endpoints account
    path("api/", include("apps.students.api.urls")),
]
