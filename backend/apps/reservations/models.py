import uuid
from django.db import models


class ReservationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    ARRIVED = "arrived", "Arrived"
    NO_SHOW = "no_show", "No Show"
    CANCELLED = "cancelled", "Cancelled"


class Reservation(models.Model):
    """
    Restaurant booking.
    Celery schedules a reminder task at booking time.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_id = models.UUIDField()
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=30, blank=True)
    party_size = models.PositiveIntegerField()
    reserved_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["reserved_at"]

    def __str__(self) -> str:
        return f"{self.customer_name} × {self.party_size} @ {self.reserved_at}"
