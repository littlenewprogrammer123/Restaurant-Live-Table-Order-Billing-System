from django.db import models
from django.utils import timezone

class Table(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        OCCUPIED = "OCCUPIED", "Occupied"
        BILL_REQUESTED = "BILL_REQUESTED", "Bill Requested"
        CLOSED = "CLOSED", "Closed"

    number = models.PositiveIntegerField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    opened_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    last_status_change = models.DateTimeField(auto_now=True)

    def occupy(self):
        if self.status != self.Status.AVAILABLE:
            raise ValueError("Table cannot be occupied")
        self.status = self.Status.OCCUPIED
        self.opened_at = timezone.now()
        self.save()

    def request_bill(self):
        if self.status != self.Status.OCCUPIED:
            raise ValueError("Bill can only be requested for occupied tables")
        self.status = self.Status.BILL_REQUESTED
        self.save()

    def close(self):
        if self.status != self.Status.BILL_REQUESTED:
            raise ValueError("Table can only be closed after billing")
        self.status = self.Status.CLOSED
        self.closed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Table {self.number} ({self.status})"
