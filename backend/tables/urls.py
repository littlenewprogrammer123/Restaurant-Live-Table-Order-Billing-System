from django.urls import path
from .views import (
    TableListView,
    CreateTableView,
    UpdateTableStatusView
)

urlpatterns = [
    path("", TableListView.as_view()),
    path("create/", CreateTableView.as_view()),
    path("<int:table_id>/status/", UpdateTableStatusView.as_view()),
]
