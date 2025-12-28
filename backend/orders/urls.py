from django.urls import path
from .views import (
    CreateOrderView,
    AddOrderItemView,
    OrderListView,
    OrdersByTableView,
    RequestBillView,
    CloseOrderView,
    UpdateOrderItemView,
)


urlpatterns = [
    path("create/", CreateOrderView.as_view()),
    path("<int:order_id>/items/", AddOrderItemView.as_view()),
    path("items/<int:item_id>/", UpdateOrderItemView.as_view()),
    path("", OrderListView.as_view()), 
    path("table/<int:table_id>/", OrdersByTableView.as_view()),
    path("<int:order_id>/request-bill/", RequestBillView.as_view()),
    path("<int:order_id>/close/", CloseOrderView.as_view()),

]
