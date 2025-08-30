from django.db import models
from django.contrib.auth.models import User
from instruments.models import Inventory, Purchases, Servicing, Rentals, Disposals


class LogEntry(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="User")
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Optional ForeignKeys to all main models
    inventory_item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_item = models.ForeignKey(Purchases, on_delete=models.SET_NULL, null=True, blank=True)
    servicing_item = models.ForeignKey(Servicing, on_delete=models.SET_NULL, null=True, blank=True)
    rental_item = models.ForeignKey(Rentals, on_delete=models.SET_NULL, null=True, blank=True)
    disposal_item = models.ForeignKey(Disposals, on_delete=models.SET_NULL, null=True, blank=True)

    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"