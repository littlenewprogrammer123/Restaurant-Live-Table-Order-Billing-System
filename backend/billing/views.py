from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from users.permissions.role_permissions import IsWaiter, IsCashier, IsManager
from orders.models import Order, OrderItem
from tables.models import Table
from .models import Bill

TAX_PERCENT = 5  # 5%


class RequestBillView(APIView):
    """
    Request Bill
    Access: Waiter / Manager
    """
    permission_classes = [IsAuthenticated, IsWaiter | IsManager]

    @transaction.atomic
    def post(self, request, order_id):
        order = Order.objects.select_for_update().get(id=order_id)
        table = order.table

        # 🔒 Order must be completed
        if order.status != Order.Status.BILL_REQUESTED:
            raise ValidationError(
                "Order must be completed before requesting bill"
            )

        # 🔥 SAFETY SYNC (handles legacy / stale table states)
        if table.status == Table.Status.AVAILABLE:
            table.occupy()

        # 🔒 Now table MUST be occupied
        table.request_bill()

        return Response({"message": "Bill requested"})


class GenerateBillView(APIView):
    """
    Generate Bill
    Access: Cashier / Manager
    """
    permission_classes = [IsAuthenticated, IsCashier | IsManager]

    @transaction.atomic
    def post(self, request, order_id):
        order = Order.objects.select_for_update().get(id=order_id)

        # 🔒 Order must be completed
        if order.status != Order.Status.BILL_REQUESTED:
            raise ValidationError(
                "Order must be completed before billing"
            )

        # 🔒 Prevent duplicate bills
        if hasattr(order, "bill"):
            raise ValidationError("Bill already exists")

        items = OrderItem.objects.filter(order=order)

        if not items.exists():
            raise ValidationError("Cannot bill an empty order")

        subtotal = sum(
            item.menu_item.price * item.quantity
            for item in items
        )
        tax = subtotal * TAX_PERCENT / 100
        total = subtotal + tax

        bill = Bill.objects.create(
            order=order,
            subtotal=subtotal,
            tax=tax,
            total=total
        )

        return Response({
            "bill_id": bill.id,
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        })


class PayBillView(APIView):
    """
    Pay Bill
    Access: Cashier / Manager
    """
    permission_classes = [IsAuthenticated, IsCashier | IsManager]

    @transaction.atomic
    def post(self, request, bill_id):
        bill = Bill.objects.select_for_update().get(id=bill_id)
        table = bill.order.table

        # 🔒 Prevent double payment
        if bill.is_paid:
            raise ValidationError("Bill already paid")

        payment_method = request.data.get("payment_method")
        if not payment_method:
            raise ValidationError("Payment method is required")

        bill.mark_paid(payment_method)

        # 🔒 Close table only after successful payment
        table.close()

        return Response({
            "message": "Payment successful, table closed"
        })
