from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from instruments.models import Inventory, Purchases, Servicing, Rentals, Disposals
from .models import LogEntry


# Function to creat log
def create_log(user, action, inventory=None, purchase=None, servicing=None, rental=None, disposal=None, note=None):
    LogEntry.objects.create(
        user=user,
        action=action,
        inventory_item=inventory,
        purchase_item=purchase,
        servicing_item=servicing,
        rental_item=rental,
        disposal_item=disposal,
        note=note
    )