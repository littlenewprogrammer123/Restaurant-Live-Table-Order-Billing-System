from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("users.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/billing/", include("billing.urls")),
    path("api/tables/", include("tables.urls")),
    path("api/menu/", include("menu.urls")),
]
