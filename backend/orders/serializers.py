from rest_framework import serializers
from .models import Order, OrderItem
from menu.serializers import MenuItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "menu_item_id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    table_number = serializers.IntegerField(source="table.number", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "table", "table_number", "status", "items", "created_at"]
