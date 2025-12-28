from django.db import models
from menu.models import MenuItem
from tables.models import Table


class Order(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("BILL_REQUESTED", "Bill Requested"),
        ("PAID", "Paid"),
        ("CLOSED", "Closed"),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - Table {self.table.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"
