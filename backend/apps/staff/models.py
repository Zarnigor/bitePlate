import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class StaffRole(models.TextChoices):
    WAITER = "waiter", "Waiter"
    CHEF = "chef", "Chef"
    CASHIER = "cashier", "Cashier"
    MANAGER = "manager", "Manager"


class StaffMember(AbstractUser):
    """
    Extended user model with restaurant role.
    Demonstrates: Inheritance (extends AbstractUser), Encapsulation
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=StaffRole.choices, default=StaffRole.WAITER)
    phone = models.CharField(max_length=30, blank=True)

    def can_override_orders(self) -> bool:
        return self.role == StaffRole.MANAGER

    def can_process_payment(self) -> bool:
        return self.role in (StaffRole.CASHIER, StaffRole.MANAGER)

    def can_manage_queue(self) -> bool:
        return self.role in (StaffRole.CHEF, StaffRole.MANAGER)

    def __str__(self) -> str:
        return f"{self.get_full_name()} ({self.role})"
