from django.urls import path
from .views import RequestBillView, GenerateBillView, PayBillView

urlpatterns = [
    path("orders/<int:order_id>/request-bill/", RequestBillView.as_view()),
    path("orders/<int:order_id>/generate-bill/", GenerateBillView.as_view()),
    path("bills/<int:bill_id>/pay/", PayBillView.as_view()),
    
]
