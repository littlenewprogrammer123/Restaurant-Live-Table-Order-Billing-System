from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Order, OrderItem
from .serializers import OrderSerializer
from tables.models import Table
from menu.models import MenuItem
from users.permissions.role_permissions import IsWaiter, IsCashier, IsManager


# -------------------------
# CREATE ORDER (WAITER)
# -------------------------
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated, IsWaiter]

    def post(self, request):
        table_id = request.data.get("table_id")

        if not table_id:
            return Response(
                {"error": "table_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return Response(
                {"error": "Invalid table"},
                status=status.HTTP_404_NOT_FOUND
            )

        order = Order.objects.create(
            table=table,
            status=Order.Status.OPEN
        )
        table.occupy()




        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )


# -------------------------
# ADD ITEM TO ORDER (WAITER)
# -------------------------
class AddOrderItemView(APIView):
    permission_classes = [IsAuthenticated, IsWaiter]

    def post(self, request, order_id):
        menu_item_id = request.data.get("menu_item_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            order = Order.objects.get(
                id=order_id,
                status=Order.Status.OPEN
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found or closed"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            menu_item = MenuItem.objects.get(
                id=menu_item_id,
                is_active=True
            )
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Invalid menu item"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 🔥 MERGE ITEMS
        item, created = OrderItem.objects.get_or_create(
            order=order,
            menu_item=menu_item,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response(
            {"message": "Item added"},
            status=status.HTTP_201_CREATED
        )

# -------------------------
# LIST ORDERS (MANAGER / CASHIER)
# -------------------------
class OrderListView(APIView):
    permission_classes = [IsAuthenticated, IsManager | IsCashier]

    def get(self, request):
        orders = Order.objects.all().order_by("-created_at")
        return Response(OrderSerializer(orders, many=True).data)


# -------------------------
# ORDERS BY TABLE
# -------------------------
class OrdersByTableView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, table_id):
        orders = Order.objects.filter(table_id=table_id).order_by("-created_at")
        return Response(OrderSerializer(orders, many=True).data)


# -------------------------
# REQUEST BILL (WAITER)
# -------------------------
class RequestBillView(APIView):
    permission_classes = [IsAuthenticated, IsWaiter]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(
                id=order_id,
                status=Order.Status.OPEN
            )

        except Order.DoesNotExist:
            return Response(
                {"error": "Order not open"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = Order.Status.BILL_REQUESTED
        order.save()

        order.table.request_bill()



        return Response({"message": "Bill requested"})


# -------------------------
# PAY & CLOSE ORDER (CASHIER)
# -------------------------
class CloseOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCashier]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(
                id=order_id,
                status=Order.Status.BILL_REQUESTED
            )

        except Order.DoesNotExist:
            return Response(
                {"error": "Order not ready for payment"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = Order.Status.CLOSED
        order.save()

        table = order.table
        table.close()

        table.status = Table.Status.AVAILABLE
        table.save()



        return Response({"message": "Order closed"})


# -------------------------
# UPDATE ORDER ITEM (WAITER)
# -------------------------
class UpdateOrderItemView(APIView):
    permission_classes = [IsAuthenticated, IsWaiter]

    def patch(self, request, item_id):
        quantity = request.data.get("quantity")

        try:
            item = OrderItem.objects.get(
                id=item_id,
                order__status=Order.Status.OPEN

            )
        except OrderItem.DoesNotExist:
            return Response(
                {"error": "Order item not found or order closed"},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = int(quantity)

        # 🔥 DELETE IF QUANTITY < 1
        if quantity < 1:
            item.delete()
            return Response(
                {"message": "Item removed"},
                status=status.HTTP_200_OK
            )

        item.quantity = quantity
        item.save()

        return Response(
            {"message": "Quantity updated", "quantity": item.quantity},
            status=status.HTTP_200_OK
        )

