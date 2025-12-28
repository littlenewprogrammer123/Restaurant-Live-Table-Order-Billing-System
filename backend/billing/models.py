from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from orders.models import Order


class Bill(models.Model):

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        UPI = "UPI", "UPI"
        CARD = "CARD", "Card"

    order = models.OneToOneField(Order, on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        null=True,
        blank=True
    )

    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.is_paid and not self.payment_method:
            raise ValidationError("Payment method required when bill is paid")

    def mark_paid(self, method):
        if self.is_paid:
            raise ValidationError("Paid bill cannot be modified")

        self.payment_method = method
        self.is_paid = True
        self.paid_at = timezone.now()
        self.save()
