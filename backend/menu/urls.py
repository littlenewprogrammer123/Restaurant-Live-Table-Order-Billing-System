from django.urls import path
from .views import (
    MenuListView,
    CreateMenuItemView,
    ToggleMenuItemStatusView
)

urlpatterns = [
    path("", MenuListView.as_view()),
    path("create/", CreateMenuItemView.as_view()),
    path("<int:item_id>/toggle/", ToggleMenuItemStatusView.as_view()),
]
